#!/bin/bash
#SBATCH -J z1-t142-red
#SBATCH -o /public/home/jxm/codex_runs/z1-task142-chain39-spplus-20260706-100010/red.txt
#SBATCH -e /public/home/jxm/codex_runs/z1-task142-chain39-spplus-20260706-100010/red.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:10:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task142-chain39-spplus-20260706-100010/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd /public/home/jxm/codex_runs/z1-task142-chain39-spplus-20260706-100010/src
/public/home/jxm/codex_runs/z1-task129-20260705-230350/.mm-env/bin/python -m pytest tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain39_matches_oracle_pairs -q
