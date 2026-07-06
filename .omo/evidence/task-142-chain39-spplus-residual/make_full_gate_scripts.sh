#!/bin/bash
set -euo pipefail

RUN_ROOT=$1
PY=/public/home/jxm/codex_runs/z1-task129-20260705-230350/.mm-env/bin/python
VENV=/public/home/jxm/codex_runs/z1-task129-20260705-230350/.mm-env

cd "$RUN_ROOT"
mkdir -p full-gate/logs full-gate/shards

cat > run_pytest_shard.py <<'PY'
from pathlib import Path
import sys

import pytest


nodeids = [
    line.strip()
    for line in Path(sys.argv[1]).read_text().splitlines()
    if line.strip()
]
raise SystemExit(pytest.main(["-q", *nodeids]))
PY

export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
cd "$RUN_ROOT/src"
"$PY" -m pytest --collect-only -q tests > "$RUN_ROOT/full-gate/collect.raw"
"$PY" - "$RUN_ROOT/full-gate/collect.raw" "$RUN_ROOT/full-gate/shards" <<'PY'
from pathlib import Path
import sys

collect = Path(sys.argv[1])
shard_dir = Path(sys.argv[2])
nodeids = [
    line.strip()
    for line in collect.read_text().splitlines()
    if "::" in line and not line.startswith("<")
]
nonsp = [nodeid for nodeid in nodeids if "tests/test_spplus_regression.py::" not in nodeid]
spplus = [nodeid for nodeid in nodeids if "tests/test_spplus_regression.py::" in nodeid]
for prefix, selected, shards in (("nonsp", nonsp, 3), ("spplus", spplus, 7)):
    for shard_index in range(shards):
        shard_nodeids = [
            nodeid
            for index, nodeid in enumerate(selected)
            if index % shards == shard_index
        ]
        (shard_dir / f"{prefix}-{shard_index:02d}.txt").write_text(
            "\n".join(shard_nodeids) + "\n",
        )
(shard_dir.parent / "shard-summary.txt").write_text(
    f"total {len(nodeids)}\nnonsp {len(nonsp)}\nspplus {len(spplus)}\n",
)
PY
cd "$RUN_ROOT"

cat > pytest_nonsp.sbatch <<EOF
#!/bin/bash
#SBATCH -J z1-t142-nonsp
#SBATCH -o $RUN_ROOT/full-gate/logs/nonsp-%a.txt
#SBATCH -e $RUN_ROOT/full-gate/logs/nonsp-%a.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:20:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd $RUN_ROOT/src
SHARD=\$(printf "../full-gate/shards/nonsp-%02d.txt" "\$SLURM_ARRAY_TASK_ID")
$PY ../run_pytest_shard.py "\$SHARD"
EOF

cat > pytest_spplus.sbatch <<EOF
#!/bin/bash
#SBATCH -J z1-t142-spplus
#SBATCH -o $RUN_ROOT/full-gate/logs/spplus-%a.txt
#SBATCH -e $RUN_ROOT/full-gate/logs/spplus-%a.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:30:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd $RUN_ROOT/src
SHARD=\$(printf "../full-gate/shards/spplus-%02d.txt" "\$SLURM_ARRAY_TASK_ID")
$PY ../run_pytest_shard.py "\$SHARD"
EOF

cat > static_gate.sbatch <<EOF
#!/bin/bash
#SBATCH -J z1-t142-static
#SBATCH -o $RUN_ROOT/full-gate/logs/static.txt
#SBATCH -e $RUN_ROOT/full-gate/logs/static.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:20:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
export PATH=$VENV/bin:\$PATH
cd $RUN_ROOT/src
ruff check .
basedpyright --pythonpath $VENV/bin/python
EOF

cat > package_smoke.sbatch <<EOF
#!/bin/bash
#SBATCH -J z1-t142-pkg
#SBATCH -o $RUN_ROOT/full-gate/logs/package-smoke.txt
#SBATCH -e $RUN_ROOT/full-gate/logs/package-smoke.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:20:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd $RUN_ROOT/src
$PY -m pytest tests/test_package_integration_smoke.py -q
EOF

cat > benchmark_gate.sbatch <<EOF
#!/bin/bash
#SBATCH -J z1-t142-bench
#SBATCH -o $RUN_ROOT/full-gate/logs/benchmark.txt
#SBATCH -e $RUN_ROOT/full-gate/logs/benchmark.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --time=00:20:00
set -euo pipefail
export LC_ALL=C
export LANG=C
export PYTHONPATH=$RUN_ROOT/src/src
export PYZ1_SOURCE_Z1=/public/home/jxm/z1src-task129
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
cd $RUN_ROOT/src
$PY -m pyz1.regression_cli \
  --source-dir /public/home/jxm/z1src-task129 \
  --oracle-root tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703 \
  --report-path $RUN_ROOT/full-gate/benchmark-04-05-spplus.md \
  --benchmark-id 04 \
  --benchmark-id 05 \
  --mode spplus
EOF
