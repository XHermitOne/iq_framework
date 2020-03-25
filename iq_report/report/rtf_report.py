#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Заполнение rtf шаблона.
"""

import copy

__version__ = (0, 1, 1, 2)

tblDct = {'__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
          '__name__': 'P1',
          '__data__': [(1, 'лот 1.1', 200.0),
                       (2, 'лот 1.2', 210.0),
                       (3, 'лот 1.3', 220.0),
                       (4, 'лот 1.4', 300.0)]}

tblDct2 = {'__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
           '__name__': 'P2',
           '__data__': [(1, 'лот 2.1', 500.0),
                        (2, 'лот 2.2', 510.0),
                        (3, 'лот 2.3', 520.0)]}

tblDct3 = {'__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
           '__name__': 'P1',
           '__data__': [(1, 'лот 3.1', 200.0),
                        (2, 'лот 3.2', 210.0),
                        (3, 'лот 3.3', 220.0),
                        (4, 'лот 3.4', 300.0)]}

tblDct4 = {'__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
           '__name__': 'P2',
           '__data__': [(1, 'лот 4.1', 500.0),
                        (2, 'лот 4.2', 510.0),
                        (3, 'лот 4.3', 520.0)]}

LDct1 = {'__variables__': {'VAR_L': 'Слот 1'},
         '__tables__': [tblDct, tblDct2]}
LDct2 = {'__variables__': {'VAR_L': 'Слот 2'},
         '__tables__': [tblDct3, tblDct4]}
LDct3 = {'__variables__': {'VAR_L': 'Слот 3'}}


def getSD(var, val):
    return {'__variables__': {var: val}}


DataDct = {'__variables__': {'form_torg': '''Тип торгов
hjkfdshjkhjksfadhlkhfsa
sfdjhjkhfajkhfjdskhfhks
    GGGGGGGGGGGGGGGGGg
''',
                             'izveschen_url': 'www.abakan.ru',
                             'VAR_L_1': 'Слот 1',
                             'VAR_L_2': 'Слот 2',
                             'VAR_LG': 'Общий текст',
                             'name_torg': 'Имя торгов'},
           '__loop__': {'L': [LDct1, LDct2],
                        'I': [getSD('I', 1), getSD('I', 2), getSD('I', 3)],
                        'J': [getSD('J', 1), getSD('J', 2), getSD('J', 3)]},
           '__tables__': []}


def findNextVar(rep, pos=0):
    """
    Ищет следующую переменную.
    
    :type rep: C{string}
    :param rep: Шаблон.
    :type pos: C{int}
    :param pos: Позиция, с которой искать.
    :rtype: C{tuple}
    :return: Возвращает картеж. 1-й элемент начальная позиция текста замены;
        2-й элемент конечная позиция; 3-й элемент - имя переменной.
    """
    p1 = rep.find('#', pos)

    if p1 == -1:
        return -1, -1, None
    
    p2 = rep.find('#', p1+1)

    if p2 == -1:
        return -1, -1, None
    
    # --- Определяем имя переменной
    var = rep[p1+1:p2]
    
    # --- Выкидываем все лишнее
    
    # Ищем конец группы
    n2 = var.find('}')
        
    if n2 > -1:
        s = var[: n2]
    else:
        s = ''
        
    n1 = 0
    
    while 1:
        n1 = var.find(' ', n1)
        
        if n1 == -1:
            s = var
            break
        
        # Ищем конец группы
        n2 = var.find('}', n1+1)
        
        if n2 == -1:
            s += var[n1+1: p2]
            break
        
        s += var[n1+1: n2]
        n1 = n2+1
        
    s = s.replace('\r', '').replace('\n', '')

    if ' ' in s:
        p1, p2, s = findNextVar(rep, p1+1)

    return p1, p2, s


def getLoopList(data, lname):
    """
    Определяет список элементов в цикле.
    """
    lst = []
    if '__loop__' in data and lname in data['__loop__']:
        ls = data['__loop__'][lname]
        
        #   Заимствуем описание родительских переменных
        for el in ls:
        
            # Заимствуем описание циклов
            if '__loop__' in el:
                elm={'__loop__': copy.copy(el['__loop__'])}
            else:
                elm = {'__loop__': {}}
                if '__loop__' in data:
                    for lp, sp in data['__loop__'].items():
                        if lp != lname:
                            elm['__loop__'][lp] = copy.copy(sp)
            
            # Заимствуем описание переменных
            elm['__variables__'] = copy.copy(data['__variables__'])
            elm['__variables__'].update(el['__variables__'])
            
            # Заимствуем описание таблиц
            elm['__tables__'] = copy.copy(data['__tables__'])
            nmLst = [x['__name__'] for x in elm['__tables__']]

            if '__tables__' in el:
                for tbl in el['__tables__']:
                    if '__name__' in tbl and not tbl['__name__'] in nmLst:
                        elm['__tables__'].append(tbl)
            
            lst.append(elm)
            
        return lst
    
    return lst


def getTableTemplate(rep, pos):
    """
    """
    # --- Разбираем шаблон таблицы
    p2 = pos
    
    while 1:
        p1, p2, var = findNextVar(rep, p2+1)
    
        if not var:
            break

        #   Ищем коней кгруппы
        if var == '1D':
            break
        else:
            pass
            
    return pos, p2


repTest = '''
    #Variable1#
    #Variblee2#
'''


def _gen_table(table, templ):
    """
    Генерирует таблицу по шаблону и табличным данным.
    """
    txt = ''
    for r in table['__data__']:
        replDct = {}
        for indx, col in enumerate(table['__fields__']):
            replDct[col[0]] = str(r[indx])
            
        txt += parse_rtf(None, templ, replDct)

    return txt


def doTableByName(data, templ, name):
    """
    Генерация по имени таблицы.
    """
    table = None
    
    for tbl in data['__tables__']:
        if tbl['__name__'] == name:
            return _gen_table(tbl, templ)

    return ''


def doTableByIdx(data, templ, idx):
    """
    Генерация по индексу таблицы.
    """
    if len(data['__tables__']) > idx:
        tbl = data['__tables__'][idx]
        return _gen_table(tbl, templ)

    return ''


def parse_rtf(data, rep, replace_dict=None, idx_loop=None, idx_key=None):
    """
    """
    p2 = 0
        
    if not replace_dict:
        replace_dict = data['__variables__']

    if data and '__tables__' not in data:
        data['__tables__'] = []
        
    bTableBeg = False
    tBegTag = 0
    tEndTag = 0
    tName = None
    
    bLoopBeg = False
    lBegTag = 0
    lEndTag = 0
    lName = None

    indx = 0
    
    if idx_loop and idx_key:
        varKey = '%s_%s' % (idx_loop, idx_key)
    else:
        varKey = ''
    
    # --- Разбираем шаблон
    while 1:
        p1, p2, var = findNextVar(rep, p2+1)
    
        if not var:
            break
            
        if var[:2] == 'D1' and not bLoopBeg:
            bTableBeg = True
            tBegTag = p1
            tEndTag = p2
            
            if varKey:
                tName = var[3:] +'_' + idx_key
            else:
                tName = var[3:]

        elif var[:4] == 'LOOP' and not bLoopBeg:
            bLoopBeg = True
            lBegTag = p1
            lEndTag = p2
            lName = var[5:]

        elif var[:7] == 'ENDLOOP':
            loop_name = var[8:]
            
            if loop_name == lName:
                # Выделяем повторяющуюся часть
                templ = rep[lEndTag+2:p1]
                txt = ''
                
                n = templ.find('}')
                # Убираем первую группу из шаблона
                if n != -1:
                    templ = templ[n+1:]
                
                n = templ.rfind('{')
                # Убираем последнюю группу из шаблона
                if n != -1:
                    templ = templ[:n]

                lst = getLoopList(data, lName)
                txt = ''
                if lst:
                    for sp in lst:
                        txt += parse_rtf(sp, templ)
                else:
                    # Если список не определен просто запустить генерацию
                    # чтобы стереть все теги из текста
                    txt += parse_rtf({'__variables__': {}}, templ)
                    
                # Вставляем текст
                if txt:
                    rep = rep[:lBegTag] + txt + rep[p2+1:]
                    p2 = lBegTag + 1
                    
                bLoopBeg = False
        
        elif var == '1D' and not bLoopBeg:
            # Выделяем табличную часть
            templ = rep[tEndTag+2:p1]
            txt = ''
            
            n = templ.find('}')
            # Убираем первую группу из шаблона
            if n != -1:
                templ = templ[n+1:]
            
            n = templ.rfind('{')
            # Убираем последнюю группу из шаблона
            if n != -1:
                templ = templ[:n]
            
            # Генерируем таблицу
            if tName:
                txt = doTableByName(data, templ, tName)
            else:
                txt = doTableByIdx(data, templ, indx)
                indx += 1

            # Вставляем таблицу
            rep = rep[:tBegTag] + txt + rep[p2+1:]
            p2 = tBegTag + 1
            bTableBeg = False

        #   Вставляем переменные
        elif not bTableBeg and not bLoopBeg:
            
            if varKey:
                v = var+'_'+str(idx_key)
                if v not in replace_dict.keys():
                    v = var
            else:
                v = var
                
            if v in replace_dict.keys():
                replTxt = str(replace_dict[v]).replace('\n', '\line ')
                rep = rep[:p1] + replTxt + rep[p2+1:]
                p2 = p1 + len(str(replace_dict[v])) + 1
            else:
                rep = rep[:p1] + rep[p2+1:]
                p2 = p1 + 1
    
    return rep


def genRTFReport(data, rep_filename, tmpl_filename):
    """
    Создает rtf отчет по шаблону.
    """
    f = open(tmpl_filename, 'rt')
    rep = f.read()
    f.close()

    rep = parse_rtf(data, rep)
    
    f = open(rep_filename, 'wt')
    f.write(rep)
    f.close()


def test():
    genRTFReport(DataDct, 'V:/pythonprj/ReportRTF/IzvTEST.rtf', 'V:/pythonprj/ReportRTF/Blank_Izv.rtf')


if __name__ == '__main__':
    test()
