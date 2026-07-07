#!/bin/bash
#SBATCH -J z1-t162-geom
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task162-contact-relaxation-20260707/evidence/remote-gate-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task162-contact-relaxation-20260707/evidence/remote-gate-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task162-contact-relaxation-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task162-contact-relaxation-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  -m pytest tests/test_geometry.py -q
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/ruff \
  check src/pyz1/contact_relaxation.py src/pyz1/geometry.py tests/test_geometry.py
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/basedpyright \
  src/pyz1/contact_relaxation.py src/pyz1/geometry.py tests/test_geometry.py
