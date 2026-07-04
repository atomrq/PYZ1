from __future__ import annotations

import pytest

from pyz1.models import Chain, Snapshot, Vector3


def test_snapshot_counts_true_chains_and_dumbbells() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                nodes=(
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                    Vector3(2.0, 0.0, 0.0),
                ),
            ),
            Chain(nodes=(Vector3(0.0, 0.0, -1.0), Vector3(0.0, 0.0, 1.0))),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    assert snapshot.chain_count == 2
    assert snapshot.node_count == 5
    assert snapshot.true_chain_count == 1
    assert snapshot.true_chain_lengths == (3,)


def test_chain_rejects_single_node() -> None:
    with pytest.raises(ValueError, match="at least two nodes"):
        _ = Chain(nodes=(Vector3(0.0, 0.0, 0.0),))


def test_snapshot_rejects_empty_chains() -> None:
    with pytest.raises(ValueError, match="at least one chain"):
        _ = Snapshot(chains=(), box=Vector3(1.0, 1.0, 1.0), label=None, shear=None)
