# AMP / Protein Structure Quick Report
**生成时间:** 2026-06-06 14:20
---

## 1. 输入概要

- **序列数量:** 3
- **结构文件:** ✅ 已提供

## 2. 序列分析

### 1. example_amp

| 属性 | 数值 |
|---|---|
| 长度 | 13 aa |
| 分子量 | 1480.8 Da |
| 净电荷 (pH 7) | +0 |
| Cys 数量 | 0 |
| 疏水残基比例 | 0.54 |
| AMP 判断 | Not obviously AMP-like |

✅ 初步判断符合 AMP 特征：疏水比 54%; 短序列（13 aa）

### 2. magainin_2

| 属性 | 数值 |
|---|---|
| 长度 | 23 aa |
| 分子量 | 2466.9 Da |
| 净电荷 (pH 7) | +3 |
| Cys 数量 | 0 |
| 疏水残基比例 | 0.43 |
| AMP 判断 | Possible AMP-like peptide |

✅ 初步判断符合 AMP 特征：阳离子（净电荷 +3）; 疏水比 43%; 短序列（23 aa）

### 3. defensin_like

| 属性 | 数值 |
|---|---|
| 长度 | 30 aa |
| 分子量 | 3448.1 Da |
| 净电荷 (pH 7) | +3 |
| Cys 数量 | 6 |
| 疏水残基比例 | 0.43 |
| AMP 判断 | Possible AMP-like peptide |

✅ 初步判断符合 AMP 特征：阳离子（净电荷 +3）; 疏水比 43%; 短序列（30 aa）

## 3. 结构分析

- **文件:** defensin_like__HNMP-1___human_neutrophil_defensin_mimic__unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb
- **格式:** PDB
- **链数:** 1
- **残基数:** 30
- **原子数:** 237
- **平均 B-factor:** 61.49

### 质量结论

**AlphaFold 预测结构** — 中低置信度预测，需谨慎使用（🟢 整体置信度可接受）

## 4. 下一步建议

- 1. **AlphaFold 预测结构** — 低 pLDDT 区域不要过度解读
- 2. 如需发表展示图，可用 PyMOL 打开 pymol_view.pml
- 3. 短肽（< 30 aa）在膜环境和水溶液中构象可能不同
- 4. 建议结合实验数据进一步验证

---
*由 AMP Structure Reporter 自动生成，2026-06-06 14:20*
