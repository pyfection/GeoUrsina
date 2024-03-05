from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from ursina import Sprite
#from ursina import Entity

if TYPE_CHECKING:
    from map_view import MapView


class NodeLocation(Enum):
    """Location of node inside parent node."""
    ROOT = -1
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


@dataclass
class Node(ABC):
    """Base class for all types of nodes."""
    map_view: "MapView"
    parent_node: "Node" = None
    location: NodeLocation = NodeLocation.ROOT
    level: int = 1
    x: int = 0
    y: int = 0
    sprite: Sprite = None
    children: list = field(default_factory=list)
    num_children: int = 4  # Maximum number of children

    def __post_init__(self):
        texture = self.map_view.provider.fetch_tile(self.level, self.x, self.y)
        lvl = self.level - 1
        self.sprite = Sprite(texture=texture)
        #self.sprite = Entity(model='cube', texture=texture)
        s = 1/2**lvl
        self.sprite.scale = (s, s, 1)
        # s * 0.5 because it calculates where it is from its center point
        self.sprite.x = self.x / 2 ** lvl + s * 0.5
        self.sprite.z = 1 - (self.y / 2 ** lvl + s * 0.5)
        # For testing comment out the next line, makes it very easy to see the subdivisions since the sprites will be vertical instead of horizontal
        self.sprite.rotation_x = 90
        print("Created node", self.level, self.x, self.y, self.sprite.position, self.sprite.world_position, self.sprite.screen_position)

    @property
    def scale(self):
        return self.sprite.scale

    @scale.setter
    def scale(self, value):
        self.sprite.scale = value

    @property
    def scale_x(self):
        return self.sprite.scale_x

    @property
    def scale_y(self):
        return self.sprite.scale_y

    @property
    def scale_z(self):
        return self.sprite.scale_z

    @abstractmethod
    def create_child_nodes(self):
        """Creates child nodes. Has to be overridden by subclass."""

    def subdivide(self):
        """Subdivides current node into child nodes."""
        max_zoom = self.map_view.provider.max_zoom
        if self.children or self.level >= max_zoom:
            return
        print("Subdivide", self.level, self.x, self.y, len(self.children))
        self.create_child_nodes()
        self.sprite.visible = False

    def simplify(self):
        """
        Simplifies current node
        by becoming visible again and deleting children.
        """
        self.sprite.visible = True
        for node in self.children:
            node.sprite.visible = False
        print("Simplify", self.level, self.x, self.y)
        self.children.clear()

    def walk(self) -> list["Node"]:
        """Returns this node and all nodes below it."""
        nodes = [self]
        i = 0
        while i < len(nodes):
            node = nodes[i]
            nodes += node.children
            i += 1
        return nodes
