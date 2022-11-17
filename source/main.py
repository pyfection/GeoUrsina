"""Main file to test the package."""

import os

from ursina import (
    Ursina,
)

from providers.bing_maps import BingMapsProvider
from map_view import MapView, MapMode


app = Ursina()


provider = BingMapsProvider(
    name="Test",
    api_key=os.getenv("BING_MAPS_API_KEY"),
)
map_view = MapView(MapMode.PLANAR, provider)
# Mouse Movement:
#  Move -> Middle click/drag
#  Rotate -> Right click
#  Zoom -> Scroll wheel

app.run()
