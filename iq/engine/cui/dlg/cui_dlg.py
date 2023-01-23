#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CUI dialog class module.
"""

import hashlib

from ....util import log_func
from ....util import lang_func

try:
    import dialog
except ImportError:
    log_func.warning(u'Import error pythondialog')
    log_func.warning(u'For install: sudo apt install python3-dialog')
    dialog = None

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_DLG_HEIGHT = 30
DEFAULT_DLG_WIDTH = 100

BUTTONS_ALIGN_LEFT = 'left'
BUTTONS_ALIGN_CENTER = 'center'
BUTTONS_ALIGN_RIGHT = 'right'

DEFAULT_LIST_HEIGHT = DEFAULT_DLG_HEIGHT - 10

LIST_ITEM_HIDDEN = 0x1
LIST_ITEM_READ_ONLY = 0x2


class iqCUIDialogProto(object):
    """
    CUI dialog prototype.
    """
    def __init__(self, title='',
                 height=DEFAULT_DLG_HEIGHT,
                 width=DEFAULT_DLG_WIDTH, body=None):
        """
        Constructor.

        :param title: Dialog title.
        :param height: Dialog height.
        :param width: Dialog width.
        :param body: Dialog body.
        """
        self.title = title
        self.width = width
        self.height = height
        self.body = body

    def addButtons(self, buttons, align=BUTTONS_ALIGN_RIGHT):
        """
        Add buttons to dialog.

        :param buttons: Button list:
            [('Label', Button code), ...]
        :param align: Button list alignment.
        """
        pass

    def main(self):
        pass

    def onExit(self, exitcode):
        return exitcode

    def getCheckList(self):
        """
        Get check items.
        """
        return list()


class iqCUIPyDlgDialog(iqCUIDialogProto, dialog.Dialog):
    """
    CUI dialog class.
    """
    def __init__(self, title='', height=DEFAULT_DLG_HEIGHT,
                 width=DEFAULT_DLG_WIDTH, body='',
                 background_title='',
                 *args, **kwargs):
        """
        Constructor.

        :param title:
        :param height:
        :param width:
        :param body:
        :param background_title:
        :param args:
        :param kwargs:
        """
        iqCUIDialogProto.__init__(self, title=title, height=height, width=width, body=body)
        dialog.Dialog.__init__(self, *args, **kwargs)
        self.set_background_title(background_title)


class iqCUIPyDlgYesNoDialog(iqCUIPyDlgDialog):

    def main(self):
        result = self.yesno(self.body, width=self.width, height=self.height, title=self.title)
        return result == self.OK


class iqCUIPyDlgMsgBoxDialog(iqCUIPyDlgDialog):

    def main(self):
        result = self.msgbox(self.body, width=self.width, height=self.height, title=self.title)
        return result == self.OK


class iqCUIPyDlgInputBoxDialog(iqCUIPyDlgDialog):

    def main(self):
        return self.inputbox(self.title, width=self.width, height=self.height)


class iqCUIPyDlgTextBoxDialog(iqCUIPyDlgDialog):

    def main(self):
        return self.editbox(self.body, width=self.width, height=self.height)


class iqCUIPyDlgCheckListDialog(iqCUIPyDlgDialog):

    def __init__(self, title='', height=DEFAULT_DLG_HEIGHT, width=DEFAULT_DLG_WIDTH,
                 list_height=DEFAULT_LIST_HEIGHT, body='',
                 background_title='', *args, **kwargs):
        iqCUIPyDlgDialog.__init__(self, title=title, height=height, width=width, body=body,
                                  background_title=background_title, *args, **kwargs)

        self.list_height = list_height
        self.result = None

    def main(self):
        if self.body:
            self.result = self.checklist(text=self.title, width=self.width, height=self.height,
                                         list_height=self.list_height, choices=self.body)
        else:
            self.result = (self.msgbox(_(u'Check list is empty'),
                                       width=self.width, height=self.height, title=self.title), None)
        return self.result[0] == self.OK, self.result[1:]

    def getCheckList(self):
        body = [line[0] for line in self.body]
        result = [name in self.result[1] for name in body]
        return result


class iqCUIPyDlgRadioListDialog(iqCUIPyDlgDialog):

    def __init__(self, title='', height=DEFAULT_DLG_HEIGHT, width=DEFAULT_DLG_WIDTH,
                 list_height=DEFAULT_LIST_HEIGHT, body='', background_title='',
                 *args, **kwargs):
        iqCUIPyDlgDialog.__init__(self, title=title, height=height, width=width, body=body,
                                  background_title=background_title, *args, **kwargs)

        self.list_height = list_height
        self.result = None

    def main(self):
        # print self.body
        self.result = self.radiolist(text=self.title, width=self.width, height=self.height,
                                     list_height=self.list_height, choices=self.body)
        return self.result[0] == self.OK, self.result[1]

    def getCheckList(self):
        body = [line[0] for line in self.body]
        result = [name in self.result[1] for name in body]
        return result


class iqCUIPyDlgListDialog(iqCUIPyDlgDialog):

    def __init__(self, title='', height=DEFAULT_DLG_HEIGHT, width=DEFAULT_DLG_WIDTH,
                 list_height=DEFAULT_LIST_HEIGHT, body='', background_title='', *args, **kwargs):
        iqCUIPyDlgDialog.__init__(self, title=title, height=height, width=width, body=body,
                                  background_title=background_title, *args, **kwargs)

        self.list_height = list_height
        self.result = None

    def main(self):
        try:
            if self.body:
                self.result = self.mixedform(text=self.title, elements=self.body,
                                             height=self.height, width=self.width,
                                             form_height=self.list_height)

                return self.result[0] == self.OK
            else:
                #
                return True
        except:
            raise


DEFAULT_USERNAME_DLG_WIDTH = 120
DEFAULT_USERNAME_DLG_HEIGHT = 15
DEFAULT_USERNAME_DLG_LIST_HEIGHT = 7


class iqCUIUsernameDialog(iqCUIPyDlgDialog):
    """
    CUI select username dialog class.
    """
    def __init__(self, title='',
                 height=DEFAULT_USERNAME_DLG_HEIGHT, width=DEFAULT_USERNAME_DLG_WIDTH,
                 list_height=DEFAULT_USERNAME_DLG_LIST_HEIGHT, body='', background_title='',
                 default_username='', reg_users=None, user_descriptions=(),
                 *args, **kwargs):
        """
        Constructor.
        """
        iqCUIPyDlgDialog.__init__(self, title=title, height=height, width=width, body=body,
                                  background_title=background_title, *args, **kwargs)

        if not isinstance(user_descriptions, (list, tuple)):
            user_descriptions = tuple()

        self.choices = [(username, user_descriptions[i] if i < len(user_descriptions) else '')for i, username in enumerate(reg_users)] if reg_users else list()
        self.default_username = default_username
        self.list_height = list_height
        self.result = None

    def main(self):
        try:
            if self.body:
                code, tag = self.menu(text=_(u'Select a user to login '),
                                      title=self.title,
                                      height=self.height, width=self.width,
                                      choices=self.choices)
                self.result = (code, tag)
                return code == self.OK
            else:
                #
                return True
        except:
            log_func.fatal(u'Error CUI username dialog')
        return False

    def getUsername(self):
        """
        Get selected username.

        :return: Username or None if error.
        """
        return self.result[1] if self.result else None


class iqCUIPasswordDialog(iqCUIPyDlgDialog):
    """
    CUI password dialog class.
    """
    def __init__(self, title='', height=None, width=None,
                 body='', background_title='',
                 *args, **kwargs):
        """
        Constructor.
        """
        iqCUIPyDlgDialog.__init__(self, title=title, height=height, width=width, body=body,
                                  background_title=background_title, *args, **kwargs)
        self.result = None

    def main(self):
        try:
            if self.body:
                code, password = self.passwordbox(text=_(u'Enter user password to login'),
                                                  title=self.title,
                                                  height=self.height, width=self.width,
                                                  insecure=True)
                self.result = (code, password)

                return code == self.OK
            else:
                #
                return True
        except:
            log_func.fatal(u'Error CUI password dialog')
        return False

    def getPassword(self):
        """
        Get password.
        """
        return self.result[1] if self.result else None

    def getPasswordHash(self):
        """
        Get password hash as md5.
        """
        return hashlib.md5(self.result[1].encode()).hexdigest() if self.result else None
