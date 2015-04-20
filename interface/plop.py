#!/usr/bin/env python
import wx

from phue import Bridge


class FullFrame(wx.Frame):
    def __init__(self, title):


        w = 320 #  wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = 240 # wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        size = wx.Size(w,h)
        pos = wx.Point(100,100)

        wx.Frame.__init__(self, None, title=title, pos = pos, size = size)
        # style = wx.STAY_ON_TOP | wx.CLIP_CHILDREN )

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        button = wx.Button(self, 1, "Lights OFF", size = (w/3, h/3))
        self.Bind(wx.EVT_BUTTON, self.LightsOff, button)

        panel.Add(button, 0, wx.ALL, 10)


        button = wx.Button(self, 1, "Lights ON", size = (w/3, h/3))
        self.Bind(wx.EVT_BUTTON, self.LightsOn, button)

        panel.Add(button, 0, wx.ALL, 10)


        panel.SetSizer(box)
        panel.Layout()

    def LightsOff(self, event):
        self._bridge = Bridge(ip = '192.168.0.18', username = "149171db2cd4b12f26cc0ce3336b36b7")
        self._bridge.set_light( light_id = 2, parameter = {on: False})
        self.Close(True)

    def LightsOff(self, event):
        self._bridge = Bridge(ip = '192.168.0.18', username = "149171db2cd4b12f26cc0ce3336b36b7")
        self._bridge.set_light( light_id = 2, parameter = {on: True})
        self.Close(True)



import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = wx.App(redirect=True)
top = FullFrame("Hello World")
top.Show()
app.MainLoop()
