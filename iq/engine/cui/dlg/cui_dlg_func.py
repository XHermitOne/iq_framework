#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUI dialog functions module.
"""

from ....util import log_func
from ....util import lang_func

from . import cui_dlg

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

LOGIN_USER_IDX = 0
LOGIN_PASSWORD_IDX = 1
LOGIN_PASSWORD_MD5_IDX = 2


def getLoginDlg(parent=None, title='', default_username='', reg_users=None,
                user_descriptions=()):
    """
    Open login user dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_username: Default user name.
    :param reg_users: User name list.
    :param user_descriptions: User description list.
    :return: Tuple: (username, password, password hash) or None if error.
    """
    try:
        username_dlg = cui_dlg.iqCUIUsernameDialog(title=title,
                                                   body=_(u'User name:'),
                                                   background_title=_(u'LOGIN'),
                                                   default_username=default_username,
                                                   reg_users=reg_users,
                                                   user_descriptions=user_descriptions)
        username = username_dlg.getUsername() if username_dlg.main() else None
        if username:
            password_dlg = cui_dlg.iqCUIPasswordDialog(title=title,
                                                       body=_(u'Password:'),
                                                       background_title=_(u'LOGIN'))
            password = password_dlg.getPassword() if password_dlg.main() else None

            # log_func.info(u'Login <%s : %s>' % (username, password))
            if username and password is not None:
                return username, password, password_dlg.getPasswordHash()
    except:
        log_func.fatal(u'Error login dialog')
    return None


