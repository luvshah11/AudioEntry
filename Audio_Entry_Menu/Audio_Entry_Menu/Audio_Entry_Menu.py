import wx

app = wx.App()

#frame = wx.Frame(parent, id, title, position, size, style, name)




class MainWindow(wx.Frame):
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = wx.DEFAULT_FRAME_STYLE, name = ""):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style, name)
        textLoc = wx.Point(100,100)
        menuText = wx.StaticText(self, 1, "Sound(s)",textLoc)


       
def main():
    
    global frame
    frame = MainWindow(None, 1, "Pinball Audio Entry Menu",(200,200), (600,500),wx.DEFAULT_FRAME_STYLE, "Sound(s) Collection")
   
    frame.Show()
    #put this in at the very  bottom of the main()
    app.MainLoop()

if __name__ == '__main__':
    main()