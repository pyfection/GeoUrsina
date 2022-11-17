import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import sleep
from typing import ClassVar

import requests

from . import MapProvider


class MapTypes(Enum):
    AERIAL = "a"
    ROAD = "r"
    AERIAL_LABELS = "h"
    OBLIQUE = "o"
    OBLIQUE_LABELS = "b"


@dataclass
class BingMapsProvider(MapProvider):
    """Bing Tile Maps Provider."""
    api_key: str = ""
    address: str = "https://dev.virtualearth.net"
    format: str = "jpeg"
    max_zoom: int = 6#19  # ToDo: to be reset to 19
    map_type: str = MapTypes.AERIAL.value
    map_size: int = 512
    culture: str = "en-US"
    subdomains: ClassVar = ["t0", "t1", "t2", "t3"]

    def __post_init__(self):
        path = Path(__file__).parent.parent / "image_cache/bing"
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def zoom_size(zoom: int):
        return 2 ** zoom

    def quad_key(self, zoom: int, x: int, y: int) -> str:
        """Bing Quad Key.
        https://learn.microsoft.com/en-us/bingmaps/articles/
        bing-maps-tile-system?redirectedfrom=MSDN#tile-coordinates-and-quadkeys
        """
        return str(int(bin(x)[2:]) + int(bin(y)[2:]) * 2).rjust(zoom, "0")

    def fetch_tile(self, zoom: int, x: int, y: int) -> str:
        quad_key = self.quad_key(zoom, x, y)
        path = (
            Path(__file__).parent.parent / f"image_cache/bing/{quad_key}.jpeg"
        )
        if os.path.exists(path):
            return quad_key

        while not self.subdomains:
            sleep(1)
        subdomain = self.subdomains.pop(0)

        url = "".join([
            f"http://ecn.{subdomain}.tiles.virtualearth.net"
            f"/tiles/{self.map_type}{quad_key}.jpeg"
            f"?g=1173&mkt={self.culture}&shading=hill&stl=H"
        ])
        resp = requests.get(url, stream=True)
        # ToDo: handle other status codes
        if resp.status_code == 200:
            resp.raw.decode_content = True
            with open(path, "wb") as f:
                for chunk in resp:
                    f.write(chunk)
        self.subdomains.append(subdomain)
        return quad_key

    def get_metadata(self):
        pass  # ToDo
