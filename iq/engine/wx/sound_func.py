#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sound functions.
"""

import os
import os.path

import wx
import wx.adv

from ...util import log_func

__version__ = (0, 0, 0, 1)

# Sound object
SOUND = None


def playWAV(wav_filename, play_mode=wx.adv.SOUND_ASYNC):
    """
    Play WAV file.

    :param wav_filename: WAV filename.
    :param play_mode: Play mode:
        wx.adv.SOUND_ASYNC - Play without waiting for the end
        wx.adv.SOUND_SYNC - Pending playback
        wx.adv.SOUND_LOOP - Loop play
        The mode can also be specified as a combination. For example:
        wx.adv.SOUND_LOOP | wx.adv.SOUND_ASYNC
    :return: True/False.
    """
    if not wav_filename:
        log_func.warning(u'WAV file not defined')
        return False

    if not os.path.exists(wav_filename):
        log_func.warning(u'WAV file <%s> not found' % wav_filename)
        return False

    global SOUND

    app = wx.GetApp()
    if app is not None:
        SOUND = wx.adv.Sound(wav_filename)
        if SOUND.IsOk():
            log_func.info(u'Play <%s> WAV file' % wav_filename)
            return SOUND.Play(play_mode)
        else:
            log_func.warning(u'Incorrect sound object. File <%s>' % wav_filename)
    else:
        SOUND = None
        log_func.warning(u'WX application not created. Sound files cannot be played', is_force_print=True)
    return False


def stopSound():
    """
    Stops sound playback.

    :return: True/False
    """
    global SOUND

    app = wx.GetApp()
    if app is None:
        log_func.warning(u'WX application not created. It is not possible to stop playing audio files', is_force_print=True)
        return False

    if SOUND and SOUND.IsOk():
        result = SOUND.Stop()
        SOUND = None
        return result
    else:
        log_func.warning(u'Sound object not detected when stopped')
    return False
