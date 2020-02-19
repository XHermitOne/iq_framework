#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control data validator.
"""

import wx
import wx.adv
import wx.gizmos
import wx.dataview

from ...util import log_func
from . import wxdatetime_func

__version__ = (0, 0, 0, 1)

VALIDATIONS_ATTR_NAME = '_validations'


class iqValidateManager(object):
    """
    Control data validator.
    """
    def getValidations(self):
        """
        Get validation list.
        Список проверок.
        Все проверки организуются в список и проверяются последовательно.
        Проверка представляет собой словарь:
            {'name': Наименование проверки,
             'function': Функция проверки правильного значения,
             'err_txt': Текст ошибки, в случае если проверка не прошла,
             'treelistctrl': Объект проверяемого контрола,
            }
        """
        if not hasattr(self, VALIDATIONS_ATTR_NAME):
            setattr(self, VALIDATIONS_ATTR_NAME, list())
        validations = getattr(self, VALIDATIONS_ATTR_NAME)
        return validations

    def addValidationValue(self, name, validation_func=None, error_msg=u'', ctrl=None):
        """
        Add validation.

        :param name: Validation name.
        :param validation_func: Validation function.
        :param error_msg: Error message if not valid.
        :param ctrl: Control for valid.
        :return: True/False.
        """
        validations = self.getValidations()

        try:
            validation = dict(name=name,
                              func=validation_func,
                              err_txt=error_msg,
                              ctrl=ctrl)
            validations.append(validation)
            return True
        except:
            log_func.fatal(u'Add validation error <%s>' % name)
        return False

    def _validateValuesDict(self, **values):
        """
        Run validate.

        :param values: Validate values dictionary.
        :return: Dictionary:
            { 'validation_name': error message or None if valid,
              ...
            }
        """
        validations = self.getValidations()

        validate_errors = dict()
        for validation_name, value in values.items():
            for validation in validations:
                if validation.get('name', None) == validation_name:
                    validate_msg = validation.get('err_txt', validation_name)
                    try:
                        validate_func = validation.get('function', None)
                        if validate_func:
                            is_ok = validate_func(value)
                            if not is_ok:
                                validate_errors[validation_name] = validation.get('err_txt',
                                                                                  u'Not define error message')
                        else:
                            validate_errors[validation_name] = u'Not define validate function <%s>' % validate_msg
                    except:
                        err_msg = u'Validate operation error <%s>' % validate_msg
                        log_func.fatal(err_msg)
                        validate_errors[validation_name] = err_msg
        return validate_errors

    def validateValuesDict(self, **values):
        """
        Run validate.

        :param values: Validate values dictionary.
        :return: Dictionary:
            { 'validation_name': error message or None if valid,
              ...
            }
            or None if error.
        """
        try:
            return self._validateValuesDict(**values)
        except:
            log_func.fatal(u'Validate error')
        return None

    def _validateCtrlDict(self, *names):
        """
        Run validate control values.

        :param names: Validation names.
        :return: Dictionary:
            { 'validation_name': error message or None if valid,
              ...
            }
        """
        validations = self.getValidations()

        validate_errors = dict()
        for validation in validations:
            validation_name = validation.get('name', None)
            if validation_name in names:
                validate_msg = validation.get('err_txt', validation_name)
                try:
                    validate_func = validation.get('function', None)
                    validate_ctrl = validation.get('treelistctrl', None)
                    if validate_ctrl is None:
                        log_func.warning(u'Not define validate control <%s>' % validate_msg)
                        continue

                    value = self.getCtrlValue(validate_ctrl)
                    if validate_func:
                        is_ok = validate_func(value)
                        if not is_ok:
                            validate_errors[validation_name] = validation.get('err_txt',
                                                                              u'Not define error message')
                    else:
                        validate_errors[validation_name] = u'Not define validate function <%s>' % validate_msg
                except:
                    err_msg = u'Validate error <%s>' % validate_msg
                    log_func.fatal(err_msg)
                    validate_errors[validation_name] = err_msg
        return validate_errors

    def validateCtrlDict(self, *names):
        """
        Run validate control values.

        :param names: Validation names.
        :return: Dictionary:
            { 'validation_name': error message or None if valid,
              ...
            }
            or None if error.
        """
        try:
            return self._validateCtrlDict(*names)
        except:
            log_func.fatal(u'Validate control values error')
        return None

    def getCtrlValue(self, ctrl):
        """
        Get control value.

        :param ctrl: Control object.
        :return: Control value.
        """
        value = None
        if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
            if hasattr(ctrl, 'getValue'):
                value = ctrl.getValue()
            elif issubclass(ctrl.__class__, wx.CheckBox):
                value = ctrl.IsChecked()
            elif issubclass(ctrl.__class__, wx.TextCtrl):
                value = ctrl.GetValue()
            elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
                wx_dt = ctrl.GetValue()
                value = wxdatetime_func.wxdatetime2datetime(wx_dt)
            elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
                value = ctrl.GetPath()
            elif issubclass(ctrl.__class__, wx.SpinCtrl):
                value = ctrl.GetValue()
            elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
                value = self._get_wxDataViewListCtrl_data(ctrl)
            else:
                log_func.warning(u'iqValidateManager. Get control value <%s> not support' % ctrl.__class__.__name__)
        return value
