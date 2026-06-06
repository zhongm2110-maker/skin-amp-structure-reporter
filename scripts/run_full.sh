#!/usr/bin/env bash
# run_full.sh — 完整流程：预测 → 序列分析 → 结构质检 → Markdown 报告
# 用法：bash scripts/run_full.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================"
echo " AMP Structure Reporter — 完整流程"
echo "========================================"
echo ""

# 检查环境
if ! command -v colabfold_batch &> /dev/null; then
    echo "错误: 请先激活 colabfold 环境"
    echo "  conda activate amp-gpu  # 或 base"
    exit 1
fi

mkdir -p results/predictions

# Step 1: 结构预测（CPU 模式，AMP 短肽 1-2 分钟/条）
echo "[1/4] 结构预测（CPU）..."
JAX_PLATFORMS=cpu colabfold_batch examples/input/sample.fasta \
    results/predictions/ \
    --msa-mode single_sequence \
    --num-models 1 2>&1
echo ""

# 找到预测出的 PDB 文件
PDB_FILE=$(ls results/predictions/*_rank_001_*.pdb 2>/dev/null | head -1)
if [ -z "$PDB_FILE" ]; then
    echo "错误: 未找到预测结果 PDB 文件"
    exit 1
fi
echo "预测结构: $PDB_FILE"
echo ""

# Step 2: 序列分析
echo "[2/4] 序列分析..."
python scripts/analyze_sequence.py examples/input/sample.fasta \
    --out results/sequence_properties.json
echo "  → results/sequence_properties.json"
echo ""

# Step 3: 结构质检
echo "[3/4] 结构质检..."
python scripts/inspect_structure.py "$PDB_FILE" \
    --out results/structure_qc.json
echo "  → results/structure_qc.json"
echo ""

# Step 4: 生成报告
echo "[4/4] 生成报告..."
python scripts/make_report.py \
    --seq results/sequence_properties.json \
    --structure results/structure_qc.json \
    --out results/report.md
echo "  → results/report.md"
echo ""

# Step 5: PyMOL 可视化
echo "[5/4] 生成 PyMOL 脚本..."
python scripts/generate_visualization_scripts.py "$PDB_FILE" \
    --out results/visualization
echo "  → results/visualization/pymol_view.pml"
echo ""

echo "========================================"
echo " 完成！"
echo "========================================"
echo ""
echo "报告：    results/report.md"
echo "PyMOL：   results/visualization/pymol_view.pml"
echo "结构：    $PDB_FILE"
echo ""
