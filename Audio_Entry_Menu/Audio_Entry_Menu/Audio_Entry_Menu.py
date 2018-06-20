import wx



#frame = wx.Frame(parent, id, title, position, size, style, name)




class MainWindow(wx.Frame):
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = wx.DEFAULT_FRAME_STYLE, name = ""):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style, name)

        self.gui()

        textLoc = wx.Point(100,100)
        menuText = wx.StaticText(self, 1, "Sound(s)",textLoc)

    def gui(self):
        #create a menu bar you typcally see at the top
        menuBar = wx.MenuBar()

        #first menu item is File
        fileButton = wx.Menu()

        #first item APPENDED the File tab is exit (it exits the program when clicked)
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit','Status message...')

        #append the File tab to the menu bar
        menuBar.Append(fileButton, 'File')

        #call menu bar to show up
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onExit, exitItem)

        #exit script for file menu
    def onExit(self,event):
        self.Close()



       
def main():
    
    global frame
    app = wx.App()
    frame = MainWindow(None, 1, "Pinball Audio Entry Menu",(200,200), (600,500),wx.DEFAULT_FRAME_STYLE, "Sound(s) Collection")
    frame.CenterOnScreen
    frame.Show()
    #put this in at the very  bottom of the main()
    app.MainLoop()

if __name__ == '__main__':
    main()