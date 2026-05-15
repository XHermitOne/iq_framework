#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Start folder dialog.
"""

import os.path

from ...util import log_func
from ...util import res_func
from ...util import global_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

from . import start_folder_app
from . import start_designer

from ...project import prj

__version__ = (0, 0, 0, 1)


class iqStartFolderApp(start_folder_app.StartFolderApp):
    """
    RunTUI. Start folder application class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_folder_app.StartFolderApp.__init__(self, *args, **kwargs)
        # Current folder path
        self.folder_path = None

    def on_ready(self):
        """
        Init form
        """
        start_folder_app.StartFolderApp.on_ready(self)

        if self.folder_path:
            folder_basename = os.path.basename(self.folder_path)
            prj_basename = folder_basename + res_func.RESOURCE_FILE_EXT
            prj_filename = os.path.join(self.folder_path, prj_basename)
            self.run_prj_button.enabled = os.path.exists(prj_filename)

    def onExitButtonClick(self):
        """
        Exit button click handler.
        """
        self.quit()

    def onNewFormButtonClick(self):
        """
        <New form ...> button click handler.
        """
        self.quit()
        start_designer.startRunTUIRadDesigner()

    def onRunProjectButtonClick(self):
        """
        <Run project> button click handler.
        """
        self.quit()
        project_manager = prj.iqProjectManager()
        selected_prj_name = os.path.basename(self.folder_path) if self.folder_path else None
        project_manager.run(selected_prj_name)


def startFolder(folder_path=None):
    """
    RunTUI. Start folder.

    :return: True/False.
    """
    try:
        log_func.info(u'RunTUI version: %s' % runtui.__version__)
        app = iqStartFolderApp()
        app.folder_path = folder_path
        global_func.setApplication(app)
        app.run()
        return True
    except:
        log_func.fatal(u'Error start folder RunTUI')
    return False


if __name__ == '__main__':
    startFolder()
