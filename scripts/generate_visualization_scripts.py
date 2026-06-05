#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_visualization_scripts.py — 生成 PyMOL 可视化脚本 (.pml)。

根据 PDB/mmCIF 结构文件，自动生成 PyMOL 脚本：
- 卡通图展示
- B-factor / pLDDT 着色
- 白背景
- 保存 .pse 会话文件

用法：
    python scripts/generate_visualization_scripts.py example/example_structure.pdb \
        --out results/visualization
"""

import argparse
import os
import sys


def generate_pymol_script(structure_path: str) -> str:
    """生成 PyMOL 脚本内容。"""
    abs_path = os.path.abspath(structure_path)
    basename = os.path.splitext(os.path.basename(structure_path))[0]

    pml = f"""# PyMOL 脚本 — {basename}
# 由 generate_visualization_scripts.py 自动生成

# 载入结构
load {abs_path}

# 显示设置
hide everything
show cartoon
bg_color white
set cartoon_transparency, 0.1

# B-factor / pLDDT 着色（蓝→白→红，0~100 范围）
spectrum b, blue_white_red, minimum=0, maximum=100

# 如果有配体，显示为棍状（可选）
# show sticks, hetatm

# 优化视角
orient

# 保存会话文件
save {basename}_session.pse

# 如需导出 PNG 图片（需开启 ray tracing）：
# ray 1200, 1200
# png {basename}_view.png, dpi=300
"""
    return pml.strip()


def main():
    parser = argparse.ArgumentParser(
        description="生成 PyMOL 可视化脚本（.pml）"
    )
    parser.add_argument("input", help="PDB 或 mmCIF 文件路径")
    parser.add_argument("--out", default="results/visualization",
                        help="输出目录（默认: results/visualization）")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"错误: 文件不存在 — {args.input}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    pml = generate_pymol_script(args.input)
    out_path = os.path.join(args.out, "pymol_view.pml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pml + "\n")

    print(f"PyMOL 脚本已生成 → {out_path}")
    print("在 PyMOL 中打开此脚本：")
    print(f"  pymol {out_path}")


if __name__ == "__main__":
    main()
