#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RTF file function.
"""

import copy

from iq.util import log_func

__version__ = (0, 0, 2, 1)


def getSD(var, val):
    return {'__variables__': {var: val}}


def findNextVariable(rep, pos=0):
    """
    Find next variable.
    
    :type rep: C{string}
    :param rep: Report template as text.
    :type pos: C{int}
    :param pos: Basis find position.
    :rtype: C{tuple}
    :return: Tuple:
        (start position of the replacement text,
        end position of the replacement text,
        variable name)
    """
    p1 = rep.find('#', pos)

    if p1 == -1:
        return -1, -1, None
    
    p2 = rep.find('#', p1+1)

    if p2 == -1:
        return -1, -1, None
    
    # Variable name
    var = rep[p1 + 1:p2]
    
    # Delete all unnecessary

    # Group end
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
        
        # Group end
        n2 = var.find('}', n1+1)
        
        if n2 == -1:
            s += var[n1 + 1:p2]
            break
        
        s += var[n1 + 1:n2]
        n1 = n2+1
        
    s = s.replace('\r', '').replace('\n', '')

    if ' ' in s:
        p1, p2, s = findNextVariable(rep, p1 + 1)

    return p1, p2, s


def getLoopList(data, lname):
    """
    Defines a list of items in a loop.
    """
    lst = list()
    if '__loop__' in data and lname in data['__loop__']:
        ls = data['__loop__'][lname]
        
        # We borrow the description of parent variables
        for el in ls:
        
            # We borrow a description of the cycles
            if '__loop__' in el:
                elm = {'__loop__': copy.copy(el['__loop__'])}
            else:
                elm = {'__loop__': dict()}
                if '__loop__' in data:
                    for lp, sp in data['__loop__'].items():
                        if lp != lname:
                            elm['__loop__'][lp] = copy.copy(sp)
            
            # We borrow the description of variables
            elm['__variables__'] = copy.copy(data['__variables__'])
            elm['__variables__'].update(el['__variables__'])
            
            # We borrow the description of the tables
            elm['__tables__'] = copy.copy(data['__tables__'])
            name_list = [x['__name__'] for x in elm['__tables__']]

            if '__tables__' in el:
                for tbl in el['__tables__']:
                    if '__name__' in tbl and not tbl['__name__'] in name_list:
                        elm['__tables__'].append(tbl)
            
            lst.append(elm)
        return lst
    return lst


def getTableTemplate(rep, pos):
    """
    Parsing a table template.
    """
    p2 = pos
    
    while 1:
        p1, p2, var = findNextVariable(rep, p2 + 1)
    
        if not var:
            break

        # Looking for group horses
        if var == '1D':
            break
        else:
            pass
            
    return pos, p2


def _genTable(table, templ):
    """
    Generates a table from a template and tabular data.
    """
    txt = ''
    for r in table['__data__']:
        repl_dict = dict()
        for indx, col in enumerate(table['__fields__']):
            repl_dict[col[0]] = str(r[indx])
            
        txt += parseRTF(None, templ, repl_dict)

    return txt


def doTableByName(data, templ, name):
    """
    Generate a table by name.
    """
    table = None
    
    for tbl in data['__tables__']:
        if tbl['__name__'] == name:
            return _genTable(tbl, templ)

    return ''


def doTableByIdx(data, templ, idx):
    """
    Generate a table by index.
    """
    if len(data['__tables__']) > idx:
        tbl = data['__tables__'][idx]
        return _genTable(tbl, templ)

    return ''


def parseRTF(data, rep, replace_dict=None, idx_loop=None, idx_key=None):
    """
    Parse RTF file data.
    """
    p2 = 0
        
    if not replace_dict:
        replace_dict = data['__variables__']

    if data and '__tables__' not in data:
        data['__tables__'] = []
        
    b_table_beg = False
    t_beg_tag = 0
    t_end_tag = 0
    t_name = None
    
    b_loop_beg = False
    l_beg_tag = 0
    l_end_tag = 0
    l_name = None

    indx = 0
    
    if idx_loop and idx_key:
        var_key = '%s_%s' % (idx_loop, idx_key)
    else:
        var_key = ''
    
    # Parse template
    while 1:
        p1, p2, var = findNextVariable(rep, p2 + 1)
    
        if not var:
            break
            
        if var[:2] == 'D1' and not b_loop_beg:
            b_table_beg = True
            t_beg_tag = p1
            t_end_tag = p2
            
            if var_key:
                t_name = var[3:] + '_' + idx_key
            else:
                t_name = var[3:]

        elif var[:4] == 'LOOP' and not b_loop_beg:
            b_loop_beg = True
            l_beg_tag = p1
            l_end_tag = p2
            l_name = var[5:]

        elif var[:7] == 'ENDLOOP':
            loop_name = var[8:]
            
            if loop_name == l_name:
                # Select the repeating part.
                templ = rep[l_end_tag+2:p1]
                txt = ''
                
                n = templ.find('}')
                # We remove the first group from the template
                if n != -1:
                    templ = templ[n+1:]
                
                n = templ.rfind('{')
                # We remove the last group from the template
                if n != -1:
                    templ = templ[:n]

                lst = getLoopList(data, l_name)
                txt = ''
                if lst:
                    for sp in lst:
                        txt += parseRTF(sp, templ)
                else:
                    # If the list is not defined,
                    # then start the generation to erase all tags from the text
                    txt += parseRTF({'__variables__': {}}, templ)
                    
                # Insert text
                if txt:
                    rep = rep[:l_beg_tag] + txt + rep[p2+1:]
                    p2 = l_beg_tag + 1
                    
                b_loop_beg = False
        
        elif var == '1D' and not b_loop_beg:
            # Select the tabular part
            templ = rep[t_end_tag+2:p1]
            txt = ''
            
            n = templ.find('}')
            # Remove the first group from the template
            if n != -1:
                templ = templ[n+1:]
            
            n = templ.rfind('{')
            # Remove the last group from the template
            if n != -1:
                templ = templ[:n]
            
            # Generate table
            if t_name:
                txt = doTableByName(data, templ, t_name)
            else:
                txt = doTableByIdx(data, templ, indx)
                indx += 1

            # Insert table
            rep = rep[:t_beg_tag] + txt + rep[p2+1:]
            p2 = t_beg_tag + 1
            b_table_beg = False

        # Insert variables
        elif not b_table_beg and not b_loop_beg:
            
            if var_key:
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
    Generate RTF report by template.

    :return: True/False.
    """
    rtf_file = None
    try:
        rtf_file = open(tmpl_filename, 'rt')
        rep = rtf_file.read()
        rtf_file.close()
    except:
        if rtf_file:
            rtf_file.close()
        log_func.fatal(u'Error read RTF report template file <%s>' % tmpl_filename)
        return False

    try:
        rep = parseRTF(data, rep)
    except:
        log_func.fatal(u'Error parse RTF data')
        return False

    rtf_file = None
    try:
        rtf_file = open(rep_filename, 'wt')
        rtf_file.write(rep)
        rtf_file.close()
    except:
        if rtf_file:
            rtf_file.close()
        log_func.fatal(u'Error write RTF report template file <%s>' % rep_filename)
        return False
    return True
