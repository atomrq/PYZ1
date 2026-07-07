# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
# ]
# ///
# How to run:
# PYTHONPATH=src PYZ1_SOURCE_Z1=/path/to/source_z1 uv run .omo/evidence/task-161-chain37-contour/diag-chain37-contour.py

from __future__ import annotations

from os import environ
from pathlib import Path

import numpy as np

from pyz1.output_io import read_shortest_path_file
from pyz1.output_models import ShortestPathChain, ShortestPathNode
from pyz1.reducer import ReducerSettings, reduce_snapshot
from pyz1.z1_io import read_z1_file


SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703")


def main() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")
    oracle = read_shortest_path_file(
        ORACLE_ROOT / "benchmark-05" / "spplus" / "Z1+SP.dat",
    )
    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))
    actual = result.shortest_path.chains[36]
    expected = oracle.chains[36]

    print_chain("actual", actual)
    print_chain("oracle", expected)
    print_original_source_positions(snapshot.chains[36], actual, expected)


def print_chain(label: str, chain: ShortestPathChain) -> None:
    print(f"{label} contour={contour(chain):.15f} node_count={len(chain.nodes)}")
    for index, node in enumerate(chain.nodes, start=1):
        pair = "none"
        if node.pair is not None:
            pair = f"({node.pair.chain_index},{node.pair.node_index})"
        print(
            f"{label} node{index}: source={node.source_bead:g} "
            f"pos=({node.position.x:.6f},{node.position.y:.6f},{node.position.z:.6f}) "
            f"pair={pair}",
        )
    segment_lengths = tuple(
        node_distance(first, second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )
    print(
        f"{label} segments="
        + ",".join(f"{segment_length:.6f}" for segment_length in segment_lengths),
    )


def contour(chain: ShortestPathChain) -> float:
    return sum(
        node_distance(first, second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def node_distance(first: ShortestPathNode, second: ShortestPathNode) -> float:
    first_position = np.array(first.position.as_tuple())
    second_position = np.array(second.position.as_tuple())
    return float(np.linalg.norm(first_position - second_position))


def print_original_source_positions(
    source_chain,
    actual: ShortestPathChain,
    expected: ShortestPathChain,
) -> None:
    for index, (actual_node, expected_node) in enumerate(
        zip(actual.nodes[1:-1], expected.nodes[1:-1], strict=True),
        start=2,
    ):
        source_position = interpolate_source_bead(source_chain, actual_node.source_bead)
        actual_delta = vector_distance(actual_node.position, source_position)
        oracle_delta = vector_distance(expected_node.position, source_position)
        print(
            f"source node{index}: source={actual_node.source_bead:g} "
            f"pos=({source_position.x:.6f},{source_position.y:.6f},{source_position.z:.6f}) "
            f"actual_delta={actual_delta:.6f} oracle_delta={oracle_delta:.6f}",
        )


def interpolate_source_bead(chain, source_bead: float):
    segment_index = int(source_bead) - 1
    fraction = source_bead - int(source_bead)
    start = chain.nodes[segment_index]
    end = chain.nodes[segment_index + 1]
    start_position = np.array(start.as_tuple())
    end_position = np.array(end.as_tuple())
    position = start_position + (end_position - start_position) * fraction
    return type(start)(float(position[0]), float(position[1]), float(position[2]))


def vector_distance(first, second) -> float:
    first_position = np.array(first.as_tuple())
    second_position = np.array(second.as_tuple())
    return float(np.linalg.norm(first_position - second_position))


if __name__ == "__main__":
    main()
