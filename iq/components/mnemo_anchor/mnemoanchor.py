#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme anchor manager class.
"""

from . import spc

from ...util import log_func

__version__ = (0, 0, 0, 1)

CORRECT_SVG_OFFSET_X = 0
CORRECT_SVG_OFFSET_Y = 0


class iqMnemoAnchorManager(object):
    """
    Mnemoscheme anchor manager class.
    """
    def __init__(self, mnemoscheme=None, pos=None, size=None,
                 direction=spc.ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | spc.ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                 min_size=None, max_size=None):
        """
        Constructor.

        :param mnemoscheme: Mnemoscheme object.
        :param pos: Anchor reference position in SVG units.
        :param size: Anchor cell size in SVG units.
        :param direction: Indication of the direction of the anchor displacement relative to the anchor point.
        :param min_size: Specify a minimum pixel size limit.
        :param max_size: Specifying a maximum size limit in pixels.
        """
        self._mnemoscheme = mnemoscheme
        self._position = pos
        self._size = size
        self._direction = direction
        self._min_size = min_size
        self._max_size = max_size

    def getAttachment(self):
        """
        Get the object attached to the anchor control.

        :return: Object of control, which can be placed on a mnemonic diagram
            or None if error.
        """
        log_func.error(u'The method of obtaining the object attached to the anchor control is not defined')
        return None

    def layoutControl(self, ctrl=None):
        """
        Set the position and size of control in accordance with this anchor.

        :param ctrl: Control object.
        :return: True/False.
        """
        try:
            return self._layoutControl(ctrl=ctrl)
        except:
            log_func.fatal(u'Error setting the size and position of the control in accordance with the anchor <%s>' % self.getName())
        return False

    def _layoutControl(self, ctrl=None):
        """
        Set the position and size of control in accordance with this anchor.

        :param ctrl: Control object.
        :return: True/False.
        """
        if ctrl is None:
            ctrl = self.getAttachment()

        if ctrl:
            try:
                # Calculation of the coordinates of the anchor area
                pix_left, pix_top, pix_right, pix_bottom = self.calcRectangleArea()

                # Set control position
                ctrl.SetPosition((pix_left, pix_top))

                svg_width, svg_height = self._size
                ctrl_size = ctrl.GetSize()

                # Set control size
                width = pix_right - pix_left if svg_width > 0 else ctrl_size.GetWidth()
                height = pix_bottom - pix_top if svg_height > 0 else ctrl_size.GetHeight()
                width = width if width > 0 else -1
                height = height if height > 0 else -1
                if width >= 0 and height >= 0:
                    ctrl.SetSize((width, height))

                return True
            except:
                log_func.fatal(u'Error setting the size and position of the control in accordance with the anchor <%s>' % self.getName())
        else:
            log_func.error(u'An anchor control is not defined <%s>' % self.getName())
        return False

    def calcPixPosition(self, svg_position=None):
        """
        Calculation of the position of the control point in pixels.

        :param svg_position: Anchor reference position in SVG units.
        :return: The calculated position of the reference point in pixels or (0, 0) in case of an error.
        """
        if svg_position is None:
            svg_position = self._position

        if self._mnemoscheme is None:
            log_func.error(u'Not defined mimic for anchor <%s>' % self.getName())
            return 0, 0

        # Determine the size of the mimic diagram required for calculation
        svg_width, svg_height = self._mnemoscheme.getSVGSize()
        pix_width, pix_height = self._mnemoscheme.GetSize()

        # We calculate the scaling factor for the width and height separately
        zoom_coef_width = float(svg_width) / float(pix_width)
        zoom_coef_height = float(svg_height) / float(pix_height)

        # Determine the scaling factor
        zoom_coef = max(zoom_coef_width, zoom_coef_height)

        # Сalculation
        svg_pos_x, svg_pos_y = svg_position
        if zoom_coef:
            pix_offset_x = round((float(pix_width) - float(svg_width) / zoom_coef) / 2.0)
            pix_offset_y = round((float(pix_height) - float(svg_height) / zoom_coef) / 2.0)
            pix_x = round((float(svg_pos_x) - CORRECT_SVG_OFFSET_X) / zoom_coef) + pix_offset_x
            pix_y = round((float(svg_pos_y) - CORRECT_SVG_OFFSET_Y) / zoom_coef) + pix_offset_y

            return pix_x, pix_y
        else:
            log_func.error(u'Estimated zero scale factor for mnemoscheme <%s>:' % self._mnemoscheme.getName())
            log_func.error(u'\tCheck attributes svg_width and svg_height of mnemoscheme <%s>' % self._mnemoscheme.getName())
            log_func.error(u'\tIt must not be zero!')
        return 0, 0

    def calcRectangleArea(self, svg_position=None, svg_size=None,
                          direction=spc.ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | spc.ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                          min_size=None, max_size=None):
        """
        Calculation of the coordinates of the anchor area.

        :param svg_position: Anchor reference position in SVG units.
        :param svg_size: Anchor cell size in SVG units.
        :param direction: Indication of the direction of the anchor displacement relative to the anchor point.
        :param min_size: Specify a minimum pixel size limit.
        :param max_size: Specifying a maximum size limit in pixels.
        :return: The calculated coordinates of the rectangular area in pixels or
            (0, 0, 0, 0) if error.
        """
        if svg_position is None:
            svg_position = self._position
        if svg_size is None:
            svg_size = self._size
        if min_size is None:
            min_size = self._min_size
        if max_size is None:
            max_size = self._max_size

        # Reference point calculation
        pix_position = self.calcPixPosition(svg_position)

        # Put the offset position at the same point
        svg_pos_x, svg_pos_y = svg_position
        svg_width, svg_height = svg_size
        svg_offset_x, svg_offset_y = svg_pos_x, svg_pos_y

        # Calculation of the second point taking into account the direction of displacement
        if direction & spc.ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT:
            svg_offset_x = svg_pos_x + svg_width
        if direction & spc.ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT:
            svg_offset_x = svg_pos_x - svg_width
        if direction & spc.ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM:
            svg_offset_y = svg_pos_y + svg_height
        if direction & spc.ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP:
            svg_offset_y = svg_pos_y - svg_height
        pix_offset_position = self.calcPixPosition(svg_position=(svg_offset_x, svg_offset_y))

        # Get the coordinates of the area
        pix_left = min(pix_position[0], pix_offset_position[0])
        pix_top = min(pix_position[1], pix_offset_position[1])
        pix_right = max(pix_position[0], pix_offset_position[0])
        pix_bottom = max(pix_position[1], pix_offset_position[1])

        # We produce size restrictions
        if min_size:
            if min_size[0] > 0:
                pix_right = max(pix_right, pix_left + min_size[0])
            if min_size[1] > 0:
                pix_bottom = max(pix_bottom, pix_top + min_size[1])
        if max_size:
            if max_size[0] > 0:
                pix_right = min(pix_right, pix_left + max_size[0])
            if max_size[1] > 0:
                pix_bottom = min(pix_bottom, pix_top + max_size[1])

        return pix_left, pix_top, pix_right, pix_bottom
