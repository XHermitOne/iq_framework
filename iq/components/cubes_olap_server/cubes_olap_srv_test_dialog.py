#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговая форма тестирования OLAP сервера Cubes.
"""

import keyword

import wx
import wx.stc
from . import cubes_olap_srv_test_dlg

from ic.log import log
from ic.utils import toolfunc

from STD.spreadsheet import spreadsheet_view_manager

from . import cubes_olap_srv_request_panel

__version__ = (0, 1, 1, 1)


class icCubesOLAPSrvTestDialog(cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto):
    """
    Диалоговая форма тестирования OLAP сервера Cubes.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto.__init__(self, *args, **kwargs)

        # Настройка обозревателя кода
        self.json_scintilla.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.json_scintilla.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.json_scintilla.SetProperty('fold', '1')
        self.json_scintilla.SetProperty('tab.timmy.whinge.level', '1')
        self.json_scintilla.SetMargins(0, 0)

        # Не видеть пустые пробелы в виде точек
        self.json_scintilla.SetViewWhiteSpace(False)

        # Установить ширину 'таба'
        # Indentation and tab stuff
        self.json_scintilla.SetIndent(4)                 # Proscribed indent size for wx
        self.json_scintilla.SetIndentationGuides(True)   # Show indent guides
        self.json_scintilla.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.json_scintilla.SetTabIndents(True)          # Tab key indents
        self.json_scintilla.SetTabWidth(4)               # Proscribed tab size for wx
        self.json_scintilla.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Установка поле для захвата маркеров папки
        self.json_scintilla.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.json_scintilla.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.json_scintilla.SetMarginSensitive(1, True)
        self.json_scintilla.SetMarginSensitive(2, True)
        self.json_scintilla.SetMarginWidth(1, 25)
        self.json_scintilla.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,    'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Маркеры режима отладки
        # self.json_scintilla.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        # self.json_scintilla.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')

        # Тестируемый OLAP сервер
        self._OLAP_server = None

        # Менеджер управления выводом структуры SpreadSheet
        self._spreadsheet_mngr = spreadsheet_view_manager.icSpreadSheetViewManager(grid=self.spreadsheet_grid)

    def setOLAPServer(self, olap_server):
        """
        Установить тестируемый OLAP сервер.
        :param olap_server: OLAP сервер
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            self.request_panel.setOLAPServer(self._OLAP_server)

    def onCloseButtonClick(self, event):
        """
        Обработчик кнопки ЗАКРЫТЬ.
        """
        self.EndModal(wx.ID_CLOSE)
        event.Skip()

    def _parse_dimension_names(self, dimension_url):
        """
        Список имен измерения.
        :param dimension_url: Часть элемента запроса.
            Например store_date@ymd:month
        :return: Список имен элементов измерения.
        """
        dimension_names = list()
        if '@' in dimension_url:
            # Указано измерение@иерархия:уровень
            cube_idx = self.request_panel.cube_choice.GetSelection()
            cube = self._OLAP_server.getCubes()[cube_idx]
            dimension_name = dimension_url.split('@')[0]
            dimension = cube.findDimension(dimension_name)
            hierarchy_name = dimension_url.split('@')[1].split(':')[0]
            hierarchy = dimension.findHierarchy(hierarchy_name)
            level_names = hierarchy.getLevelNames()
            hierarchy_level_name = dimension_url.split('@')[1].split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        elif ':' in dimension_url:
            # Указано измерение:уровень
            cube_idx = self.request_panel.cube_choice.GetSelection()
            cube = self._OLAP_server.getCubes()[cube_idx]
            dimension_name = dimension_url.split(':')[0]
            dimension = cube.findDimension(dimension_name)
            level_names = [level.getName() for level in dimension.getLevels()]
            hierarchy_level_name = dimension_url.split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        else:
            # Указано измерение
            dimension_names = tuple([dimension_url])

        # log.debug(u'Список элментов измерений %s' % str(dimension_names))
        return dimension_names

    def onRefreshToolClicked(self, event):
        """
        Обработчик кнопки ОБНОВИТЬ.
        """
        if self._OLAP_server:
            request_url = self.request_panel.getRequestURL()
            self.request_panel.request_textCtrl.SetValue(request_url)

            result = self._OLAP_server.get_response(request_url)

            # self.json_scintilla.SetText(str(result))
            self.json_scintilla.ClearAll()
            self.json_scintilla.AddText(toolfunc.StructToTxt(result))

            if result:
                if self.request_panel.drilldown_checkBox.GetValue() and '|' in self.request_panel.drilldown_textCtrl.GetValue():
                    row_dimension_url, col_dimension_url = self.request_panel.drilldown_textCtrl.GetValue().split('|')
                    row_dimension = self._parse_dimension_names(row_dimension_url)
                    col_dimension = self._parse_dimension_names(col_dimension_url)
                    dataframe = self._OLAP_server.to_pivot_dataframe(result, row_dimension=row_dimension,
                                                                     col_dimension=col_dimension)

                    # spreadsheet = self._OLAP_server.pivot_to_spreadsheet(result, dataframe=dataframe)
                else:
                    row_dimension_url = self.request_panel.drilldown_textCtrl.GetValue()
                    row_dimension = self._parse_dimension_names(row_dimension_url)
                    # col_dimension = self._parse_dimension_names(col_dimension_url)
                    dataframe = self._OLAP_server.to_pivot_dataframe(result, row_dimension=row_dimension)

                spreadsheet = self._OLAP_server.pivot_to_spreadsheet(result, dataframe=dataframe)
                #     spreadsheet = self._OLAP_server.to_spreadsheet(result)
                # log.debug(u'SpreadSheet: %s' % str(spreadsheet))
                self._spreadsheet_mngr.view_spreadsheet(spreadsheet)
            else:
                # Если нет ничего, то полностью очистить грид
                self._spreadsheet_mngr.reCreateGrid(self._spreadsheet_mngr.getSpreadSheetGrid(), 1, 1)

            # ВНИМАНИЕ! Для обновления грида (Чтобы появились полосы прокрутки)
            # необходимо контрол панели грида перекомпоновать
            self.spreadsheet_panel.Layout()

        event.Skip()


def show_cubes_olap_srv_test_dlg(parent=None, olap_srv=None):
    """
    Отобразить окно тестирования OLAP сервера Cubes.
    :param parent: Родительское окно.
        Если не определено, то берется самое главное окно.
    :param olap_srv: Тестируемый OLAP сервер.
    :return: True/False.
    """
    if olap_srv is None:
        log.warning(u'Не определен объект OLAP сервера для тестирования')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Запускаем OLAP сервер
        olap_srv.run()

        dlg = icCubesOLAPSrvTestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)

        dlg.ShowModal()

        # Остановить OLAP сервер
        olap_srv.stop()

        return True
    except:
        log.fatal(u'Ошибка отображения окна тестирования OLAP сервера Cubes.')
    return False
