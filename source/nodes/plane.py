from nodes import Node, NodeLocation


class PlaneNode(Node):
    """Rectangular map node."""
    def create_child_nodes(self):
        level = self.level + 1
        x = self.x * 2
        y = self.y * 2
        print("Create child nodes for", self.level, self.x, self.y)

        data = zip(
            (x, x+1, x, x+1),
            (y, y, y+1, y+1),
            list(NodeLocation)[1:],
        )
        for x_, y_, loc in data:
            node = PlaneNode(
                self.map_view, self, loc, level,
                x=x_, y=y_,
            )
            self.children.append(node)
