from dataclasses import dataclass
from typing import Dict, List, Tuple

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box


@dataclass
class Pose:
    x: float
    y: float
    theta: float

    @property
    def xy(self):
        return (self.x, self.y)


@dataclass
class GosModel:
    """Structure represents a road vehicle."""

    name: str
    dmgIdx: int
    t: float  # angle (theta)
    pX: float  # position x
    pY: float  # position y
    sX: float  # size in X direction
    sY: float  # size in Y direction
    bsX: float  # inner border in X direction
    bsY: float  # inner border in Y direction

    def outer_box(self) -> Polygon:
        return create_polygon(self.pX, self.pY, self.sX, self.sY, self.t)

    def inner_box(self) -> Polygon:
        return create_polygon(self.pX, self.pY, self.bsX, self.bsY, self.t)

    def get_center_coordinates(self) -> Tuple[float, float, float]:
        return self.pX, self.pY, self.t

    def get_pose(self) -> Pose:
        return Pose(*self.get_center_coordinates())

    def scale(self, scale: float):
        return GosModel(
            self.name,
            self.dmgIdx,
            self.t,
            self.pX * scale,
            self.pY * scale,
            self.sX * scale,
            self.sY * scale,
            self.bsX * scale,
            self.bsY * scale,
        )


@dataclass
class Label:
    """Structure represents a label."""

    posX: float  # position x
    posY: float  # position y
    sX: float  # size in X direction
    sY: float  # size in Y direction
    theta: float  # angle (theta)
    text: str

    def outer_box(self) -> Polygon:
        return create_polygon(self.posX, self.posY, self.sX, self.sY, self.theta)

    def scale(self, scale: float):
        return Label(
            self.posX * scale,
            self.posY * scale,
            self.sX * scale,
            self.sY * scale,
            self.theta,
            self.text,
        )


@dataclass
class PolyCurve:
    linestring: LineString
    attributes: Dict

    @classmethod
    def from_coords(
        cls, coords: List[Tuple[float, float]], attrs=dict()
    ) -> "PolyCurve":
        ls = LineString(coords)
        return PolyCurve(ls, attrs)

    def scale(self, scale: float):
        return PolyCurve(
            affinity.scale(self.linestring, scale, scale, origin=Point(0, 0)),
            self.attributes,
        )


def create_polygon(x, y, s_x, s_y, theta) -> Polygon:
    bbox = box(x - s_x / 2, y - s_y / 2, x + s_x / 2, y + s_y / 2)
    bbox_rotated = affinity.rotate(bbox, theta, use_radians=True)
    return bbox_rotated
