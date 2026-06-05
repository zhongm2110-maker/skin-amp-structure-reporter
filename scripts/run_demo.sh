#!/usr/bin/env bash
# run_demo.sh — 一键演示 AMP Structure Reporter 完整流程
# 从序列分析 → 结构质检 → 可视化脚本 → Markdown 报告
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================"
echo " AMP Structure Reporter — 一键演示"
echo "========================================"
echo ""

mkdir -p results/visualization

# Step 1: 序列分析
echo "[1/4] 序列分析..."
python scripts/analyze_sequence.py examples/input/sample.fasta \
    --out results/sequence_properties.json
echo "  → results/sequence_properties.json"
echo ""

# Step 2: 结构质检
echo "[2/4] 结构质检..."
python scripts/inspect_structure.py examples/input/example_structure.pdb \
    --out results/structure_qc.json
echo "  → results/structure_qc.json"
echo ""

# Step 3: PyMOL 可视化脚本
echo "[3/4] 生成 PyMOL 脚本..."
python scripts/generate_visualization_scripts.py examples/input/example_structure.pdb \
    --out results/visualization
echo "  → results/visualization/pymol_view.pml"
echo ""

# Step 4: 生成报告
echo "[4/4] 生成报告..."
python scripts/make_report.py \
    --seq results/sequence_properties.json \
    --structure results/structure_qc.json \
    --out results/report.md
echo "  → results/report.md"
echo ""

echo "========================================"
echo " 完成！输出文件："
echo "========================================"
echo ""
ls -lh results/
echo ""
echo "报告：    results/report.md"
echo "PyMOL：   results/visualization/pymol_view.pml"
