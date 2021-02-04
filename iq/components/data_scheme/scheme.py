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

__version__ = (0, 0, 0, 1)


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

        log_func.debug(u'Module filename <%s>' % module_filename)
        if module_filename and os.path.exists(module_filename):
            return imp_func.loadPyModule(name=self.getName(),
                                         path=module_filename)
        else:
            log_func.warning(u'Scheme <%s> module <%s> not exists' % (self.getName(), module_filename))
        return None

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

    def openSession(self, db_url=None, base=None, *args, **kwargs):
        """
        Create session object.

        :param db_url: Database URL.
            If is None then get from DB engine.
        :param base: Base model class.
        :return: Session object or None if error.
        """
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
        Session = sqlalchemy.orm.sessionmaker(bind=engine, *args, **kwargs)

        # create Session object
        session = Session()
        log_func.info(u'Data scheme <%s> open session' % self.getName())
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
            log_func.info(u'Data scheme <%s> close session' % self.getName())
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
