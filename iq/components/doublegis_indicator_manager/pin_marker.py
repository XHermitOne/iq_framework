#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A pointer marker management class.
"""

import jinja2
import PIL.Image

from . import double_gis_util
from . import marker_icon

from iq.util import log_func

__version__ = (0, 0, 0, 1)


MARKER_TEMPLATE = '''
DG.marker({{ location }}{% if icon %}, {icon: DG.icon({iconUrl: '{{ icon }}', iconSize: [{{ icon_width }}, {{ icon_height }}], iconAnchor: [{{ icon_anchor_x }}, {{ icon_anchor_y }}]})}{% endif %}).addTo(map)
{% if tooltip %}.bindLabel('{{ tooltip }}'){% endif %}
{% if popup %}.bindPopup('{{ popup }}'){% endif %}
;'''

DEFAULT_ICON_WIDTH = 32
DEFAULT_ICON_HEIGHT = 32
DEFAULT_ICON_SIZE = (DEFAULT_ICON_WIDTH, DEFAULT_ICON_HEIGHT)
DEFAULT_ICON_ANCHOR_X = 16
DEFAULT_ICON_ANCHOR_Y = 31


class iq2GISMarker(object):
    """
    Pin marker.
    """
    _marker_template = jinja2.Template(MARKER_TEMPLATE)

    def __init__(self, location,
                 popup=None, tooltip=None,
                 icon=None,
                 **kwargs):
        """
        Constructor.

        :param location: Marker geolocation.
        :param popup: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip: Marker pop-up text.
            A tooltip appears when you hover the mouse over the marker.
        :param icon: Icon.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
        else:
            self.location = double_gis_util.validate_location(location)

        self.popup = popup.replace('\'', '^') if isinstance(popup, str) else popup
        self.tooltip = tooltip.replace('\'', '^') if isinstance(tooltip, str) else tooltip

        self.icon = marker_icon.getMarkerIconFilename(icon) if isinstance(icon, str) else icon

    def render(self, **kwargs):
        """
        Generates the HTML representation of the element.

        :return: The generated HTML representation of the map.
        """
        icon_size = PIL.Image.open(self.icon).size if self.icon else DEFAULT_ICON_SIZE
        icon_width = icon_size[0]
        icon_height = icon_size[1]
        icon_anchor_x = int(icon_width / 2)
        icon_anchor_y = icon_height - 1

        return self._marker_template.render(location=self.location,
                                            icon=self.icon,
                                            popup=self.popup,
                                            tooltip=self.tooltip,
                                            icon_width=icon_width,
                                            icon_height=icon_height,
                                            icon_anchor_x=icon_anchor_x,
                                            icon_anchor_y=icon_anchor_y,
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
            log_func.fatal(u'Error adding pointer marker to map')
        return False


# To support rendering, class names need to be overridden
Marker = iq2GISMarker
