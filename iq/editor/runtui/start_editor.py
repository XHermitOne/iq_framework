#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Start editor dialog.
"""

from ...util import log_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

from . import start_editor_app

__version__ = (0, 0, 0, 1)


class iqStartEditorApp(start_editor_app.StartEditorApp):
    """
    RunTUI. Start editor application class.
    """
    def onDebugButtonClick(self):
        """
        Debug button click handler.
        """
        pass

    def onExitButtonClick(self):
        """
        Exit button click handler.
        """
        self.quit()

    def onExternalToolsButtonClick(self):
        """
        <External tools> button click handler.
        """
        pass

    def onHelpButtonClick(self):
        """
        Help button click handler.
        """
        pass

    def onNewButtonClick(self):
        """
        <New project> button click handler.
        """
        pass

    def onRunButtonClick(self):
        """
        <Run project> button click handler.
        """
        pass


def startEditor():
    """
    RunTUI. Start editor.

    :return: True/False.
    """
    try:
        log_func.info(u'RunTUI version: %s' % runtui.__version__)
        app = iqStartEditorApp()
        app.run()
        return True
    except:
        log_func.fatal(u'Error start editor RunTUI')
    return False


if __name__ == '__main__':
    startEditor()
