from __future__ import annotations

from dataclasses import dataclass

from pyz1.geometry import (
    GEOMETRY_TOLERANCE,
    Segment,
    chain_contour,
    closest_segment_points,
    segment_distance,
)
from pyz1.models import Chain, Vector3


@dataclass(frozen=True, slots=True)
class ContactConstrainedNodeRelaxation:
    previous: Vector3
    current: Vector3
    next_node: Vector3
    contact: Segment
    max_contact_distance: float


def relax_contact_constrained_node(
    relaxation: ContactConstrainedNodeRelaxation,
) -> Vector3:
    direct_path = Segment(start=relaxation.previous, end=relaxation.next_node)
    direct_contact = closest_segment_points(direct_path, relaxation.contact)
    candidate = direct_contact.first_point
    if direct_contact.distance > relaxation.max_contact_distance + GEOMETRY_TOLERANCE:
        candidate = direct_contact.second_point
    point_contact_distance = segment_distance(
        Segment(start=candidate, end=candidate),
        relaxation.contact,
    )
    if point_contact_distance > relaxation.max_contact_distance + GEOMETRY_TOLERANCE:
        return relaxation.current
    old_contour = chain_contour(
        Chain((relaxation.previous, relaxation.current, relaxation.next_node)),
    )
    new_contour = chain_contour(
        Chain((relaxation.previous, candidate, relaxation.next_node)),
    )
    if new_contour >= old_contour - GEOMETRY_TOLERANCE:
        return relaxation.current
    return candidate
