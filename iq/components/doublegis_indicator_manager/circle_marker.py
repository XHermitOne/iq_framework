#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Circular marker control class.
"""

import jinja2
import json
from . import double_gis_util

from iq.util import log_func

__version__ = (0, 0, 0, 1)

MARKER_TEMPLATE = '''
DG.circleMarker({{ location }}).setRadius({{ radius }}).setStyle({{ options }}){% if popup %}.bindPopup('{{ popup }}'){% endif %}{% if tooltip %}.bindLabel('{{ tooltip }}'){% endif %}.addTo(map);'''


class iq2GISCircleMarker(object):
    """
    Circle marker.
    """
    _marker_template = jinja2.Template(MARKER_TEMPLATE)

    def __init__(self, location, radius=10,
                 popup=None, tooltip=None,
                 color='blue',
                 fill=True,
                 fill_color='blue',
                 **kwargs):
        """
        Constructor.

        :param location: Marker geolocation.
        :param radius: Marker circle radius.
        :param color: Circle color.
        :param fill: Fill the inner area of the circle?
        :param fill_color: The fill color of the circle.
        :param popup: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip: Marker pop-up text.
            A tooltip appears when you hover the mouse over the marker.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
        else:
            self.location = double_gis_util.validate_location(location)

        self.radius = int(radius)

        self.popup = popup.replace('\'', '^') if isinstance(popup, str) else popup
        self.tooltip = tooltip.replace('\'', '^') if isinstance(tooltip, str) else tooltip

        self.color = color
        self.fill = fill
        self.fill_color = fill_color

    def render(self, **kwargs):
        """
        Generates the HTML representation of the element.

        :return: The generated HTML representation of the map.
        """
        options = dict(color=self.color)
        json_options = json.dumps(options)
        return self._marker_template.render(location=self.location,
                                            radius=self.radius,
                                            options=json_options,
                                            popup=self.popup,
                                            tooltip=self.tooltip,
                                            **kwargs)

    def add_to(self, geo_map):
        """
        Add a marker to the map.

        :param geo_map: Map object.
        :return: True/False.
        """
        try:
            geo_map.add_marker(self)
            return True
        except:
            log_func.fatal(u'Error adding circular marker to map')
        return False


# To support rendering, class names need to be overridden
CircleMarker = iq2GISCircleMarker
