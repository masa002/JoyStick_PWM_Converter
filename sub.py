import wx
import json
import pygame
import win32api
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
# import threading

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
        key_binding_frame = KeyBindingFrame(None, "X Axis Key Bindings", "X")

    def open_y_axis_key_bindings(self, event):
        key_binding_frame = KeyBindingFrame(None, "Y Axis Key Bindings", "Y")

    def open_z_axis_key_bindings(self, event):
        key_binding_frame = KeyBindingFrame(None, "Z Axis Key Bindings", "Z")

    def close_window(self, event):
        self.Close()

class KeyBindingFrame(wx.Frame):
    def __init__(self, parent, title, axis):
        super(KeyBindingFrame, self).__init__(parent, title=title, size=(300, 200))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.axis = axis
        self.key1_label = wx.StaticText(self.panel, label="Key -:")
        self.key2_label = wx.StaticText(self.panel, label="Key +:")

        self.key1_input = wx.TextCtrl(self.panel, size=(150, -1))
        self.key2_input = wx.TextCtrl(self.panel, size=(150, -1))

        self.save_button = wx.Button(self.panel, label="Save")

        self.sizer.Add(self.key1_label, 0, wx.ALL, 5)
        self.sizer.Add(self.key1_input, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.key2_label, 0, wx.ALL, 5)
        self.sizer.Add(self.key2_input, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.save_button, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.save_key_bindings, self.save_button)

        self.load_key_bindings()

        self.Show()

    def load_key_bindings(self):
        try:
            with open("config/key_bindings.json", "r") as f:
                key_bindings = json.load(f)

            key1 = key_bindings[self.axis]["negative"]
            key2 = key_bindings[self.axis]["positive"]

            self.key1_input.SetValue(key1)
            self.key2_input.SetValue(key2)
        except:
            pass

    def save_key_bindings(self, event):
        key1 = self.key1_input.GetValue()
        key2 = self.key2_input.GetValue()
        print(f"Axis: {self.axis}, Key 1: {key1}, Key 2: {key2}")

        try:
            with open("config/key_bindings.json", "r") as f:
                key_bindings = json.load(f)
        except:
            key_bindings = {"X": {"negative": "", "positive": ""}, "Y": {"negative": "", "positive": ""}, "Z": {"negative": "", "positive": ""}}
        with open("config/key_bindings.json", "w") as f:
            key_bindings[self.axis]["negative"] = key1
            key_bindings[self.axis]["positive"] = key2
            json.dump(key_bindings, f)

        self.Close()

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
        self.controller_input = ControllerInput()
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
        graph_frame = GraphFrame(None, "X Axis Sensitivity and Deadzone", "X")

    def open_y_axis(self, event):
        graph_frame = GraphFrame(None, "Y Axis Sensitivity and Deadzone", "Y")

    def open_z_axis(self, event):
        graph_frame = GraphFrame(None, "Z Axis Sensitivity and Deadzone", "Z")

    def open_key_binding_selection(self, event):
        key_binding_selection = KeyBindingSelection(None, "Select Key Bindings to Configure")

    def toggle_pwm_control(self, event):
        if self.start_button.GetLabel() == "Start":
            self.controller_input.start_pwm_control()
            self.start_button.SetLabel("Stop")
        else:
            self.controller_input.stop_pwm_control()
            self.start_button.SetLabel("Start")

    def on_timer(self, event):
        self.controller_input.update()

class GraphFrame(wx.Frame):
    def __init__(self, parent, title, axis):
        super(GraphFrame, self).__init__(parent, title=title, size=(600, 500))

        self.axis = axis
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.controller_input = ControllerInput()
        self.deadzone = 0.1
        self.update_controller_input()

        self.points = [(0, 0), (1, 1)]
        self.load_graph_points()
        self.line, = self.axes.plot(*zip(*self.points), marker='o', linestyle='-', color='b')

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.canvas.mpl_connect('button_release_event', self.on_release)

        self.selected_point = None
        self.dragging = False

        self.Show()

    def on_click(self, event):
        if event.button == 1 and event.xdata and event.ydata:
            self.points.append((event.xdata, event.ydata))
            self.points.sort()
            self.redraw()
        elif event.button == 3:
            if len(self.points) > 2:
                point_to_remove = None
                for point in self.points:
                    if abs(point[0] - event.xdata) < 0.05 and abs(point[1] - event.ydata) < 0.05:
                        point_to_remove = point
                        break
                if point_to_remove:
                    self.points.remove(point_to_remove)
                    self.redraw()
                elif event.button == 2:
                    for point in self.points:
                        if abs(point[0] - event.xdata) < 0.05 and abs(point[1] - event.ydata) < 0.05:
                            self.selected_point = point
                            self.dragging = True
                            break

        self.save_graph_points()

    def on_move(self, event):
        if self.dragging and self.selected_point:
            self.points.remove(self.selected_point)
            if self.selected_point == self.points[0] or self.selected_point == self.points[-1]:
                x = self.selected_point[0]
            else:
                x = min(max(event.xdata, 0), 1)
            y = min(max(event.ydata, 0), 1)

            if self.selected_point == self.points[0] or self.selected_point == self.points[-1]:
                self.selected_point = (x, y)
            else:
                self.selected_point = (x, y)

            self.points.append(self.selected_point)
            self.points.sort()
            self.redraw()

        self.save_graph_points()

    def on_release(self, event):
        if event.button == 2 and self.dragging:
            self.dragging = False
            self.selected_point = None

        self.save_graph_points()

    def redraw(self):
        self.line.set_data(*zip(*self.points))
        self.canvas.draw()

    def update_controller_input(self):
        self.controller_input.update(self.deadzone)
        wx.CallLater(10, self.update_controller_input)

    def load_graph_points(self):
        try:
            with open("config/graph_points.json", "r") as f:
                self.points = [tuple(point) for point in json.load(f)[self.axis]]
        except:
            pass

    def save_graph_points(self):
        try:
            with open("config/graph_points.json", "r") as f:
                data = json.load(f)
        except:
            data = {}
        with open("config/graph_points.json", "w") as f:
            data[self.axis] = self.points
            json.dump(data, f)

class ControllerInput:
    def __init__(self):
        self.pwm_control_active = False
        self.deadzone = 0.1

        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def start(self):
        self.update()

    def start_pwm_control(self):
        self.pwm_control_active = True
        self.load_key_bindings()

    def stop_pwm_control(self):
        self.pwm_control_active = False

    def get_axis(self, axis):
        return self.joystick.get_axis(axis)

    def pwm_control(self, value, threshold):
        if abs(value) < threshold:
            return 0
        else:
            return np.interp(value, [-1, 1], [-100, 100])  # PWM周期の軸を-100〜100に変更
        
    def key_press(self, key):
        win32api.keybd_event(ord(key), 0, 0, 0)
        
    def pwm_button_click(self, value, axis):
        try:
            if value > 0:
                self.key_press(self.key_bindings[axis]["positive"])
            elif value < 0:
                self.key_press(self.key_bindings[axis]["negative"])
        except:
            # キーバインディングが設定されていない場合は何もしない
            pass


    def load_key_bindings(self):
        try:
            with open("config/key_bindings.json", "r") as f:
                self.key_bindings = json.load(f)
        except:
            self.key_bindings = {}

    def update(self, deadzone=None):
        if deadzone is None:
            deadzone = self.deadzone
        for event in pygame.event.get():
            pass

        if self.pwm_control_active:
            x_axis = self.get_axis(0)
            y_axis = self.get_axis(1)
            z_axis = self.get_axis(2)

            x_pwm = self.pwm_control(x_axis, self.deadzone)
            y_pwm = self.pwm_control(y_axis, self.deadzone)
            z_pwm = self.pwm_control(z_axis, self.deadzone)

            self.pwm_button_click(x_pwm, "X")
            self.pwm_button_click(y_pwm, "Y")
            self.pwm_button_click(z_pwm, "Z")

            print(f"X_PWM: {x_pwm}, Y_PWM: {y_pwm}, Z_PWM: {z_pwm}")

def main():
    app = wx.App()
    axis_selection = AxisSelection(None, "Select Axis to Configure")
    app.MainLoop()

if __name__ == "__main__":
    main()