#!/bin/bash
#SBATCH -J z1-t161-red
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/evidence/red-chain37-contour-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/evidence/red-chain37-contour-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYZ1_SOURCE_Z1=/public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/source_z1_min
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  -m pytest \
  tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain37_contour_matches_oracle \
  -q
