# pyz1

[English](README.md) | [中文](README.zh-CN.md)

`pyz1` 是用于复现公开 Z1+ 工作流的本地 Python 实现路径。它是一个
clean-room Python package，用于解析 Z1+/LAMMPS 风格的聚合物输入、写出
Z1+ 兼容输出、计算 summary/`Ne`、运行原生 PPA/PPA+ slice，并构建不依赖
Linux `Z1+.ex` runtime 的原生几何 Z1 reducer。

## 快速开始

本地开发使用 `pyz1` micromamba 环境。在这台 macOS 主机上，运行 micromamba
时保持有限的文件描述符上限：

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pytest -q
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 --help
```

在 Z1 输入上运行原生 default reducer：

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 config.Z1
```

运行 SP+ pairing mode：

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -SP+ config.Z1
```

运行 selfZ execution mode：

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -selfZ config.Z1
```

写出 default/SP+/selfZ benchmark regression report：

```bash
ulimit -n 1000000; micromamba run -n pyz1 pyz1-benchmark-regression \
  --source-dir /Users/jiaxm/Contents/CodexProjects/source_code/Z1+ \
  --oracle-root tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703 \
  --report-path pyz1-benchmark-regression.md
```

默认会发现 oracle root 下的所有 `benchmark-*` 目录。可以重复传入
`--benchmark-id` 来限制报告范围。`--max-node-count` 用于调整 benchmark
skip guard，`--trace-diagnostics-max-node-count` 用于在较大可运行 case 中关闭
昂贵的 trace diagnostics，同时保留 summary 和 geometry delta。

运行原生 PPA/PPA+ modes：

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -PPA config.Z1
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -PPA+ config.Z1
```

写出 PPA/PPA+ oracle coordinate fixture-health report：

```bash
ulimit -n 1000000; micromamba run -n pyz1 pyz1-ppa-oracle-coordinates \
  --oracle-root tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703 \
  --report-path ppa-oracle-coordinate-report.md
```

默认会发现 oracle root 下的所有 `benchmark-*` 目录。可以重复传入
`--benchmark-id` 来限制报告范围。

写出原生 PPA/PPA+ summary regression report：

```bash
ulimit -n 1000000; micromamba run -n pyz1 pyz1-ppa-regression \
  --source-dir /Users/jiaxm/Contents/CodexProjects/source_code/Z1+ \
  --oracle-root tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703 \
  --report-path pyz1-ppa-regression.md \
  --max-node-count 1000
```

默认会发现 oracle root 下的所有 `benchmark-*` 目录，并运行两种 PPA mode。
可以重复传入 `--benchmark-id` 来限制报告范围。`--max-node-count` 会保护昂贵
的原生 PPA runtime case，并将 oversized case 记录为 `known-invalid`。

运行 package-level integration smoke：

```bash
ulimit -n 1000000; micromamba run -n pyz1 pytest -q tests/test_package_integration_smoke.py
```

该 smoke 会通过 `python -m pyz1` 驱动已安装 package 的 default、SP+、
selfZ、PPA、PPA+ modes，并检查 mode-specific 输出文件。

## 输出

package 已覆盖以下 parser/writer：

- `Z1+summary.dat`
- `Z1+SP.dat`，包含可选 SP+ `other-chain other-node` columns
- `Z1+initconfig.dat`
- `Ree_values.dat`
- `Lpp_values.dat`
- `N_values.dat`
- `Z_values.dat`
- `PPA.dat`
- `PPA+.dat`
- `PPA-summary.dat`
- `PPA+summary.dat`

Default 和 SP+ CLI modes 当前会写出 `Z1+SP.dat`、`Z1+summary.dat` 以及
`Ree/Lpp/N/Z_values.dat`。PPA/PPA+ modes 会写出对应的 coordinate 和
summary/value outputs。

## Benchmark 状态

原始 Linux `Z1+.ex` binary 只作为 fixture oracle；它不是 Python package 的
runtime dependency。

当前 regression evidence 写到：

```text
.omo/evidence/pyz1-benchmark-regression.md
```

该 report 会把每个公开 benchmark/mode 分类为 `passed`、`mismatch` 或
`known-invalid`。当前 clean-room reducer 尚未与 Z1+ 数值等价：
`benchmark-04` default/SP+/selfZ 报告为 `passed`，`benchmark-01`、
`benchmark-02`、`benchmark-03` 和 `benchmark-05` 仍为 `mismatch`；更大的
benchmark case 在 reducer 获得 neighbor-list 风格加速之前，会被透明的
`node_count` guard 作为性能 skip。

## 限制

- 公开源码缺少 `module-Z1.f90`，因此 default 几何 Z1 reducer 是 clean-room
  实现，不是 Fortran 翻译。
- Default/SP+ reducer parity 尚未完成。不要把当前输出当作 Z1+ scientific
  production run 的 drop-in replacement。
- PPA/PPA+ 已有原生 Python execution 和 oracle-backed summary slices，但完整
  benchmark-level runtime parity 仍未完成。
- `-selfZ` / `-0` 已有 package execution surface，但 selfZ scientific parity
  与 default/SP+ path 一样受 clean-room reducer 限制，需要通过 benchmark
  regression report 判断。
- 第一版实现有意避免 GPU、CUDA、CuPy、PyTorch、Numba 和 accelerator-specific
  dependencies。

参见 `docs/pyz1-contract.md` 了解 implementation contract 和 parity policy，
`docs/evidence-ledger.md` 查看当前 test/evidence index，
`docs/completion-audit.md` 查看当前 completion verdict。
