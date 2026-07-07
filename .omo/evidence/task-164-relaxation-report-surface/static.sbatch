#!/bin/bash
#SBATCH -J z1-t164-static
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/static-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/static-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/ruff \
  check src/pyz1/regression.py src/pyz1/regression_cli.py tests/test_spplus_regression.py tests/test_regression_cli.py
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/basedpyright \
  src/pyz1/regression.py src/pyz1/regression_cli.py tests/test_spplus_regression.py tests/test_regression_cli.py
