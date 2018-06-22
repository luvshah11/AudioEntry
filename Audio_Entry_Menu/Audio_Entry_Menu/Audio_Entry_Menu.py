import wx
import yaml



#frame = wx.Frame(parent, id, title, position, size, style, name)
def yaml_loader(filepath):
    #load yaml file
    with open(filepath, "r") as file_desc:
        data = yaml.safe_load(file_desc)
    return data

def yaml_dump(filepath, data):
    #WRITES DATA BACK TO FILE
    with open(filepath, "w") as file_desc:
        yaml.dump(data, file_desc)

def recursive_dict_print(input_dict = {} ):
    x = 0
    print "\nLenth of input dictionary :",len(input_dict)
    while x < len(input_dict):
        key = input_dict.keys()
        print input_dict[key][x]
        if(input_dict[key][x]):
            print "\nfound dictionary"
            #recursive_dict_print(key[0])
        else:
            list = []
            list.append(key[x])
        x += 1

class MainWindow(wx.Frame):

    def setChoices(self, strings):
        self.input_string = strings
        print self.input_string

    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~wx.RESIZE_BORDER, name = ""):
        super(MainWindow, self).__init__( parent, id, title, pos, size, style, name)

        #load the YAML to Mem and into list of strings
        #file_path = "test.yml"
        #self.input_string = {}
        #data = yaml_loader(file_path)
        #self.input_string = yaml.dump(data)
       
        testDict = {
            #"First Dict":{"one":"red", "two":"blue", "three":"green"},
            
            #"Second Dict":{"first": "dog", "second":"cat", "third":"bird"},
            
            "Third Dict":{
                "Nested Dict":{"bee":"hive" , "lion":"den"},
                "Another Nest":{"ant":"hill", "kanye":"his ego"}       
                        }
            }
        #self.menuText = wx.StaticText(self, 1, "Sound(s)")
        #self.choicebox = wx.Choice(self,1, (50,25), (500,100)) 
        #keys = self.input_string.keys()
        print testDict
        print"\nIs testDict a dictionary?", type(testDict)
        print testDict.itervalues()
        keys = {}
        keys = testDict.keys()
        print "\nAll Keys:",  keys
        firstkey = keys[0]
        print "Key[0]:", firstkey
        print "\nNested dictionaries :"
       
        #print "Key[0] Contents:" ,firstDict
        #secondKey = keys[1]
        #print "\nKey[1]",secondKey
        #secondDict = testDict[secondKey]
        #print "Key[1] Contents:",secondDict
        #thirdKey = keys[2]
        #print "\nKey[2]",thirdKey
        #thirdDict = testDict[thirdKey]
        #print "Key[2] Conents:",thirdDict
        #firstNestKey = keys[1][1]
       
        print "Recursive Iteration"
        recursive_dict_print(testDict)


        
        
        #default constructions
        
        self.makeToolBar()
        #self.makeAudioPanel(input_string)
    



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
    #yString = yaml.dump(data)
    #print yString
    #yString = ["Testing", "1", "2","3"]

    global frame
    app = wx.App()
    frame = MainWindow( None, 1, "Pinball Audio Entry Menu",(200,200), (600,500),wx.DEFAULT_FRAME_STYLE, "Sound(s) Collection")
    frame.CenterOnScreen
    #frame.input_string = yString
    #frame.setChoices(yString)
    #frame.makeAudioPanel(yString)
    frame.Show()

    #put this in at the very  bottom of the main()
    app.MainLoop()

if __name__ == '__main__':
    main()