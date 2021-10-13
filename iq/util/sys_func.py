#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System functions module.
"""

import sys
import socket
import platform
import os
import subprocess
import getpass

try:
    # For Python 2
    import commands as get_procesess_module
except ImportError:
    # For Python 3
    import subprocess as get_procesess_module

from . import log_func

__version__ = (0, 0, 1, 1)

# System line separator
UNIX_LINESEP = '\n'
WIN_LINESEP = '\r\n'
LINE_SEPARATORS = (WIN_LINESEP, UNIX_LINESEP)

# Current system line separator
LINESEP = os.linesep


def getComputerName():
    """
    Get computer name.

    :return: Computer name or None if error.
    """
    comp_name = socket.gethostname()
    if isWindowsPlatform():
        from . import str_func
        comp_name = str_func.rus2lat(comp_name)
    return comp_name


def getPlatform():
    """
    Get platform name.
    """
    return platform.uname()[0].lower()


def isWindowsPlatform():
    return getPlatform() == 'windows'


def isLinuxPlatform():
    return getPlatform() == 'linux'


def getActiveProcessCount(find_process):
    """
    The number of active processes running.

    :param find_process: The search string of the process.
    :return: The number of processes found.
    """
    processes_txt = get_procesess_module.getoutput('ps -eo pid,cmd')
    processes = processes_txt.strip().split('\n')
    find_processes = [process for process in processes if find_process in process]
    # log_func.debug(u'Find processes %s' % str(find_processes))
    return len(find_processes)


def isActiveProcess(find_process):
    """
    Check for the existence of an active executable process.

    :param find_process: The search string of the process.
    :return: True - process exists / False - process not found.
    """
    return getActiveProcessCount(find_process) >= 1


def exitForce():
    """
    Forced closing of the program.
    """
    sys.exit(0)


def beep(count=1):
    """
    Play system sound.

    :param count: The number of repetitions.
    """
    for i in range(count):
        print('\a')


def getSystemUsername():
    """
    Get system username.
    """
    if 'USERNAME' in os.environ:
        return os.environ['USERNAME']
    return os.environ.get('USER', None)


def isSystemRoot():
    """
    System username is root?

    :return: True - root/ False - not root.
    """
    return getSystemUsername() == 'root'


def getLocalIP():
    """
    Get local IP address.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except:
        log_func.fatal(u'Error get local IP')
    return None


def getOSVersion():
    """
    Get OS version.
    """
    try:
        if isLinuxPlatform():
            import distro
            return distro.linux_distribution()
        elif isWindowsPlatform():
            try:
                cmd = 'wmic os get Caption'
                p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
            except FileNotFoundError:
                log_func.error('WMIC.exe was not found... Make sure \'C:\Windows\System32\wbem\' is added to PATH')
                return None

            stdout, stderror = p.communicate()

            output = stdout.decode('UTF-8', 'ignore')
            lines = output.split('\r\r')
            lines = [line.replace('\n', '').replace('  ', '') for line in lines if len(line) > 2]
            return lines[-1]
    except:
        log_func.fatal(u'Error get OS version')
    return None


def getScreenSize():
    """
    Get screen size.
    """
    try:
        if isLinuxPlatform():
            import tkinter
            root = tkinter.Tk()
            return '%s x %s' % (root.winfo_screenwidth(), root.winfo_screenheight())
        elif isWindowsPlatform():
            import ctypes
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return '%s x %s' % (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    except:
        log_func.fatal(u'Error get screen size')
    return None


def getUptime():
    """
    Get uptime.
    """
    try:
        if isLinuxPlatform():
            return subprocess.check_output(['uptime -p'], shell=True).decode('utf-8').strip()
        elif isWindowsPlatform():
            import time
            try:
                import psutil
                delta = round(time.time() - psutil.boot_time())
                hours, remainder = divmod(int(delta), 3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)

                def includeS(text: str, num: int):
                    return f"{num} {text}{'' if num == 1 else 's'}"

                d = includeS('day', days)
                h = includeS('hour', hours)
                m = includeS('minute', minutes)
                s = includeS('second', seconds)

                if days:
                    output = f'{d}, {h}, {m} and {s}'
                elif hours:
                    output = f'{h}, {m} and {s}'
                elif minutes:
                    output = f'{m} and {s}'
                else:
                    output = s
            except ImportError:
                p = subprocess.Popen(['powershell', '-command', '(gcim Win32_OperatingSystem).LastBootUpTime'],
                                     stdout=subprocess.PIPE)

                stdout, stderror = p.communicate()

                output = stdout.decode('UTF-8', 'ignore')
                lines = output.split('\r\r')
                lines = [line.replace('\n', '').replace('\r', '') for line in lines if len(line) > 2]
                output = lines[-1]
            return output
    except:
        log_func.fatal(u'Error get uptime')
    return None


def getShell():
    """
    Get shell.
    """
    try:
        return os.environ.get('SHELL', '')
    except:
        log_func.fatal(u'Error get shell')
    return None


def getPlatformKernel():
    """
    Get kernel.
    """
    try:
        return platform.release()
    except:
        log_func.fatal(u'Error get platform kernel')
    return None


def getCPUSpec():
    """
    Get CPU specification.
    """
    try:
        return platform.processor()
    except:
        log_func.fatal(u'Error get CPU specification')
    return None


def getDesktopEnvironment():
    """
    Get desktop environment.
    """
    try:
        return os.environ.get('DESKTOP_SESSION', '')
    except:
        log_func.fatal(u'Error get desktop environment')
    return None


def getOSUsername():
    """
    Get OS username.
    """
    try:
        return getpass.getuser()
    except:
        log_func.fatal(u'Error get OS username')
    return None


LINUX_FETCH_FMT = '''
\033[92m       a88888.       \033[0m   {hostname} 
\033[92m      d888888b.      \033[0m   {hostname_sep}
\033[92m      d888888b.      \033[0m\033[93m  OS: {os_version}
\033[92m      8P"YP"Y88      \033[0m\033[93m  Kernel: {kernel}
\033[93m      8|o||o|88      \033[0m\033[93m  Cpu architecture: {cpu}
\033[93m      8'    .88      \033[0m\033[93m  Shell: {shell}
\033[93m      8'    .88      \033[0m\033[93m  DE(WM): {de}
\033[93m      8`._.' Y8      \033[0m\033[93m  Uptime: {uptime}
\033[91m     d/      `8b.    \033[0m\033[93m  Resolution: {size}
\033[91m   .dP   .     Y8b   \033[0m\033[93m  Local IP: {local_ip}
\033[91m   d8:'   "   `::88b.\033[0m\033[93m  User: {os_username}
\033[95m  d8"           `Y88b
\033[95m :8P     '       :888
\033[95m  8a.    :      _a88
\033[94m  ._/"Yaa_ :    .| 88P|
\033[94m   \    YP"      `| 8P  `.
\033[94m  /     \._____.d|    .'
\033[94m  `--..__)888888P`._.'

\033[30m███\033[0m\033[91m███\033[0m\033[92m███\033[0m\033[93m███\033[0m\033[94m███\033[0m\033[95m███\033[0m\033[96m███\0
'''

WINDOWS_FETCH_FMT = '''
                                ..,     {hostname}
                    ....,,:;+ccllll     {hostname_sep}
      ...,,+:;  cllllllllllllllllll     OS: {os_version}
,cclllllllllll  lllllllllllllllllll     Kernel: {kernel}
llllllllllllll  lllllllllllllllllll     Cpu architecture: {cpu}
llllllllllllll  lllllllllllllllllll     Shell: {shell}
llllllllllllll  lllllllllllllllllll     DE(WM): {de}
llllllllllllll  lllllllllllllllllll     Uptime: {uptime}
llllllllllllll  lllllllllllllllllll     Resolution: {size}
                                        Local IP: {local_ip}
llllllllllllll  lllllllllllllllllll     User: {os_username}
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
`'ccllllllllll  lllllllllllllllllll
      `' \\*::  :ccllllllllllllllll
                       ````''*::cll
                                 ``
'''


def getOSFetchInfo():
    """
    Get OS fetch info.
    """
    try:
        computer_name = getComputerName()
        fetch_fmt = LINUX_FETCH_FMT if isLinuxPlatform() else WINDOWS_FETCH_FMT
        info_txt = fetch_fmt.format(hostname=computer_name,
                                    hostname_sep='-' * len(computer_name),
                                    os_version=getOSVersion(),
                                    kernel=getPlatformKernel(),
                                    cpu=getCPUSpec(),
                                    shell=getShell(),
                                    de=getDesktopEnvironment(),
                                    uptime=getUptime(),
                                    size=getScreenSize(),
                                    local_ip=getLocalIP(),
                                    os_username=getOSUsername())
        return info_txt
    except:
        log_func.fatal(u'Error get OS fetch info', is_force_print=True)
    return None


def printOSFetchInfo():
    """
    Print OS fetch info.
    """
    info_txt = getOSFetchInfo()
    if info_txt:
        if isLinuxPlatform():
            print(info_txt)
        elif isWindowsPlatform():
            import termcolor
            lines = info_txt.splitlines()
            for line in lines:
                print(termcolor.colored(line[:40], 'cyan'), termcolor.colored(line[40:], 'yellow'))
        else:
            print(info_txt)
        return True
    else:
        return False
