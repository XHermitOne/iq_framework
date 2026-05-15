#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Text entry dialog.
"""

from ....util import log_func
from ....util import lang_func
from ....util import global_func

try:
    import runtui
    import runtui.rendering.painter
    import runtui.core.types
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqTextEntryDialog(runtui.Dialog):
    """
    Text entry dialog.
    """
    def __init__(self, title='', prompt_text='', default_text='',
                 width: int = 60, height: int = 6):
        """
        Constructor.

        :param title: Dialog form title.
        :param prompt_text: Dialog prompt text.
        :param default_text: Default value.
        :param width: Width dialog.
        :param height: Width dialog.
        """
        super().__init__(title=title, width=width, height=height)

        self._prompt_text = prompt_text
        try:
            # Widgets
            self.prompt_label = runtui.Label(text=_(self._prompt_text), x = 1, y = 1, width = width - 4)
            self.text_input = runtui.TextInput(x = 1, y=2, width = width - 4)

            self.add_child(self.prompt_label)
            self.add_child(self.text_input)

            self.cancel_button = runtui.Button(text=_('Cancel'), x = 1, y = 5, width = 10)
            self.ok_button = runtui.Button(text=_('OK'), x = 11, y = 5, width = 10)

            self.add_child(self.cancel_button)
            self.add_child(self.ok_button)
        except:
            log_func.fatal(u'Error init text entry dialog')

    def paint(self, painter: runtui.rendering.painter.Painter):
        """
        Paint function.
        """
        super().paint(painter)

        sr = self._screen_rect
        lx = sr.x - painter._offset.x
        ly = sr.y - painter._offset.y
        content_w = sr.width - 4

        bg = self.theme_color('dialog.bg', runtui.core.types.Color.BRIGHT_BLACK)
        fg = self.theme_color('dialog.fg', runtui.core.types.Color.BLACK)

        painter.put_str(lx + self.prompt_label.x, ly + self.prompt_label.y, self._prompt_text, fg=fg, bg=bg, max_width=content_w)

        self.text_input._screen_rect = runtui.Rect(sr.x + self.text_input.x, sr.y + self.text_input.y, sr.width - 2, 1)
        self.text_input.paint(painter)

        btn_y = sr.y + sr.height - 2
        self.cancel_button._screen_rect = runtui.Rect(sr.x + sr.width - 24, btn_y, self.ok_button.width, self.ok_button.height)
        self.cancel_button.paint(painter)
        self.ok_button._screen_rect = runtui.Rect(sr.x + sr.width - 13, btn_y, self.ok_button.width, self.ok_button.height)
        self.ok_button.paint(painter)


def getTextEntryDlg(title='', prompt_text='', default_value='', *args, **kwargs):
    """
    Line input dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog prompt text.
    :param default_value: Default value.
    :return: Input text value or None if pressed cancel.
    """
    app = global_func.getApplication()
    if app is None:
        app = global_func.createApplication()

    try:
        dlg = iqTextEntryDialog(title=title, prompt_text=prompt_text, default_text=default_value)
        dlg.center_on_screen(app._screen.width if app._screen else 80,
                             app._screen.height if app._screen else 24)

        app.root.add_child(dlg)
        dlg.invalidate()
    except:
        log_func.fatal(u'Open login dialog error')
    return None


