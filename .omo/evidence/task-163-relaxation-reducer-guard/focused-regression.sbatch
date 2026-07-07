#!/bin/bash
#SBATCH -J z1-t163-focus
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/focused-regression-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/evidence/focused-regression-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo/src
export PYZ1_SOURCE_Z1=/public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/source_z1_min

cd /public/home/jxm/codex_runs/z1-task163-relaxation-reducer-guard-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  -m pytest tests/test_spplus_regression.py::test_reduce_snapshot_when_contact_relaxation_shortens_chain37 -q
