#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iqFramework installer - application project installation program.

Command line options:

    python3 install_app_linux.py <Launch parameters>

Launch parameters:

    [Help and debugging]
        --help|-h|-?        Print help
        --version|-v        Print version
        --debug|-d          Set debug mode
"""

import sys
import getopt
import os
import os.path
import subprocess
import getpass
import datetime
import sysconfig
import glob
import tempfile
import time

__version__ = (0, 1, 1, 1)

DEBUG_MODE = True

ROOT_USERNAME = None
ROOT_PASSWORD = None

DEFAULT_MNT_SERVER = '10.0.0.26'
DEFAULT_NETWORK_RESOURCE_NAME = 'defis'
DEFAULT_MNT_PATH = '/mnt/defis'
RC_LOCAL_FILENAME = '/etc/rc.local'

REPLACE_WAIT_NETWORK_UP_SIGNATURE = '# By default this script does nothing.'
WAIT_NETWORK_UP = 'until ping -nq -c3 %s; do sleep 1; done'
RC_LOCAL_EXIT_CMD = os.linesep + 'exit 0'
MOUNT_CMD_FMT = 'mount --types nfs --options vers=4 %s:/%s %s'
WAIT_MOUNT_CMD_FMT = '((%s); mount --types nfs --options vers=4 %s:/%s %s)&'

DEFAULT_RC_LOCAL_CONTENT = '''#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

exit 0

'''

IQ_FRAMEWORK_FOLDER_NAME = 'iq_framework'
IQ_FOLDER_NAME = 'iq'
REQUIREMENTS_FILENAME = 'requirements.sh'


CONSOLE = None

HOME_PATH = os.environ['HOME'] if 'HOME' in os.environ else (os.environ.get('HOMEDRIVE',
                                                                            '') + os.environ.get('HOMEPATH', ''))
TITLE = 'iqFramework application installer for Ubuntu Linux'

DEFAULT_MENU_SELECTION_CHAR = '==>'

EXCEPTION_EXTRA_LINE_COUNT = 8

AUTHOR_LOGO = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⢻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣄⣀⣹⣷⣶⣾⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣀⣈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣀⡀⠈⢻⣿⣿⣿⣿⣿⣿⡿⡛⡛⢏⠱⡀⢂⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣶⣬⣻⣿⣿⠿⠿⠹⣄⠀⠈⢦⡀⢱⠈⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣴⣦⣤⣽⣿⣿⣿⡿⠯⠛⠻⢧⣀⠀⠀⠙⢦⠀⠱⡌⣷⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠐⠛⠛⠻⠿⣿⣿⣿⡟⠿⢭⣀⡀⠀⠀⠈⠑⠦⡀⠀⢳⡀⡘⣿⣿⣿⣦⠂⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣠⣶⣶⡚⠻⣶⣄⣀⠀⠄⡉⠓⢦⣄⣢⣀⣸⣦⣮⣿⣾⣿⣿⣿⣯⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣾⣿⣿⠛⠿⠤⠀⠤⢄⣉⠓⠲⢾⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀
⠀⠀⣴⣿⣿⡿⠿⠿⣿⣦⡤⠤⠤⠤⠖⠒⠛⣋⣉⣩⣭⣿⣿⣿⣿⣿⣿⣿⡿⡿⢿⡅⠀⠀⠀⠀⠀
⠀⠠⠋⠀⠀⣀⣶⣿⣿⣿⣶⣄⣠⣤⣶⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⢷⢧⣤⣤⣤⣤⡄⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⠏⢰⣿⡿⢿⣿⠋⠁⠎⢸⠟⣛⣉⠀⢇⠀⠀⠀⠀⠀
⠀⠀⢰⣿⣿⡿⠛⠉⣩⣿⡿⠏⠀⣽⣿⣿⡇⢀⣾⡏⠀⣰⡏⢁⠌⢠⣿⣞⠙⠿⠿⣞⠀⠀⠀⠀⠀
⠀⠀⠀⠛⠀⠀⠀⣸⣿⣿⡃⠀⠀⣿⣿⣿⣧⣾⣿⣿⣿⠟⢠⠊⣠⣾⣿⣿⣿⠶⠄⠘⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⡇⠘⡀⢹⣿⣿⣿⣿⣿⡿⢁⠔⢁⣴⣿⣿⣿⣿⠇⠘⡿⠶⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⠄⠡⠈⣿⣿⣿⣿⣿⣀⣡⣴⣿⣿⣿⣿⣿⣷⣖⣒⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠇⠀⠠⣿⣿⣿⡿⣿⡿⣿⣿⣿⣿⡿⣿⣿⣯⣸⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⡈⢳⣤⡙⠻⣿⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠙⠄⠙⢿⣦⣉⠒⢄⠀⠀⠀XHermitOne@gmail.com
'''

NOT_APPLICATION_FOLDER_NAMES = ('iq', 'ide',
                                'iq_report','iq_scanner',
                                'locale', '.git', '.idea', '__pycache__')

IQ_FRAMEWORK_LOGO = '''
 _     _____                                 _
|_|___|   __|___ ___ _____ ___ _ _ _ ___ ___| |_
| | . |   __|  _| .'|     | -_| | | | . |  _| '_|
|_|_  |__|  |_| |__,|_|_|_|___|_____|___|_| |_,_|
    |_|
'''


def printStyledText(text, style=None):
    """
    Печать в консоли стилизованного текста.

    :param text: Текст.
    :param style: Стиль текста.
    """
    if not isinstance(text, str):
        text = str(text)

    global CONSOLE
    if CONSOLE is not None:
        CONSOLE.print(text, style=style)
    else:
        print(text)


def debug(message=u'', is_force_print=False):
    """
    Печать отладочной информации.

    :param message: Сообщение.
    :param is_force_print: Печать не зависимо от режима отладки.
    """
    if not isinstance(message, str):
        message = str(message)

    if DEBUG_MODE or is_force_print:
        printStyledText(message, style='blue')


def info(message=u'', is_force_print=False):
    """
    Печать информации.

    :param message: Сообщение.
    :param is_force_print: Печать не зависимо от режима отладки.
    """
    if not isinstance(message, str):
        message = str(message)

    if DEBUG_MODE or is_force_print:
        printStyledText(message, style='green')


def warning(message=u'', is_force_print=False):
    """
    Печать предупреждающей информации.

    :param message: Сообщение.
    :param is_force_print: Печать не зависимо от режима отладки.
    """
    if not isinstance(message, str):
        message = str(message)

    if DEBUG_MODE or is_force_print:
        printStyledText(message, style='yellow')


def error(message=u'', is_force_print=True):
    """
    Печать ошибочной информации.

    :param message: Сообщение.
    :param is_force_print: Печать не зависимо от режима отладки.
    """
    if not isinstance(message, str):
        message = str(message)

    if DEBUG_MODE or is_force_print:
        printStyledText(message, style='red')


def fatal(message=u'', is_force_print=True):
    """
    Печать информации системной ошибки.

    :param message: Сообщение.
    :param is_force_print: Печать не зависимо от режима отладки.
    """
    global CONSOLE
    if DEBUG_MODE or is_force_print:
        error(message, is_force_print=is_force_print)
        if CONSOLE is not None:
            CONSOLE.print_exception(extra_lines=EXCEPTION_EXTRA_LINE_COUNT, show_locals=True)


def getTextTitle():
    """
    Get full title text.

    :return: Title text.
    """
    title_text = '%s %s' % (TITLE, '.'.join([str(sign) for sign in __version__]))
    return title_text


def clearScreen():
    """
    Clear console.

    :return: True/False.
    """
    global CONSOLE
    if CONSOLE is not None:
        CONSOLE.clear()
        return True
    return False


def printTitle(title_text=None, style=None, auto_clear=True):
    """
    Print title.

    :param title_text: Title text. If not specified, it is used by default.
    :param style: Title style.
    :param auto_clear: Clear console screen?
    :return: True/False.
    """
    global CONSOLE
    if CONSOLE is None:
        return False

    import rich

    if title_text is None:
        title_text = getTextTitle()
    if auto_clear:
        clearScreen()

    grid = rich.table.Table.grid(expand=True)
    grid.add_column(justify='left', ratio=1)
    grid.add_column(justify='right')
    grid.add_row('[b]%s[/b]' % title_text,
                 datetime.datetime.now().ctime().replace(':', '[blink]:[/]'))
    panel = rich.panel.Panel(grid, style='green')
    rich.print(panel)
    return True


def initConsole():
    """
    Init console object.
    :return: Console object.
    """
    global CONSOLE
    if CONSOLE is None:
        import rich.console
        CONSOLE = rich.console.Console()
    return CONSOLE

def main(argv):
    """
    Main function.

    :param argv: List of command line parameters.
    """
    global DEBUG_MODE

    try:
        options, args = getopt.getopt(argv, 'h?vd',
                                      ['help', 'version', 'debug', 'author'])
    except getopt.error as msg:
        print(str(msg))
        print(__doc__)
        sys.exit(2)

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            print(__doc__)
            sys.exit(0)
        elif option in ('-v', '--version'):
            txt_version = '.'.join([str(ver) for ver in __version__])
            print('iqFramework installer version: %s' % txt_version)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            DEBUG_MODE = True
            print('Set debug mode')
        elif option == '--author':
            print(AUTHOR_LOGO)
            sys.exit(0)
        else:
            print(u'Error. An unprocessed command line parameter <%s>' % option)

    try:
        run()
    except:
        print('Error:')
        raise


def getRootUsernamesLinux():
    """
    Get system administrator usernames for Linux.
    :return: Username list.
    """
    usernames = list()
    try:
        if os.path.exists('/etc/group'):
            out_txt = subprocess.getoutput('cat /etc/group | grep sudo')
            out_lines = out_txt.strip().split('\n')
            usernames = [line.split(':')[-1] for line in out_lines]
        else:
            print(u'Not found /etc/group file')
    except:
        print(u'Error get system administartor usernames for Linux')
    return usernames


def getRootUsername():
    """
    Get root user name.
    :return: Root user name.
    """
    root_usernames = getRootUsernamesLinux()
    if len(root_usernames) == 0:
        print(u'Not found root user')
    elif len(root_usernames) > 1:
        print(u'Found several root users %s. Return first' % str(root_usernames))
        return root_usernames[0]
    elif len(root_usernames) == 1:
        return root_usernames[0]
    return None


def getUsernamesLinux():
    """
    Get usernames for Linux.
    :return: Username list.
    """
    usernames = list()
    try:
        if os.path.exists('/etc/passwd'):
            records = [line.split(':') for line in open('/etc/passwd').readlines()]
            # UID--------------------------------------------------------V
            usernames = [record[0] for record in records if 1000 <= int(record[2]) < 65534]
        else:
            warning('Not found /etc/passwd file')
    except:
        fatal('Error get usernames for Linux')
    return usernames


def installAptPackage(root_username=None, root_password=None, *package_names):
    """
    Install packages by APT.

    :param root_username: Root username.
    :param root_password: Root password.
    :param package_names: Package names.
    """
    if root_username is None:
        global ROOT_USERNAME
        root_username = ROOT_USERNAME
    if root_password is None:
        global ROOT_PASSWORD
        root_password = ROOT_PASSWORD

    for package_name in package_names:
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= apt install --assume-yes {package_name}"'
        os.system(cmd)

def installPipPackage(root_username=None, root_password=None, *package_names):
    """
    Install packages by PIP3.

    :param root_username: Root username.
    :param root_password: Root password.
    :param package_names: Package names.
    """
    if root_username is None:
        global ROOT_USERNAME
        root_username = ROOT_USERNAME
    if root_password is None:
        global ROOT_PASSWORD
        root_password = ROOT_PASSWORD

    for package_name in package_names:
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= pip3 install --break-system-packages {package_name}"'
        os.system(cmd)


def saveTextFile(txt_filename, txt='', rewrite=True):
    """
    Save text file.

    :param txt_filename: Text file name.
    :param txt: Body text file as unicode.
    :param rewrite: Rewrite file if it exists?
    :return: True/False.
    """
    if not isinstance(txt, str):
        txt = str(txt)

    file_obj = None
    try:
        if rewrite and os.path.exists(txt_filename):
            os.remove(txt_filename)
            info(f'Remove file <{txt_filename}>')
        if not rewrite and os.path.exists(txt_filename):
            warning(f'File <{txt_filename}> not saved')
            return False

        file_obj = open(txt_filename, 'wt')
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        error(f'Save text file <{txt_filename}> error')
        raise
    return False


def loadTextFile(txt_filename):
    """
    Load from text file.

    :param txt_filename: Text file name.
    :return: File text or empty text if error.
    """
    if not os.path.exists(txt_filename):
        warning(f'File <{txt_filename}> not found')
        return ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'rt')
        txt = file_obj.read()
        file_obj.close()
    except:
        if file_obj:
            file_obj.close()
        error(f'Load text file <{txt_filename}> error')
        return ''

    return txt


def appendTextFile(txt_filename, txt, cr=None):
    """
    Add lines to text file.
    If the file does not exist, then the file is created.

    :param txt_filename: Text filename.
    :param txt: Added text.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    if not isinstance(txt, str):
        txt = str(txt)

    txt_filename = os.path.normpath(txt_filename)

    if not os.path.exists(txt_filename):
        cr = ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'at')
        file_obj.write(cr + txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        error(f'Error append to text file <{txt_filename}>')
        raise
    return False


def replaceTextFile(txt_filename, src_text, dst_text, auto_add=True, cr=None):
    """
    Replacing a text in a text file.

    :param txt_filename: Text filename.
    :param src_text: Source text.
    :param dst_text: Destination text.
    :param auto_add: A flag to automatically add a new line.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            file_obj.close()
            txt = txt.replace(src_text, dst_text)
            if auto_add and (dst_text not in txt):
                txt += cr
                txt += dst_text
                info(f'Text file append <{dst_text}> in <{txt_filename}>')
            file_obj = None
            file_obj = open(txt_filename, 'wt')
            file_obj.write(txt)
            file_obj.close()
            file_obj = None
            return True
        except:
            if file_obj:
                file_obj.close()
            error(f'Error replace in text file <{txt_filename}>')
            raise
    else:
        warning(f'Text file <{txt_filename}> not exists')
    return False


def isInTextFile(txt_filename, find_text):
    """
    Is there text in a text file?

    :param txt_filename: Text filename.
    :param find_text: Find text.
    :return: True/False.
    """
    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            result = find_text in txt
            file_obj.close()
            file_obj = None
            return result
        except:
            if file_obj:
                file_obj.close()
            error(f'Error find <{find_text}> in text file <{txt_filename}>')
            raise
    else:
        warning(f'Text file <{txt_filename}> not exists')
    return False


def generateTextFile(txt_template_filename, txt_output_filename, context=None, output_encoding=None):
    """
    Generation of a text file from a template file.

    :param txt_template_filename: Template is a text file.
    :param txt_output_filename: Name the output text file.
    :param context. Context.
        Any dictionary structure can be used as a context.
    :param output_encoding: The code page of the resulting file.
        If not specified, then the code page remains the same as the template.
    :return: True - generation was successful, False - generation error.
    """
    if context is None:
        context = dict()

    template_file = None
    output_file = None

    template_filename = os.path.abspath(txt_template_filename)
    if not os.path.exists(template_filename):
        warning(f'Template file <{template_filename}> not found')
        return False

    # Read template file
    try:
        template_file = open(template_filename, 'r')
        template_txt = template_file.read()
        template_file.close()
    except:
        if template_file:
            template_file.close()
        error(f'Read error template file <{template_filename}>')
        return False

    # Generate text
    try:
        import jinja2
        template = jinja2.Template(template_txt)
        gen_txt = template.render(**context)
    except:
        error(f'Error generate text <{template_txt}>')
        gen_txt = u''

    # Write output file
    output_filename = os.path.abspath(txt_output_filename)
    try:
        output_path = os.path.dirname(output_filename)
        if not os.path.exists(output_path):
            info(f'Create directory <{output_path}>')
            os.makedirs(output_path)

        output_file = open(output_filename, 'w+')
        output_file.write(gen_txt)
        output_file.close()
        return os.path.exists(output_filename)
    except:
        if output_file:
            output_file.close()
        error(f'Write error text file <{output_filename}>')
    return False


def mountFrameworkNetworkResource(mnt_path=DEFAULT_MNT_PATH, root_username=None, root_password=None):
    """
    Mount framework network resource.
    :return: Mount path.
    """
    global CONSOLE
    if CONSOLE is None:
        return None
    if root_username is None:
        global ROOT_USERNAME
        root_username = ROOT_USERNAME
    if root_password is None:
        global ROOT_PASSWORD
        root_password = ROOT_PASSWORD

    mnt_path = CONSOLE.input(f'[green]Input framework mount path:[/] (Default [bold cyan]{mnt_path}[/]): ') or mnt_path
    server = CONSOLE.input(f'[green]Input server:[/] (Default [bold cyan]{DEFAULT_MNT_SERVER}[/]): ') or DEFAULT_MNT_SERVER
    share_name = CONSOLE.input(f'[green]Input share:[/] (Default [bold cyan]{DEFAULT_NETWORK_RESOURCE_NAME}[/]): ') or DEFAULT_NETWORK_RESOURCE_NAME

    if not os.path.exists(mnt_path):
        info(f'Make directory <{mnt_path}>')
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= mkdir {mnt_path}"'
        os.system(cmd)
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt=  chmod 777 {mnt_path}"'
        os.system(cmd)

    if os.path.exists(mnt_path) and (not os.listdir(mnt_path)):
        mount_cmd = MOUNT_CMD_FMT % (server, share_name, mnt_path)
        info(f'Mount network resource <{mnt_path} : {mount_cmd}>')
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= {mount_cmd}"'
        os.system(cmd)

    if not os.path.exists(RC_LOCAL_FILENAME):
        info(f'Create <{RC_LOCAL_FILENAME}> file')
        tmp_rc_local_filename = os.path.join(tempfile.gettempdir(), os.path.basename(RC_LOCAL_FILENAME))
        saveTextFile(txt_filename=tmp_rc_local_filename, txt=DEFAULT_RC_LOCAL_CONTENT)
        # Copy rc.local file
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= cp {tmp_rc_local_filename} {RC_LOCAL_FILENAME}"'
        os.system(cmd)
        if os.path.exists(RC_LOCAL_FILENAME):
            # Set permissions
            cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= chmod 777 {RC_LOCAL_FILENAME}"'
            os.system(cmd)

    mount_cmd_enabled = WAIT_MOUNT_CMD_FMT % (WAIT_NETWORK_UP % server, server, share_name, mnt_path)

    mount_cmd_disabled = '# ' + mount_cmd_enabled
    mount_cmd_disabled2 = '#' + mount_cmd_enabled
    if isInTextFile(RC_LOCAL_FILENAME, mount_cmd_disabled):
        replaceTextFile(RC_LOCAL_FILENAME, mount_cmd_disabled, mount_cmd_enabled)
        info(f'Automatic resource mounting is enabled <{mount_cmd_enabled}>')
    elif isInTextFile(RC_LOCAL_FILENAME, mount_cmd_disabled2):
        replaceTextFile(RC_LOCAL_FILENAME, mount_cmd_disabled2, mount_cmd_enabled)
        info(f'Automatic resource mounting is enabled <{mount_cmd_enabled}>')
    elif isInTextFile(RC_LOCAL_FILENAME, mount_cmd_enabled):
        info(f'Automatic resource mounting is already enabled <{mount_cmd_enabled}>')
    else:
        commands = os.linesep + mount_cmd_enabled + os.linesep + RC_LOCAL_EXIT_CMD
        replaceTextFile(RC_LOCAL_FILENAME, RC_LOCAL_EXIT_CMD, commands)
        info(f'Automatic resource mounting is enabled <{mount_cmd_enabled}>')

    if os.path.exists(mnt_path) and os.path.exists(RC_LOCAL_FILENAME):
        return mnt_path
    return None


def saveIqPthFile(mnt_path, root_username, root_password):
    """
    Create iq.pth file for import.

    :param mnt_path:
    :return: True/False.
    """
    if mnt_path is None or not os.path.exists(mnt_path):
        return False
    iq_framework_path = os.path.join(mnt_path, IQ_FRAMEWORK_FOLDER_NAME)
    if os.path.exists(iq_framework_path):
        tmp_iq_pth_filename = os.path.join(tempfile.gettempdir(), 'iq.pth')
        saveTextFile(txt_filename=tmp_iq_pth_filename, txt=iq_framework_path)
        iq_pth_filename = os.path.join(sysconfig.get_paths()['purelib'], 'iq.pth')
        cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= cp {tmp_iq_pth_filename} {iq_pth_filename}"'
        os.system(cmd)
        # Test iq import
        try:
            import iq
            info(f'Import iq: <{iq.__file__}>')
            return True
        except ImportError:
            error('Import error <iq>')
    return False

def installRequirementsSH(sh_filename, root_username=None, root_password=None):
    """
    Install requirements.sh file.
    :param sh_filename: Shell template filename.
    :return: True/False.
    """
    if not os.path.exists(sh_filename):
        error(f'File <{sh_filename}> not found')
        return False

    if root_username is None:
        global ROOT_USERNAME
        root_username = ROOT_USERNAME
    if root_password is None:
        global ROOT_PASSWORD
        root_password = ROOT_PASSWORD

    # Generate script
    import jinja2
    import distro

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(sh_filename)))
    template = env.get_template(os.path.basename(sh_filename))
    variables = dict(DISTRO_ID=distro.id(), DISTRO_VERSION=distro.version())
    script = template.render(**variables)

    # Execute script
    for line in script.split(os.linesep):
        cmd = line.strip()
        if not cmd or cmd.startswith('#'):
            continue
        elif not cmd.startswith('sudo '):
            info(f'Execute command <{cmd}>')
            os.system(cmd)
        elif cmd.startswith('sudo '):
            info(f'Execute command <{cmd}>')
            new_cmd = f'echo {root_password} | su {root_username} --login --session-command "{cmd}"'
            os.system(new_cmd)


def selectApplication(iq_framework_path):
    """
    Select application for install.
    :param iq_framework_path: iqFramework path.
    :return: Application path or None if Exit selected.
    """
    if not os.path.exists(iq_framework_path):
        error(f'Not found iqFramework path <{iq_framework_path}>')
        return None
    app_paths = [os.path.join(iq_framework_path, folder_name) for folder_name in os.listdir(iq_framework_path) if folder_name not in NOT_APPLICATION_FOLDER_NAMES]
    app_paths = [folder_path for folder_path in app_paths if os.path.isdir(folder_path)]

    import rich_menu
    import importlib.util

    menuitems = list()
    for app_path in app_paths:
        name = os.path.basename(app_path)
        init_filename = os.path.join(app_path, '__init__.py')
        spec = importlib.util.spec_from_file_location('iq_app', init_filename)
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        # debug(f'Package {package}:')
        # debug(f'{package.__doc__}')
        description = package.__doc__.strip().split(os.linesep)[0] if package.__doc__ else ''
        menuitems.append(f'{name} : {description}')
    menuitems.append('Exit')

    menu = rich_menu.Menu(*menuitems,
                          color='green',
                          title=u'iqFramework applications',
                          align='left',
                          selection_char=DEFAULT_MENU_SELECTION_CHAR,
                          highlight_color='bold green')
    menu.ask(screen=False)
    if menu.index == (len(menuitems) - 1):
        # Select EXIT
        return None
    return app_paths[menu.index]


def installDesktop(app_path, root_username=None, root_password=None):
    """
    Install *.desktop files for all users.
    :param app_path: Application path.
    :return: True/False.
    """
    if not os.path.exists(app_path):
        error(f'Application path <{app_path}> not found')
        return False

    desktop_pattern = os.path.join(app_path, '*.desktop')
    desktop_filenames = glob.glob(desktop_pattern)

    if root_username is None:
        global ROOT_USERNAME
        root_username = ROOT_USERNAME
    if root_password is None:
        global ROOT_PASSWORD
        root_password = ROOT_PASSWORD

    # Generate script
    import jinja2
    import distro

    variables = dict(DISTRO_ID=distro.id(), DISTRO_VERSION=distro.version(), APP_PATH=app_path)

    for desktop_filename in desktop_filenames:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(app_path))
        template = env.get_template(os.path.basename(desktop_filename))
        desktop_content = template.render(**variables)

        # Save desktop file
        for username in getUsernamesLinux():
            info(f'Install application <{os.path.basename(app_path)}> for user <{username}>')
            tmp_desktop_filename = os.path.join(tempfile.gettempdir(),
                                                os.path.basename(desktop_filename))
            dst_applications_path =os.path.join('/home', username,
                                                '.local', 'share', 'applications')
            dst_desktop_filename = os.path.join(dst_applications_path,
                                                os.path.basename(desktop_filename))

            saveTextFile(txt_filename=tmp_desktop_filename, txt=desktop_content)
            # Copy desktop file
            info(f'Copy desktop file <{tmp_desktop_filename}> - > <{dst_desktop_filename}>')
            cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= cp {tmp_desktop_filename} {dst_applications_path}"'
            os.system(cmd)
            # Set permissions
            info(f'Set permission desktop file <{dst_desktop_filename}>')
            cmd = f'echo {root_password} | su {root_username} --login --session-command "echo {root_password} | sudo --stdin --prompt= chmod +rx {dst_desktop_filename}"'
            os.system(cmd)
    return True


def run():
    """
    Run install.
    :return:
    """
    global ROOT_USERNAME
    global ROOT_PASSWORD

    # 1. Get root username
    ROOT_USERNAME = getRootUsername()
    if ROOT_USERNAME:
        # 2. Get root password
        ROOT_PASSWORD = getpass.getpass(f'Get password for <{ROOT_USERNAME}> user: ')
        # 3. Install basic packages
        installAptPackage(ROOT_USERNAME, ROOT_PASSWORD, 'python3-pip', 'nfs-common')
        installPipPackage(ROOT_USERNAME, ROOT_PASSWORD, 'rich', 'rich-menu', 'distro', 'jinja2')
        # 4. Control mode
        initConsole()
        clearScreen()
        printTitle()
        try:
            # 5. Mount network resource
            mnt_path = mountFrameworkNetworkResource()
            if mnt_path is None:
                error('Error mount network resource')
                return
            # 6. Save PTH file
            if not saveIqPthFile(mnt_path, root_username=ROOT_USERNAME, root_password=ROOT_PASSWORD):
                error('Error save iq.pth file for import')
                return
            # 7. Install packages for iq
            iq_framework_path = os.path.join(mnt_path, IQ_FRAMEWORK_FOLDER_NAME)
            iq_requirements_filename = os.path.join(iq_framework_path, IQ_FOLDER_NAME, REQUIREMENTS_FILENAME)
            installRequirementsSH(iq_requirements_filename, root_username=ROOT_USERNAME, root_password=ROOT_PASSWORD)
            # 8. Select application for install
            # time.sleep(1)
            clearScreen()
            printTitle()
            app_path = selectApplication(iq_framework_path)
            # 9. Install packages for application
            if app_path is not None:
                app_requirements_filename = os.path.join(app_path, REQUIREMENTS_FILENAME)
                installRequirementsSH(app_requirements_filename, root_username=ROOT_USERNAME, root_password=ROOT_PASSWORD)
                # 10. Get DESKTOP file
                installDesktop(app_path=app_path, root_username=ROOT_USERNAME, root_password=ROOT_PASSWORD)

            info(IQ_FRAMEWORK_LOGO)
        except:
            fatal('Error installation')


if __name__ == '__main__':
    main(sys.argv[1:])