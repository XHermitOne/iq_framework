#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Map management class 2GIS.
"""

import jinja2

from . import double_gis_util

from iq.util import txtfile_func

__version__ = (0, 0, 0, 1)

# Template for the resulting HTML document
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
        <script src="https://maps.api.2gis.ru/2.0/loader.js?pkg=full"></script>
        {{ map }}
    </head>
    <body>
        <div id="map" style="width:{{ width[0] }}{{ width[1] }}; height:{{ height[0] }}{{ height[1] }}"></div>
    </body>
</html>
'''

# Card template
MAP_TEMPLATE = '''
<script type="text/javascript">
    var map;

    DG.then(function () {
        map = DG.map('map', {
            center: {{ location }},
            zoom: {{ zoom }}
        });
        
{% for marker in markers %}
    {{ marker.render() }}
{% endfor %}
    });
</script>
'''


class iq2GISMap(object):
    """
    Map management class 2GIS.
    """
    _map_template = jinja2.Template(MAP_TEMPLATE)
    _html_template = jinja2.Template(HTML_TEMPLATE)

    def __init__(self, location=None,
                 width='2000px', height='1300px',
                 left='0%', top='0%',
                 position=None,
                 tiles='OpenStreetMap',
                 attr=None,
                 min_zoom=0,
                 max_zoom=18,
                 zoom_start=10,
                 min_lat=-90,
                 max_lat=90,
                 min_lon=-180,
                 max_lon=180,
                 max_bounds=False,
                 crs='EPSG3857',
                 control_scale=False,
                 prefer_canvas=False,
                 no_touch=False,
                 disable_3d=False,
                 png_enabled=False,
                 zoom_control=True,
                 **kwargs):
        """
        Constructor.

        :param location: Geolocation point (latitude, longitude) of the center of the map.
        :param width: Map width.
        :param height: Map height.
        :param left:
        :param top:
        :param position:
        :param tiles: Map of the set of tiles to use.
        :param attr: Map tile attribution; only required when passing a custom tile url.
        :param min_zoom: The minimum allowed zoom level for the tile layer being created.
        :param max_zoom: The maximum allowable zoom level for the created tile layer.
        :param zoom_start: The initial zoom level for the map.
        :param min_lat:
        :param max_lat:
        :param min_lon:
        :param max_lon:
        :param max_bounds:
        :param crs:
        :param control_scale: Regardless of whether to add scale controls on the map.
        :param prefer_canvas:
        :param no_touch:
        :param disable_3d:
        :param png_enabled:
        :param zoom_control: Display zoom control on the map.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
            zoom_start = 1
        else:
            self.location = double_gis_util.validate_location(location)

        #
        self.width = double_gis_util.parse_size(width)
        self.height = double_gis_util.parse_size(height)
        self.left = double_gis_util.parse_size(left)
        self.top = double_gis_util.parse_size(top)
        # self.position = position

        # Scaling
        self.zoom = zoom_start

        # Markers
        self.markers = list()

    def add_marker(self, marker):
        """
        Add a marker to the map.

        :param marker: Marker object.
        :return: True/False.
        """
        self.markers.append(marker)
        return True

    def render(self, **kwargs):
        """
        Generates the HTML representation of the element.

        :return: The generated HTML representation of the map.
        """
        return self._map_template.render(location=self.location,
                                         zoom=self.zoom,
                                         markers=self.markers,
                                         **kwargs)

    def save(self, html_filename):
        """
        Save the map to HTML file.

        :param html_filename: Full name of the HTML file.
        :return: True/False.
        """
        map_html = self.render()
        html = self._html_template.render(map=map_html,
                                          width=self.width,
                                          height=self.height)

        return txtfile_func.saveTextFile(html_filename, html)


# To support rendering, class names need to be overridden
Map = iq2GISMap
