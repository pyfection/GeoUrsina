from ursina import camera, distance
import time

from lod import LOD


class RadialLOD(LOD):
    """Calculates LOD based on distance to tiles."""
    # Higher number makes image more clear, but takes longer to load because
    # it has to load more tiles
    ideal_distance: float = 3.0

    def update(self):
        super().update()
        for node in self.view.root_node.walk():
            if not node.sprite.visible:
                continue
            ideal_distance = self.ideal_distance / 2 ** (node.level - 1)
            d = distance(self.position, node.sprite)
            #print("Observer position = ", self.position)
            #print("D", d, ideal_distance, node.level, node.x, node.y)
            if d < ideal_distance * 0.7:#0.75:
                node.subdivide()
            elif node.parent_node and d > ideal_distance * 1.6: #1.5:
                node.parent_node.simplify()
