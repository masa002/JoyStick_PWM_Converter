import wx
import json

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