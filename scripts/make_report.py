#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_report.py — 生成 Markdown 结构分析报告。

合并序列分析（analyze_sequence.py）和结构质检（inspect_structure.py）的结果，
输出一份可读的 Markdown 报告。

用法：
    # 有结构
    python scripts/make_report.py \
        --seq result/sequence_properties.json \
        --structure result/structure_qc.json \
        --out result/report.md

    # 只有序列，没结构
    python scripts/make_report.py \
        --seq result/sequence_properties.json \
        --out result/report.md
"""

import argparse
import json
import os
import sys
from datetime import datetime


def load_json(path: str) -> dict | list:
    """加载 JSON 文件，失败时退出。"""
    if not os.path.isfile(path):
        print(f"错误: 文件不存在 — {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def interpret_amp(seq: dict) -> str:
    """判断是否像 AMP。"""
    reasons = []
    charge = seq.get("net_charge_estimate_pH7", 0)
    hydro = seq.get("hydrophobic_ratio", 0)

    if charge >= 2:
        reasons.append(f"阳离子（净电荷 +{charge}）")
    if hydro >= 0.3:
        reasons.append(f"疏水比 {hydro:.0%}")
    if seq.get("length", 0) <= 60:
        reasons.append(f"短序列（{seq['length']} aa）")

    if len(reasons) >= 2:
        return f"✅ 初步判断符合 AMP 特征：{'; '.join(reasons)}"
    elif len(reasons) == 1:
        return f"⚠️ 部分符合 AMP 特征（{reasons[0]}），需进一步验证"
    else:
        return "❌ 不具备典型 AMP 特征"


def assess_structure(struct: dict) -> str:
    """根据结构质检结果给出结论。"""
    if "error" in struct:
        return f"❌ 结构分析出错：{struct['error']}"

    is_nmr = struct.get("is_nmr", False)
    is_af = struct.get("is_alphafold_likely", False)
    mean_b = struct.get("mean_bfactor")
    low_ratio = struct.get("low_confidence_ratio", 0)

    # 判断类型
    if is_nmr:
        struct_type = "NMR 结构"
    elif is_af:
        struct_type = "AlphaFold 预测结构"
    else:
        struct_type = "X 射线晶体结构"

    # 质量判断
    if mean_b == 0 and is_nmr:
        verdict = "结构完整，但需查看 NMR ensemble 评估柔性"
    elif is_af and mean_b and mean_b > 90:
        verdict = "高置信度预测"
    elif is_af and mean_b and mean_b > 70:
        verdict = "中高置信度预测"
    elif is_af and mean_b and mean_b > 50:
        verdict = "中低置信度预测，需谨慎使用"
    elif not is_af and mean_b and mean_b < 40:
        verdict = "有序结构，质量良好"
    elif not is_af and mean_b and mean_b < 80:
        verdict = "结构质量一般"
    elif not is_af and mean_b and mean_b >= 80:
        verdict = "柔性较大"

    severity = "🔴 区域低置信度高" if low_ratio > 0.2 else "🟢 整体置信度可接受"
    return f"**{struct_type}** — {verdict}（{severity}）"


def next_steps(seq: dict, struct: dict | None) -> list:
    """生成下一步建议。"""
    steps = []
    seq_len = seq.get("length", 0)

    if not struct or "error" in struct:
        steps.append("1. **未找到结构**，建议用 ColabFold 进行预测")
        if seq_len < 15:
            steps.append("2. 短肽（< 15 aa）也可尝试 PEP-FOLD 预测")
        else:
            steps.append("2. 可在 PDB 或 AlphaFold DB 中检索是否有已知同源结构")
    else:
        is_nmr = struct.get("is_nmr", False)
        is_af = struct.get("is_alphafold_likely", False)
        mean_b = struct.get("mean_bfactor")

        if is_nmr:
            steps.append("1. **NMR 结构** — 参考 20 个模型的 RMSD 评估柔性")
        elif is_af:
            steps.append("1. **AlphaFold 预测结构** — 低 pLDDT 区域不要过度解读")
        else:
            if mean_b and mean_b > 80:
                steps.append("1. **柔性区域较多** — 建议去除高柔性区域后再分析")
            else:
                steps.append("1. **结构可用** — 可继续用于下游分析")

        steps.append(f"{len(steps)+1}. 如需发表展示图，可用 PyMOL 打开 pymol_view.pml")

    if seq_len < 30:
        steps.append(f"{len(steps)+1}. 短肽（< 30 aa）在膜环境和水溶液中构象可能不同")

    steps.append(f"{len(steps)+1}. 建议结合实验数据进一步验证")

    return steps


def generate_report(seq_list: list, struct: dict | None, input_desc: str = "") -> str:
    """生成完整 Markdown 报告。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("# AMP / Protein Structure Quick Report")
    lines.append(f"**生成时间:** {now}")
    lines.append("---")
    lines.append("")

    # ── 1. 输入概要 ──
    lines.append("## 1. 输入概要")
    lines.append("")
    lines.append(f"- **序列数量:** {len(seq_list)}")
    lines.append(f"- **结构文件:** {'✅ 已提供' if struct and 'error' not in struct else '❌ 未提供'}")
    lines.append("")

    # ── 2. 序列分析 ──
    lines.append("## 2. 序列分析")
    lines.append("")
    for i, seq in enumerate(seq_list, 1):
        lines.append(f"### {i}. {seq.get('sequence_id', '未知')}")
        lines.append("")
        lines.append(f"| 属性 | 数值 |")
        lines.append(f"|---|---|")
        lines.append(f"| 长度 | {seq['length']} aa |")
        lines.append(f"| 分子量 | {seq['molecular_weight']:.1f} Da |")
        lines.append(f"| 净电荷 (pH 7) | {seq['net_charge_estimate_pH7']:+.0f} |")
        lines.append(f"| Cys 数量 | {seq['cys_count']} |")
        lines.append(f"| 疏水残基比例 | {seq['hydrophobic_ratio']:.2f} |")
        lines.append(f"| AMP 判断 | {seq.get('amp_prediction_note', '未分析')} |")
        lines.append("")
        lines.append(interpret_amp(seq))
        lines.append("")

    # ── 3. 结构分析 ──
    lines.append("## 3. 结构分析")
    lines.append("")
    if struct and "error" not in struct:
        lines.append(f"- **文件:** {struct.get('file_name', '未知')}")
        lines.append(f"- **格式:** {struct.get('format', '?')}")
        lines.append(f"- **链数:** {struct['chain_count']}")
        lines.append(f"- **残基数:** {struct['residue_count']}")
        lines.append(f"- **原子数:** {struct['atom_count']}")
        lines.append(f"- **平均 B-factor:** {struct.get('mean_bfactor', 'N/A')}")
        if struct.get("bfactor_note"):
            lines.append(f"- **提示:** {struct['bfactor_note']}")
        lines.append("")
        lines.append("### 质量结论")
        lines.append("")
        lines.append(assess_structure(struct))
        lines.append("")
    else:
        lines.append("未提供结构文件，无法进行结构分析。")
        lines.append("")

    # ── 4. 下一步建议 ──
    lines.append("## 4. 下一步建议")
    lines.append("")
    # 取第一条序列做判断
    first_seq = seq_list[0] if seq_list else {}
    steps = next_steps(first_seq, struct)
    for s in steps:
        lines.append(f"- {s}")
    lines.append("")

    lines.append("---")
    lines.append(f"*由 AMP Structure Reporter 自动生成，{now}*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成 Markdown 结构分析报告")
    parser.add_argument("--seq", required=True, help="序列分析结果 JSON")
    parser.add_argument("--structure", help="结构质检结果 JSON（可选）")
    parser.add_argument("--out", default="result/report.md", help="输出路径")
    args = parser.parse_args()

    seq_data = load_json(args.seq)
    if not isinstance(seq_data, list):
        seq_data = [seq_data]

    struct_data = None
    if args.structure:
        raw = load_json(args.structure)
        if "error" not in raw:
            struct_data = raw

    report = generate_report(seq_data, struct_data)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"报告已生成 → {args.out}")


if __name__ == "__main__":
    main()
