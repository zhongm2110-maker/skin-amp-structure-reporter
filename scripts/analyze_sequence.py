#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
analyze_sequence.py
Day 1 Skill: 读取FASTA序列（支持多条），输出基础序列属性和AMP-like判断
"""

import argparse
import json
from Bio import SeqIO
from Bio.SeqUtils import molecular_weight

# =========================
# 命令行参数
# =========================

parser = argparse.ArgumentParser(
    description="Analyze FASTA sequences and output basic properties with AMP-like note."
)

parser.add_argument(
    "input",
    help="Input FASTA file (single or multi-FASTA)"
)

parser.add_argument(
    "--out",
    default="results/sequence_properties.json",
    help="Output JSON file path"
)

args = parser.parse_args()

# =========================
# 读取FASTA
# =========================

records = SeqIO.parse(args.input, "fasta")

all_results = []

for record in records:
    sequence = str(record.seq)
    length = len(sequence)
    cys_count = sequence.count("C")
    lys_count = sequence.count("K")
    arg_count = sequence.count("R")
    hydrophobic_residues = "AILMFWVY"
    hydrophobic_count = sum(sequence.count(aa) for aa in hydrophobic_residues)
    hydrophobic_ratio = round(hydrophobic_count / length, 2)
    positive = lys_count + arg_count
    negative = sequence.count("D") + sequence.count("E")
    net_charge = positive - negative
    mw = round(molecular_weight(sequence, seq_type="protein"), 2)

    # =========================
    # 科研解释：AMP-like简单判断
    # =========================
    if net_charge >= 2 and hydrophobic_ratio >= 0.3:
        amp_like = "Possible AMP-like peptide"
    else:
        amp_like = "Not obviously AMP-like"

    result = {
        "sequence_id": record.id,
        "length": length,
        "molecular_weight": mw,
        "cys_count": cys_count,
        "lys_count": lys_count,
        "arg_count": arg_count,
        "hydrophobic_ratio": hydrophobic_ratio,
        "net_charge_estimate_pH7": net_charge,
        "amp_prediction_note": amp_like
    }

    all_results.append(result)

# =========================
# 保存JSON
# =========================

with open(args.out, "w") as f:
    json.dump(all_results, f, indent=4)

print("Sequence analysis complete.")
print(json.dumps(all_results, indent=4))