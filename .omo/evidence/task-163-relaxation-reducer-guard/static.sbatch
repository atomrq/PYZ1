#!/bin/bash
#SBATCH -J z1-t163-static
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/static-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/static-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/ruff \
  check src/pyz1/reducer.py src/pyz1/contact_relaxation.py tests/test_spplus_regression.py
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/basedpyright \
  src/pyz1/reducer.py src/pyz1/contact_relaxation.py tests/test_spplus_regression.py
