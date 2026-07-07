#!/bin/bash
#SBATCH -J z1-t164-static2
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/static2-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/static2-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo/src
VENV=/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv

cd /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo
"$VENV"/bin/ruff \
  check src/pyz1/regression.py src/pyz1/regression_cli.py tests/test_spplus_regression.py tests/test_regression_cli.py
"$VENV"/bin/basedpyright \
  --pythonpath "$VENV"/bin/python \
  src/pyz1/regression.py src/pyz1/regression_cli.py tests/test_spplus_regression.py tests/test_regression_cli.py
