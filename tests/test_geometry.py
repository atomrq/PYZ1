from __future__ import annotations

from math import isclose

from pyz1.geometry import (
    CleanedPath,
    GeometryBox,
    MoveContext,
    NodeMove,
    Segment,
    chain_contour,
    clean_collinear_kinks,
    closest_segment_points,
    evaluate_node_move,
    minimum_image_delta,
    segment_distance,
    segment_intersects_triangle,
    segments_cross_xy,
    unfold_chain,
)
from pyz1.models import Chain, Vector3

FLOAT_TOLERANCE = 1.0e-12


def test_minimum_image_delta_when_sheared_boundary_is_crossed() -> None:
    box = GeometryBox(lengths=Vector3(10.0, 10.0, 10.0), shear=2.0)

    delta = minimum_image_delta(
        Segment(start=Vector3(1.0, 1.0, 0.0), end=Vector3(9.0, 9.0, 0.0)),
        box,
    )

    assert_vector_close(delta, Vector3(-4.0, -2.0, 0.0))


def test_unfold_chain_when_periodic_nodes_cross_boundary() -> None:
    chain = Chain(
        (
            Vector3(9.5, 5.0, 0.0),
            Vector3(0.5, 5.0, 0.0),
            Vector3(1.5, 5.0, 0.0),
        ),
    )
    box = GeometryBox(lengths=Vector3(10.0, 10.0, 10.0), shear=0.0)

    unfolded = unfold_chain(chain, box)

    assert_vector_close(unfolded.nodes[0], Vector3(9.5, 5.0, 0.0))
    assert_vector_close(unfolded.nodes[1], Vector3(10.5, 5.0, 0.0))
    assert isclose(chain_contour(unfolded), 2.0, abs_tol=FLOAT_TOLERANCE)


def test_segment_distance_when_skew_segments_have_positive_gap() -> None:
    first = Segment(start=Vector3(0.0, 0.0, 0.0), end=Vector3(1.0, 0.0, 0.0))
    second = Segment(start=Vector3(0.5, 1.0, 1.0), end=Vector3(0.5, 1.0, -1.0))

    distance = segment_distance(first, second)

    assert isclose(distance, 1.0, abs_tol=FLOAT_TOLERANCE)


def test_closest_segment_points_returns_contact_fractions() -> None:
    first = Segment(start=Vector3(0.0, 0.0, 0.0), end=Vector3(2.0, 0.0, 0.0))
    second = Segment(start=Vector3(1.5, 1.0, 0.0), end=Vector3(1.5, -1.0, 0.0))

    closest = closest_segment_points(first, second)

    assert isclose(closest.distance, 0.0, abs_tol=FLOAT_TOLERANCE)
    assert isclose(closest.first_fraction, 0.75, abs_tol=FLOAT_TOLERANCE)
    assert isclose(closest.second_fraction, 0.5, abs_tol=FLOAT_TOLERANCE)
    assert_vector_close(closest.first_point, Vector3(1.5, 0.0, 0.0))
    assert_vector_close(closest.second_point, Vector3(1.5, 0.0, 0.0))


def test_segments_cross_xy_when_projections_intersect() -> None:
    first = Segment(start=Vector3(0.0, 0.0, 0.0), end=Vector3(1.0, 1.0, 0.0))
    second = Segment(start=Vector3(0.0, 1.0, 0.0), end=Vector3(1.0, 0.0, 0.0))

    crosses = segments_cross_xy(first, second)

    assert crosses is True


def test_segment_intersects_triangle_when_segment_pierces_swept_area() -> None:
    triangle = (
        Vector3(0.0, 0.0, 0.0),
        Vector3(0.0, 2.0, 0.0),
        Vector3(1.0, 1.0, 0.0),
    )
    segment = Segment(
        start=Vector3(0.5, 1.0, -1.0),
        end=Vector3(0.5, 1.0, 1.0),
    )

    intersects = segment_intersects_triangle(segment, triangle)

    assert intersects is True


def test_segment_intersects_triangle_when_segment_is_above_area_is_false() -> None:
    triangle = (
        Vector3(0.0, 0.0, 0.0),
        Vector3(0.0, 2.0, 0.0),
        Vector3(1.0, 1.0, 0.0),
    )
    segment = Segment(
        start=Vector3(0.5, 0.2, 1.0),
        end=Vector3(0.5, 0.8, 1.0),
    )

    intersects = segment_intersects_triangle(segment, triangle)

    assert intersects is False


def test_evaluate_node_move_when_endpoint_is_targeted_rejects_move() -> None:
    chain = Chain(
        (
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.5, 1.0, 0.0),
            Vector3(1.0, 0.0, 0.0),
        ),
    )
    move = NodeMove(node_index=0, position=Vector3(0.1, 0.0, 0.0))
    context = MoveContext(blocking_segments=())

    evaluation = evaluate_node_move(chain, move, context)

    assert evaluation.accepted is False
    assert evaluation.reason == "endpoint"


def test_evaluate_node_move_when_contour_shortens_accepts_move() -> None:
    chain = Chain(
        (
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.5, 1.0, 0.0),
            Vector3(1.0, 0.0, 0.0),
        ),
    )
    move = NodeMove(node_index=1, position=Vector3(0.5, 0.0, 0.0))
    context = MoveContext(blocking_segments=())

    evaluation = evaluate_node_move(chain, move, context)

    assert evaluation.accepted is True
    assert evaluation.reason == "accepted"
    assert evaluation.new_contour < evaluation.old_contour


def test_evaluate_node_move_when_candidate_crosses_blocker_rejects_move() -> None:
    chain = Chain(
        (
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 2.0, 0.0),
            Vector3(1.0, 1.0, 0.0),
        ),
    )
    blocker = Segment(
        start=Vector3(0.5, -0.2, 0.0),
        end=Vector3(0.5, 0.8, 0.0),
    )
    move = NodeMove(node_index=1, position=Vector3(1.0, 0.0, 0.0))
    context = MoveContext(blocking_segments=(blocker,))

    evaluation = evaluate_node_move(chain, move, context)

    assert evaluation.accepted is False
    assert evaluation.reason == "crossing"


def test_evaluate_node_move_when_projected_crossing_is_3d_separated() -> None:
    chain = Chain(
        (
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 2.0, 0.0),
            Vector3(1.0, 1.0, 0.0),
        ),
    )
    blocker = Segment(
        start=Vector3(0.5, -0.2, 1.0),
        end=Vector3(0.5, 0.8, 1.0),
    )
    move = NodeMove(node_index=1, position=Vector3(1.0, 0.0, 0.0))
    context = MoveContext(blocking_segments=(blocker,))

    evaluation = evaluate_node_move(chain, move, context)

    assert evaluation.accepted is True


def test_clean_collinear_kinks_when_path_has_redundant_nodes() -> None:
    chain = Chain(
        (
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.5, 0.0, 0.0),
            Vector3(1.0, 0.0, 0.0),
            Vector3(1.0, 1.0, 0.0),
        ),
    )

    cleaned = clean_collinear_kinks(chain)

    assert cleaned == CleanedPath(
        chain=Chain(
            (
                Vector3(0.0, 0.0, 0.0),
                Vector3(1.0, 0.0, 0.0),
                Vector3(1.0, 1.0, 0.0),
            ),
        ),
        removed_node_count=1,
    )


def assert_vector_close(actual: Vector3, expected: Vector3) -> None:
    assert isclose(actual.x, expected.x, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.y, expected.y, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.z, expected.z, abs_tol=FLOAT_TOLERANCE)
