#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text autocomplete manager.
"""

import os.path

from ..util import log_func
from ..util import res_func
from ..util import file_func
from ..util import str_func
from ..util import global_func

from . import stored_manager

__version__ = (0, 0, 0, 1)


AUTOCOMPLETES_ATTR_NAME = '__autocompletes'
LIMIT_AUTOCOMPLETES = 50
AUTOCOMPLETE_FILENAME_EXT = '.autocomplete'


class iqAutoCompleteManager(stored_manager.iqStoredManager):
    """
    Auto-complete manager class.
    """
    def getAutoCompletes(self):
        """
        Get autocomplete list.

        :return: List [['text1', weight], ['text2', weight], ...]
        """
        if not hasattr(self, AUTOCOMPLETES_ATTR_NAME):
            setattr(self, AUTOCOMPLETES_ATTR_NAME, list())
        return getattr(self, AUTOCOMPLETES_ATTR_NAME)

    def setAutoCompletes(self, autocompletes=None):
        """
        Get autocompletes list.
        """
        if autocompletes is None:
            autocompletes = list()

        assert isinstance(autocompletes, list), u'Autocomplete list type error'

        setattr(self, AUTOCOMPLETES_ATTR_NAME, autocompletes)

    def genAutoCompleteFilename(self, name=None):
        """
        Generate custom data stored file name.

        :param name: Name autocomplete object.
        :return:
        """
        profile_path = file_func.getProjectProfilePath()
        if name is None:
            name = self.getClassName()
        return os.path.join(profile_path, name + AUTOCOMPLETE_FILENAME_EXT)

    def loadAutoCompletes(self, name=None):
        """
        Load object autocomplete list.

        :param name: Name autocomplete object.
        :return: List [['text1', weight], ['text2', weight], ...]
        """
        autocomplete_filename = self.genAutoCompleteFilename(name=name)
        autocompletes = self.loadCustomData(save_filename=autocomplete_filename)
        self.setAutoCompletes(autocompletes=autocompletes)
        return autocompletes

    def saveAutoCompletes(self, name=None):
        """
        Save object autocomplete list.

        :param name: Name autocomplete object.
        :return: True/False.
        """
        autocomplete_filename = self.genAutoCompleteFilename(name=name)
        autocompletes = self.getAutoCompletes()
        return self.saveCustomData(save_filename=autocomplete_filename,
                                   save_data=autocompletes)

    def appendAutoCompletes(self, autocompletes=None):
        """
        Append autocompletes.

        :param autocompletes: Autocompletes.
        :return: New autocompletes.
        """
        assert isinstance(autocompletes, list), u'Autocomplete list type error'

        cur_autocompletes = self.getAutoCompletes()
        cur_autocompletes += autocompletes
        self.setAutoCompletes(cur_autocompletes)
        return cur_autocompletes

    def splitAutoCompleteWords(self, *phrases):
        """
        Splitting the list of suggested meanings into words and sorting them.
        Lowercase text sorting is used.

        :param phrases: A list of frequently used values.
        :return: A list of frequently used values sorted and with highlighted words.
            For example:
            ['Document to transfer'] ->
            ['document', 'document to', 'document to transfer']
        """
        result = list()
        for phrase in phrases:
            if not isinstance(phrase, str):
                value = str_func.toUnicode(phrase, code_page=global_func.getDefaultEncoding())
            words = phrase.split(u' ')

            sub_phrase = u''
            for word in words:
                sub_phrase = sub_phrase + u' ' + word
                sub_phrase = sub_phrase.strip()
                if sub_phrase not in result:
                    result.append(sub_phrase)

        result = sorted(result, key=lambda item: item[0].lower())
        return result

    def genAutoCompletes(self, *phrases):
        """
        Generate a list of frequently used words with a coefficient usage.

        :param phrases: List of frequently used phrases:
        :return: Autocompletes list.
        """
        sub_phrases = self.splitAutoCompleteWords(*phrases)
        word_count = len(sub_phrases)
        return [[word_value, word_count - i] for i, word_value in enumerate(sub_phrases)]

    def findAutoComplete(self, word):
        """
        Returns the most frequently repeated variant of the word.

        :type word: C{string}
        :param word: The search word
        :return: Autocomplete phrase or None if not found.
        """
        autocompletes = self.getAutoCompletes()

        find_phrase = None
        for autocomplete in autocompletes:
            phrase = autocomplete[0]
            if not isinstance(phrase, str):
                phrase = str_func.toUnicode(phrase, code_page=global_func.getDefaultEncoding())
            if phrase.find(word) == 0:
                find_phrase = phrase
                break

        return find_phrase

    def addAutoCompleteWords(self, phrase=None):
        """
        Add phrase/words to autocomple list.
        If None, then autocomplete list sort by descending count.

        :type phrase: C{string}
        :param phrase: Added phrase.
        :return: New autocomplete list.
        """
        autocompletes = self.getAutoCompletes()

        found = False
        for text, count in autocompletes:
            if text == phrase:
                count += 1
                found = True
                break

        self._model[key] = self.gen_words_with_count(*self._model[key])

        #   Если слово впервые вводится
        if not bFind:
            buff_size = self.buffSize
            #   По необходимости чистим буфер - выкидываем наименее
            #   используемые слова
            if len(self._model[key]) > buff_size * 2:
                self._model[key] = self._model[key][:buff_size]
                ######################################################################
                #   Нормируем показания счетчиков, чтобы у новых вариантов была возможность
                #   задержаться в буфере, в противном случае начиная с некоторого момента
                #   в буффере будут оставатся варианты с большим показанием счетчика, превысить
                #   которое новый вариант в принципе не сможет.
                ######################################################################
                factor = float(buff_size) / self._model[key][0][1]
                if factor > 1:
                    factor = 1
                self._model[key] = [[x[0], int(x[1] * factor + 1)] + x[2:] for x in self._model[key]]
            #   Добавляем новое слово
            if val:
                self._model[key].append([val, 1])
        elif val:
            self._model[key] = [[val, 1]]

        return self._model
