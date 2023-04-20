import wx

import KeyBindingFrame as KBF

class KeyBindingSelection(wx.Frame):
    def __init__(self, parent, title):
        super(KeyBindingSelection, self).__init__(parent, title=title, size=(300, 200))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.x_axis_button = wx.Button(self.panel, label="X Axis Key Bindings")
        self.y_axis_button = wx.Button(self.panel, label="Y Axis Key Bindings")
        self.z_axis_button = wx.Button(self.panel, label="Z Axis Key Bindings")
        self.back_button = wx.Button(self.panel, label="Back")

        self.sizer.Add(self.x_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.y_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.z_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.back_button, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.open_x_axis_key_bindings, self.x_axis_button)
        self.Bind(wx.EVT_BUTTON, self.open_y_axis_key_bindings, self.y_axis_button)
        self.Bind(wx.EVT_BUTTON, self.open_z_axis_key_bindings, self.z_axis_button)
        self.Bind(wx.EVT_BUTTON, self.close_window, self.back_button)

        self.Show()

    def open_x_axis_key_bindings(self, event):
        key_binding_frame = KBF.KeyBindingFrame(None, "X Axis Key Bindings", "X")

    def open_y_axis_key_bindings(self, event):
        key_binding_frame = KBF.KeyBindingFrame(None, "Y Axis Key Bindings", "Y")

    def open_z_axis_key_bindings(self, event):
        key_binding_frame = KBF.KeyBindingFrame(None, "Z Axis Key Bindings", "Z")

    def close_window(self, event):
        self.Close()