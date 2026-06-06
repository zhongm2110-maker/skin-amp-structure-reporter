# PyMOL 脚本 — defensin_like__HNMP-1___human_neutrophil_defensin_mimic__unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000
# 由 generate_visualization_scripts.py 自动生成

# 载入结构
load /home/lsk/AMP_structure_skill/results/predictions/defensin_like__HNMP-1___human_neutrophil_defensin_mimic__unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb

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
save defensin_like__HNMP-1___human_neutrophil_defensin_mimic__unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000_session.pse

# 如需导出 PNG 图片（需开启 ray tracing）：
# ray 1200, 1200
# png defensin_like__HNMP-1___human_neutrophil_defensin_mimic__unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000_view.png, dpi=300
