#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The module of dialog functions of waiting.
"""

import os
import os.path
import wx
import wx.adv
import _thread
import time

from iq.util import lang_func

from .. import wxbitmap_func

# Delay between frames
FRAME_DELAY = 0.3

__version__ = (0, 2, 2, 1)

_ = lang_func.getTranslation().gettext

WAIT_PROCESS_DLG = None


def waitBox(parent, message,
            function, func_args=(), func_kwargs={},
            art_frames=None):
    """
    Waiting window.

    :param parent: Parent window.
    :param message: Dialog text.
    :param function: A function to wait for.
    :param func_args: Function arguments.
    :param func_kwargs: Named arguments of the function.
    :param art_frames: Files are frames.
    """
    global WAIT_PROCESS_DLG
    
    wait_result = [None]
    art_gif = None
    if not art_frames:
        # Define default frames
        cur_dir = os.path.dirname(__file__)
        if not cur_dir:
            cur_dir = os.getcwd()
        wait_dir = os.path.join(cur_dir, 'img')
        art_gif = os.path.join(wait_dir, 'spinner.gif')

    if parent is None:
        parent = wx.GetApp().GetTopWindow()
    WAIT_PROCESS_DLG = wait_box = iqWaitBox(parent, message, art_gif)
    wait_box.setResultList(wait_result)

    _thread.start_new(wait_box.run, (function, func_args, func_kwargs))
    wait_box.ShowModal()
    wait_box.Destroy()
    WAIT_PROCESS_DLG = None
    return wait_result[0]


def waitDeco(f):
    def func(*arg, **kwarg):
        return waitBox(arg[0], _(u'Wait...'), f, arg, kwarg)
    return func


def waitNoParentDeco(f):
    def func(*arg, **kwarg):
        return waitBox(None, _(u'Wait...'), f, arg, kwarg)
    return func


def setWaitBoxLabel(label):
    if WAIT_PROCESS_DLG:
        sx, sy = WAIT_PROCESS_DLG.GetSize()
        WAIT_PROCESS_DLG.SetSize((len(label) * 10 + 20, sy))
        WAIT_PROCESS_DLG.CenterOnScreen()
        WAIT_PROCESS_DLG.set_label(label)
        

class iqWaitBox(wx.Dialog):
    def __init__(self, parent, message, art, style=0):
        """
        Constructor.
        """
        if parent is None:
            style = wx.STAY_ON_TOP
            
        wx.Dialog.__init__(self, parent, -1, size=wx.Size(220, 34), style=style)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/hourglass')))

        self.msg = wx.StaticText(self, -1, message)
        self._lastTime = time.clock()

        self.ani = wx.adv.Animation(art)
        self.ani_ctrl = wx.adv.AnimationCtrl(self, -1, self.ani)
        self.ani_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.ani_ctrl, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.msg, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.ani_ctrl.Play()

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.CenterOnScreen()

        self._running = True    # Признак запущенной функции
        self._closed = False    # Признак закрытия окна
        self._result_list = None
        
        self.Bind(wx.EVT_UPDATE_UI, self.onCheckClose)

    def refresh(self):
        """
        Refresh.
        """
        event = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(event)

    def setResultList(self, result_list):
        self._result_list = result_list
        
    def onCheckClose(self, event=None):
        """
        Checking the window closing.
        """
        if not self._running and not self._closed:
            try:
                self.EndModal(wx.ID_OK)
            except:
                pass
            self._closed = True
            
        if event:
            event.Skip()
        
    def run(self, function, args, kwargs):
        """
        Starting the waiting function.
        """
        self._running = True
        result = function(*args, **kwargs)
        self._running = False
        # Reset to the resulting list
        if isinstance(self._result_list, list):
            self._result_list[0] = result
            
    def setLabel(self, label=None):
        """
        Set label.
        """
        if self.msg:
            self.refresh()
            if label:
                self.msg.SetLabel(label)
            event = wx.PaintEvent(self.msg.GetId())
            self.msg.GetEventHandler().ProcessEvent(event)
