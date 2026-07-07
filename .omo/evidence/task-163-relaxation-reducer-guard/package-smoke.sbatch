#!/bin/bash
#SBATCH -J z1-t163-smoke
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/package-smoke-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/package-smoke-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  -m pytest tests/test_package_integration_smoke.py -q
