from dataclasses import dataclass

@dataclass
class BoundingBoxData():
    position: (float, float, float) = (0, 0, 0)
    height: float = 0
    width: float = 0
    length: float = 0
    ry: float = 0

@dataclass
class Vector3():
    x: float = 0
    y: float = 0
    z: float = 0

@dataclass
class Vector2():
    x: float = 0
    y: float = 0