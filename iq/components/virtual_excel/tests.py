#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль тестов для виртуального Excel.
"""

import time
import sys
import os
import os.path

import unittest

from . import v_excel

__version__ = (0, 1, 1, 1)


class icVirtualExcelTests(unittest.TestCase):
    """
    Тесты для виртуального Excel.
    """
    test_path = None

    def setUp(self):
        sys.path.append(os.getcwd())
        try:
            self.test_path = os.path.dirname(__file__)
        except:
            self.test_path = os.getcwd()

    def test_all(self):
        """
        Тестирование генерации XML.
        """
        app = v_excel.iqVExcel()

        app.load(self.test_path + '/testfiles/example.xml')

        work_book = app.getActiveWorkbook()

        work_sheet = work_book.findWorksheet('Worksheet1')

        table = work_sheet.getTable()

        cell = table.getCell(5, 5)
        cell.setValue('Yea')
        cell = table.getCell(3, 3)
        cell.setValue('Привет')

        row = table.getRow(3)
        cell = row.createCellIdx(2)
        cell.setValue('Проба')

        new_range = work_sheet.getRange(1, 1, 3, 2)
        new_range.setValues([[11.2, '222'], [333, 333.2], ['444', '5555']])

        new_range = work_sheet.getRange(1, 1, 2, 2)
        new_range.setStyle(font={'Bold': 1, 'Size': 16, 'Italic': 1},
                           interior={'Color': '#00FF00'})

        # Проверка обрамления
        new_range = work_sheet.getRange(3, 3, 4, 5)
        new_range.setBorderOn(border_left={'LineStyle': 'Continuous', 'Weight': 1},
                              border_top={'LineStyle': 'Continuous', 'Weight': 1},
                              border_right={'LineStyle': 'Continuous', 'Weight': 1},
                              border_bottom={'LineStyle': 'Continuous', 'Weight': 1})

        new_range.updateStyle(font={'Bold': 1, 'Size': 14, 'Italic': 1}, style_auto_create=True)

        new_range = work_sheet.getRange(10, 1, 1, 6)
        new_range.setBorderOn(border_left={'LineStyle': 'Continuous', 'Weight': 1},
                              border_top={'LineStyle': 'Continuous', 'Weight': 1},
                              border_right={'LineStyle': 'Continuous', 'Weight': 1},
                              border_bottom={'LineStyle': 'Continuous', 'Weight': 1})

        new_range = work_sheet.getRange(1, 10, 10, 1)
        new_range.setBorderOn(border_left={'LineStyle': 'Continuous', 'Weight': 1},
                              border_top={'LineStyle': 'Continuous', 'Weight': 1},
                              border_right={'LineStyle': 'Continuous', 'Weight': 1},
                              border_bottom={'LineStyle': 'Continuous', 'Weight': 1})

        styles = work_book.getStyles()
        id1 = styles.createStyle().getAttributes()['ID']
        id2 = styles.createStyle().getAttributes()['ID']
        ids = styles.clearUnUsedStyles()

        app.saveAs(self.test_path + '/testfiles/result.xml')

        app.load(self.test_path + '/testfiles/result.xml')
        app.saveAs(self.test_path + '/testfiles/result_ok.xml')

    def test_hello_word(self):
        """
        Тестирование генерации xml для openOffice.org Calc.
        """
        app = v_excel.iqVExcel()
        work_book = app.getActiveWorkbook()
        work_sheet = work_book.createWorksheet()
        table = work_sheet.createTable()

        cell = table.createCell(3, 3)
        cell.setValue('Привет')

        app.saveAs(self.test_path + '/testfiles/ooo1.xml')

    def test_ooo2_calc(self):
        """
        Тестирование генерации xml для openOffice.org Calc.
        """
        app = v_excel.iqVExcel()
        work_book = app.getActiveWorkbook()
        work_sheet = work_book.createWorksheet()
        table = work_sheet.createTable()

        new_range = work_sheet.getRange(1, 1, 3, 2)
        new_range.setValues([[11.2, '222'], [333, 333.2], ['444', '5555']])
        app.saveAs(self.test_path + '/testfiles/ooo2.xml')

    def test_ooo3_calc(self):
        """
        Тестирование генерации xml для openOffice.org Calc.
        """
        app = v_excel.iqVExcel()
        work_book = app.getActiveWorkbook()
        work_sheet = work_book.createWorksheet()
        table = work_sheet.createTable()

        new_range = work_sheet.getRange(1, 1, 3, 2)
        new_range.setValues([[11.2, '222'], [333, 333.2], ['444', '5555']])

        new_range = work_sheet.getRange(1, 1, 2, 2)
        new_range.setStyle(font={'Bold': 1, 'Size': 16, 'Italic': 1},
                           interior={'Color': '#00FF00'})
        app.saveAs(self.test_path + '/testfiles/ooo3.xml')

    def test_ooo4_calc(self):
        """
        Тестирование генерации xml для openOffice.org Calc.
        """
        app = v_excel.iqVExcel()
        work_book = app.getActiveWorkbook()
        work_sheet = work_book.createWorksheet()
        table = work_sheet.createTable()

        new_range = work_sheet.getRange(3, 1, 3, 3)
        new_range.setBorderOn(border_left={'LineStyle': 'Continuous', 'Weight': 1},
                              border_top={'LineStyle': 'Continuous', 'Weight': 2},
                              border_right={'LineStyle': 'Continuous', 'Weight': 1},
                              border_bottom={'LineStyle': 'Continuous', 'Weight': 2})
        app.saveAs(self.test_path + '/testfiles/ooo4.xml')

    def test_ooo5_hidden(self):
        """
        Тестирование генерации xml для openOffice.org Calc.
        """
        app = v_excel.iqVExcel()
        app.load(self.test_path + '/testfiles/example.xml')

        work_book = app.getActiveWorkbook()
        work_sheet = work_book.findWorksheet('Worksheet1')

        cell = work_sheet.getCell(3, 3)
        cell.setValue('Привет')

        app.saveAs(self.test_path + '/testfiles/ooo5.xml')

    def test_merge(self):
        """
        Тестирование поддержки объединенных ячеек.
        """
        app = v_excel.iqVExcel()

        app.load(self.test_path + '/testfiles/merge0.xml')
        app.saveAs(self.test_path + '/testfiles/merge_ok.xml')


def test_work_sheet():
    """
    Вставка/Удаление/Копирование листов.
    """
    start_time = time.time()
    print('test_work_sheet START')
    v_excel = v_excel.icVExcel()
    v_excel.openWorkbook('testfiles/worksheet01.xml')
    print('open...ok','testfiles/worksheet01.xml')
    v_excel.openWorkbook('testfiles/worksheet02.xml')
    print('open...ok', 'testfiles/worksheet02.xml')
    v_excel.activeWorkbook('testfiles/worksheet01.xml')
    print('active...ok', 'testfiles/worksheet01.xml')
    v_excel.copyWorksheet('testfiles/worksheet01.xml', 'Лист1')
    print('copy...ok', 'testfiles/worksheet01.xml')
    v_excel.pasteWorksheet('testfiles/worksheet02.xml', None, 'ЛистXXX')
    print('paste...ok', 'testfiles/worksheet02.xml')
    v_excel.activeWorkbook('testfiles/worksheet02.xml')
    print('active...ok', 'testfiles/worksheet02.xml')
    v_excel.saveAs('testfiles/worksheet03.xml')
    print('test_work_sheet STOP', time.time()-start_time)


def test_work_sheet_list():
    """
    Группавая работа с листами.
    """
    start_time = time.time()
    print('test_work_sheet_list START')
    v_excel = v_excel.icVExcel()
    v_excel.openWorkbook('testfiles/worksheet01.xml')
    print('open...ok', 'testfiles/worksheet01.xml')
    v_excel.openWorkbook('testfiles/worksheet02.xml')
    print('open...ok', 'testfiles/worksheet02.xml')
    v_excel.selectWorksheet('testfiles/worksheet01.xml', u'Лист1')
    v_excel.selectWorksheet('testfiles/worksheet01.xml', u'Лист1#1')
    print('select...ok', 'testfiles/worksheet01.xml')
    v_excel.copyWorksheetListTo('testfiles/worksheet02.xml', [u'Вот1', u'Вот1'])
    print('copy...ok', 'testfiles/worksheet02.xml')
    v_excel.activeWorkbook('testfiles/worksheet02.xml')
    print('active...ok', 'testfiles/worksheet02.xml')
    v_excel.saveAs('testfiles/worksheet03.xml')
    print('test_work_sheet_list STOP', time.time()-start_time)


def test_del_work_sheet_list():
    """
    Групповое удаление листов.
    """
    start_time = time.time()
    print('test_del_work_sheet_list START')
    v_excel = v_excel.icVExcel()
    v_excel.openWorkbook('testfiles/worksheet03.xml')
    print('open...ok', 'testfiles/worksheet03.xml')
    v_excel.selectWorksheet('testfiles/worksheet03.xml', 'ЛистXXX')
    # v_excel.selectWorksheet('testfiles/worksheet03.xml', u'Литс1_1')
    print('select...ok', 'testfiles/worksheet03.xml', v_excel.getLastSelectedWorksheet())
    # v_excel.delSelectedWorksheetList('testfiles/worksheet03.xml')
    v_excel.delWithoutSelectedWorksheetList('testfiles/worksheet03.xml')
    print('del...ok', 'testfiles/worksheet03.xml')
    v_excel.activeWorkbook('testfiles/worksheet03.xml')
    print('active...ok', 'testfiles/worksheet03.xml')
    v_excel.saveAs('testfiles/worksheet03.xml')
    print('test_del_work_sheet_list STOP', time.time()-start_time)


def test_del_col_row():
    """
    Удаление колонок/строк из листа.
    """
    start_time = time.time()
    print('test_del_col_row START')
    v_excel = v_excel.icVExcel()
    v_excel.openWorkbook('testfiles/worksheet02.xml')
    print('open...ok', 'testfiles/worksheet02.xml')
    work_book = v_excel.getActiveWorkbook()
    work_sheet = work_book.findWorksheet(u'Worksheet1')
    print('find...ok', work_sheet)
    work_tab = work_sheet.getTable()
    print('getTable...ok', work_tab)
    work_tab.delColumn(5)
    print('delColumn...ok')
    work_tab.delRow(4)
    print('delRow...ok')
    v_excel.saveAs('testfiles/worksheet04.xml')
    print('test_del_col_row STOP', time.time()-start_time)


def test_merge_cell():
    """
    Объединение ячеек.
    """
    start_time = time.time()
    print('test_merge_cell START')
    v_excel = v_excel.icVExcel()
    v_excel.openWorkbook('testfiles/worksheet02.xml')
    print('open...ok', 'testfiles/worksheet02.xml')

    print('merge...start')
    v_excel.mergeCell('Worksheet1', 3, 1, 0, 1)
    v_excel.mergeCell('Worksheet1', 1, 2, 1, 0)     # правильно
    v_excel.mergeCell('Worksheet1', 3, 3, 2, 3)
    print('merge...ok')

    v_excel.saveAs('testfiles/worksheet04.xml')
    print('test_merge_cell STOP', time.time()-start_time)


if __name__ == '__main__':
    test_merge_cell()
