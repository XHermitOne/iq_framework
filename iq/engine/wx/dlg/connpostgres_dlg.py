#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно редактирования связи с БД PostgreSQL.
"""

import wx
import ic.components.icResourceParser as prs
from ic.utils import util
import ic.utils.resource as res

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (250, 210), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'Dialog', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'd5242e525b796af2e317e212ecb3ea19', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'sizer1', 'flexRows': [], 'minCellWidth': 10, 'type': u'GridBagSizer', 'border': 0, '_uuid': u'17f906685f3884f86650080aa36e77ae', 'proportion': 0, 'alias': None, 'flag': 0, 'minCellHeight': 10, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'text': u'\u0412\u041d\u0418\u041c\u0410\u041d\u0418\u0415!!! \u041f\u043e\u0441\u043b\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0443 \u0441\u043b\u0435\u0434\u0443\u0435\u0442 \u043f\u0435\u0440\u0435\u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c.', 'refresh': None, 'font': {}, 'border': 0, 'size': (200, 50), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 2), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'adf41d63b1e17c68be1dc229a281235d', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'NoteTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': 1, 'show': 1, 'text': u'\u0418\u043c\u044f \u0411\u0414:', 'refresh': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'a97d333d9701ff47338c3e82778e1641', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'dbnameTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 1)}, {'activate': 1, 'show': 1, 'text': u'\u0425\u043e\u0441\u0442:', 'refresh': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'90e0d71837d3e80c9240c4b6cb694ee1', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'hostTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 1)}, {'activate': 1, 'show': 1, 'text': u'\u041f\u043e\u0440\u0442:', 'refresh': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'10f2e1929fea4489a1f446ef6417f7d0', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'portTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 1)}, {'activate': 1, 'show': 1, 'text': u'\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c:', 'refresh': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'65d1b41c9ba30767da861a28f7130e83', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'userTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (4, 1)}, {'activate': 1, 'show': 1, 'text': u'\u041f\u0430\u0440\u043e\u043b\u044c:', 'refresh': None, 'font': {}, 'border': 0, 'size': (100, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'1072390c4f6809d79e283b765068d5c2', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'passwdTxt', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 1)}, {'activate': 1, 'treelistctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'63698fa4750dc18a4bd95d3fe3a066dc', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'dbnameEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (1, 2), 'refresh': []}, {'activate': 1, 'treelistctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'5320e5ddaa1f0068151334767d811b9a', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'hostEdt', 'changed': None, 'value': u'localhost', 'alias': None, 'init_expr': None, 'position': (2, 2), 'refresh': []}, {'activate': 1, 'treelistctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'de41fb1d2f381370f9b1d05d39c9bbeb', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'portEdt', 'changed': None, 'value': u'5432', 'alias': None, 'init_expr': None, 'position': (3, 2), 'refresh': []}, {'activate': 1, 'treelistctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'cf1158d64b3e4fe47e459c0c07954a48', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'userEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (4, 2), 'refresh': []}, {'activate': 1, 'treelistctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'c6c00c6d7fb5c505d8f322a27dd8e67c', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'passwdEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (5, 2), 'refresh': []}, {'activate': 1, 'show': 1, 'mouseClick': u'_root_obj.EndModal(wx.CANCEL)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'76ad513d6b2b2ae1cba27f8b5f6f3325', 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'cancelBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 1), 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u'_root_obj.EndModal(wx.OK)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'a4082275b1873797228c1d13d4da6979', 'moveAfterInTabOrder': u'', 'flag': 512, 'recount': None, 'name': u'okBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 2), 'refresh': None, 'mouseContextDown': None}], 'position': (-1, -1), 'flexCols': [], 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'ConnectionPostgresDLG', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0)}

#   Версия объекта
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK


# --- Функции ---
def editConnectionPostgreSQL(parent, db_res_name):
    """
    Отредактировать ресурс описывающи связь с БД POstgreSQL.

    :param parent: Родительское окно диалога.
    :param db_res_name: Имя ресурса БД.
    """
    # Сначала получить ресурс
    db_res = res.icGetRes(db_res_name, 'src', nameRes=db_res_name)
    db_res = getConnectionPostgresDlg(parent, db_res)
    return res.icSaveRes(db_res_name, 'src', nameRes=db_res_name, resData=db_res)


def getConnectionPostgresDlg(parent, title, db_resource):
    """
    Функция вызова диалога для редактирования коннекшн стринга PostgreSQL.

    :param parent: Родительское окно диалога.
    :param title: Заголовок диалогового окна.
    :param db_resource: Ресурс БД.
    """
    try:
        win_clear = False
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icConnectionPostgresDialog(parent)
        dlg.setTitle(title)
        if dlg.editConnectionString(db_resource) == wx.ID_OK:
            result = dlg.getDBResource()
            dlg.destroyDlg()
            # Удаляем созданное родительское окно
            if win_clear:
                parent.Destroy()
            return result
    finally:
        dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()
    return None


#   Имя класса
ic_class_name = 'icConnectionPostgresDialog'


# --- Классы ---
class icConnectionPostgresDialog:
    def __init__(self, parent):
        """
        Конструктор.

        :param parent: Родительское окно.
        """
        self.evalSpace = icwidget.icResObjContext()
        self.evalSpace['WrapperObj'] = self
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        # Редактируемый ресурс
        self.db_res = None
        
    def getObject(self):
        """
        Главный объект - диалоговое окно.
        """
        return self.object

    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if name in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj'][name]
        else:
            return None
            
    def editConnectionString(self, DBRes_=None):
        """
        Редактирование ресурса БД PostgreSQL.

        :param DBRes_: Ресурс БД.
        """
        self.db_res = DBRes_
        if self.object:
            return self.object.ShowModal()
        return None

    def getDBResource(self):
        """
        Получить редактируеый ресурс.
        """
        return self.db_res

    def destroyDLg(self):
        """
        Удалить диалог.
        """
        if self.object:
            self.object.Destroy()
            self.object = None


def test(par=0):
    """
    Тестируем класс icConnectionPostgresDialog.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
