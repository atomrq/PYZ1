#!/bin/bash
#SBATCH -J z1-t164-report
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -o /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/guard-report-%j.out
#SBATCH -e /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/guard-report-%j.err
set -euo pipefail

export LC_ALL=C
export LANG=C
export PYTHONPATH=/public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo/src

cd /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/repo
/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706/.venv/bin/python \
  -m pyz1.regression_cli \
  --source-dir /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/source_z1_min \
  --oracle-root tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703 \
  --report-path /public/home/jxm/codex_runs/z1-task164-relaxation-report-surface-20260707/evidence/benchmark-04-05-spplus-contact-relaxation.md \
  --benchmark-id 04 \
  --benchmark-id 05 \
  --mode spplus \
  --contact-relaxation
