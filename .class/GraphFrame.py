import wx
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import ControllerInput as CI

class GraphFrame(wx.Frame):
    def __init__(self, parent, title, axis):
        super(GraphFrame, self).__init__(parent, title=title, size=(600, 500))

        self.axis = axis
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.controller_input = CI.ControllerInput()
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