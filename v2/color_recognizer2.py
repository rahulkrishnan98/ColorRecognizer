import wx
import cv2
import numpy as np
import uuid

class viewWindow(wx.Frame):
    def __init__(self, parent, title="Color Recognizer 2"):
            wx.Frame.__init__(self, parent)        

            self.imgSizer = (800, 600)
            self.pnl = wx.Panel(self)
            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.image = wx.Image(self.imgSizer[0],self.imgSizer[1])
            self.imageBit = wx.Bitmap(self.image)
            self.staticBit = wx.StaticBitmap(self.pnl, wx.ID_ANY, self.imageBit)

            self.vbox.Add(self.staticBit)

            self.capture = cv2.VideoCapture(0)
            ret, self.frame = self.capture.read()
            if ret:
                self.height, self.width = self.frame.shape[:2]
                self.bmp = wx.Bitmap.FromBuffer(self.width, self.height, self.frame)
                self.timex = wx.Timer(self)
                self.timex.Start(1000./24)
                self.Bind(wx.EVT_TIMER, self.redraw)
                self.SetSize(self.imgSizer)
            else:
                print("Error no webcam image")
            self.pnl.SetSizer(self.vbox)
            self.vbox.Fit(self)

             # Create buttons
            btn_black = wx.Button(self, -1, "Black", pos=(10,20))
            btn_white = wx.Button(self, -1, "White", pos=(110,20))
            btn_red = wx.Button(self, -1, "Red", pos=(210,20))
            btn_green = wx.Button(self, -1, "Green", pos=(310,20))
            btn_blue = wx.Button(self, -1, "Blue", pos=(410,20))
            btn_orange = wx.Button(self, -1, "Orange", pos=(510,20))
            btn_yellow = wx.Button(self, -1, "Yellow", pos=(610,20))
            btn_purple = wx.Button(self, -1, "Purple", pos=(710,20))
            self.Bind(wx.EVT_BUTTON, self.OnClick)

            # Create statusbar
            demotext = 'Classifier was loaded correctly! \t\t Most probably: Red \t\t Weights: 0.1, 2.3, 5.1 \t\t Image size: 800 x 600 px \t\t Average RGB: 255, 250, 124'

            self.statusbar = self.CreateStatusBar(1)
            self.statusbar.SetStatusText(demotext)

            self.Show()

    def OnClick(self, event):
        button_name = event.GetEventObject().GetLabel()
        print(button_name)
        cv2.imwrite((button_name + '_' + str(uuid.uuid4()) + '.jpg'), self.image)
        event.Skip()

    def redraw(self,e):
        ret, self.frame = self.capture.read()
        self.image = self.frame
        self.status_dimension = np.shape(self.image)
        if ret:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(self.frame)
            self.staticBit.SetBitmap(self.bmp)
            self.Refresh()

def main():
    try:
        app = wx.App()
        frame = viewWindow(None)
        frame.Center()
        frame.Show()
        app.MainLoop()
    except:
        app.Close()

if __name__ == '__main__':
    main()