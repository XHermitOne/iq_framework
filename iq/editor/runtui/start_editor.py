#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Start editor dialog.
"""

from ...util import log_func
from ... import global_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

from . import start_editor_app

from ...dialog import dlg_func

from ...project import prj
from ...project import prj_func

__version__ = (0, 0, 0, 1)


class iqStartEditorApp(start_editor_app.StartEditorApp):
    """
    RunTUI. Start editor application class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_editor_app.StartEditorApp.__init__(self, *args, **kwargs)

        self._project_manager = prj.iqProjectManager()

    def on_ready(self):
        """
        Init form
        """
        start_editor_app.StartEditorApp.on_ready(self)

        self.debug_project_button.enabled = False
        self.external_tools_button.enabled = False
        self.help_button.enabled = False

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
        self._project_manager.create()

    def onRunButtonClick(self):
        """
        <Run project> button click handler.
        """
        prj_descriptions = prj_func.getProjectDescriptions()

        prj_data = list(prj_descriptions.items())
        prj_data.sort()
        prj_names = [name for name, description in prj_data]
        prj_items = [u'%s\t:\t%s' % (name, description) for name, description in prj_data]
        selected_prj_idx = dlg_func.getSingleChoiceIdxDlg(parent=self, title='PROJECTS',
                                                          prompt_text=u'Select a project to run:',
                                                          choices=prj_items)
        if selected_prj_idx >= 0:
            selected_prj_name = prj_names[selected_prj_idx]
            self._project_manager.run(selected_prj_name)


def startEditor():
    """
    RunTUI. Start editor.

    :return: True/False.
    """
    try:
        log_func.info(u'RunTUI version: %s' % runtui.__version__)
        app = iqStartEditorApp()
        global_func.setApplication(app)
        app.run()
        return True
    except:
        log_func.fatal(u'Error start editor RunTUI')
    return False


if __name__ == '__main__':
    startEditor()
