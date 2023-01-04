from typing import TYPE_CHECKING

from ursina import Vec3

from viewcontroller import ViewController

if TYPE_CHECKING:
    from map_view import MapView


class LOD(ViewController):
    """Base class for Level Of Detail calculations."""
    def __init__(self, view: "MapView"):
        self.view = view
        super().__init__()
        self.position = Vec3(0, 0, -5)
        self.rotation_smoothing = 10
        self.origin_y = -0.5
        self.speed = 1
