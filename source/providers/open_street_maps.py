from dataclasses import dataclass

import aiohttp
from ursina import Sprite

from . import MapProvider


@dataclass
class OpenStreetMapsProvider(MapProvider):
    """OpenStreetMaps Provider."""
    # ToDo: this provider is under construction
    address: str = "https://a.tile.openstreetmap.org/"
    format: str = "png"
    max_zoom: int = 19

    async def fetch_tile(self, zoom: int, x: int, y: int) -> Sprite:
        url = f"{self.address}{zoom}/{x}/{y}.{self.format}"
        print("Getting", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print("Response:")
                print(resp)
