#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Login user dialog.
"""

from ....util import log_func
from ....util import lang_func
from ....util import global_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

from ... import stored_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

USER_ITEM_DELIMETER = '\t:\t'

LOGIN_USER_IDX = 0
LOGIN_PASSWORD_IDX = 1
LOGIN_PASSWORD_MD5_IDX = 2


class iqLoginDialog(runtui.Dialog, stored_manager.iqStoredManager):
    """
    Login user dialog.
    """
    def __init__(self, title='', default_username=None, reg_users=None, user_descriptions=None,
                 width: int = 60, height: int = 10):
        """
        Constructor.

        :param title: Dialog form title.
        :param default_username: Default user name.
        :param user_descriptions: User description list.
        :param reg_users: User name list.
        :param width: Width dialog.
        :param height: Width dialog.
        """
        super().__init__(title=title, width=width, height=height)

        try:
            login_data = self.loadCustomData()

            if reg_users is None:
                reg_users = list()
            if not default_username:
                last_login_username = login_data.get('last_login_username', '') if login_data else ''
                default_username = last_login_username

            user_choices = reg_users
            if user_descriptions:
                user_choices = [u'%s%s%s' % (username,
                                             USER_ITEM_DELIMETER,
                                             user_descriptions[i]) for i, username in enumerate(reg_users)]
            selected = 0
            if user_choices:
                selected = reg_users.index(default_username) if default_username and default_username in reg_users else 0

            # Widgets
            self.username_label = runtui.Label(text=_('User'), x = 1, y = 1, width=10)
            self.username_list = runtui.DropDownList(items=user_choices,
                                                     selected_index=selected,
                                                     x = 12, y = 1,
                                                     width = width - 12)
            self.password_label = runtui.Label(text=_('Password'), x = 1, y = 3, width = 10)
            self.password_input = runtui.PasswordInput(x = 12, y=3, width = width - 12)

            self.add_child(self.username_label)
            self.add_child(self.username_list)
            self.add_child(self.password_label)
            self.add_child(self.password_input)

            self.cancel_button = runtui.Button(text=_('Cancel'), x = 1, y = 5, width = 10)
            self.ok_button = runtui.Button(text=_('OK'), x = 11, y = 5, width = 10)

            self.add_child(self.cancel_button)
            self.add_child(self.ok_button)
        except:
            log_func.fatal(u'Error init login dialog')


def getLoginDlg(title='', default_username=None, reg_users=None, user_descriptions=None, *args, **kwargs):
    """
    Open login user dialog.

    :param title: Dialog form title.
    :param default_username: Default user name.
    :param reg_users: User name list.
    :param user_descriptions: User description list.
    :return: Tuple: (username, password, password hash) or None if error.
    """
    app = global_func.getApplication()
    if app is None:
        app = global_func.createApplication()

    try:
        dlg = iqLoginDialog(title=_('LOGIN'))
        dlg.center_on_screen(app._screen.width if app._screen else 80,
                             app._screen.height if app._screen else 24)
        app.root.add_child(dlg)
    except:
        log_func.fatal(u'Open login dialog error')
