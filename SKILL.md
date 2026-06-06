---
name: AMP-structure-skill
description: AMP（抗菌肽）与皮肤微生态蛋白结构快速体检。当用户提到 AMP、抗菌肽、多肽结构分析、FASTA 结构评估、PDB 质量分析、PyMOL 可视化、结构预测时使用。
version: 1.2.0
---

# AMP Structure Reporter

## 输入
- FASTA 序列
- PDB ID（通过 fetch_structure.py 下载）
- UniProt ID（通过 AlphaFold DB 下载）
- 本地 PDB / mmCIF 文件

## 工作流程

### 路线 A：已有结构文件
1. 如果有 PDB ID → 运行 `fetch_structure.py` 下载
2. 如果有 FASTA → 运行 `analyze_sequence.py`
3. 运行 `inspect_structure.py` 质检
4. 生成 PyMOL 可视化脚本
5. 输出 Markdown 报告

### 路线 B：从序列开始预测
1. 运行 `bash scripts/run_full.sh`
   - ColabFold CPU 预测结构（AMP 短肽 1-2 分钟/条）
   - 自动接序列分析 + 结构质检 + 报告

## 预测说明
- 使用 ColabFold（CPU 模式），AMP 短肽（<30 aa） 1-2 分钟出结果
- 需先装：`conda create -n amp-gpu python=3.10 && conda activate amp-gpu && pip install "colabfold[alphafold]"`
- GPU 在 WSL2 + TensorFlow 下存在兼容限制，CPU 模式稳定可靠

## 解读规则
- AlphaFold pLDDT > 90 高置信度，70-90 骨架可靠，50-70 低置信度，<50 不可靠
- B-factor < 40 有序，> 80 柔性大
- NMR 结构不适用 B-factor，看 ensemble RMSD
- 短 AMP（< 30 aa）在不同环境中构象可能不同

## 输出
- `report.md` — 完整分析报告
- `pymol_view.pml` — PyMOL 可视化脚本
- 各步骤 JSON 中间结果
