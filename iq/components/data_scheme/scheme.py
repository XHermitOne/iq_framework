#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme manager.
"""

import os.path
import sqlalchemy.orm
import sqlalchemy

from ...util import log_func
from ...util import imp_func

from . import scheme_module_generator

__version__ = (0, 0, 1, 2)

DEFAULT_MODULE_ATTR_NAME = '__module'
DEFAULT_SESSION_CLASS_ATTR_NAME = '__session_class'


class iqSchemeManager(object):
    """
    Data scheme manager.
    """
    def destroy(self):
        """
        Destructor.
        """
        self.closeSession()

    def getDBEngine(self):
        """
        Get database engine.

        :return:
        """
        return None

    def getModule(self, module_filename=None):
        """
        Get module object.

        :param module_filename: Module filename.
            If None then generate module filename.
        :return: Module object if None if error.
        """
        if module_filename is None:
            module_filename = self.getModuleFilename()

        if not hasattr(self, DEFAULT_MODULE_ATTR_NAME):
            if module_filename and os.path.exists(module_filename):
                log_func.debug(u'Module filename <%s>' % module_filename)
                module = imp_func.importPyModule(import_name=self.getName(),
                                                 import_filename=module_filename)
                setattr(self, DEFAULT_MODULE_ATTR_NAME, module)
            else:
                log_func.warning(u'Scheme <%s> module <%s> not exists' % (self.getName(), module_filename))
        return getattr(self, DEFAULT_MODULE_ATTR_NAME) if hasattr(self, DEFAULT_MODULE_ATTR_NAME) else None

    def getModel(self, model_name):
        """
        Get model class object.

        :param model_name: Model name.
        :return: Model class object or None if error.
        """
        module = self.getModule()
        if module is None:
            log_func.warning(u'Data scheme <%s> module not defined' % self.getName())
            return None

        if module and hasattr(module, model_name):
            model = getattr(module, model_name)
            log_func.debug(u'Get model <%s : %s : %s>' % (module, model_name, model))
            return model
        else:
            log_func.warning(u'Model <%s> not find in module <%s>' % (model_name, module.__file__))
        return None

    def getSessionClass(self, db_url=None, base=None, *args, **kwargs):
        """
        Get session class.

        :param db_url: Database URL.
            If is None then get from DB engine.
        :param base: Base model class.
        :return: Session class.
        """
        if not hasattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME):
            db_engine = self.getDBEngine()
            if db_engine is None:
                log_func.warning(u'Not define DB engine in data scheme <%s>' % self.getName())
                return None

            if db_url is None:
                db_url = db_engine.getDBUrl()

            if base is None:
                module = self.getModule()
                base = module.Base if module else None

            if base is None:
                log_func.warning(u'Not define base model class in data scheme <%s>' % self.getName())
                return None

            engine = db_engine.create(db_url)
            base.metadata.create_all(engine, checkfirst=True)

            # creating a Session class configuration
            session_class = sqlalchemy.orm.sessionmaker(bind=engine, *args, **kwargs)
            log_func.info(u'Create scheme <%s> session' % self.getName())
            setattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME, session_class)

        if hasattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME):
            return getattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME)
        else:
            log_func.warning(u'Error create scheme <%s> session class' % self.getName())
        return None

    def openSession(self, db_url=None, base=None, *args, **kwargs):
        """
        Create session object.

        :param db_url: Database URL.
            If is None then get from DB engine.
        :param base: Base model class.
        :return: Session object or None if error.
        """
        session_class = self.getSessionClass(db_url=db_url, base=base, *args, **kwargs)

        # create Session object
        session = None
        if session_class is not None:
            session = session_class()
        return session

    def closeSession(self, session=None):
        """
        Close session.
        Always close the session after use.
        otherwise the DB server does not release the connection and happens
        excess of the limit of open connections. After exceeding the limit
        DB server denies service to clients.

        :param session: Session object.
        :return: True/False.
        """
        if session is None:
            log_func.warning(u'Not define session for close')
            return False

        if session is not None:
            # session.expunge_all()
            session.close()
            # log_func.info(u'Data scheme <%s> close session' % self.getName())
            return True
        else:
            log_func.warning(u'Not define session object in data scheme <%s>' % self.getName())
        return False

    def startTransaction(self, *args, **kwargs):
        """
        Start transaction.

        :return: Session/transaction object.
        """
        return self.openSession(*args, **kwargs)

    def stopTransaction(self, transaction):
        """
        Stop transaction.

        :param transaction: Session/transaction object.
        :return: True/False.
        """
        return self.closeSession(session=transaction)
