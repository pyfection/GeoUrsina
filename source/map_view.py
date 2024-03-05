from enum import Enum

from lod import LOD
from lod.radial import RadialLOD
from nodes import Node
from nodes.plane import PlaneNode
from providers import MapProvider


class MapMode(Enum):
    """The mode in which the map is displayed."""
    PLANAR = PlaneNode


class MapView:
    """Main class for viewing the map."""
    sprites = {}
    mode: MapMode
    provider: MapProvider
    root_node: Node
    lod: LOD

    def __init__(self, mode, provider):
        self.mode = mode
        self.provider = provider
        self.lod = RadialLOD(self)
        self.root_node = mode.value(self)
