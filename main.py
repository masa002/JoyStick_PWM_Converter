import wx

import AxisSelection as AS

def main():
    app = wx.App()
    axis_selection = AS.AxisSelection(None, "Select Axis to Configure")
    app.MainLoop()

if __name__ == "__main__":
    main()