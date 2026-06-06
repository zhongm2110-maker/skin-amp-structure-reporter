#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect_structure.py — 分析 PDB/mmCIF 结构文件的基础信息。

输入 PDB/mmCIF 文件，输出：
- 链数、残基数、原子数
- 平均 B-factor / pLDDT
- 低置信度区域比例

用法：
    python scripts/inspect_structure.py example/example_structure.pdb --out result/structure_qc.json
    python scripts/inspect_structure.py model.cif --out result/structure_qc.json
"""

import argparse
import json
import os
import sys
import warnings

import numpy as np
from Bio.PDB import PDBParser, MMCIFParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning

warnings.filterwarnings("ignore", category=PDBConstructionWarning)


def inspect(filepath: str) -> dict:
    """解析 PDB/mmCIF 并返回结构质量指标。"""
    ext = os.path.splitext(filepath)[1].lower()

    if ext in (".pdb", ".ent"):
        parser = PDBParser(QUIET=True)
        struct = parser.get_structure("model", filepath)
    elif ext in (".cif", ".mmcif"):
        parser = MMCIFParser(QUIET=True)
        struct = parser.get_structure("model", filepath)
    else:
        return {"error": f"不支持的文件格式: {ext}"}

    # 只分析第一个 model（NMR 只取 model 0）
    model = struct[0]

    # 收集数据
    all_bfactors = []
    chain_count = 0
    residue_count = 0
    atom_count = 0

    for chain in model:
        chain_count += 1
        for residue in chain:
            if residue.id[0] != " ":
                continue  # 跳过 HETATM 非标准残基
            residue_count += 1
            if residue.has_id("CA"):
                b = residue["CA"].get_bfactor()
                all_bfactors.append(b)
            for _ in residue:
                atom_count += 1

    # 统计
    bfactors = np.array(all_bfactors)
    mean_b = round(float(bfactors.mean()), 2) if len(bfactors) > 0 else None
    std_b = round(float(bfactors.std()), 2) if len(bfactors) > 0 else None
    min_b = round(float(bfactors.min()), 2) if len(bfactors) > 0 else None
    max_b = round(float(bfactors.max()), 2) if len(bfactors) > 0 else None

    # 判断是否为 Alphafold 模型（pLDDT 范围 0-100）
    is_alphafold = False
    if len(bfactors) > 0:
        in_range_0_100 = ((bfactors >= 0) & (bfactors <= 100)).mean()
        if in_range_0_100 > 0.95 and mean_b > 50:
            is_alphafold = True

    # 低置信度判断
    if is_alphafold:
        low_conf_threshold = 50  # pLDDT < 50
        low_label = "pLDDT < 50"
    else:
        low_conf_threshold = 80  # B-factor > 80
        low_label = "B-factor > 80"

    low_count = int((bfactors < low_conf_threshold).sum()) if is_alphafold else int((bfactors > low_conf_threshold).sum())
    low_ratio = round(low_count / max(len(bfactors), 1), 3)
    bfactor_note = None
    if max_b == 0.0:
        bfactor_note = "3"

    report = {
        "file_name": os.path.basename(filepath),
        "format": "PDB" if ext in (".pdb", ".ent") else "mmCIF",
        "is_alphafold_likely": is_alphafold,
        "chain_count": chain_count,
        "residue_count": residue_count,
        "atom_count": atom_count,
        "mean_bfactor": mean_b,
        "std_bfactor": std_b,
        "min_bfactor": min_b,
        "max_bfactor": max_b,
        "low_confidence_threshold": low_label,
        "low_confidence_count": low_count,
        "low_confidence_ratio": low_ratio,
        "bfactor_note": bfactor_note,
    }
    return report


def main():
    parser = argparse.ArgumentParser(
        description="分析 PDB/mmCIF 结构文件，输出基础结构质量信息。"
    )
    parser.add_argument("input", help="PDB 或 mmCIF 文件路径")
    parser.add_argument("--out", default="result/structure_qc.json",
                        help="输出 JSON 路径（默认: result/structure_qc.json）")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"错误: 文件不存在 — {args.input}", file=sys.stderr)
        sys.exit(1)

    result = inspect(args.input)

    if "error" in result:
        print(f"错误: {result['error']}", file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"结构分析完成 → {args.out}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
