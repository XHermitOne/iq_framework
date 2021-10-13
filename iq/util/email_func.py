#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EMail functions.
"""

import os
import os.path
import smtplib
import email.message
import mimetypes
import tempfile

from . import log_func

__version__ = (0, 0, 0, 1)

EMAIL_ADR_DELIMETER = u';'
DEFAULT_ENCODING = 'utf-8'

#
SMTP_PROTECT_NO = u'NO'                 #
SMTP_PROTECT_STARTTLS = u'STARTTLS'     # STARTTLS
SMTP_PROTECT_SSL_TLS = u'SSL/TLS'       # SSL/TLS

# Authentication method
SMTP_AUTHENT_NO = u'NO'                     # Without authentication
SMTP_AUTHENT_UNDEFENDED = u'UNDEFENDED'     # Simple password
SMTP_AUTHENT_ENCRYPTED = u'ENCRYPTED'       # Encrypted password
SMTP_AUTHENT_KERBEROS = u'Kerberos/GSSAPI'  # Kerberos/GSSAPI
SMTP_AUTHENT_NTLM = u'NTLM'                 # NTLM
SMTP_AUTHENT_OAUTH2 = u'OAuth2'             # OAuth2


class iqEMailSender(object):
    """
    EMail sender class.
    """
    def __init__(self, from_adr=None, to_adr=None,
                 subject=None, body=None, attache_files=None,
                 smtp_server=None, smtp_port=None,
                 login=None, password=None, enable_send=True,
                 encoding='utf-8',
                 outbox_dir=None, auto_del_files=False,
                 prev_send_cmd=None, post_send_cmd=None,
                 connect_protect=None, authent=None):
        """
        Constructor.

        :param from_adr: Sender address.
        :param to_adr: Receiver address.
            As list or as string with delimeter EMAIL_ADR_DELIMETER.
        :param subject: Email subject.
        :param body: Email text
        :param attache_files: Attached file names.
        :param smtp_server: SMTP server address.
        :param smtp_port: SMTP server port. Default 25.
        :param login: SMTP server user name.
        :param password: SMTP server password.
        :param enable_send: On/off send.
        :param encoding: Code page. Default UTF-8.
        :param outbox_dir: Outbox folder.
        :param auto_del_files: Automatically delete attachments after sending?
        :param prev_send_cmd: The command to execute before sending an email.
        :param post_send_cmd: The command executed after sending the letter.
        :param connect_protect: Connection protection.
        :param authent: Authentication method.
        """
        self.from_adr = from_adr
        self.to_adr = to_adr.split(EMAIL_ADR_DELIMETER) if isinstance(to_adr, str) else to_adr
        self.subject = subject
        self.body = body
        self.attache_files = attache_files
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.login = login
        self.password = password

        self.enable_send = enable_send
        self.encoding = encoding
        self.outbox_dir = outbox_dir
        self.auto_del_files = auto_del_files

        self.prev_send_cmd = prev_send_cmd
        self.post_send_cmd = post_send_cmd

        self.connect_protect = connect_protect
        # Authentication method
        self.authent = authent

    def _encode(self, txt, from_codepage, to_codepage):
        """
        Recoding a string from one code page to another.
        """
        if isinstance(txt, bytes):
            return txt.decode(to_codepage)
        elif isinstance(txt, str):
            return txt.encode(to_codepage)
        return str(txt)

    def _doCommandList(self, cmd_list, mode=os.P_WAIT):
        """
        Running a list of OS commands.

        :param cmd_list: Command list.
        """
        if cmd_list and isinstance(cmd_list, list):
            for cmd in cmd_list:
                cmd = cmd.strip()
                if cmd:
                    self._doCommand(cmd, mode)

    def _parseCommand(self, cmd):
        """
        Parse command string.
        """
        cmd_arg = cmd.split(' ')
        return tuple(cmd_arg)

    def _doCommand(self, cmd, mode=None):
        """
        Run the command in the specified mode (with waiting for completion / without waiting).
        """
        try:
            if mode is None:
                os.system(cmd)
            else:
                arg_cmd = self._parseCommand(cmd)
                os.spawnl(mode, arg_cmd[0], *arg_cmd)

            log_func.info(u'Command <%s> completed' % cmd)
        except:
            log_func.fatal(u'Error execute command <%s>' % cmd)

    def sendMail(self, from_adr=None, to_adr=None,
                 subject=None, body=None, attache_files=None,
                 smtp_server=None, smtp_port=None,
                 login=None, password=None,
                 connect_protect=None, authent=None):
        """
        Send email.

        :param from_adr: Sender address.
        :param to_adr: Receiver address.
            As list or as string with delimeter EMAIL_ADR_DELIMETER.
        :param subject: Email subject.
        :param body: Email text
        :param attache_files: Attached file names.
        :param smtp_server: SMTP server address.
        :param smtp_port: SMTP server port. Default 25.
        :param login: SMTP server user name.
        :param password: SMTP server password.
        :return: True/False.
        """
        if self.prev_send_cmd:
            self._doCommandList(self.prev_send_cmd, None)

        try:
            result = self._sendMail(from_adr, to_adr,
                                    subject, body, attache_files,
                                    smtp_server, smtp_port,
                                    login, password,
                                    connect_protect, authent)
        except:
            log_func.fatal(u'Error send mail')
            result = False

        if self.post_send_cmd:
            self._doCommandList(self.post_send_cmd)

        return result

    def _sendMail(self, from_adr=None, to_adr=None,
                  subject=None, body=None, attache_files=None,
                  smtp_server=None, smtp_port=None,
                  login=None, password=None,
                  connect_protect=None, authent=None):
        """
        Send email.

        :param from_adr: Sender address.
        :param to_adr: Receiver address.
            As list or as string with delimeter EMAIL_ADR_DELIMETER.
        :param subject: Email subject.
        :param body: Email text
        :param attache_files: Attached file names.
        :param smtp_server: SMTP server address.
        :param smtp_port: SMTP server port. Default 25.
        :param login: SMTP server user name.
        :param password: SMTP server password.
        :return: True/False.
        """
        if not self.enable_send:
            log_func.warning(u'Send email disabled')
            return False

        from_adr = self.from_adr if from_adr is None else from_adr
        to_adr = self.to_adr if to_adr is None else to_adr
        subject = self.subject if subject is None else subject
        body = self.body if body is None else body
        attache_files = self.attache_files if attache_files is None else attache_files
        smtp_server = self.smtp_server if smtp_server is None else smtp_server
        smtp_port = self.smtp_port if smtp_port is None else smtp_port
        login = self.login if login is None else login
        password = self.password if password is None else password
        connect_protect = self.connect_protect if connect_protect is None else connect_protect
        authent = self.authent if authent is None else authent

        assert isinstance(from_adr, str)
        assert type(to_adr) in (list, tuple)
        if attache_files:
            assert type(attache_files) in (list, tuple, None)

        # Create message
        msg = email.message.EmailMessage()
        log_func.debug(u'EMail body:\n%s' % str(body))
        msg.set_content(str(body))

        msg['Subject'] = subject
        msg['From'] = from_adr
        msg['To'] = to_adr

        # If the files are not defined, then look in the outgoing files folder
        if not attache_files and self.outbox_dir:
            attache_files = self.getOutboxFilenames()

        # Attachment files
        if attache_files:
            for filename in attache_files:
                with open(filename, 'rb') as attachment_file:
                    file_data = attachment_file.read()
                # Guess the content type based on the file's extension.  Encoding
                # will be ignored, although we should check for simple things like
                # gzip'd or compressed files.
                ctype, encoding = mimetypes.guess_type(filename)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                msg.add_attachment(file_data,
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=filename)

                file_size = os.stat(filename).st_size
                log_func.info(u'File <%s> (%s) attached' % (filename, file_size))

        msg_txt = msg.as_string()

        # Connect SMTP server and send mail
        try:
            smtp = smtplib.SMTP(smtp_server, smtp_port)
            smtp.set_debuglevel(0)
            if connect_protect == SMTP_PROTECT_STARTTLS:
                # If we use communication protection STARTTLS, then it is necessary
                # put the server into mode using the .starttls () method
                smtp.starttls()

            if login and authent != SMTP_AUTHENT_NO:
                log_func.info(u'SMTP. %s. login: <%s> password: <%s>' % (authent, login, password))
                smtp.login(login, password)

            to_adr = [to.strip() for to in to_adr]
            log_func.info(u'Send mail from <%s> to <%s>' % (from_adr, to_adr))
            # log_func.debug(msg_txt)
            smtp.sendmail(from_adr, to_adr, msg_txt)
            smtp.close()

            log_func.info(u'Mail from <%s> to <%s> is sent' % (from_adr, to_adr))
        except smtplib.SMTPException:
            log_func.fatal(u'SMTP. Error send mail')
            return False

        if attache_files and self.auto_del_files:
            for file_name in attache_files:
                if os.path.exists(file_name):
                    try:
                        os.remove(file_name)
                        log_func.info(u'File <%s> deleted' % file_name)
                    except:
                        log_func.fatal(u'Error delete file <%s>' % file_name)
                        return False
        return True

    def getOutboxFilenames(self, outbox_dir=None):
        """
        Get file names in outbox folder.

        :param outbox_dir: Outbox folder.
        :return: File name list in outbox folder.
        """
        outbox_dir = self.outbox_dir if outbox_dir is None else outbox_dir

        outbox_filenames = list()
        if outbox_dir:
            if os.path.isdir(outbox_dir):
                outbox_filenames = [os.path.join(outbox_dir, element) for element in os.listdir(outbox_dir) if
                                    os.path.isfile(os.path.join(outbox_dir, element))]
        return outbox_filenames


def sendMail(*args, **kwargs):
    """
    Send mail.

    :param from_adr: Sender address.
    :param to_adr: Receiver address.
        As list or as string with delimeter EMAIL_ADR_DELIMETER.
    :param subject: Email subject.
    :param body: Email text
    :param attache_files: Attached file names.
    :param smtp_server: SMTP server address.
    :param smtp_port: SMTP server port. Default 25.
    :param login: SMTP server user name.
    :param password: SMTP server password.
    :param enable_send: On/off send.
    :param encoding: Code page. Default UTF-8.
    :param outbox_dir: Outbox folder.
    :param auto_del_files: Automatically delete attachments after sending?
    :param prev_send_cmd: The command to execute before sending an email.
    :param post_send_cmd: The command executed after sending the letter.
    :param connect_protect: Connection protection.
    :param authent: Authentication method.
    :return: True/False.
    """
    mail_sender = iqEMailSender(*args, **kwargs)
    result = mail_sender.sendMail()
    return result


def sendMailByCurl(from_adr=None, to_adr=None,
                   subject=None, body=None, attache_files=None,
                   smtp_server=None, smtp_port=None,
                   login=None, password=None,
                   encoding='utf-8'):
    """
    Send mail by curl tools.

    :param from_adr: Sender address.
    :param to_adr: Receiver address.
        As list or as string with delimeter EMAIL_ADR_DELIMETER.
    :param subject: Email subject.
    :param body: Email text
    :param attache_files: Attached file names.
    :param smtp_server: SMTP server address.
    :param smtp_port: SMTP server port. Default 25.
    :param login: SMTP server user name.
    :param password: SMTP server password.
    :param encoding: Code page. Default UTF-8.
    :return: True/False.
    """
    try:
        mail_filename = tempfile.mktemp()
        mail_file = None
        try:
            mail_file = open(mail_filename, 'wt')
            mail_txt = '''From: <%s>
To: <%s>
Subject: %s

%s
''' % (from_adr if from_adr else '',
       to_adr if to_adr else '',
       subject if subject else '',
       body if body else '')
            mail_file.close()
        except:
            if mail_file:
                mail_file.close()
                os.remove(mail_filename)
            log_func.fatal(u'Error save mail file <%s>' % mail_filename)
            return False

        cmd = '''curl --url \'smtps://%s:%s\' --ssl-reqd \
--mail-from \'%s\' --mail-rcpt \'%s\' \
--upload-file %s --user \'%s%s:%s\'
        ''' % (smtp_server, smtp_port, from_adr, to_adr, mail_filename,
               login, '@' + from_adr.split('@')[1] if '@' in from_adr else '', password)
        os.system(cmd)
        return True
    except:
        log_func.fatal(u'Error send email by curl')
    return False
