---
name: AMP-structure-skill
description: AMP（抗菌肽）与皮肤微生态蛋白结构快速体检。当用户提到 AMP、抗菌肽、多肽结构分析、FASTA 结构评估、PDB 质量分析、PyMOL 可视化时使用。
version: 1.1.0
---

# AMP Structure Reporter

## 输入
- FASTA 序列
- PDB ID（通过 fetch_structure.py 下载）
- UniProt ID（通过 AlphaFold DB 下载）
- 本地 PDB / mmCIF 文件

## 工作流程

1. 判断输入类型（序列 / PDB ID / UniProt ID / 本地文件）
2. 如果是 ID → 运行 `fetch_structure.py` 下载
3. 如果有序列 → 运行 `analyze_sequence.py`
4. 如果有结构文件 → 运行 `inspect_structure.py`
5. 生成 PyMOL 可视化脚本
6. 合并结果输出 Markdown 报告

## 解读规则

- AlphaFold pLDDT > 90 高置信度，70-90 骨架可靠，50-70 低置信度，<50 不可靠
- B-factor < 40 有序，> 80 柔性大
- NMR 结构不适用 B-factor，看 ensemble RMSD
- 短 AMP（< 30 aa）在不同环境中构象可能不同

## 输出

- `report.md` — 完整分析报告
- `pymol_view.pml` — PyMOL 可视化脚本
- 各步骤 JSON 中间结果
