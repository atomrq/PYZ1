#!/bin/bash
#SBATCH -J z1-t161-diag
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/evidence/diag-chain37-contour-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/evidence/diag-chain37-contour-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYZ1_SOURCE_Z1=/public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/source_z1_min
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task161-chain37-contour-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  .omo/evidence/task-161-chain37-contour/diag-chain37-contour.py
