from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MapProvider(ABC):
    """Base class for Map Providers."""
    name: str
    max_zoom: int = 20
    min_zoom: int = 0

    @staticmethod
    def zoom_size(zoom: int):
        """Width and height of map in tiles for given zoom."""
        raise NotImplementedError

    @abstractmethod
    def fetch_tile(self, zoom: int, x: int, y: int):
        """Get tile at given location."""

    @abstractmethod
    def get_metadata(self):
        """Get any metadata available from provider."""
