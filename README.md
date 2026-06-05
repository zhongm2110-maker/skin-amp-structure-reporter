# Skin AMP Structure Reporter

AMP（抗菌肽）与皮肤微生态蛋白的**结构快速体检工具**。

输入 FASTA 序列、PDB ID 或结构文件，自动输出序列性质、结构质检报告、PyMOL 可视化脚本。

---

## 快速开始

```bash
git clone https://github.com/SkinMicrobe/skin-amp-structure-reporter.git
cd skin-amp-structure-reporter

# 装依赖
pip install biopython numpy

# 一键演示
bash scripts/run_demo.sh
```

## 脚本功能

| 脚本 | 输入 → 输出 | 用途 |
|---|---|---|
| `analyze_sequence.py` | FASTA → JSON | 序列长度、电荷、疏水比、Cys 数 |
| `inspect_structure.py` | PDB/mmCIF → JSON | 链数、残基数、B-factor/pLDDT、低置信度比例 |
| `generate_visualization_scripts.py` | PDB → .pml | PyMOL 可视化脚本（卡通图 + B-factor 着色） |
| `make_report.py` | JSON → report.md | 合并数据输出 Markdown 报告 |
| `fetch_structure.py` | PDB ID / UniProt ID → PDB | 从 RCSB 或 AlphaFold DB 下载结构 |
| `run_demo.sh` | — | 一键跑完整流程 |

## 使用示例

```bash
# 1. 分析序列
python scripts/analyze_sequence.py examples/input/sample.fasta \
    --out results/sequence_properties.json

# 2. 质检结构
python scripts/inspect_structure.py examples/input/example_structure.pdb \
    --out results/structure_qc.json

# 3. 生成 PyMOL 脚本
python scripts/generate_visualization_scripts.py examples/input/example_structure.pdb \
    --out results/visualization

# 4. 生成报告
python scripts/make_report.py \
    --seq results/sequence_properties.json \
    --structure results/structure_qc.json \
    --out results/report.md

# 5. 下载结构
python scripts/fetch_structure.py --pdb 1LFC --out results/structures/
python scripts/fetch_structure.py --uniprot P0DTC2 --out results/structures/
```

## 三种结构类型

| 类型 | 来源 | 质量指标 |
|---|---|---|
| X 射线 | 实验（蛋白晶体） | B-factor，＜40 有序 |
| NMR | 实验（溶液） | 不适用 B-factor，看 RMSD |
| AlphaFold | AI 预测 | pLDDT，＞90 高置信度 |

## 输出示例

生成的报告包含：
- 序列基本信息（长度、分子量、电荷）
- AMP 特征判断
- 结构质量评估（NMR / X-ray / AlphaFold 自动识别）
- 下游分析建议（展示、对接、突变）
- PyMOL 可视化脚本

## 局限性

- 短 AMP（＜30 aa）在水和膜中构象可能不同
- AlphaFold 是预测，不是实验结构
- 当前不做分子对接或 MD 模拟

## License

MIT
