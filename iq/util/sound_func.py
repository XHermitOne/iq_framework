#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sound functions.
"""

import time

from . import log_func

try:
    import multiprocessing
except ImportError:
    log_func.error('Error import <multiprocessing> module', is_force_print=True)

try:
    import playsound
except ImportError:
    log_func.error('Error import <playsound> module. Install: pip3 install playsound', is_force_print=True)


__version__ = (0, 1, 1, 1)

# Play without waiting for the end
SOUND_ASYNC = 1
# Pending playback
SOUND_SYNC = 2
# Loop play
SOUND_LOOP = 4

SOUND_PROCESS = None

# Played status
PLAYED_STATUS = False


def playLoopWAV(wav_filename, count=-1):
    """
    Play loop WAV file.

    :param wav_filename: WAV filename.
    :param count: The number of cycles. If not defined, then infinite.
    :return: True/False.
    """
    global PLAYED_STATUS

    if count >= 0:
        try:
            PLAYED_STATUS = True
            for i in range(count):
                playsound.playsound(wav_filename, block=True)
            PLAYED_STATUS = False
            return True
        except:
            log_func.fatal(u'Error play loop [%d] WAV file <%s>' % (count, wav_filename))
    else:
        try:
            PLAYED_STATUS = True
            while True:
                playsound.playsound(wav_filename, block=True)
                time.sleep(1)
            return True
        except:
            log_func.fatal(u'Error play loop WAV file <%s>' % wav_filename)

    PLAYED_STATUS = False
    return False


def playWAV(wav_filename, play_mode=SOUND_ASYNC):
    """
    Play WAV file.

    :param wav_filename: WAV filename.
    :param play_mode: Play mode:
        SOUND_ASYNC - Play without waiting for the end
        SOUND_SYNC - Pending playback
        SOUND_LOOP - Loop play
        The mode can also be specified as a combination. For example:
        SOUND_LOOP | SOUND_ASYNC
    :return: True/False.
    """
    global SOUND_PROCESS
    global PLAYED_STATUS

    if SOUND_PROCESS is not None:
        log_func.warning(u'Sound process is running. Stop it for play')
        return False
    try:
        if play_mode == SOUND_ASYNC:
            PLAYED_STATUS = True
            playsound.playsound(wav_filename, block=False)
            PLAYED_STATUS = False
        elif play_mode & SOUND_LOOP:
            SOUND_PROCESS = multiprocessing.Process(target=playLoopWAV, args=(wav_filename,))
            SOUND_PROCESS.start()
        else:
            PLAYED_STATUS = True
            playsound.playsound(wav_filename, block=True)
            PLAYED_STATUS = False
        return True
    except:
        log_func.fatal(u'Error play sound. Start sound process')
    return False


def stopSound():
    """
    Stops sound playback.

    :return: True/False
    """
    global SOUND_PROCESS
    global PLAYED_STATUS

    if SOUND_PROCESS:
        try:
            SOUND_PROCESS.terminate()
            log_func.info(u'Terminate sound process')
            SOUND_PROCESS = None
            PLAYED_STATUS = False
            return True
        except:
            log_func.fatal(u'Error stop sound. Terminate sound process')
    return False


def getPlayedStatus():
    """
    Get played status.

    :return: True/False.
    """
    global PLAYED_STATUS
    return PLAYED_STATUS