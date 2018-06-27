import wx
import yaml


def stinr_allign(in_srting):
    return in_srting



#frame = wx.Frame(parent, :id, title, position, size, style, name)
def yaml_loader(filepath):
    #load yaml file
    with open(filepath, "r") as file_desc:
        data = yaml.safe_load(file_desc)
    return data

def yaml_dump(data):
    #WRITES DATA BACK TO FILE
    with open("exported_test.yml", "w") as file_desc:
        yaml.dump(data, file_desc, default_flow_style= False)
       

class MainWindow(wx.Frame):

  
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~wx.RESIZE_BORDER, name = ""):
        super(MainWindow, self).__init__( parent, id, title, pos, size, style, name)
        
        #members
        self.holding_list = []
        self.finalKeyList = []
        self.finalFileList= []
        self.input_string = {}
        #title
        #StaticText(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, name=StaticTextNameStr)
        text = wx.StaticText(self, wx.ID_ANY, "\t\t\t\t\tSound(s) Menu", (1,1), (350,35))

        #load the YAML to Mem and into list of strings
        file_path = "test.yml"
        
        self.input_string = yaml_loader(file_path)
        in_keys = self.input_string["Audio"].keys()
        #value = value_for_key(input_string, in_keys)

        print self.input_string
        #getKeys = input_string.keys("Audio") only pulls 'Audio



        #print len(input_string)                             prints 1 key
        #print len(input_string["Audio"])                    prints 5 keys
        #print len(input_string["Audio"]["Dictionaries"])    prints 2 keys

        x = 0
        selections = []
       #here, I am triyng to extract all values that are under the "file" key in the YAML

        print "\n",self.input_string["Audio"]["Music"]
        holding_list = []
        Dictionaries_keys = {}
        Audio_keys = {}
        
        Dictionaries_keys = self.input_string["Audio"]["Dictionaries"]
        print "\n\nDictionaires List: ", Dictionaries_keys #shows now_showing and houdinin_letters
        print"\nDictionaries Keys only: ", Dictionaries_keys.keys()

        Audio_keys = self.input_string["Audio"]
        print "\n\n Audio list: ", Audio_keys

        print "\nAudio keys only: ", Audio_keys.keys() #gets all keys 'Fanfare', 'Voice', 'Music', 'Effects', 'Dictionaries'

        print "\nStoring Values of Audio_keys in list"
        key_list = []   #stores only key values in the dictionary,5 total 
        key_list = Audio_keys.keys()
        print key_list
        
        print"iterating thorugh dictionary to print keys and values"

        peakKeyStrLen = 0
        peakFileStrLen = 0
        x = 0
        z = 0
        isFiredOff = False
        while x < len(key_list):
            print "\nKey at index ",x,"is", key_list[x]
            print "\n", Audio_keys[key_list[x]]
            print len(Audio_keys[key_list[x]])
            if len(Audio_keys[key_list[x]]) > 0: #if a sub dictionary exists at key in 'key_list[x]' index, loop a nested loop and print keys only
                #grab the keys in sub dictionary
                sub_dict = Audio_keys[key_list[x]] #sub_dict is actually a list, but it's "values" are ALL INDIVUDUAL DICTIONARIES
                print sub_dict
                y = 0
                while y < len(sub_dict):
                    if key_list[x] == "Dictionaries":
                        if not isFiredOff:
                            isFiredOff = True
                            terror_list = sub_dict["now_showing_terror"]
                            letter_list = sub_dict["houdini_letter"]
                            combo_list = terror_list + letter_list
                            z = 0
                            while z < len(combo_list):
                                temp_dict = combo_list[z]
                                string_line = temp_dict["key"]
                                self.finalKeyList.append(string_line)
                                holding_list.append(string_line)
                                z += 1
                    else:
                        temp_dict = {}
                        temp_dict = sub_dict[y]
                        #print "Element ",y," is :",temp_dict["key"], "\n\tfile: ", temp_dict["file"], "\n\tvolume: ", temp_dict["volume"], "\n\tDuck: ", temp_dict["duck"], "\n\tunduck_duration_offset: ", temp_dict["unduck_duration_offset"]
                       
                        print temp_dict["key"] , temp_dict["file"]
                        if len(temp_dict["key"]) > peakKeyStrLen:
                            peakKeyStrLen = len(temp_dict["key"])
                        if len(temp_dict["file"]) > peakFileStrLen:
                            peakFileStrLen = len(temp_dict["file"])

                        string_line = "{:70s} {:<80s}".format(temp_dict["key"], temp_dict["file"])
                        self.finalFileList.append(temp_dict["file"])
                        self.finalKeyList.append(temp_dict["key"])
                        self.holding_list.append(string_line) 
                    y += 1 
                  
            x += 1

        print "\n\n\n Peak Key string : ", peakKeyStrLen
        print "\n\n\n Peak File string: ", peakFileStrLen
   
       
     
        #default constructions
        self.makeAudioPanel(self.holding_list)
        self.makeToolBar()
        self.makeButtons()
    

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

    def makeAudioPanel(self, in_string):
        print "firing off audiopanel"
        self.choicebox = wx.Choice(self,1, (25,50), (800,20),in_string)        
        self.Bind(wx.EVT_CHOICE, self.audioPanelScript, self.choicebox)
        #audioMenuListBox.AppendAndEnsureVisible('hello')
 
    def audioPanelScript(self,event):
        print "\nYou selected: ",self.holding_list[self.choicebox.GetCurrentSelection()]
        

    def makeButtons(self):
        print "making buttons"
        playButton = wx.Button(self, 1, "Play", (830,50), (35,25), name = "playButton")
        editButton = wx.Button(self, 1, "Edit", (875,50), (35,25), name = "editButton")
        deleteBttn = wx.Button(self, 1, "Delete", (920,50), (45,25), name = "deleteBttn")        

        #bind script to buttons
        self.Bind(wx.EVT_BUTTON, self.buttonEventHandler, playButton)
            
    def playbttnFunc(self, file):
        print "playing file", file

    def editBttnFunc(self, file):
        print "editting file", self.input_string
        yaml_dump(self.input_string)

    def dletBttnFunc(self, file):
        print "deleting file",file

    def buttonEventHandler(self, event):
        button = event.GetEventObject()
      
        if button.GetName() == "playButton":
            #playButtonFunc
            print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
            self.playbttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])         
           
        if button.GetName() == "editButton":
            #editButtonFunc
            print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
            self.editBttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])
            
        
        if button.GetName() == "deleteBttn":
            #deleteButtonFunc
            print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
            self.dletBttnFunc,(self.finalFileList[self.choicebox.GetCurrentSelection()])  


def main():
    
    #uncomment below to run legit

    #test out reading YAML

    global frame
    app = wx.App()
    frame = MainWindow( None, 1, "Pinball Audio Entry Menu",(200,200), (1000,500),wx.DEFAULT_FRAME_STYLE, "Sound(s) Collection")
    frame.CenterOnScreen
    frame.Show()

    #put this in at the very  bottom of the main()
    app.MainLoop()

if __name__ == '__main__':
    main()