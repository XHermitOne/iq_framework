#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CryptoPro manager class.
"""

import os
import os.path

from ...util import log_func
from ...util import sys_func
from ...util import exec_func
from ...util import lang_func

from ...dialog import dlg_func

__version__ = (0, 0, 1, 4)

_ = lang_func.getTranslation().gettext

WINDOWS_FIND_FOLDER_PATHS = (u'C:\\Program Files\\Crypto Pro\\CSP',
                             u'C:\\Program Files (x86)\\Crypto Pro\\CSP')

LINUX_FIND_FOLDER_PATHS = (u'/opt/cprocsp/bin/amd64/',
                           u'/opt/cprocsp/bin/i386/')

CERTMGR_LINUX = 'certmgr'
CERTMGR_WINDOWS = 'certmgr.exe'

CERT_OPTION_NAME_REPLACEMENT = {
    u'Издатель': 'Issuer',
    u'Субъект': 'Subject',
    u'Серийный номер': 'Serial',
    u'SHA1 отпечаток': 'SHA1 Hash',
    u'Идентификатор ключа': 'SubjKeyID',
    u'Алгоритм подписи': 'Signature Algorithm',
    u'Алгоритм откр. кл.': 'PublicKey Algorithm',
    u'Выдан': 'Not valid before',
    u'Истекает': 'Not valid after',
    u'Ссылка на ключ': 'PrivateKey Link',
    u'Контейнер': 'Container',
    u'Имя провайдера': 'Provider Name',
    u'Инфо о провайдере': 'Provider Info',
    u'Тип идентификации': 'Indent type',
    u'OCSP URL': 'OCSP URL',
    u'URL сертификата УЦ': 'CA cert URL',
    u'URL списка отзыва': 'CDP',
    u'Назначение/EKU': 'Extended Key Usage',
}

LINUX_SIGN_CRYPTCP_CMD_FMT = '%s -sign -thumbprint %s \"%s\" \"%s\" -nochain -norev'
WINDOWS_SIGN_CSPTEST_CMD_FMT = '%s -sfsign -sign -my %s -in \"%s\" -out \"%s\" -addsigtime -add'


class iqCryptoProManagerProto(object):
    """
    CryptoPro manager prototype class.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._folder = None

    def getFolder(self):
        """
        Get CryptoPro console utilities folder.
        """
        if self._folder is None:
            self._folder = self.findFolder()
        return self._folder

    def getFindPaths(self):
        """
        Get find CryptoPro console utilities paths.
        """
        if sys_func.isLinuxPlatform():
            return LINUX_FIND_FOLDER_PATHS
        elif sys_func.isWindowsPlatform():
            return WINDOWS_FIND_FOLDER_PATHS
        else:
            log_func.warning(u'Unsupported platform <%s> for use CryptoPro tools' % sys_func.getPlatform())
        return tuple()

    def findFolder(self):
        """
        Find CryptoPro console utilities folder.
        """
        find_paths = self.getFindPaths()

        for path in find_paths:
            if os.path.exists(path):
                log_func.info(u'Find CryptoPro console utilities folder <%s>' % path)
                return path
        log_func.warning(u'Not find CryptoPro console utilities folder')
        return None

    def getCertificateList(self):
        """
        Get certificates.
        """
        result = tuple()
        folder = self.getFolder()
        if folder and os.path.exists(folder):
            certmgr = CERTMGR_WINDOWS if sys_func.isWindowsPlatform() else CERTMGR_LINUX
            certmgr = os.path.join(folder, certmgr)
            # if sys_func.isWindowsPlatform():
            #     certmgr = '"%s"' % certmgr
            cmd = (certmgr, '-list')
            lines = exec_func.getLinesExecutedCommand(cmd)

            # Parsing lines
            result = self.parseCertificateLines(lines)

        if not result:
            log_func.warning(u'Not found certificates')
        return result

    def parseCertificateLines(self, lines):
        """
        Parse certmgr output lines on Linux.

        :param lines: List os string.
        :return: List of certificate dictionaries.
        """
        result = list()
        i_cert = 1
        cur_certificate = dict()
        option_signature = ' : '
        for i_line, line in enumerate(lines):
            start_signature = '%d-------' % i_cert
            if line.startswith(start_signature):
                if cur_certificate:
                    result.append(cur_certificate)
                cur_certificate = dict()
                i_cert += 1

            if option_signature in line:
                name = line[:line.index(option_signature)].strip()
                name = CERT_OPTION_NAME_REPLACEMENT.get(name, name)
                value = line[line.index(option_signature) + len(option_signature):].strip()
                if name == 'Issuer':
                    value = self._parseCertificateOptionValue(value)
                elif name == 'Subject':
                    value = self._parseCertificateOptionValue(value)

                if name in ('CA cert URL', 'CDP'):
                    if name not in cur_certificate:
                        cur_certificate[name] = list()
                    cur_certificate[name].append(value)
                else:
                    cur_certificate[name] = value

        if cur_certificate:
            result.append(cur_certificate)
        return tuple(result)

    def _parseCertificateOptionValue(self, value):
        """
        Parse certificate option value.

        :param value: Value string.
        :return: Options dictionary.
        """
        blocks = value.split(', ')
        options = list()
        for item in blocks:
            if '=' in item:
                options.append(item)
            else:
                options[-1] += ', ' + item
        options = [item.split('=') for item in options]
        option_list = [[name, val.strip()] for name, val in options]
        option_list = [[name, val[1:-1] if val.startswith('"') and val.endswith('"') else val] for name, val in option_list]
        options_dict = dict(option_list)
        return options_dict

    def selectCertificate(self, parent=None):
        """
        Select certificate.

        :param parent: Parent window.
        :return: Certificate dictionary or None if cancel pressed.
        """
        certificates = self.getCertificateList()

        for certificate in certificates:
            print(certificate)

        choices = [' '.join((certificate.get('Subject', dict()).get('SN', ''),
                             certificate.get('Subject', dict()).get('G', ''),
                             certificate.get('Subject', dict()).get('O', ''),
                             certificate.get('Subject', dict()).get('T', ''))) for certificate in certificates]
        i_selection = dlg_func.getSingleChoiceIdxDlg(parent=parent,
                                                     title=_('CRYPTO PRO'),
                                                     prompt_text=_('Select certificate'),
                                                     choices=choices)
        if i_selection >= 0:
            return certificates[i_selection]
        return None

    def getThumbprint(self, certificate=None, parent=None):
        """
        Get certificate thumbprint.

        :param certificate: Certificate dictionary.
            If not define then open select certificate dialog.
        :param parent: Parent window.
        :return: Certificate thumbprint.
        """
        if certificate is None:
            certificate = self.selectCertificate(parent=parent)

        if certificate is not None:
            if 'SHA1 Hash' in certificate:
                return certificate['SHA1 Hash']
            log_func.warning(u'Not [SHA1 Hash] in certificate')
        return None

    def getOwner(self, certificate=None, parent=None):
        """
        Get certificate token owner.

        :param certificate: Certificate dictionary.
            If not define then open select certificate dialog.
        :param parent: Parent window.
        :return: Certificate token owner.
        """
        if certificate is None:
            certificate = self.selectCertificate(parent=parent)

        if certificate is not None:
            if 'Subject' in certificate and 'CN' in certificate['Subject']:
                return certificate['Subject']['CN']
            log_func.warning(u'Not [Subject][CN] in certificate')
        return None

    def signFile(self, src_filename, dst_filename, certificate=None, parent=None, cmd_fmt=None):
        """
        Sign file.

        :param certificate: Certificate dictionary.
            If not define then open select certificate dialog.
        :param parent: Parent window.
        :param cmd_fmt: Sign command format.
        :return: True/False.
        """
        if certificate is None:
            certificate = self.selectCertificate(parent=parent)
        if not os.path.exists(src_filename):
            log_func.warning(u'File <%s> for sign by CryptoPro not found' % src_filename)
            return False

        if certificate is not None:
            if sys_func.isLinuxPlatform():
                return self.signFileLinux(src_filename=src_filename,
                                          dst_filename=dst_filename,
                                          certificate=certificate,
                                          parent=parent,
                                          cmd_fmt=LINUX_SIGN_CRYPTCP_CMD_FMT if cmd_fmt is None else cmd_fmt)
            elif sys_func.isWindowsPlatform():
                return self.signFileWindows(src_filename=src_filename,
                                            dst_filename=dst_filename,
                                            certificate=certificate,
                                            parent=parent,
                                            cmd_fmt=WINDOWS_SIGN_CSPTEST_CMD_FMT if cmd_fmt is None else cmd_fmt)
            else:
                log_func.warning(u'Not supported OS platform <%s> for sign file <%s> by CryptoPro' % (sys_func.getPlatform(),
                                                                                                      src_filename))

        return False

    def signFileLinux(self, src_filename, dst_filename, certificate=None, parent=None, cmd_fmt=LINUX_SIGN_CRYPTCP_CMD_FMT):
        """
        Sign file on Linux OS.

        :param certificate: Certificate dictionary.
            If not define then open select certificate dialog.
        :param parent: Parent window.
        :param cmd_fmt: Sign command format.
        :return: True/False.
        """
        try:
            folder = self.getFolder()
            if cmd_fmt == LINUX_SIGN_CRYPTCP_CMD_FMT:
                cryptcp = os.path.join(folder, 'cryptcp')
                thumbprint = self.getThumbprint(certificate=certificate, parent=parent)
                cmd = cmd_fmt % (cryptcp, thumbprint, src_filename, dst_filename)
                return exec_func.execSystemCommand(cmd)
            log_func.warning(u'Not supported sign method Crypto Pro' % cmd_fmt)
        except:
            log_func.fatal(u'Error sign file <%s> by Crypto Pro on Linux OS' % src_filename)
        return None

    def signFileWindows(self, src_filename, dst_filename, certificate=None, parent=None, cmd_fmt=WINDOWS_SIGN_CSPTEST_CMD_FMT):
        """
        Sign file on Windows OS.

        :param certificate: Certificate dictionary.
            If not define then open select certificate dialog.
        :param parent: Parent window.
        :param cmd_fmt: Sign command format.
        :return: True/False.
        """
        try:
            folder = self.getFolder()
            if cmd_fmt == WINDOWS_SIGN_CSPTEST_CMD_FMT:
                csptest = os.path.join(folder, 'csptest.exe')
                owner = self.getOwner(certificate=certificate, parent=parent)
                cmd = cmd_fmt % (csptest, owner, src_filename, dst_filename)
                return exec_func.execSystemCommand(cmd)
            log_func.warning(u'Not supported sign method Crypto Pro' % cmd_fmt)
        except:
            log_func.fatal(u'Error sign file <%s> by Crypto Pro on Windows OS' % src_filename)
        return None
