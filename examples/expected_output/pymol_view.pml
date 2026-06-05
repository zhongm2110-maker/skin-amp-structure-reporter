# PyMOL 脚本 — example_structure
# 由 generate_visualization_scripts.py 自动生成

# 载入结构
load /home/lsk/AMP_structure_skill/examples/input/example_structure.pdb

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
save example_structure_session.pse

# 如需导出 PNG 图片（需开启 ray tracing）：
# ray 1200, 1200
# png example_structure_view.png, dpi=300
