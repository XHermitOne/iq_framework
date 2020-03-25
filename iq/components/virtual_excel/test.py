#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль тестов для виртуального Excel.
"""
import os


def test_oc1():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/OC1/OC1.ods')
    excel.saveAs('./testfiles/OC1/result_oc1.xml')
    excel.saveAs('./testfiles/OC1/result_oc1.ods')


def test_oc1_1():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/OC1/oc1.xml')
    excel.saveAs('./testfiles/OC1/result_oc1_1.ods')


def test_oc1_2():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/OC1/oc1.xml')
    excel.saveAs('./testfiles/OC1/result_oc1_2.xml')


def test_2():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test2.ods')
    excel.saveAs('./testfiles/result_test2.ods')


def test_3():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test3.ods')
    excel.saveAs('./testfiles/result_test3.ods')


def test_4():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/bpr1137.ods')
    excel.saveAs('./testfiles/bpr1137_result.ods')


def test_5():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/narjad.ods')

    excel.setCellValue('Сдельн.', 19, 13, 1.99)

    excel.saveAs('./testfiles/narjad_result.ods')
    excel.saveAs('./testfiles/narjad_result.xml')
    
    # cmd='soffice ./testfiles/narjad.ods'
    # os.system(cmd)
    cmd = 'soffice ./testfiles/narjad_result.ods'
    os.system(cmd)


def test_6():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/t1.ods')
    excel.saveAs('./testfiles/t1_result.ods')
    
    cmd = 'soffice ./testfiles/t1.ods'
    os.system(cmd)
    cmd = 'soffice ./testfiles/t1_result.ods'
    os.system(cmd)


def test_7():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/tabmilk.ods')
    excel.saveAs('./testfiles/tabmilk_result.ods')
    
    cmd = 'soffice ./testfiles/tabmilk.ods'
    os.system(cmd)
    cmd = 'soffice ./testfiles/tabmilk_result.ods'
    os.system(cmd)


def test_8():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/narjadok.ods')
    excel.saveAs('./testfiles/narjadok_result.ods')
    
    cmd = 'soffice ./testfiles/narjadok.ods'
    os.system(cmd)
    cmd = 'soffice ./testfiles/narjadok_result.ods'
    os.system(cmd)


def test_9():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/narjadpv.ods')
    excel.saveAs('./testfiles/narjadpv_result.ods')
    excel.saveAs('./testfiles/narjadpv_result.xml')
    
    cmd = 'soffice ./testfiles/narjadpv.ods'
    os.system(cmd)
    cmd = 'soffice ./testfiles/narjadpv_result.ods'
    os.system(cmd)


def test_10():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/new/narjadpv.ods')
    excel.saveAs('./testfiles/new/narjadpv_result.ods')
    excel.saveAs('./testfiles/new/narjadpv_result.xml')
    
    cmd = 'soffice ./testfiles/new/narjadpv.ods'
    os.system(cmd)
    cmd = 'soffice ./testfiles/new/narjadpv_result.ods'
    os.system(cmd)


def test_11():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/tabbnew.ods')
    # excel.saveAs('./testfiles/tabbnew_result.ods')
    excel.saveAs('./testfiles/tabbnew_result.xml')
    
    # cmd='soffice ./testfiles/tabbnew_result.ods'
    # os.system(cmd)


def test_sum():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test.ods')
    excel.saveAs('./testfiles/test_result.ods')
    # excel.saveAs('./testfiles/test_result.xml')
    
    cmd = 'soffice ./testfiles/test_result.ods'
    # cmd='soffice ./testfiles/test_result.xml'
    os.system(cmd)


def test_12():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test.ods')
    
    excel.setCellValue('Лист1', 10, 9, 1.99)
    excel.setCellValue('Лист1', 11, 9, '=SUM(I8:I10)')
    
    excel.saveAs('./testfiles/test_result.ods')
    excel.saveAs('./testfiles/test_result.xml')
    
    cmd = 'soffice ./testfiles/test_result.ods'
    # cmd='soffice ./testfiles/test_result.xml'
    os.system(cmd)


def test_13():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')
    if os.path.exists('./testfiles/test_result.ods'):
        os.remove('./testfiles/test_result.ods')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test.ods')
    excel.saveAs('./testfiles/test_result.ods')
    excel.saveAs('./testfiles/test_result.xml')

    cmd = 'libreoffice ./testfiles/test_result.ods'
    os.system(cmd)


def test_14():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/report/rep.xml')
    excel.saveAs('./testfiles/report/rep.ods')

    cmd = 'libreoffice ./testfiles/report/rep.ods'
    os.system(cmd)


def test_15():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/ttn/ttn_original.ods')
    # excel.load('./testfiles/ttn/ttn.xml')
    excel.saveAs('./testfiles/ttn/ttn_result.ods')
    excel.saveAs('./testfiles/ttn/ttn_result.xml')

    cmd = 'libreoffice ./testfiles/ttn/ttn_result.ods'
    os.system(cmd)


def test_16():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/imns/prib101.ods')
    excel.saveAs('./testfiles/imns/prib101_result.ods')

    cmd = 'libreoffice ./testfiles/imns/prib101_result.ods'
    os.system(cmd)


def test_17():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/bpr_735u.ods')
    excel.saveAs('./testfiles/bpr735u_result.ods')

    cmd = 'libreoffice ./testfiles/bpr735u_result.ods'
    os.system(cmd)


def test_18():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/break_page.ods')
    excel.saveAs('./testfiles/break_page_test.ods')

    cmd = 'libreoffice ./testfiles/break_page_test.ods'
    os.system(cmd)


def test_19():
    if os.path.exists('./log/virtual_excel.log'):
        os.remove('./log/virtual_excel.log')

    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/oc1.ods')
    excel.saveAs('./testfiles/oc1_test.ods')

    cmd = 'libreoffice ./testfiles/oc1_test.ods'
    os.system(cmd)


def test_ods():
    from . import v_excel
    
    excel = v_excel.iqVExcel()
    excel.load('./testfiles/ods/schm_19.ods')
    excel.saveAs('./testfiles/ods/result.ods')

    cmd = 'libreoffice ./testfiles/ods/result.ods'
    os.system(cmd)


def test_report():
    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('/home/xhermit/.icreport/rep_tmpl_report_result.xml')
    excel.saveAs('/home/xhermit/.icreport/rep_tmpl_report_result.ods')

    cmd = 'libreoffice /home/xhermit/.icreport/rep_tmpl_report_result.ods'
    os.system(cmd)


def test_worksheet_options():
    from . import v_excel

    # if os.path.exists('./log/virtual_excel.log'):
    #     os.remove('./log/virtual_excel.log')

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/month_params_report.ods')
    excel.saveAs('./testfiles/ods/result.ods')

    cmd = 'libreoffice ./testfiles/ods/result.ods'
    os.system(cmd)


def test_schm19():
    from . import v_excel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/schm/19.ods')
    excel.saveAs('./testfiles/schm/result_19.xml')


def test_save():
    try:
        from . import v_excel
    except ImportError:
        import icexcel

    excel = v_excel.iqVExcel()
    excel.load('./testfiles/test.ods')
    excel.saveAs('./testfiles/test.xml')


if __name__ == '__main__':
    import config
    from ic.log import log
    log.init(config)

    # test_oc1()
    # test_sum()
    # test_12()
    # test_5()
    # test_17()
    # test_ods()
    # test_worksheet_options()
    # test_report()
    # test_schm19()
    test_save()
