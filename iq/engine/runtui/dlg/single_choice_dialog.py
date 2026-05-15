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

__version__ = (0, 0, 0, 1)

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
        try:
            # Widgets
            self.prompt_label = runtui.Label(text=_(prompt_text), x = 1, y = 1, width = width - 2)
            self.item_listbox = runtui.ListBox(items=choices, x = 1, y=3, width = width - 2)
            if default_idx >= 0:
                self.item_listbox.selected_index = default_idx

            self.add_child(self.prompt_label)
            self.add_child(self.item_listbox)

            self.cancel_button = runtui.Button(text=_('Cancel'), x = 1, y = 5, width = 10)
            self.ok_button = runtui.Button(text=_('OK'), x = 11, y = 5, width = 10)

            self.add_child(self.cancel_button)
            self.add_child(self.ok_button)
        except:
            log_func.fatal(u'Error init single choice dialog')


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
        app.root.add_child(dlg)
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
        app.root.add_child(dlg)
    except:
        log_func.fatal(u'Open single choice dialog error')
    return None
