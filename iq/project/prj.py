#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project manager module.
"""

import os
import os.path

from ..util import file_func
from ..util import log_func
from ..dialog import dlg_func
from ..util import py_func
from ..util import spc_func
from ..util import res_func
from ..util import exec_func
from ..util import global_func
from ..util import lang_func
from ..util import txtfile_func
from ..util import ini_func

from ..passport import passport
from .. import user
from .. import role
from .. import global_data

from . import spc

__version__ = (0, 0, 3, 2)

_ = lang_func.getTranslation().gettext

RUN_SH_FMT = '''#!/bin/sh

cd %s
python3 ./framework.py --debug --os --mode=runtime --engine=%s --prj=%s
'''


class iqProjectManager(object):
    """
    Project manager class.
    """
    def __init__(self, name=None):
        """
        Constructor.

        :param name: Project name.
        """
        self.name = name

    def setName(self, name):
        """
        Set name of actual project.

        :param name: Project name.
        :return:
        """
        self.name = name

    def create(self, name=None, parent=None):
        """
        Create new project.

        :param name: New project name.
            If None then open dialog for input.
        :param parent: Parent from.
        :return: True/False.
        """
        if name is None:
            name = dlg_func.getTextEntryDlg(parent=parent,
                                            title=_(u'PROJECT NAME'),
                                            prompt_text=_(u'Enter the name of the project:'), default_value='new_name')
        if name:
            prj_path = self.getPath(name)
            self.createPath(prj_path)
            self.createDefaultResources(parent=parent, prj_path=prj_path,
                                        prj_name=name)

            self.setName(name)
            return True
        return False

    def createDefaultResources(self, parent=None, prj_path=None, prj_name=None, rewrite=False):
        """
        Create default project resources (menubars, forms and etc).

        :param parent: Parent from.
        :param prj_path: Project path.
        :param prj_name: Project name.
        :param rewrite: Rewrite resource file if it exists?
        :return: True/False.
        """
        if not prj_path:
            log_func.warning(u'Not define project path for save default project path')
            return False

        if not os.path.exists(prj_path):
            if not self.createPath(prj_path):
                return False

        if not prj_name:
            prj_name = os.path.splitext(os.path.basename(prj_path))[0]

        choices = tuple([u'%s project' % engine_type for engine_type in global_data.ENGINE_TYPES])
        select_engine_idx = dlg_func.getSingleChoiceIdxDlg(parent=parent,
                                                           title=_(u'ENGINE TYPE'),
                                                           prompt_text=_(u'Select engine type of the project:'),
                                                           choices=choices,
                                                           default_idx=0)
        if 0 <= select_engine_idx < len(global_data.ENGINE_TYPES):
            selected_engine = global_data.ENGINE_TYPES[select_engine_idx]
            save_ok = self.saveDefaultPrjResource(prj_path=prj_path, prj_name=prj_name, default_engine=selected_engine)
            return all([save_ok,
                        self.createDefaultMenubarResource(engine=selected_engine, prj_name=prj_name),
                        self.createDefaultMainFormResource(engine=selected_engine, prj_name=prj_name),
                        self.createDefaultReportsFolder(engine=selected_engine, prj_name=prj_name),
                        self.createDefaultSettingsINI(prj_path=prj_path, prj_name=prj_name)])

        return False

    def createDefaultMenubarResource(self, engine=global_data.WX_ENGINE_TYPE,
                                     prj_name=u'default'):
        """
        Create default menubar resources.

        :param engine: Engine type.
        :param prj_name: Project name.
        :return: True/False.
        """
        if engine == global_data.WX_ENGINE_TYPE:
            menubar_res_filename = os.path.join(file_func.getFrameworkPath(),
                                                prj_name,
                                                'menubars',
                                                'main_menubar_proto.fbp')
            menubar_py_filename = file_func.setFilenameExt(menubar_res_filename, '.py')

            from ..editor.wx.code_generator import menubar_generator
            from ..editor.wx.code_generator import gui_generator
            from ..editor.wx import wxfb_manager

            return all([menubar_generator.genDefaultMenubarFormBuilderPrj(prj_filename=menubar_res_filename),
                        wxfb_manager.adaptWXWFormBuilderPy(menubar_py_filename),
                        gui_generator.gen(src_filename=menubar_py_filename)])

        return False

    def createDefaultMainFormResource(self, engine=global_data.WX_ENGINE_TYPE,
                                      prj_name=u'default'):
        """
        Create default main form resources.

        :param engine: Engine type.
        :param prj_name: Project name.
        :return: True/False.
        """
        if engine == global_data.WX_ENGINE_TYPE:
            mainform_res_filename = os.path.join(file_func.getFrameworkPath(),
                                                 prj_name,
                                                 'main_forms',
                                                 'main_form_proto.fbp')
            mainform_py_filename = file_func.setFilenameExt(mainform_res_filename, '.py')

            from ..editor.wx.code_generator import mainform_generator
            from ..editor.wx.code_generator import gui_generator
            from ..editor.wx import wxfb_manager

            return all([mainform_generator.genDefaultMainFormFormBuilderPrj(prj_filename=mainform_res_filename),
                        wxfb_manager.adaptWXWFormBuilderPy(mainform_py_filename),
                        gui_generator.genMainForm(src_filename=mainform_py_filename)])

        elif engine == global_data.GTK_ENGINE_TYPE:
            mainform_res_filename = os.path.join(file_func.getFrameworkPath(),
                                                 prj_name,
                                                 'main_forms',
                                                 'main_appwin.glade')
            mainform_py_filename = file_func.setFilenameExt(mainform_res_filename, '.py')

            from ..editor.gtk.code_generator import main_appwin_generator
            from ..editor.gtk.code_generator import gui_generator

            return all([main_appwin_generator.genDefaultMainAppWindowGlade(prj_filename=mainform_res_filename),
                        gui_generator.genMainForm(src_filename=mainform_py_filename)])
        else:
            log_func.warning(u'Create main form resource not supported for <%s> engine' % engine)

        return False

    def createDefaultReportsFolder(self, engine=global_data.WX_ENGINE_TYPE,
                                   prj_name=u'default'):
        """
        Create default reports folder.

        :param engine: Engine type.
        :param prj_name: Project name.
        :return: True/False.
        """
        reports_folder = os.path.join(file_func.getFrameworkPath(),
                                      prj_name,
                                      'reports')
        description_filename = os.path.join(reports_folder, 'descript.ion')

        return all([file_func.createDir(reports_folder),
                    py_func.createInitModule(reports_folder),
                    txtfile_func.saveTextFile(txt_filename=description_filename,
                                              txt=u'%s <%s>' % (_('Reports folder'), prj_name))])

    def createDefaultSettingsINI(self, prj_path=None, prj_name=None):
        """
        Create default project settings INI file.

        :param prj_path: Project path.
        :param prj_name: Project name.
        :return: True/False.
        """
        if not prj_path:
            log_func.warning(u'Not define project path for save default project settings ini file')
            return False

        if not os.path.exists(prj_path):
            log_func.warning(u'Project path <%s> not found for save default project settings ini file')
            return False

        if not prj_name:
            prj_name = os.path.splitext(os.path.basename(prj_path))[0]

        ini_filename = os.path.join(prj_path, prj_name + ini_func.INI_FILE_EXT)
        # Save empty settings INI file if not exists
        return txtfile_func.saveTextFile(ini_filename, rewrite=False)

    def saveDefaultPrjResource(self, prj_path=None, prj_name=None, rewrite=False,
                               default_engine=global_data.WX_ENGINE_TYPE):
        """
        Save default project resource.

        :param prj_path: Project path.
        :param prj_name: Project name.
        :param rewrite: Rewrite resource file if it exists?
        :param default_engine: Default engine type.
        :return: True/False.
        """
        if not prj_path:
            log_func.warning(u'Not define project path for save default project path')
            return False

        if not os.path.exists(prj_path):
            if not self.createPath(prj_path):
                return False

        if not prj_name:
            prj_name = os.path.splitext(os.path.basename(prj_path))[0]

        try:
            prj_res_filename = os.path.join(prj_path, prj_name + res_func.RESOURCE_FILE_EXT)

            prj_resource = spc_func.clearResourceFromSpc(spc.SPC)
            prj_resource['name'] = prj_name
            prj_resource['description'] = u'Application project'

            prj_resource[spc_func.CHILDREN_ATTR_NAME] = list()
            for item in (dict(name='admin', description=u'Administrator', role=role.ADMINISTRATORS_ROLE_NAME),
                         dict(name='user', description=u'User', role=role.USERS_ROLE_NAME)):
                user_resource = spc_func.clearResourceFromSpc(user.SPC)
                user_resource['name'] = item['name']
                user_resource['description'] = item['description']
                user_resource['roles'] = [item['role']]
                if default_engine:
                    user_resource['engine'] = default_engine
                user_resource['do_main'] = '''from %s.main_forms import main_form\nreturn main_form.runMainForm()''' % prj_name

                role_resource = spc_func.clearResourceFromSpc(role.SPC)
                role_resource['name'] = item['role']
                role_resource['description'] = u'%ss' % item['description']

                prj_resource[spc_func.CHILDREN_ATTR_NAME].append(role_resource)
                prj_resource[spc_func.CHILDREN_ATTR_NAME].append(user_resource)

            return res_func.saveResourceText(prj_res_filename, prj_resource, rewrite=rewrite)
        except:
            log_func.fatal(u'Error save default project resource')
        return False

    def createPath(self, prj_path):
        """
        Create project directory.

        :param prj_path: Project directory path.
        :return: True/False.
        """
        if prj_path and os.path.exists(prj_path):
            log_func.warning(u'Project path <%s> exists' % prj_path)
            return py_func.createInitModule(prj_path)
        elif not prj_path:
            log_func.warning(u'Project path <%s> not defined' % prj_path)
        elif prj_path and not os.path.exists(prj_path):
            log_func.info(u'Create project package path <%s>' % prj_path)
            return py_func.createPackage(prj_path)
        return False

    def getPath(self, name=None):
        """
        Get project path by project name.

        :param name: Project name.
        :return: Full path to project or None if error.
        """
        if name is None:
            name = self.name

        framework_path = file_func.getFrameworkPath()
        if framework_path:
            if name:
                return os.path.join(framework_path, name)
            else:
                log_func.warning(u'Not define project name')
        return None

    def run(self, name=None):
        """
        Run project.

        :param name: Project name. If None run actual.
        :return: True/False.
        """
        if name:
            self.setName(name)

        cmd = RUN_SH_FMT % (file_func.getFrameworkPath(), global_func.getEngineType(), name)
        return exec_func.runTask(cmd, run_filename=name, rewrite=True)

    def debug(self, name=None):
        """
        Debug project.

        :param name: Project name. If None debug actual.
        :return: True/False.
        """
        if name:
            self.setName(name)

        pass

    def start(self, username=None, password=None):
        """
        Start project.

        :param username: User name.
        :param password: User password.
        :return: True/False.
        """
        result = False
        if username is None:
            if global_func.isWXEngine():
                result = dlg_func.getLoginDlg(title=_(u'LOGIN'),
                                              reg_users=self.getUserNames(),
                                              user_descriptions=[user.getDescription() for user in self.getUsers()])
            elif global_func.isCUIEngine():
                from ..engine.cui.dlg import cui_dlg_func
                result = cui_dlg_func.getLoginDlg(title=_(u'LOGIN'),
                                                  reg_users=self.getUserNames(),
                                                  user_descriptions=[user.getDescription() for user in self.getUsers()])
            elif global_func.isGTKEngine():
                result = dlg_func.getLoginDlg(title=_(u'LOGIN'),
                                              reg_users=self.getUserNames(),
                                              user_descriptions=[user.getDescription() for user in self.getUsers()])
            else:
                log_func.warning(u'Not supported %s engine login' % global_func.getEngineType())

            if not result:
                # If login failed then exit
                log_func.warning(u'Failed login')
                return result
            else:
                # After login change engine
                # Clear import dialog functions
                dlg_func._clearImportDialogFunctions()

                username, password, password_hash = result

        user_psp = passport.iqPassport(prj=self.name, module=self.name,
                                       typename=user.COMPONENT_TYPE, name=username)
        log_func.debug(u'User passport <%s>' % user_psp.getAsStr())
        user_obj = self.getKernel().createObject(psp=user_psp, parent=self, register=True)

        global_data.setGlobal('USER', user_obj)

        result = user_obj.login(password)
        if not result:
            # If login failed then exit
            log_func.warning(u'Failed login user <%s>' % user_obj.getName())
            return result

        global_data.setGlobal('USER', user_obj if result else None)
        if result:
            user_obj.initEngineType()
            user_obj.run()
        return result

    def stop(self):
        """
        Stop programm.

        :return: True/False
        """
        user_obj = global_data.getGlobal('USER')
        if user_obj:
            return user_obj.logout()
        return False

    def getUserNames(self):
        """
        Get project user names.

        :return: User name list.
        """
        return ('admin', )
