#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного контрола панели инструментов WX.
"""

# Подключение библиотек
import wx

from ic.log import log
from ic.bitmap import bmpfunc


__version__ = (0, 1, 1, 2)


class icToolBarManager(object):
    """
    Менеджер WX панели инструментов.
    В самом общем случае в этот класс перенесены функции работы
    с панелью инструментов из менеджера форм.
    Перенос сделан с целью рефакторинга.
    Также этот класс могут наследовать классы специализированных
    менеджеров, которые работают с панелями инструментов управления
    записями/объектами.
    """
    def enableTools_toolbar(self, toolbar, **kwargs):
        """
        Установить вкл./выкл. инструментов панели инструментов wx.ToolBar.

        :param toolbar: Объект контрола wx.ToolBar.
        :param kwargs: Словарь формата:
            {
                Имя инструмента1: True/False,
                ...
            }
            Имя инструмента - имя контрола в проекте wx.FormBuilder.
            Объект инструмента ищется среди атрибутов формы по типу wx.ToolBarToolBase.
        :return: True - все ок, False - какая то ошибка
        """
        result = True

        if not isinstance(toolbar, wx.ToolBar):
            log.warning(u'Объект %s не типа wx.ToolBar' % str(toolbar))
            return False

        for tool_name, enable in kwargs.items():
            tool = getattr(self, tool_name) if hasattr(self, tool_name) else None
            if tool and isinstance(tool, wx.ToolBarToolBase):
                toolbar.EnableTool(tool.GetId(), enable)
                result = result and True
            else:
                log.warning(u'Инструмент <%s> не найден или не соответствует типу' % tool_name)
                result = result and False

        return result

    def setLibImages_ToolBar(self, tool_bar=None, **tools):
        """
        Установить библиотечне картинки в качестве картинок
        инструментов в wxToolBar.

        :param tool_bar: Объект wx.ToolBar.
        :param tools: Словарь соответствий имен инструментов с именами файлов образов библиотеки.
            Например:
                edit_tool = 'document--pencil.png'
        :return: True/False.
        """
        if not tools:
            # Если словарь соответствий пуст, то ничего не делаем
            return False

        for tool_name, lib_img_filename in tools.items():
            if hasattr(self, tool_name):
                # <wx.Tool>
                tool = getattr(self, tool_name)
                tool_id = tool.GetId()
                bmp = bmpfunc.createLibraryBitmap(lib_img_filename)

                if bmp:
                    if tool_bar is None:
                        tool_bar = tool.getToolBar()
                    # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
                    # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
                    # Для этого вызываем метод панели инструметнтов
                    # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
                    tool_bar.SetToolNormalBitmap(tool_id, bmp)
                else:
                    log.warning(u'Не найдена библиотечная картинка <%s>' % lib_img_filename)
            else:
                log.warning(u'Не найден инструмент <%s> панели инструментов' % tool_name)

        if tool_bar:
            tool_bar.Realize()
        else:
            log.warning(u'Не определена панель инструментов wxToolBar')

    def getButtonLeftBottomPoint(self, button=None):
        """
        Определить точку левого-нижнего края кнопки.
        Используется для вызова всплывающих меню.

        :param button: Объект кнопки wx.Button.
        """
        if button is None:
            # Если кнопка не определена, то функция бессмыслена
            return None

        point = button.GetPosition()
        point = button.GetParent().ClientToScreen(point)
        return wx.Point(point.x, point.y + button.GetSize().y)

    def getToolLeftBottomPoint(self, toolbar, tool):
        """
        Определить точку левого-нижнего края кнопки.
        Используется для вызова всплывающих меню.

        :param toolbar: Объект панели инструментов wx.ToolBar.
        :param tool: Объект инструмента панели инструментов wx.ToolBarToolBase.
        """
        if tool is None:
            # Если инструмент не определен, то функция бессмыслена
            return None

        toolbar_pos = toolbar.GetScreenPosition()
        toolbar_size = toolbar.GetSize()
        tool_index = toolbar.GetToolPos(tool.GetId())
        tool_size = toolbar.GetToolSize()
        x_offset = 0
        for i in range(tool_index):
            prev_tool = toolbar.GetToolByPos(i)
            prev_ctrl = prev_tool.GetControl() if prev_tool.IsControl() else None
            x_offset += prev_ctrl.GetSize()[0] if prev_ctrl else tool_size[0]

        return wx.Point(toolbar_pos[0] + x_offset, toolbar_pos[1] + toolbar_size[1])

