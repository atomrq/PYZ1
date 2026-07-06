#!/bin/bash
#SBATCH -J z1-t143-green2
#SBATCH -o /public/home/jxm/codex_runs/z1-task143-z1plus-code-io-contract-20260706-162453/green-final.txt
#SBATCH -e /public/home/jxm/codex_runs/z1-task143-z1plus-code-io-contract-20260706-162453/green-final.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:10:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task143-z1plus-code-io-contract-20260706-162453/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd /public/home/jxm/codex_runs/z1-task143-z1plus-code-io-contract-20260706-162453/src
/public/home/jxm/codex_runs/z1-task129-20260705-230350/.mm-env/bin/python -m pytest tests/test_lammps_dump_import.py::test_import_dump_when_negative_xy_triclinic_bounds_uses_z1plus_sign_rule -q
