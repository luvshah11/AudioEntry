import wx
import yaml
import copy

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
    with open("exported_test.yaml", "w") as file_desc:
        yaml.dump(data, file_desc, default_flow_style= False)
       

class MainWindow(wx.Frame):

  
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~wx.RESIZE_BORDER, name = ""):
        super(MainWindow, self).__init__( parent, id, title, pos, size, style, name)
        
        #members
        self.holding_list = []
        self.finalKeyList = []
        self.finalFileList= []
        self.input_structure = {}
        #title
        #StaticText(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, name=StaticTextNameStr)
        text = wx.StaticText(self, wx.ID_ANY, "\t\t\t\t\tSound(s) Menu", (1,1), (350,35))

        #load the YAML to Mem and into list of strings
        file_path = "test.yml"
        
        self.input_structure = yaml_loader(file_path)
        in_keys = self.input_structure["Audio"].keys()
        #value = value_for_key(input_structure, in_keys)

        print self.input_structure
        #getKeys = input_structure.keys("Audio") only pulls 'Audio



        #print len(input_structure)                             prints 1 key
        #print len(input_structure["Audio"])                    prints 5 keys
        #print len(input_structure["Audio"]["Dictionaries"])    prints 2 keys

        x = 0
        selections = []
       #here, I am triyng to extract all values that are under the "file" key in the YAML

        print "\n",self.input_structure["Audio"]["Music"]
        holding_list = []
        Dictionaries_keys = {}
        Audio_keys = {}
        
        Dictionaries_keys = self.input_structure["Audio"]["Dictionaries"]
        print "\n\nDictionaires List: ", Dictionaries_keys #shows now_showing and houdinin_letters
        print"\nDictionaries Keys only: ", Dictionaries_keys.keys()

        Audio_keys = self.input_structure["Audio"]
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
        print "editting file", self.input_structure
        #open a new window to edit an entry
        self.Disable()
        editWindow = EditSubWindow(self)
        editWindow.Show()
        #self.__init__()

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


class EditSubWindow (wx.Frame):
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~wx.RESIZE_BORDER, name = ""):
        super(EditSubWindow, self).__init__(parent, title = "Edit Entry", pos = (250,250), size = (460,260))
        self.instance = wx.SingleInstanceChecker()
        self.SetFocus()
        print parent.input_structure.keys()
        

        #print "Address of parnet : ", id(parent.input_structure)
        print parent.choicebox.CurrentSelection
        self.writeflag = False
        self.finalDict = parent.input_structure
        self.finalList = None
        self.finalKey = None
        self.finalFile = None
        self.finalVol = None
        self.finalDuck = None
        self.finalUnduck = None
        self.isSelected = False

        
        #check for congruency dictionary 
        if(self.finalDict is parent.input_structure):
            print "yes"
        else:
            print "no"




        if parent.choicebox.CurrentSelection > -1:
            self.finalKey = parent.finalKeyList[parent.choicebox.CurrentSelection]
            isSelected = True
            isFiredOff = False
            x = 0
            z = 0
            AudioKeys = self.finalDict["Audio"] # grabs effect, fanfare ect
            keyList = AudioKeys.keys()
            while x < len(keyList):
                y = 0
                sub_list = AudioKeys[keyList[x]]    #grabs a dict of list, ie it becomes fanfare, or effects  ect
                while y < len(sub_list):
                    if keyList[x] == "Dictionaries":
                        #diction egde case
                        print "Dictionaries"
                        y +=1
                        if not isFiredOff:
                            isFiredOff = True
                            terror_list = sub_list["now_showing_terror"]
                            letter_list = sub_list["houdini_letter"]
                            combo_list = terror_list + letter_list
                            z = 0
                            while z < len(combo_list):
                                if(combo_list[z]["key"] is self.finalKey):
                                    try:
                                        self.finalFile = sub_list[y]["file"]
                                        print "File found"
                                    except:
                                        print "No File found for this Key"
                                z +=1
                            
                    else:
                        #notmal lists of dictionaries
                        print sub_list[y]
                        print sub_list[y]["key"]
                        if(sub_list[y]["key"] is self.finalKey) :
                           self.finalFile = sub_list[y]["file"]

                           try:
                               self.finalFile = sub_list[y]["file"]
                               print "File found"
                           except:
                               print "No File found for this Key"

                           try:
                               self.finalVol = sub_list[y]["volume"]
                               print "Volume found"
                           except:
                               print "No Volume found for this key"
                   
                           try:
                               self.finalDuck = sub_list[y]["duck"]
                               print "Duck found (quack)"
                           except:
                               print "No Duck found for this Key"
                           
                           try:
                               self.finalUnduck = sub_list[y]["unduck_duration_offset"]
                               print "Unduck value found"
                           except:
                               print "No Unduck for this key"
                           break
                        else:
                            y += 1
                x +=1   
       
        self.displaySelctionInfo();


        def __destroy(_):
            print "destroying edit menu"
            parent.Enable()
            parent.SetFocus()

        self.Bind(wx.EVT_WINDOW_DESTROY, __destroy)   
        self.Bind(wx.EVT_LEFT_DOWN, self.mouseClickCoordinates)

    def mouseClickCoordinates(self, event):
        print "Mouse Cooridnate: ", event.x, event.y
            
    def refreshEntries(self):
       #robust check - if they MADE a selection, then only execute, otherwise yell at them
        
        isSelected = True
        if isSelected:
           isFiredOff = False
           x = 0
           z = 0
           AudioKeys = self.finalDict["Audio"] # grabs effect, fanfare ect
           keyList = AudioKeys.keys()
           while x < len(keyList):
               y = 0
               sub_list = AudioKeys[keyList[x]]    #grabs a dict of list, ie it becomes fanfare, or effects  ect
               while y < len(sub_list):
                   if keyList[x] == "Dictionaries":
              
                       #diction egde case
                        print "Dictionaries"
                        y +=1
                        if not isFiredOff:
                            isFiredOff = True
                            terror_list = sub_list["now_showing_terror"]
                            letter_list = sub_list["houdini_letter"]
                            combo_list = terror_list + letter_list
                            z = 0
                            while z < len(combo_list):
                                if(combo_list[z]["key"] is self.finalKey):
                                    try:
                                        self.finalFile = sub_list[y]["file"]
                                        print "File found"
                                    except:
                                        print "No File found for this Key"
                                z+=1
                   else:
                         #normal lists of dictionaries
                         print sub_list[y]
                         print sub_list[y]["key"]
                         if(sub_list[y]["key"] is self.finalKey) :
                            self.finalFile = sub_list[y]["file"]
              
                            try:
                                self.finalFile = sub_list[y]["file"]
                                print "File found"
                            except:
                                print "No File found for this Key"
              
                            try:
                                self.finalVol = sub_list[y]["volume"]
                                print "Volume found"
                            except:
                                print "No Volume found for this key"
                    
                            try:
                                self.finalDuck = sub_list[y]["duck"]
                                print "Duck found (quack)"
                            except:
                                print "No Duck found for this Key"
                            
                            try:
                                self.finalUnduck = sub_list[y]["unduck_duration_offset"]
                                print "Unduck value found"
                            except:
                                print "No Unduck for this key"
                            break
                         else:
                             y += 1
               x +=1   
           else:
               print "no file selected"

        print self.finalKey
        print self.finalFile
        print self.finalVol
        print self.finalDuck
        print self.finalUnduck

        #self.keyEntry.Refresh()
        #self.fileEntry.Refresh()
        #self.volEntry.Refresh()
        #self.duckEntry.Refresh()
        #self.unDuckEntry.Refresh()
        
        #self.keyEntry.Show()
        #self.fileEntry.Show()
        #self.volEntry.Show()
        #self.duckEntry.Show()
        #self.unDuckEntry.Show()

        self.keyEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalKey), (25,19), (400,23))
        self.fileEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalFile), (25,74), (400,23))
        self.volEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalVol), (25,129), (70,23))
        self.duckEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalDuck), (25,184), (70,23))
        self.unDuckEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalUnduck), (125,184), (300,23))

    def displaySelctionInfo(self):

        keyName_SBOX = wx.StaticBox(self, wx.ID_ANY, "Key: ", (20,5), (410,45))
        fileName_SBOX = wx.StaticBox(self, wx.ID_ANY, "File: ", (20,60), (410,45))
        volume_SBOX = wx.StaticBox(self, wx.ID_ANY, "Volume: ", (20,115), (80,45))
        duck_SBOX= wx.StaticBox(self, wx.ID_ANY, "Duck: ", (20,170), (80,45))
        unduck_SBOX = wx.StaticBox(self, wx.ID_ANY, "Unduck Duration Offset: ", (120,170), (310,45))
       
        self.keyEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalKey), (25,19), (400,23))
        self.fileEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalFile), (25,74), (400,23))
        self.volEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalVol), (25,129), (70,23))
        self.duckEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalDuck), (25,184), (70,23))
        self.unDuckEntry = wx.TextCtrl(self, wx.ID_ANY, str(self.finalUnduck), (125,184), (300,23))

        #self.keyEntry.Refresh()
        #self.fileEntry.Refresh()
        #self.volEntry.Refresh()
        #self.duckEntry.Refresh()
        #self.unDuckEntry.Refresh()

        print "making buttons"
        okButton = wx.Button(self, 1, "OK", (375,129), (50,25), name = "okButton")
        refreshButton = wx.Button(self, 1, "Refresh", (305,129), (50,25), name = "refreshButton")
        

        #bind script to buttons
        self.Bind(wx.EVT_BUTTON, self.buttonEventHandler, okButton)
        self.Bind(wx.EVT_BUTTON, self.buttonEventHandler, refreshButton)

    def buttonEventHandler(self, event):
        button = event.GetEventObject()
      
        if button.GetName() == "okButton":
            #ok button presed
            print "Button pressed: ", button.GetLabel(), "\nButton Name: ", button.GetName()
            self.okPressed()

        if button.GetName() == "refreshButton":
            print "Button pressed: ", button.GetLabel(), "\nButton Name:", button.GetName()
            #refresh button pressed
            self.refreshEntries()

    def refreshPressed(self):
        refreshEntries()

    def okPressed(self):
        print "ok button function of class Edit Window"
        self.writeflag = False
        if wx.MessageBox("Are you sure?", "All changes are permanent", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
            print "Nothing wirtten to disc"
        else:
            print "Write to disc: "
            print "Key: ", self.keyEntry.GetValue()
            self.finalKey = copy.deepcopy(self.unDuckEntry.GetValue()) 

            print "File: ", self.fileEntry.GetValue()
            self.finalFile = copy.deepcopy(self.fileEntry.GetValue())
            
            print "Volume: ", self.volEntry.GetValue()
            self.finalVol = copy.deepcopy(self.volEntry.GetValue())

            print "Duck: ", self.duckEntry.GetValue()
            self.finalDuck = copy.deepcopy(self.duckEntry.GetValue())

            print "Unduck: ", self.unDuckEntry.GetValue()
            self.finalUnduck = copy.deepcopy(self.unDuckEntry.GetValue())

    

        

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