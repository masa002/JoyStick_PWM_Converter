import wx

import ControllerInput as CI
import GraphFrame as GF
import KeyBindingSelection as KBS

class AxisSelection(wx.Frame):
    def __init__(self, parent, title):
        super(AxisSelection, self).__init__(parent, title=title, size=(300, 200))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.timer = wx.Timer(self)

        self.x_axis_button = wx.Button(self.panel, label="X Axis")
        self.y_axis_button = wx.Button(self.panel, label="Y Axis")
        self.z_axis_button = wx.Button(self.panel, label="Z Axis")
        self.key_binding_button = wx.Button(self.panel, label="Key Bindings")
        self.start_button = wx.Button(self.panel, label="Start")

        self.sizer.Add(self.x_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.y_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.z_axis_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.key_binding_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.start_button, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.sizer)
        self.controller_input = CI.ControllerInput()
        self.controller_input.start()

        self.Bind(wx.EVT_BUTTON, self.open_x_axis, self.x_axis_button)
        self.Bind(wx.EVT_BUTTON, self.open_y_axis, self.y_axis_button)
        self.Bind(wx.EVT_BUTTON, self.open_z_axis, self.z_axis_button)
        self.Bind(wx.EVT_BUTTON, self.open_key_binding_selection, self.key_binding_button)
        self.Bind(wx.EVT_BUTTON, self.toggle_pwm_control, self.start_button)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.Show()
        self.timer.Start(10)

    def open_x_axis(self, event):
        graph_frame = GF.GraphFrame(None, "X Axis Sensitivity and Deadzone", "X")

    def open_y_axis(self, event):
        graph_frame = GF.GraphFrame(None, "Y Axis Sensitivity and Deadzone", "Y")

    def open_z_axis(self, event):
        graph_frame = GF.GraphFrame(None, "Z Axis Sensitivity and Deadzone", "Z")

    def open_key_binding_selection(self, event):
        key_binding_selection = KBS.KeyBindingSelection(None, "Select Key Bindings to Configure")

    def toggle_pwm_control(self, event):
        if self.start_button.GetLabel() == "Start":
            self.controller_input.start_pwm_control()
            self.start_button.SetLabel("Stop")
        else:
            self.controller_input.stop_pwm_control()
            self.start_button.SetLabel("Start")

    def on_timer(self, event):
        self.controller_input.update()