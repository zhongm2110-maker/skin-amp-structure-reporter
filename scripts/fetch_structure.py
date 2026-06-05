#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_structure.py — 自动下载结构文件。

支持：
  --pdb <ID>        从 RCSB PDB 下载实验结构
  --uniprot <ID>    从 AlphaFold DB 下载预测结构

用法：
    python scripts/fetch_structure.py --pdb 1LFC --out result/structures/
    python scripts/fetch_structure.py --uniprot P0DTC2 --out result/structures/
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


PDB_URL = "https://files.rcsb.org/download"
AF_API = "https://alphafold.ebi.ac.uk/api/prediction"


def download_pdb(pdb_id: str, out_dir: str) -> str:
    """从 RCSB PDB 下载结构文件。"""
    pdb_id = pdb_id.strip().upper()
    filename = f"{pdb_id}.pdb"
    url = f"{PDB_URL}/{filename}"
    dest = os.path.join(out_dir, filename)

    if os.path.isfile(dest):
        print(f"✓ 文件已存在: {filename}")
        return dest

    print(f"正在下载 {url} ...")
    try:
        urllib.request.urlretrieve(url, dest)
    except urllib.error.HTTPError:
        # 如果 .pdb 404，尝试 .cif 格式
        url = f"{PDB_URL}/{pdb_id}.cif"
        filename = f"{pdb_id}.cif"
        dest = os.path.join(out_dir, filename)
        print(f"  PDB 格式不存在，尝试 mmCIF 格式 ...")
        try:
            urllib.request.urlretrieve(url, dest)
        except urllib.error.HTTPError:
            os.remove(dest)
            raise RuntimeError(f"未找到该结构: {pdb_id}（PDB 和 mmCIF 均不存在）")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络错误: {e.reason}")

    size = os.path.getsize(dest)
    print(f"✓ 已下载: {filename}（{size:,} 字节）")
    return dest


def download_alphafold(uniprot_id: str, out_dir: str) -> str:
    """从 AlphaFold DB 下载预测结构（通过 API 查询真实下载地址）。"""
    uniprot_id = uniprot_id.strip().upper()

    # 通过 API 获取下载地址
    api_url = f"{AF_API}/{uniprot_id}"
    print(f"正在查询 AlphaFold API ...")
    try:
        req = urllib.request.urlopen(api_url, timeout=30)
        data = json.loads(req.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"AlphaFold DB 中未找到 {uniprot_id}（HTTP {e.code}）")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络错误: {e.reason}")
    except json.JSONDecodeError:
        raise RuntimeError(f"API 返回格式异常")

    if not data or not isinstance(data, list):
        raise RuntimeError(f"未找到 {uniprot_id} 的预测结构")

    entry = data[0]
    pdb_url = entry.get("pdbUrl")
    if not pdb_url:
        raise RuntimeError(f"该条目没有可用的 PDB 文件")

    filename = pdb_url.strip().split("/")[-1]
    dest = os.path.join(out_dir, filename)

    if os.path.isfile(dest):
        print(f"✓ 文件已存在: {filename}")
        return dest

    print(f"正在下载 {pdb_url} ...")
    try:
        urllib.request.urlretrieve(pdb_url, dest)
    except urllib.error.HTTPError as e:
        if os.path.isfile(dest):
            os.remove(dest)
        raise RuntimeError(f"下载失败（HTTP {e.code}）")
    except urllib.error.URLError as e:
        if os.path.isfile(dest):
            os.remove(dest)
        raise RuntimeError(f"网络错误: {e.reason}")

    size = os.path.getsize(dest)
    print(f"✓ 已下载: {filename}（{size:,} 字节）")
    return dest


def main():
    parser = argparse.ArgumentParser(description="从 PDB 或 AlphaFold DB 下载结构文件")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdb", help="PDB ID，例如 1LFC")
    group.add_argument("--uniprot", help="UniProt ID，例如 P0DTC2")
    parser.add_argument("--out", default="result/structures", help="保存目录")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    try:
        if args.pdb:
            path = download_pdb(args.pdb, args.out)
        elif args.uniprot:
            path = download_alphafold(args.uniprot, args.out)

        print(f"\n结构已保存 → {path}")
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
