#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно множественного выбора элементов в дереве данных.
"""

import wx

from ic.components import icwidget
import ic.components.icResourceParser as prs

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'hgap': u'0', 'activate': 1, 'obj_module': None, 'data_name': None, 'border': 5, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 1, 'type': 'BoxSizer', 'res_module': None, 'description': None, '_uuid': 'e601d87f454936a9e3962ed9d7555d1a', 'flag': 240, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'labels': ['col1'], 'keyDown': None, 'selectChanged': None, 'border': 0, 'titleRoot': 'root', 'treeDict': {}, 'style': 2177, 'foregroundColor': None, 'span': (1, 2), 'alias': None, 'component_module': None, 'proportion': 1, 'itemCollapsed': None, 'source': None, 'itemActivated': None, 'itemExpanded': None, 'size': (-1, -1), 'type': 'MultiCheckTreeListCtrl', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'f77524d1dd57e50b41e336c75a87e596', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'hideHeader': False, 'backgroundColor': None, 'child': [], 'name': u'multi_check_tree_ctrl', 'wcols': [], 'data_name': None, 'refresh': None, 'itemChecked': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'hgap': u'0', 'activate': 1, 'obj_module': None, 'data_name': None, 'border': 5, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'description': None, '_uuid': 'fa9b78c147f8ca17cf516410638c1d70', 'flag': 752, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'_root_obj.EndModal(wx.CANCEL)', 'font': {}, 'border': 5, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'd8ac3c771a616036f3532cb59fc10e53', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2560, 'recount': None, 'name': u'cancelBtn', 'mouseUp': None, 'keyDown': None, 'init_expr': None, 'position': (2, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'_root_obj.EndModal(wx.OK)', 'font': {}, 'border': 5, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'OK', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': '35761f30dbce0346f5dd1a31a513bfda', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 512, 'recount': None, 'name': u'okBtn', 'mouseUp': None, 'keyDown': None, 'init_expr': None, 'position': (2, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'layout': u'horizontal', 'name': 'DefaultName_1856', 'init_expr': None, 'position': (0, 0), 'vgap': u'0'}], 'layout': 'vertical', 'name': 'DefaultName_1691', 'init_expr': None, 'position': (0, 0), 'vgap': u'0'}], 'refresh': None, 'border': 0, 'size': (450, 300), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'Dialog', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': 'b762dbe6359eb70e080bd932fa58ff7d', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'alias': None, 'recount': None, 'icon': None, 'setFocus': None, 'name': u'MultiCheckTreeDLG', 'data_name': None, 'keyDown': None, 'init_expr': None, 'position': wx.Point(5, 5), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK


# --- Функции ---
def icMultiCheckTreeDlg(Parent_, Title_, TreeData_):
    """
    Функция вызова диалога для множественного выбора элементов 
    из дерева данных.

    :param Parent_: Родительское окно диалога.
    :param Title_: Заголовок диалогового окна.
    :param TreeData_: Данные древовидной структуры.
    """
    try:
        win_clear = False
        if Parent_ is None:
            id_ = wx.NewId()
            Parent_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icMultiCheckTreeDialog(Parent_)
        dlg.setTitle(Title_)
        if dlg.edit(TreeData_) == wx.ID_OK:
            result = dlg.getResult()
            dlg.destroyDlg()
            # Удаляем созданное родительское окно
            if win_clear:
                Parent_.Destroy()
            return result
    finally:
        dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Parent_.Destroy()
        return None


#   Имя класса
ic_class_name = 'icMultiCheckTreeDialog'


# --- Классы ---
class icMultiCheckTreeDialog:
    """
    Диалоговое окно множественного выбора элементов дерева данных.
    """
    def __init__(self, parent):
        """
        Конструктор.

        :param parent: Родительское окно.
        """
        self.evalSpace = icwidget.icResObjContext()
        self.evalSpace['WrapperObj'] = self
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        Главный объект - диалоговое окно.
        """
        return self.object

    def destroyDLg(self):
        """
        Удалить диалог.
        """
        if self.object:
            self.object.Destroy()
            self.object = None
            
    def edit(self, TreeData_):
        """
        Запуск редактирования данных.
        """
        if self.object:
            tree_ctrl = self.evalSpace.GetObject('multi_check_tree_ctrl')
            tree_ctrl.loadTree(TreeData_)
            return self.object.ShowModal()
        return None
    
    def getResult(self):
        """
        Возвратить результат редактирования.
        """
        tree_ctrl = self.evalSpace.GetObject('multi_check_tree_ctrl')
        return tree_ctrl.get_check_list()


def test(par=0):
    """
    Тестируем класс.
    """
    from ic.components import ictestapp
    from ic.components.user import icmultichecktreelistctrl
    app = ictestapp.TestApp(par)
    
    result = icMultiCheckTreeDlg(None, u'Заголовок', icmultichecktreelistctrl.load_data())
    
    app.MainLoop()


if __name__ == '__main__':
    test()
