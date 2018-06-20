import wx
import yaml



#frame = wx.Frame(parent, id, title, position, size, style, name)
def yaml_loader(filepath):
    #load yaml file
    with open(filepath, "r") as file_desc:
        data = yaml.load(file_desc)
    return data

def yaml_dump(filepath, data):
    #WRITES DATA BACK TO FILE
    with open(filepath, "w") as file_desc:
        yaml.dump(data, file_desc)



class MainWindow(wx.Frame):

    def setChoices(self, strings):
        self.input_string = strings    

    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~ wx.RESIZE_BORDER, name = ""):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style, name)

        self.menuText = wx.StaticText(self, 1, "Sound(s)")
        input_string = ["none"]
        self.choicebox = wx.Choice(self,1, (50,25), (500,100),input_string) 

        #default constructions
        
        self.makeToolBar()
        self.makeAudioPanel(input_string)

    def get_ChoiceStrings(self):
        return choicestrings

    def makeToolBar(self):
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

        #exit script for tool bar's 'File' tab
    def onExit(self,event):
        self.Close()

    def makeAudioPanel(self, input_string):
        self.choicebox = wx.Choice(self,1, (50,25), (500,100),input_string) 
        
        print "firing off audiopanel"
        #audioMenuListBox.AppendAndEnsureVisible('hello')
 
        
     
def main():
    
    #uncomment below to run legit

    #test out reading YAML
    #file_path = "test.yml"
    #data = yaml_loader(file_path)
    #yString = [yaml.dump(data)]
    #print yString
    yString = ["Testing", "1", "2","3"]

    global frame
    app = wx.App()
    frame = MainWindow(None, 1, "Pinball Audio Entry Menu",(200,200), (600,500),wx.DEFAULT_FRAME_STYLE, "Sound(s) Collection")
    frame.CenterOnScreen
    frame.input_string = yString
    frame.makeAudioPanel(yString)
    frame.setChoices(yString)
    frame.Show()

    #put this in at the very  bottom of the main()
    app.MainLoop()

if __name__ == '__main__':
    main()