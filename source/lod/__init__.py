from typing import TYPE_CHECKING

from ursina import EditorCamera

if TYPE_CHECKING:
    from map_view import MapView


class LOD(EditorCamera):
    """Base class for Level Of Detail calculations."""
    def __init__(self, view: "MapView"):
        self.view = view
        super().__init__()
