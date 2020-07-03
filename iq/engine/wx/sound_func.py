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
    if not os.path.exists(wav_filename):
        log_func.error(u'WAV file <%s> not found' % wav_filename)
        return False

    global SOUND

    app = wx.GetApp()
    if app is not None:
        SOUND = wx.adv.Sound(wav_filename)
        return SOUND.Play(play_mode)
    else:
        SOUND = None
        log_func.error(u'WX application not created. Sound files cannot be played')
    return False


def stopSound():
    """
    Stops sound playback.

    :return: True/False
    """
    global SOUND

    app = wx.GetApp()
    if app is None:
        log_func.error(u'WX application not created. It is not possible to stop playing audio files')
        return False

    if SOUND:
        result = SOUND.Stop()
        SOUND = None
        return result
    else:
        log_func.error(u'Sound object not detected when stopped')
    return False
