#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Single choice dialog.
"""

from ....util import log_func
from ....util import lang_func
from ....util import global_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

__version__ = (0, 1, 1, 1)

_ = lang_func.getTranslation().gettext


class iqSingleChoiceDialog(runtui.Dialog):
    """
    Single choice dialog.
    """
    def __init__(self, title='', prompt_text='', choices=(), default_idx=-1,
                 width: int = 60, height: int = 10):
        """
        Constructor.

        :param title: Dialog form title.
        :param prompt_text: Dialog prompt text.
        :param choices: List of selection lines.
        :param default_idx: Default selected line index.
        :param width: Width dialog.
        :param height: Width dialog.
        """
        super().__init__(title=title, width=width, height=height)

        self._result_choice_idx = -1
        try:
            # Widgets
            self.prompt_label = runtui.Label(text=_(prompt_text), x = 1, y = 1, width = width - 2)
            self.item_listbox = runtui.ListBox(items=choices, x = 1, y=3, width = width - 2, height=4)
            if default_idx >= 0:
                self.item_listbox.selected_index = default_idx

            self.add_child(self.prompt_label)
            self.add_child(self.item_listbox)

            self.cancel_button = runtui.Button(text=_('Cancel'), x = 1, y = 5, width = 10, on_click=self.onCancelButtonClick)
            self.ok_button = runtui.Button(text=_('OK'), x = 11, y = 5, width = 10, on_click=self.onOkButtonClick)

            self.add_child(self.cancel_button)
            self.add_child(self.ok_button)
        except:
            log_func.fatal(u'Error init single choice dialog')

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

        painter.put_str(lx + self.prompt_label.x, ly + self.prompt_label.y, self.prompt_label.text, fg=fg, bg=bg, max_width=content_w)

        self.item_listbox._screen_rect = runtui.Rect(sr.x + self.item_listbox.x, sr.y + self.item_listbox.y, sr.width - 2, 4)
        self.item_listbox.paint(painter)

        btn_y = sr.y + sr.height - 2
        self.cancel_button._screen_rect = runtui.Rect(sr.x + sr.width - 24, btn_y, self.cancel_button.width, self.cancel_button.height)
        self.cancel_button.paint(painter)
        self.ok_button._screen_rect = runtui.Rect(sr.x + sr.width - 13, btn_y, self.ok_button.width, self.ok_button.height)
        self.ok_button.paint(painter)

    def onCancelButtonClick(self):
        """
        Cancel button click handler.
        """
        self._result_choice_idx = -1
        app = global_func.getApplication()
        app.end_modal(self)

    def onOkButtonClick(self):
        """
        Cancel button click handler.
        """
        self._result_choice_idx = self.item_listbox.selected_index
        app = global_func.getApplication()
        app.end_modal(self)


def getSingleChoiceDlg(title='', prompt_text='',
                       choices=(), default_idx=-1, *args, **kwargs):
    """
    List selection dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines.
    :param default_idx: Default selected line index.
    :return: Selected text or None if pressed cancel.
    """
    app = global_func.getApplication()
    if app is None:
        app = global_func.createApplication()

    try:
        dlg = iqSingleChoiceDialog(title=title, prompt_text=prompt_text, choices=choices, default_idx=default_idx)
        dlg.center_on_screen(app._screen.width if app._screen else 80,
                             app._screen.height if app._screen else 24)
        app.show_modal(dlg)

        result = dlg.item_listbox.items[dlg._result_choice_idx] if dlg._result_choice_idx >= 0 else None
        return result
    except:
        log_func.fatal(u'Open single choice dialog error')
    return None


def getSingleChoiceIdxDlg(title='', prompt_text='', choices=[],
                          default_idx=-1, *args, **kwargs):
    """
    Select index dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines.
    :param default_idx: Default selected line index.
    :return: Selected line index or -1 if pressed cancel.
    """
    app = global_func.getApplication()
    if app is None:
        app = global_func.createApplication()

    try:
        dlg = iqSingleChoiceDialog(title=title, prompt_text=prompt_text, choices=choices, default_idx=default_idx)
        dlg.center_on_screen(app._screen.width if app._screen else 80,
                             app._screen.height if app._screen else 24)
        app.show_modal(dlg)

        result = dlg._result_choice_idx
        return result
    except:
        log_func.fatal(u'Open single choice dialog error')
    return None
