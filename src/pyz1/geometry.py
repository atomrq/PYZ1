from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise
from math import sqrt
from typing import Final

from pyz1.errors import InvalidSnapshotError
from pyz1.models import Chain, Vector3

GEOMETRY_TOLERANCE: Final = 1.0e-10


@dataclass(frozen=True, slots=True)
class GeometryBox:
    lengths: Vector3
    shear: float = 0.0

    def __post_init__(self) -> None:
        if (
            self.lengths.x <= 0.0
            or self.lengths.y <= 0.0
            or self.lengths.z <= 0.0
        ):
            raise InvalidSnapshotError(reason="geometry box lengths must be positive")


@dataclass(frozen=True, slots=True)
class Segment:
    start: Vector3
    end: Vector3


@dataclass(frozen=True, slots=True)
class NodeMove:
    node_index: int
    position: Vector3


@dataclass(frozen=True, slots=True)
class MoveContext:
    blocking_segments: tuple[Segment, ...]
    tolerance: float = GEOMETRY_TOLERANCE


class MoveDecision(StrEnum):
    ACCEPTED = "accepted"
    ENDPOINT = "endpoint"
    CONTOUR = "contour"
    CROSSING = "crossing"


@dataclass(frozen=True, slots=True)
class MoveEvaluation:
    accepted: bool
    reason: MoveDecision
    old_contour: float
    new_contour: float


@dataclass(frozen=True, slots=True)
class CleanedPath:
    chain: Chain
    removed_node_count: int


@dataclass(frozen=True, slots=True)
class ClosestSegmentPoints:
    first_fraction: float
    second_fraction: float
    first_point: Vector3
    second_point: Vector3
    distance: float


@dataclass(frozen=True, slots=True)
class _SegmentParameters:
    first_fraction: float
    second_fraction: float


def minimum_image_delta(segment: Segment, box: GeometryBox) -> Vector3:
    return _fold_delta(_subtract(segment.end, segment.start), box)


def unfold_chain(chain: Chain, box: GeometryBox) -> Chain:
    nodes = [chain.nodes[0]]
    for wrapped_node in chain.nodes[1:]:
        delta = minimum_image_delta(
            Segment(start=nodes[-1], end=wrapped_node),
            box,
        )
        nodes.append(_add(nodes[-1], delta))
    return Chain(tuple(nodes))


def chain_contour(chain: Chain) -> float:
    return sum(_distance(first, second) for first, second in pairwise(chain.nodes))


def closest_segment_points(first: Segment, second: Segment) -> ClosestSegmentPoints:
    parameters = _closest_segment_parameters(first, second, GEOMETRY_TOLERANCE)
    first_point = _lerp(first, parameters.first_fraction)
    second_point = _lerp(second, parameters.second_fraction)
    return ClosestSegmentPoints(
        first_fraction=parameters.first_fraction,
        second_fraction=parameters.second_fraction,
        first_point=first_point,
        second_point=second_point,
        distance=_distance(first_point, second_point),
    )


def segment_distance(first: Segment, second: Segment) -> float:
    return closest_segment_points(first, second).distance


def segments_cross_xy(first: Segment, second: Segment) -> bool:
    first_start = _point_xy(first.start)
    first_end = _point_xy(first.end)
    second_start = _point_xy(second.start)
    second_end = _point_xy(second.end)
    first_orientation = _orientation_xy(first_start, first_end, second_start)
    second_orientation = _orientation_xy(first_start, first_end, second_end)
    third_orientation = _orientation_xy(second_start, second_end, first_start)
    fourth_orientation = _orientation_xy(second_start, second_end, first_end)
    return (
        first_orientation * second_orientation < 0.0
        and third_orientation * fourth_orientation < 0.0
    )


def segment_intersects_triangle(
    segment: Segment,
    triangle: tuple[Vector3, Vector3, Vector3],
) -> bool:
    triangle_origin = triangle[0]
    first_edge = _subtract(triangle[1], triangle_origin)
    second_edge = _subtract(triangle[2], triangle_origin)
    normal = _cross(first_edge, second_edge)
    segment_delta = _subtract(segment.end, segment.start)
    denominator = _dot(normal, segment_delta)
    if abs(denominator) <= GEOMETRY_TOLERANCE:
        return False
    fraction = _dot(normal, _subtract(triangle_origin, segment.start)) / denominator
    if fraction < -GEOMETRY_TOLERANCE or fraction > 1.0 + GEOMETRY_TOLERANCE:
        return False
    intersection = _add(segment.start, _scale(segment_delta, fraction))
    return _point_in_triangle(intersection, triangle)


def evaluate_node_move(
    chain: Chain,
    move: NodeMove,
    context: MoveContext,
) -> MoveEvaluation:
    old_contour = chain_contour(chain)
    if move.node_index <= 0 or move.node_index >= chain.node_count - 1:
        return MoveEvaluation(
            accepted=False,
            reason=MoveDecision.ENDPOINT,
            old_contour=old_contour,
            new_contour=old_contour,
        )
    moved_chain = _replace_node(chain, move)
    new_contour = chain_contour(moved_chain)
    if new_contour >= old_contour - context.tolerance:
        return MoveEvaluation(
            accepted=False,
            reason=MoveDecision.CONTOUR,
            old_contour=old_contour,
            new_contour=new_contour,
        )
    if _move_crosses_blocker(moved_chain, move.node_index, context):
        return MoveEvaluation(
            accepted=False,
            reason=MoveDecision.CROSSING,
            old_contour=old_contour,
            new_contour=new_contour,
        )
    return MoveEvaluation(
        accepted=True,
        reason=MoveDecision.ACCEPTED,
        old_contour=old_contour,
        new_contour=new_contour,
    )


def clean_collinear_kinks(chain: Chain) -> CleanedPath:
    kept_nodes = [chain.nodes[0]]
    removed_count = 0
    for node_index in range(1, chain.node_count - 1):
        candidate = chain.nodes[node_index]
        next_node = chain.nodes[node_index + 1]
        if _is_redundant_kink(kept_nodes[-1], candidate, next_node):
            removed_count += 1
        else:
            kept_nodes.append(candidate)
    kept_nodes.append(chain.nodes[-1])
    return CleanedPath(
        chain=Chain(tuple(kept_nodes)),
        removed_node_count=removed_count,
    )


def _fold_delta(delta: Vector3, box: GeometryBox) -> Vector3:
    y_images = round(delta.y / box.lengths.y)
    shifted_x = delta.x - box.shear * y_images
    return Vector3(
        x=shifted_x - round(shifted_x / box.lengths.x) * box.lengths.x,
        y=delta.y - y_images * box.lengths.y,
        z=delta.z - round(delta.z / box.lengths.z) * box.lengths.z,
    )


def _closest_segment_parameters(
    first: Segment,
    second: Segment,
    tolerance: float,
) -> _SegmentParameters:
    first_delta = _subtract(first.end, first.start)
    second_delta = _subtract(second.end, second.start)
    start_delta = _subtract(first.start, second.start)
    first_length = _dot(first_delta, first_delta)
    second_length = _dot(second_delta, second_delta)
    first_projection = _dot(first_delta, start_delta)
    second_projection = _dot(second_delta, start_delta)
    if first_length <= tolerance and second_length <= tolerance:
        return _SegmentParameters(first_fraction=0.0, second_fraction=0.0)
    if first_length <= tolerance:
        return _SegmentParameters(
            first_fraction=0.0,
            second_fraction=_clamp(second_projection / second_length),
        )
    if second_length <= tolerance:
        return _SegmentParameters(
            first_fraction=_clamp(-first_projection / first_length),
            second_fraction=0.0,
        )
    denominator = first_length * second_length - _dot(first_delta, second_delta) ** 2
    return _closest_nonzero_segment_parameters(
        _NonzeroSegmentData(
            first_length=first_length,
            second_length=second_length,
            cross_projection=_dot(first_delta, second_delta),
            first_projection=first_projection,
            second_projection=second_projection,
            denominator=denominator,
            tolerance=tolerance,
        ),
    )


@dataclass(frozen=True, slots=True)
class _NonzeroSegmentData:
    first_length: float
    second_length: float
    cross_projection: float
    first_projection: float
    second_projection: float
    denominator: float
    tolerance: float


def _closest_nonzero_segment_parameters(
    data: _NonzeroSegmentData,
) -> _SegmentParameters:
    if data.denominator <= data.tolerance:
        first_fraction = 0.0
    else:
        first_fraction = _clamp(
            (
                data.cross_projection * data.second_projection
                - data.second_length * data.first_projection
            )
            / data.denominator,
        )
    second_fraction = (
        data.cross_projection * first_fraction + data.second_projection
    ) / data.second_length
    if second_fraction < 0.0:
        return _SegmentParameters(
            first_fraction=_clamp(-data.first_projection / data.first_length),
            second_fraction=0.0,
        )
    if second_fraction > 1.0:
        return _SegmentParameters(
            first_fraction=_clamp(
                (data.cross_projection - data.first_projection) / data.first_length,
            ),
            second_fraction=1.0,
        )
    return _SegmentParameters(
        first_fraction=first_fraction,
        second_fraction=second_fraction,
    )


def _move_crosses_blocker(
    moved_chain: Chain,
    node_index: int,
    context: MoveContext,
) -> bool:
    moved_segments = (
        Segment(
            start=moved_chain.nodes[node_index - 1],
            end=moved_chain.nodes[node_index],
        ),
        Segment(
            start=moved_chain.nodes[node_index],
            end=moved_chain.nodes[node_index + 1],
        ),
    )
    return any(
        segment_distance(moved_segment, blocker) <= context.tolerance
        for moved_segment in moved_segments
        for blocker in context.blocking_segments
    )


def _replace_node(chain: Chain, move: NodeMove) -> Chain:
    return Chain(
        (
            *chain.nodes[: move.node_index],
            move.position,
            *chain.nodes[move.node_index + 1 :],
        ),
    )


def _is_redundant_kink(
    previous: Vector3,
    candidate: Vector3,
    next_node: Vector3,
) -> bool:
    incoming = _subtract(candidate, previous)
    outgoing = _subtract(next_node, candidate)
    incoming_length = _norm(incoming)
    outgoing_length = _norm(outgoing)
    if incoming_length <= GEOMETRY_TOLERANCE or outgoing_length <= GEOMETRY_TOLERANCE:
        return True
    direction = _dot(incoming, outgoing)
    if direction <= 0.0:
        return False
    cross = _cross(incoming, outgoing)
    return _norm(cross) <= GEOMETRY_TOLERANCE * incoming_length * outgoing_length


def _point_xy(vector: Vector3) -> tuple[float, float]:
    return (vector.x, vector.y)


def _orientation_xy(
    origin: tuple[float, float],
    first: tuple[float, float],
    second: tuple[float, float],
) -> float:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (
        first[1] - origin[1]
    ) * (second[0] - origin[0])


def _lerp(segment: Segment, fraction: float) -> Vector3:
    delta = _subtract(segment.end, segment.start)
    return _add(segment.start, _scale(delta, fraction))


def _clamp(value: float) -> float:
    return min(max(value, 0.0), 1.0)


def _point_in_triangle(
    point: Vector3,
    triangle: tuple[Vector3, Vector3, Vector3],
) -> bool:
    origin = triangle[0]
    first_edge = _subtract(triangle[1], origin)
    second_edge = _subtract(triangle[2], origin)
    point_delta = _subtract(point, origin)
    first_dot = _dot(first_edge, first_edge)
    cross_dot = _dot(first_edge, second_edge)
    second_dot = _dot(second_edge, second_edge)
    point_first_dot = _dot(point_delta, first_edge)
    point_second_dot = _dot(point_delta, second_edge)
    denominator = first_dot * second_dot - cross_dot * cross_dot
    if abs(denominator) <= GEOMETRY_TOLERANCE:
        return False
    first_coordinate = (
        second_dot * point_first_dot - cross_dot * point_second_dot
    ) / denominator
    second_coordinate = (
        first_dot * point_second_dot - cross_dot * point_first_dot
    ) / denominator
    return (
        first_coordinate >= -GEOMETRY_TOLERANCE
        and second_coordinate >= -GEOMETRY_TOLERANCE
        and first_coordinate + second_coordinate <= 1.0 + GEOMETRY_TOLERANCE
    )


def _add(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x + second.x, first.y + second.y, first.z + second.z)


def _subtract(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x - second.x, first.y - second.y, first.z - second.z)


def _scale(vector: Vector3, scale: float) -> Vector3:
    return Vector3(vector.x * scale, vector.y * scale, vector.z * scale)


def _dot(first: Vector3, second: Vector3) -> float:
    return first.x * second.x + first.y * second.y + first.z * second.z


def _cross(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(
        x=first.y * second.z - first.z * second.y,
        y=first.z * second.x - first.x * second.z,
        z=first.x * second.y - first.y * second.x,
    )


def _norm(vector: Vector3) -> float:
    return sqrt(_dot(vector, vector))


def _distance(first: Vector3, second: Vector3) -> float:
    return _norm(_subtract(first, second))
