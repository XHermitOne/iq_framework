#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sound functions.
"""

import os
import os.path
import time

import wx
import wx.adv

from ...util import log_func

__version__ = (0, 1, 1, 2)

# Sound object
SOUND = None
# Current filename
CUR_SOUND_FILENAME = None

#
DELAY = 1

# Play without waiting for the end
SOUND_ASYNC = wx.adv.SOUND_ASYNC
# Pending playback
SOUND_SYNC = wx.adv.SOUND_SYNC
# Loop play
SOUND_LOOP = wx.adv.SOUND_LOOP


def _playWAV(wav_filename, play_mode=wx.adv.SOUND_ASYNC):
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
        if SOUND is None:
            SOUND = wx.adv.Sound(wav_filename)

        if SOUND.IsOk():
            log_func.info(u'Play <%s> WAV file' % wav_filename)
            global CUR_SOUND_FILENAME
            CUR_SOUND_FILENAME = wav_filename
            return SOUND.Play(play_mode)
        else:
            log_func.warning(u'Incorrect sound object. File <%s>' % wav_filename)
    else:
        SOUND = None
        log_func.warning(u'WX application not created. Sound files cannot be played', is_force_print=True)
    return False


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
    try:
        return _playWAV(wav_filename=wav_filename, play_mode=play_mode)
    except:
        log_func.fatal(u'Error play WAV file <%s>' % wav_filename)
    return False


def _stopSound():
    """
    Stops sound playback.

    :return: True/False
    """
    global SOUND

    app = wx.GetApp()
    if app is None:
        log_func.warning(u'WX application not created. It is not possible to stop playing audio files', is_force_print=True)
        return False

    if SOUND is not None and SOUND.IsOk():
        global CUR_SOUND_FILENAME
        log_func.info(u'Stop play sound %s' % CUR_SOUND_FILENAME)
        result = SOUND.Stop()
        time.sleep(DELAY)
        SOUND = None
        return result
    else:
        log_func.warning(u'Sound object not detected when stopped')
    return False


def stopSound():
    """
    Stops sound playback.

    :return: True/False
    """
    try:
        return _stopSound()
    except:
        log_func.fatal(u'Error stop sound')
    return False


def getPlayedStatus():
    """
    Get played status.

    :return: True/False.
    """
    return SOUND is not None
