import wx
import yaml
import copy
import difflib
import wave
from wx.lib.scrolledpanel import ScrolledPanel


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
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "mainPanel")
        #self.SetScrollbar(self)
        #members
        self.vertBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.holding_list = []
        self.finalKeyList = []
        self.finalFileList = []
        self.finalKeySelection = None
        self.finalFileSelection = None
        self.finalSubDict = {}
        self.input_structure = {}
        #title
        #StaticText(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, name=StaticTextNameStr)
        text = wx.StaticText(self.panel, wx.ID_ANY, "\t\t\t\t\tSound(s) Menu", (1,1), (350,35))
        #load the YAML to Mem and into list of strings
        file_path = "yaml/test.yml"
        
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
        self.holding_list = []
        Dictionaries_keys = {}
        Audio_keys = {}
        
        Dictionaries_keys = self.input_structure["Audio"]["Dictionaries"]
        print "\n\nDictionaires List: ", Dictionaries_keys #shows now_showing and houdinin_letters
        print"\nDictionaries Keys only: ", Dictionaries_keys.keys()

        Audio_keys = self.input_structure["Audio"]
        print "\n\n Audio list: ", Audio_keys

        print "\nAudio keys only: ", Audio_keys.keys() #gets all keys 'Fanfare', 'Voice', 'Music', 'Effects', 'Dictionaries'
     
        #default constructions
        self.holding_list = Audio_keys.keys()
        self.channel_list = copy.deepcopy(self.holding_list)
        self.channel_list = self.channel_list[:-1]
        self.makeAudioPanel(self.channel_list)
        self.makeToolBar()
        self.makeButtons()
        self.makeSearchBar()
        #self.makesearchResults()
        self.SetSizer(self.vertBoxSizer)
        self.Layout()

    def makeSearchBar(self):
        print "making search bar"
        self.vertBoxSizer.Add(0,50,0)
        vertSizer = wx.BoxSizer(wx.VERTICAL)
        horBoxizer = wx.BoxSizer( wx.HORIZONTAL)
        staticbox = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, "Search:")
        horBoxizer.Add(25,0,0)
        choiceList = ["key","file", "tag"]
        self.typeChoiceBox = wx.Choice(self.panel, 2,wx.DefaultPosition,wx.DefaultSize,choiceList, 0, wx.DefaultValidator, "typeChoiceBox")
        staticbox.Add(self.typeChoiceBox,0,0)
        searchBar = wx.SearchCtrl(self.panel, 1, "",wx.DefaultPosition,wx.DefaultSize + (315,0), wx.TE_PROCESS_ENTER, wx.DefaultValidator, "searchBar")
        staticbox.Add(20,0,0)
        staticbox.Add(searchBar,0,0,0)
        self.resultsList = wx.ListBox(self.panel,wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize + (391,100), [], wx.LB_NEEDED_SB, wx.DefaultValidator, "results")
        self.resultsList.Bind(wx.EVT_LISTBOX_DCLICK, self.onListBoxSelect, self.resultsList)

        searchBar.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.searchForKey)
        searchBar.Bind(wx.EVT_TEXT_ENTER, self.searchForKey)
        #horStaticBoxizer.SetDimension((wx.DefaultPosition),(1000,35))
        vertSizer.Add(staticbox)
        vertSizer.Add(self.resultsList)
        horBoxizer.Add(vertSizer)
        self.vertBoxSizer.Add(horBoxizer)
    
    def onListBoxSelect(self, event):
        print "woowweee u doubleclicked the list box"
        obj = event.GetEventObject()
        print obj.GetSelection()
        selectionNode = self.listOfCandidates[obj.GetSelection()]
        print selectionNode
        channel = ""
        #find channel
        sub_dicts = self.input_structure["Audio"]
        temp = copy.deepcopy(sub_dicts)
        temp.pop("Dictionaries")
        sub_dicts = temp
        print sub_dicts
        listOfKeys = self.channel_list
        for x in range(len(listOfKeys)):
            dicts = sub_dicts[listOfKeys[x]]
            for y in range(len(dicts)):
                if selectionNode["file"] in dicts[y]["file"]:
                    channel = x 
                    print channel


        self.channelbox.SetSelection(channel)
        self.listy = []
        self.listy.append(selectionNode["file"])
        self.finalFileList = copy.deepcopy(self.listy)
        self.finalFileSelection = self.listy[0]
        self.choicebox.SetItems(self.finalFileList)
        self.choicebox.SetSelection(0)

    def searchForKey(self, event):
        #for every key press, check for seach results in each dictionary.
        print "searching for key"
        input = event.GetEventObject()
        input = input.GetValue()
        print input

        #get slection
        print self.typeChoiceBox.GetString(self.typeChoiceBox.GetSelection())
        typeFromChoice = self.typeChoiceBox.GetString(self.typeChoiceBox.GetSelection())
        #create 3 lists of strings, key, file and tag
        key_List = []
        file_List = []
        tag_List = []
        self.listOfCandidates = []
        listOfCandStrings = []

        if(typeFromChoice != ''):
            for audio in self.input_structure:
                print audio
                for audioKeys in self.input_structure[audio]:
                    print audioKeys
                    if audioKeys == "Dictionaries":
                        print"sorry"
                    else:
                        #populate a list of strings to search trhough
                        for node in self.input_structure[audio][audioKeys]:
                            try:
                             
                                if(self.KMP_algo(node[typeFromChoice],input)):
                                    listOfCandStrings.append(node[typeFromChoice])
                                    self.listOfCandidates.append(node)
                                else:
                                    print"no match in node"
                            except:
                                print "no tag found at key:", node["key"]
                            
        self.resultsList.SetItems(listOfCandStrings)
        print self.listOfCandidates
        #self.resultsList.EnsureVisible()


    def KMP_algo(self,text, pattern):

        # allow indexing into pattern and protect against change during yield
        text = str(text.lower())
        pattern = str(pattern.lower())
        pattern = list(pattern)

        # build table of shift amounts
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        for pos in range(len(pattern)):
            while shift <= pos and pattern[pos] != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift

        # do the actual search
        x = 0
        startPos = 0
        matchLen = 0
        for c in text:
            while matchLen == len(pattern) or matchLen >= 0 and pattern[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(pattern):
                x+=1
        return x
            


    def makeToolBar(self):
        #create a menu bar you typcally see at the top
        menuBar = wx.MenuBar()

        #Menus
        fileButton = wx.Menu()
        createButton = wx.Menu()

        #menu items for file
        fileButton.Append(wx.ID_SAVE, 'Save', 'Saving structure...')
        fileButton.Append(wx.ID_EXIT, 'Exit','Exiting...')
        crtAudEnt = createButton.Append(wx.ID_ANY, 'Create Audio Entry')
        crtDict = createButton.Append(wx.ID_ANY, 'Create Dictionary')

        #menu items for Create

        #append menus to menu bar
        menuBar.Append(fileButton, 'File')
        menuBar.Append(createButton, 'Create')

        #call menu bar to show up
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onExit, id = wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onSave, id = wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.onCreatAudioEntry, crtAudEnt)
        self.Bind(wx.EVT_MENU, self.onCreatDictionary, crtDict)

        #exit script for tool bar's 'File' tab

    def onCreatAudioEntry(self, event):
        print "creating audio entry"
        self.Disable
        caeWindow = CreateAudioEntryWindow(self)
        caeWindow.Show()
        
    def onCreatDictionary(self, event):
        print "creating dictionary"
        self.Disable
        dictWindow = CreateDictionaryWindow(self)
        dictWindow.Show()

    def onExit(self,event):
        self.Close()

    def onSave(self, event):
        print "saving"
        yaml_dump(self.input_structure)

    def makeAudioPanel(self, in_string):
        #add a space between content and tool bar
        self.vertBoxSizer.Add(0,50,0)
        
        #sizer pre-start
        self.horBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        choicebox_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (430,36), (390,45))
        channel_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Channel: ", (20,36), (390,45))
        self.channelbox = wx.Choice(channel_SBOX,1, wx.DefaultPosition + (5,15), (380,25), in_string)
        self.choicebox = wx.Choice(choicebox_SBOX,1,wx.DefaultPosition+ (5,15), (380,25))
        
        self.horBoxSizer.Add(25,0,0)
        self.horBoxSizer.Add(channel_SBOX,1,0)
        self.horBoxSizer.Add(choicebox_SBOX,1,0)

        self.vertBoxSizer.Add(self.horBoxSizer,0,0)

        self.Bind(wx.EVT_CHOICE, self.channelPanelScript, self.channelbox)
        self.choicebox.Bind(wx.EVT_CHOICE, self.choicePanelScript, self.choicebox)
 
    def channelPanelScript(self, event):
        print self.channelbox.GetCurrentSelection()
        #find the appropriate list of entries
        self.finalFileList = []
        x = 0
        key_list = self.input_structure["Audio"].keys()
        sub_list = self.input_structure["Audio"][key_list[self.channelbox.GetCurrentSelection()]]
        displayString = []
        while x < len(sub_list):
            self.finalFileList.append(sub_list[x]["file"])
            x += 1
        print "sucess"
        self.finalFileList.sort()
        self.choicebox.SetItems(self.finalFileList)
        
    def choicePanelScript(self,event):
        print self.choicebox.GetCurrentSelection()
        sub_list = self.input_structure["Audio"][self.holding_list[self.channelbox.GetCurrentSelection()]]
        print sub_list
        print sub_list[self.choicebox.GetCurrentSelection()]
        try:
            print "\nYou selected: ",self.finalFileList[self.choicebox.GetCurrentSelection()]
            print self.choicebox.GetSelection()
            self.finalFileSelection = self.finalFileList[self.choicebox.GetSelection()]
        except:
            self.finalFileSelection = self.listy[0]
            print "pause"
        #print sub_list[self.finalFileSelection]

    def makeButtons(self):
        print "making buttons"
        playButton = wx.Button(self.panel, 1, "Play",  wx.DefaultPosition + (0,5),(35,50), name = "playButton")
        editButton = wx.Button(self.panel, 1, "Edit",  wx.DefaultPosition+(0,15),(35,50), name = "editButton")
        deleteBttn = wx.Button(self.panel, 1, "Delete", wx.DefaultPosition+(0,15), (45,50), name = "deleteBttn")        
        self.horBoxSizer.Add(playButton,0,0)
        self.horBoxSizer.Add(editButton,0,0)
        self.horBoxSizer.Add(deleteBttn,0,0)
        #bind script to buttons
        self.Bind(wx.EVT_BUTTON, self.buttonEventHandler, playButton)
    
    def refresh(self):
        #self.choicebox.Clear()
        self.finalFileList = []
        x = 0
        key_list = self.input_structure["Audio"].keys()
        #key_list = key_list[:-1]
        if(len(key_list)>4):
            copy_key_list = copy.deepcopy(key_list)
            sub_list = copy_key_list[:-1]
            print sub_list
        else:
            sub_list = key_list
        #displayString = []
        #while x < len(sub_list):
        #    self.finalFileList.append(sub_list[x]["file"])
        #    x += 1
        #print "sucess"
        #self.finalFileList.sort()
        #self.choicebox.SetItems(self.finalFileList)
        #self.channelbox.SetSelection(wx.NOT_FOUND)
        #self.choicebox.SetSelection(wx.NOT_FOUND)
        #self.choicebox.Clear()
        #print "end"

    def playbttnFunc(self, file):
        print "playing file", file



    def editBttnFunc(self, file):
        #print "editting file", self.input_structure
        #open a new window to edit an entry
        self.Disable()
        editWindow = EditSubWindow(self)
        editWindow.Show()
        #self.__init__()

    def dletBttnFunc(self, file):
        
        if wx.MessageBox("Are you sure?", "Are you sure you want to delete this?", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
            print "Nothing wirtten to disc"
        elif wx.MessageBox("Are you DAMN sure you want to delete this? You might get in trouble","No...Seriously",  wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
            print "Nothing wirtten to disc"
        else: 
            print "deleting file",file
            #begin deletion of element
            targetfile = self.finalFileSelection
            isSelected = True
            sub_list = []
            if isSelected:
               isFiredOff = False
               x = 0
               z = 0
               AudioKeys = self.input_structure["Audio"] # grabs effect, fanfare ect
               keyList = AudioKeys.keys()
               while x < len(keyList):
                   y = 0
                   sub_list = AudioKeys[keyList[x]]    #grabs a dict of list, ie it becomes fanfare, or effects  ect
                   while y < len(sub_list):
                       if keyList[x] == "Dictionaries":                  
                           #diction egde case
                           print "Dictionary skip"
                           break
                       else:
                             #normal lists of dictionaries
                             print sub_list[y]
                             print sub_list[y]["file"]
                             if(sub_list[y]["file"] is targetfile) :
                                sub_list.remove(sub_list[y])
                                #print "sub_dict[y]['key'] = ", sub_list[y]["key"]
                                break
                             else:
                                 y += 1
                   x +=1   
               else:
                   print "no file selected"
        yaml_dump(self.input_structure)
        self.refresh()


    def buttonEventHandler(self, event):
        button = event.GetEventObject()
        try:
            if button.GetName() == "playButton":
                #playButtonFunc
                print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
                self.playbttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])         
               
            if button.GetName() == "editButton":
                #editButtonFunc
                print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
                try:
                    self.editBttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])         
                except:
                    self.editBttnFunc(self.listy[0])
            if button.GetName() == "deleteBttn":
                #deleteButtonFunc
                print "Button pressed: ", button.GetLabel(), " \nButton Name: ", button.GetName()
                self.dletBttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])  
        except:
            print "error nothing selcted"


class EditSubWindow (wx.Frame):
    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, 
                 style = ~wx.RESIZE_BORDER, name = ""):
        super(EditSubWindow, self).__init__(parent, title = "Edit Entry", pos = (250,250), size = (500,350))
        self.SetFocus()
        print parent.input_structure.keys()
        self.SetBackgroundColour('Gray')
        #print "Address of parnet : ", id(parent.input_structure)
        print self.GetPosition()
        print self.GetSize()
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "panel for edit")
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
            #if(parent.finalFileSelection != None):
            #    self.finalFile = parent.finalFileSelection
            #elif parent.listy[0] != None:
            #    self.finalFile = parent.listy[0]
            if(len(parent.choicebox.GetStrings()) == 1 ):
                self.finalFile = parent.listy[0]
            elif(len(parent.choicebox.GetStrings())):
                self.finalFile = parent.finalFileSelection
                
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
                                        #self.finalFile = sub_list[y]["file"]
                                        print "File found"
                                    except:
                                        print "No File found for this Key"
                                z +=1                            
                    else:
                        #notmal lists of dictionaries
                        print sub_list[y]
                        print sub_list[y]["file"]
                        if(sub_list[y]["file"] is self.finalFile) :
                           self.finalFile = sub_list[y]["file"]
                           try:
                               self.finalKey = sub_list[y]["key"]
                               print "key found"
                           except:
                               print "No key found for this file"
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
            parent.input_structure = self.finalDict
            parent.refresh()
            parent.Enable()
            parent.SetFocus()

        self.Bind(wx.EVT_WINDOW_DESTROY, __destroy)   
        self.Bind(wx.EVT_LEFT_DOWN, self.mouseClickCoordinates)

    def mouseClickCoordinates(self, event):
        print "Mouse Cooridnate: ", event.x, event.y
            
    def refreshEntries(self):
       #robust check - if they MADE a selection, then only execute, otherwise yell at them

        self.finalVol = None
        self.finalDuck = None
        self.finalUnduck = None

        self.isSelected = False
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
                         if(sub_list[y]["file"] == self.finalFile) :
                            self.finalKey = sub_list[y]["key"]
              
                            try:
                                self.finalFile = sub_list[y]["file"]
                                print "File found, adress: ", hex(id(sub_list[y]["file"]))
                                print "address of local: ", hex(id(self.finalFile))
                            except:
                                print "No File found for this Key"
              
                            try:
                                self.finalVol = sub_list[y]["volume"]
                                print "Volume found adress: ", hex(id(sub_list[y]["volume"])) 
                                print "address of local: ", hex(id(self.finalVol))
                            except:
                                print "No Volume found for this key"
                    
                            try:
                                self.finalDuck = sub_list[y]["duck"]
                                print "Duck found adress: ", hex(id(sub_list[y]["duck"])) 
                                print "address of local: ", hex(id(self.finalDuck))
                            except:
                                print "No Duck found for this Key"
                            
                            try:
                                self.finalUnduck = sub_list[y]["unduck_duration_offset"]
                                print "Unduck value found adress: ", hex(id(sub_list[y]["unduck_duration_offset"]))
                                print "address of local: ", hex(id(self.finalUnduck))
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
        print "address of local: ", hex(id(self.finalFile))
        print "address of local: ", hex(id(self.finalVol))
        print "address of local: ", hex(id(self.finalDuck))
        print "address of local: ", hex(id(self.finalUnduck))
       

        self.keyEntry.SetValue(str(self.finalKey))
        self.fileEntry.SetValue(str(self.finalFile))
        self.volEntry.SetValue(str(self.finalVol))
        self.duckEntry.SetValue(str(self.finalDuck))
        self.unDuckEntry.SetValue(str(self.finalUnduck))
        
        print self.finalDict

    def displaySelctionInfo(self):

        keyName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (20,5), (410,45))
        fileName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "File: ", (20,60), (410,45))
        volume_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Volume: ", (20,115), (80,45))
        duck_SBOX= wx.StaticBox(self.panel, wx.ID_ANY, "Duck: ", (20,170), (80,45))
        unduck_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Unduck Duration Offset: ", (120,170), (310,45))
       
        self.keyEntry = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.finalKey), (25,19), (400,23))
        self.fileEntry = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.finalFile), (25,74), (400,23))
        self.volEntry = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.finalVol), (25,129), (70,23))
        self.duckEntry = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.finalDuck), (25,184), (70,23))
        self.unDuckEntry = wx.TextCtrl(self.panel, wx.ID_ANY, str(self.finalUnduck), (125,184), (300,23))

        self.statusBar = wx.StatusBar(self, 1, wx.STB_DEFAULT_STYLE)
        
        self.SetStatusBar(self.statusBar)
        self.SetStatusText("Enter data and press OK | Refresh to see current selection")

        print "making buttons"
        okButton = wx.Button(self.panel, 1, "OK", (375,129), (50,25), name = "okButton")
        refreshButton = wx.Button(self.panel, 1, "Refresh", (305,129), (50,25), name = "refreshButton")
        

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
            
            status = ""

            #Robust data check - DID YOU FEED ME BAD DATA??


            if(type(str(self.keyEntry.GetValue())) is not str):
               status = " Keys(str) "
            if(type(str(self.fileEntry.GetValue())) is not str):
               status += " File(str) "

            if(str(self.volEntry.GetValue()) != 'None' and str(self.volEntry.GetValue()) != ''):
                try:
                    type(int(self.volEntry.GetValue())) is not int 
                except:
                    status += " Volume(int) "
            if(str(self.duckEntry.GetValue()) != "None" and str(self.duckEntry.GetValue()) != ''):
                try:
                    type(float(self.duckEntry.GetValue())) is not float
                except:
                    status += " Duck(float) "
            if(str(self.unDuckEntry.GetValue()) != "None" and str(self.unDuckEntry.GetValue()) != ''):
                try:
                    type(float(self.unDuckEntry.GetValue())) is not float
                except:
                    status += " Unduck(float) "



            if(status is ""):
                #iterate through dictionary and find data to mutate
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
                                          combo_list[z]["key"] = self.keyEntry.GetValue()
                                          combo_list[z]["file"] = self.fileEntry.GetValue()
                                      z+=1
                         else:
                               #normal lists of dictionaries
                               print sub_list[y]
                               print sub_list[y]["key"]
                               if(sub_list[y]["key"] is self.finalKey) :

                                  sub_list[y]["key"] = str(self.keyEntry.GetValue())
                                  sub_list[y]["file"] = str(self.fileEntry.GetValue())

                                  if(self.volEntry.GetValue() != 'None' and self.volEntry.GetValue() != ''): 
                                      sub_list[y]["volume"] = int(self.volEntry.GetValue())
                                  else:
                                      try: 
                                          del sub_list[y]["volume"]
                                      except:
                                          print "no vol"

                                  if(self.duckEntry.GetValue() != 'None' and self.duckEntry.GetValue() != ''):
                                      sub_list[y]["duck"] = float(self.duckEntry.GetValue())
                                  else:
                                      try:
                                          del sub_list[y]["duck"]
                                      except:
                                          print "no duck"

                                  if(self.unDuckEntry.GetValue() != 'None' and self.unDuckEntry.GetValue() != ''):
                                      sub_list[y]["unduck_duration_offset"] = float(self.unDuckEntry.GetValue())
                                  else:
                                      try:
                                          del sub_list[y]["unduck_duration_offset"]
                                      except:
                                          print "no unduck"

                                  try:
                                      self.finalKey = str(self.keyEntry.GetValue())
                                      print "File found, adress: ", hex(id(sub_list[y]["file"]))
                                      print "address of local: ", hex(id(self.finalKey))
                                  except:
                                      print "No File found for this Key"

                                  try:
                                      self.finalFile = str(self.fileEntry.GetValue())
                                      print "File found, adress: ", hex(id(sub_list[y]["file"]))
                                      print "address of local: ", hex(id(self.finalFile))
                                  except:
                                      print "No File found for this Key"
                    
                                  try:
                                      self.finalVol = int(self.volEntry.GetValue())
                                      print "Volume found adress: ", hex(id(sub_list[y]["volume"])) 
                                      print "address of local: ", hex(id(self.finalVol))
                                  except:
                                      print "No Volume found for this key"
                          
                                  try:
                                      self.finalDuck = float(self.duckEntry.GetValue())
                                      print "Duck found adress: ", hex(id(sub_list[y]["duck"])) 
                                      print "address of local: ", hex(id(self.finalDuck))
                                  except:
                                      print "No Duck found for this Key"
                                  
                                  try:
                                      self.finalUnduck = float(self.unDuckEntry.GetValue())
                                      print "Unduck value found adress: ", hex(id(sub_list[y]["unduck_duration_offset"]))
                                      print "address of local: ", hex(id(self.finalUnduck))
                                  except:
                                      print "No Unduck for this key"
                                  break
                               else:
                                   y += 1
                     x +=1   
                 else:
                     print "no file selected"
                 print "dictionary ", self.finalDict
                 yaml_dump(self.finalDict)
                 self.statusBar.SetBackgroundColour("Green")
                 self.statusBar.SetForegroundColour("White")
                 status = "DONE Entry Updated "
            else:
                #BAd data
                self.statusBar.SetBackgroundColour("Red")
                status = "ERROR: Bad data at field(s): " + status
            
            self.SetStatusText(status)
            

class CreateAudioEntryWindow(wx.Frame):

    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, style = ~wx.RESIZE_BORDER, name = ""):
        super(CreateAudioEntryWindow, self).__init__(parent, title = "Create Audio Entry", pos = (250,250), size = (580,450))
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "panel for edit")

        #important data
        self.panel.SetBackgroundColour('Gray')
        parent.Disable()
        self.SetFocus() 
        self.finalDict = parent.input_structure
        temp = self.finalDict["Audio"]
        self.key_list = self.finalDict["Audio"].keys()
        ver_Box = wx.BoxSizer(wx.VERTICAL)

        #defaults for presest
        #Fanfare
        self.default_F_Vol = "1"
        self.default_F_Duck = "0.5"
        self.default_F_UnDuck = "-.5"
        #effects
        self.default_E_Vol = "1"
        self.default_E_Duck = "0.5"
        self.default_E_UnDuck = "-.5"
        #music
        self.default_M_Vol = "1"
        self.default_M_Duck = str(None)
        self.default_M_UnDuck = str(None)
        #voice
        self.default_V_Vol = str(None)
        self.default_V_Duck = "0.5"
        self.default_V_UnDuck = "-.5"

        #text labels
        list_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "List: ", (120,16), (360,45))
        keyName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (120,52), (360,45))
        fileName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "File: ", (120,107), (360,45))
        volume_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Volume: ", (120,162), (100,45))
        duck_SBOX= wx.StaticBox(self.panel, wx.ID_ANY, "Duck: ", (120,217), (100,45))
        unduck_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Unduck Duration Offset: ", (250,217), (230,45))

        #buttons
        self.okButton = wx.Button(self.panel, 1, "Save", (425,176), (50,45), name = "okButton")
        self.testButton = wx.Button(self.panel, 2, "Test", wx.DefaultPosition, (50,45), name = "testButton")
        self.presetsButton = wx.Button(self.panel, 3, "Presets...", wx.DefaultPosition, (50,45), name = "presetsButton")
        self.okButton.Disable()

        #list
        self.listChoice = wx.Choice(list_SBOX,1,(3, 15), (350,25), self.key_list)
        hor_listChoice_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        hor_listChoice_boxsizer.AddSpacer(75)
        hor_listChoice_boxsizer.Add(list_SBOX)
        hor_listChoice_boxsizer.AddSpacer(1)

        #entries
        hor_Box_key = wx.BoxSizer(wx.HORIZONTAL)
        hor_Box_file = wx.BoxSizer(wx.HORIZONTAL)
        hor_Box_vol = wx.BoxSizer(wx.HORIZONTAL)
        hor_Box_duck = wx.BoxSizer(wx.HORIZONTAL)

        hor_Box_key.AddSpacer(75)
        self.keyEntry = wx.TextCtrl(keyName_SBOX, wx.ID_ANY, pos = (3, 15), size = (350,25),name = "keyE")
        hor_Box_key.Add(keyName_SBOX)
        hor_Box_key.AddSpacer(0)

        hor_Box_file.AddSpacer(75)
        self.fileEntry = wx.TextCtrl(fileName_SBOX, wx.ID_ANY,  pos = (3, 15), size = (350,25), name= "fileE")
        hor_Box_file.Add(fileName_SBOX) 
        hor_Box_file.AddSpacer(1)

        hor_Box_vol.AddSpacer(75)
        self.VolEntry = wx.TextCtrl(volume_SBOX, wx.ID_ANY,  pos = (3, 15), size = (90,25))
        hor_Box_vol.Add(volume_SBOX)
        hor_Box_vol.AddSpacer(35)
        hor_Box_vol.Add(self.presetsButton)
        hor_Box_vol.AddSpacer(35)
        hor_Box_vol.Add(self.testButton)
        hor_Box_vol.AddSpacer(35)
        hor_Box_vol.Add(self.okButton)

        hor_Box_duck.AddSpacer(75)
        self.duckEntry = wx.TextCtrl(duck_SBOX, wx.ID_ANY,  pos = (3, 15), size = (90,25))
        self.unduckEntry = wx.TextCtrl(unduck_SBOX, wx.ID_ANY,  pos = (3, 15), size = (220,25))
        hor_Box_duck.Add(duck_SBOX)
        hor_Box_duck.AddSpacer(25)
        hor_Box_duck.Add(unduck_SBOX)
        hor_Box_duck.AddSpacer(1)        

        #disable for now, enable once you make a selection in listCHoice
        self.keyEntry.Disable()
        self.fileEntry.Disable()
        self.VolEntry.Disable()
        self.duckEntry.Disable()
        self.unduckEntry.Disable()

  #sizer
        #listrow
        ver_Box.AddSpacer(25)
        ver_Box.Add(hor_listChoice_boxsizer)

        #key row
        ver_Box.AddSpacer(25)
        ver_Box.Add(hor_Box_key)

        #file row
        ver_Box.AddSpacer(25)
        ver_Box.Add(hor_Box_file)

        #vol & button row
        ver_Box.AddSpacer(25)
        ver_Box.Add(hor_Box_vol)

        #duck & unduck row
        ver_Box.AddSpacer(25)
        ver_Box.Add(hor_Box_duck)
        ver_Box.AddSpacer(25)

        #set sizer
        self.panel.SetSizer(ver_Box)
        self.panel.Fit()

        #Status Bar    
        self.isKeyEntered = False
        self.isFileEntered = False
        self.status = wx.StatusBar(self, 1, wx.STB_DEFAULT_STYLE, "helooooo")
        self.SetStatusBar(self.status)
        self.SetStatusText("Enter data and press OK | Key/File are required, other data fields can be left blank")


        #bind list box to function, to enable text feilds 
        self.Bind(wx.EVT_CHOICE, self.enableTextCtrl, self.listChoice)
        self.Bind(wx.EVT_BUTTON, self.addToDict, self.okButton)
        self.Bind(wx.EVT_BUTTON, self.presetsMenu, self.presetsButton)

        def __destroy(_):
                print "destroying CAE menu"
                parent.refresh()
                parent.Enable()
                parent.SetFocus()
               
        self.Bind(wx.EVT_WINDOW_DESTROY, __destroy)  
        self.Bind(wx.EVT_TEXT,self.enableButton, self.keyEntry)
        self.Bind(wx.EVT_TEXT,self.enableButton, self.fileEntry)

    def testFunc(self, event):
        print "testing entry"
        

    def presetsMenu(self, event):
       
        print "change presets"
        presetWindow = wx.Dialog(self, wx.ID_ANY, "Change Default Presets", wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_DIALOG_STYLE, "presetsWindow")
        presetWindow_Sizer = wx.BoxSizer(wx.VERTICAL)

        sbs1 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Fanfare")
        sbs2 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Effects")
        sbs3 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Music")
        sbs4 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Voice")

        row0 = wx.BoxSizer(wx.HORIZONTAL)
        row1 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Fanfare")
        row2 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow, "Music")
        row3 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow,"Voice")
        row4 = wx.StaticBoxSizer(wx.HORIZONTAL, presetWindow,"Effectgs")

        volSTEXT = wx.StaticText(presetWindow, wx.ID_ANY, "Volume")
        duckSTEXT = wx.StaticText(presetWindow, wx.ID_ANY, "Duck")
        unduckSTEXT = wx.StaticText(presetWindow, wx.ID_ANY, "UnDuck")
        row0.AddMany([(volSTEXT,0, wx.LEFT|wx.RIGHT,17), (duckSTEXT,0,wx.LEFT|wx.RIGHT,20), (unduckSTEXT,0,wx.LEFT|wx.RIGHT,15)])

        #textctrl
        #fanfare: vol, duck, undukc
        r1_vol = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_F_Vol, wx.DefaultPosition, (50,23))
        r1_duc = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_F_Duck, wx.DefaultPosition, (50,23))
        r1_udk = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_F_UnDuck, wx.DefaultPosition, (50,23))
        row1.AddMany([(r1_vol, 0, wx.LEFT|wx.RIGHT,15),(r1_duc,0, wx.RIGHT, 15),(r1_udk,0,wx.RIGHT, 15)])
        #music: vol
        r2_vol = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_M_Vol, wx.DefaultPosition, (50,23))
        r2_duc = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_M_Duck, wx.DefaultPosition, (50,23))
        r2_udk = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_M_UnDuck, wx.DefaultPosition, (50,23))
        row2.AddMany([(r2_vol, 0, wx.LEFT|wx.RIGHT,15),(r2_duc,0, wx.RIGHT, 15),(r2_udk,0,wx.RIGHT, 15)])
        #voice: duck, unduck
        r3_vol = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_V_Vol, wx.DefaultPosition, (50,23))
        r3_duc = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_V_Duck, wx.DefaultPosition, (50,23))
        r3_udk = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_V_UnDuck, wx.DefaultPosition, (50,23))
        row3.AddMany([(r3_vol, 0, wx.LEFT|wx.RIGHT,15),(r3_duc,0, wx.RIGHT, 15),(r3_udk,0,wx.RIGHT, 15)])

        #effect: none
        r4_vol = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_E_Vol, wx.DefaultPosition, (50,23))
        r4_duc = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_E_Duck, wx.DefaultPosition, (50,23))
        r4_udk = wx.TextCtrl(presetWindow, wx.ID_ANY, self.default_E_UnDuck, wx.DefaultPosition, (50,23))
        row4.AddMany([(r4_vol, 0, wx.LEFT|wx.RIGHT,15),(r4_duc,0, wx.RIGHT, 15),(r4_udk,0,wx.RIGHT, 15)])

        #button
        ok = wx.Button(presetWindow, wx.ID_ANY,"Apply", wx.DefaultPosition, (50,23) )
        def presetWindowOK(event):
            print"preset window ok pressed"
            self.default_F_Vol = r1_vol.GetValue()
            self.default_F_Duck= r1_duc.GetValue()
            self.default_F_UnDuck= r1_udk.GetValue()
            
            self.default_M_Vol = r2_vol.GetValue()
            self.default_M_Duck= r2_duc.GetValue()
            self.default_M_UnDuck= r2_udk.GetValue()
            
            self.default_V_Vol = r3_vol.GetValue()
            self.default_V_Duck= r3_duc.GetValue()
            self.default_V_UnDuck= r3_udk.GetValue()
            
            self.default_E_Vol = r4_vol.GetValue()
            self.default_E_Duck= r4_duc.GetValue()
            self.default_E_UnDuck= r4_udk.GetValue()
            print self.default_F_Vol
            
        ok.Bind(wx.EVT_BUTTON, presetWindowOK, ok)

        presetWindow_Sizer.AddSpacer(15)
        presetWindow_Sizer.Add(row0,0, wx.LEFT|wx.RIGHT, 15)
        presetWindow_Sizer.AddSpacer(15)
        presetWindow_Sizer.Add(row1,0, wx.LEFT|wx.RIGHT, 15)
        presetWindow_Sizer.AddSpacer(15)
        presetWindow_Sizer.Add(row2,0, wx.LEFT|wx.RIGHT, 15)
        presetWindow_Sizer.AddSpacer(15)
        presetWindow_Sizer.Add(row3,0, wx.LEFT|wx.RIGHT, 15)
        presetWindow_Sizer.AddSpacer(15)
        presetWindow_Sizer.Add(row4,0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 15)
        presetWindow_Sizer.Add(ok, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 25)
        
        presetWindow.SetSizer(presetWindow_Sizer)
        presetWindow.Fit()
        presetWindow.Show()

        

    def enableButton(self, event):
        #disable OK button until Key and File are modified  
        box = event.GetEventObject()
        print box.GetName()
        if(box.GetName() == 'keyE'):
            self.isKeyEntered = True
        elif(box.GetName() == 'fileE'):
            self.isFileEntered =True

        print self.keyEntry.GetLineLength(1) 
        print self.fileEntry.GetLineLength(1) 
        if (self.keyEntry.GetLineLength(1) < 1):
            self.isKeyEntered = False
        if (self.fileEntry.GetLineLength(1) < 1):
            self.isFileEntered = False

        if(self.isKeyEntered and self.isFileEntered and self.key_list[self.listChoice.GetSelection()] != "Dictionaries"):
            self.okButton.Enable()
        else:
            self.okButton.Disable()

    def enableTextCtrl(self, event):

        if(self.key_list[self.listChoice.GetSelection()] == "Music"):
            self.VolEntry.Enable()
            self.VolEntry.SetValue(self.default_M_Vol)
            self.duckEntry.Disable()
            self.duckEntry.Clear()
            self.unduckEntry.Disable()
            self.unduckEntry.Clear()

        elif(self.key_list[self.listChoice.GetSelection()] == "Voice"):
            self.VolEntry.Disable()
            self.VolEntry.Clear()
            self.duckEntry.Enable()
            self.duckEntry.SetValue(self.default_V_Duck)
            self.unduckEntry.Enable()
            self.unduckEntry.SetValue(self.default_V_UnDuck)

        elif(self.key_list[self.listChoice.GetSelection()] == "Fanfare"):
            self.VolEntry.Enable()
            self.VolEntry.SetValue(self.default_F_Vol)
            self.duckEntry.Enable()
            self.duckEntry.SetValue(self.default_F_Duck)
            self.unduckEntry.Enable()
            self.unduckEntry.SetValue(self.default_F_UnDuck)

        elif(self.key_list[self.listChoice.GetSelection()] == "Effects"):
            self.VolEntry.Enable()
            self.VolEntry.SetValue(self.default_E_Vol)
            self.duckEntry.Disable()
            self.duckEntry.Clear()
            self.unduckEntry.Enable()
            self.unduckEntry.SetValue(self.default_E_UnDuck)

        if(self.key_list[self.listChoice.GetSelection()] == "Dictionaries"):
            #nothing sbhould work if u chose dictionary
            self.VolEntry.Disable()
            self.VolEntry.Clear()
            self.duckEntry.Disable()
            self.duckEntry.Clear()
            self.unduckEntry.Disable()
            self.unduckEntry.Clear()
            self.keyEntry.Disable()
            self.fileEntry.Disable()
            self.okButton.Disable()

        elif(self.keyEntry.GetLineLength(1) > 1 and self.fileEntry.GetLineLength(1) > 1):
            self.okButton.Enable()

        self.keyEntry.Enable()
        self.fileEntry.Enable()

        print self.keyEntry.GetValue()
        print self.keyEntry.IsModified()


    def refreshAllFields(self):

        self.keyEntry.SetLabelText("")
        self.fileEntry.SetLabelText("")
        self.VolEntry.SetLabelText("")
        self.duckEntry.SetLabelText("")
        self.unduckEntry.SetLabelText("")

        self.keyEntry.Disable()
        self.fileEntry.Disable()
        self.VolEntry.Disable()
        self.duckEntry.Disable()
        self.unduckEntry.Disable()

        self.keyEntry.SetModified(False)
        self.fileEntry.SetModified(False)
        self.VolEntry.SetModified(False)
        self.duckEntry.SetModified(False)
        self.unduckEntry.SetModified(False)

        self.okButton.Disable()
        self.isKeyEntered = False
        self.isFileEntered = False
        
    def addToDict(self, event):
        selection = self.key_list[self.listChoice.GetCurrentSelection()] #effects, fanfare, muslice, voice <----choose one
        print selection 
        stagingDict = {}
        status = ""

        #Robust data check - DID YOU FEED ME BAD DATA?
         
        if(type(str(self.keyEntry.GetValue())) is not str):
           status = " Keys(str) "
        if(type(str(self.fileEntry.GetValue())) is not str):
           status += " File(str) "
        if(str(self.VolEntry.GetValue()) != 'None' and str(self.VolEntry.GetValue()) != ''):
            try:
                type(int(self.VolEntry.GetValue())) is not int 
            except:
                status += " Volume(int) "
        if(str(self.duckEntry.GetValue()) != "None" and str(self.duckEntry.GetValue()) != ''):
            try:
                type(float(self.duckEntry.GetValue())) is not float
            except:
                status += " Duck(float) "
        if(str(self.unduckEntry.GetValue()) != "None" and str(self.unduckEntry.GetValue()) != ''):
            try:
                type(float(self.unduckEntry.GetValue())) is not float
            except:
                status += " Unduck(float) "

        if status is "":
            #1. create a dict to hold the key, file, vol, duck, unduck
            print self.keyEntry.IsModified()
            if(self.keyEntry.IsModified()and self.keyEntry.GetLineLength(1) > 1):
                stagingDict["key"] = str(self.keyEntry.GetValue())
                status += "Key &"
            else:
                print "ERROR: NO KEY"
                self.SetStatusText("ERROR: You must enter a Key name")
                return
            
            if(self.fileEntry.IsModified() and self.fileEntry.GetLineLength(1) > 1):
                stagingDict["file"] = str(self.fileEntry.GetValue())
                status = status + " File "
            else:
                print "ERROR: NO FILE"
                self.SetStatusText("ERROR: You must enter a File name")
                return

            if(self.VolEntry.IsModified() and self.VolEntry.GetLineLength(1) > 1):
                stagingDict["volume"] = int(self.VolEntry.GetValue())
                status = status + "& volume "
            else:
                print "NO VOLUME ENTERED, NO VOLUME WRITTEN"

            
            if(self.duckEntry.IsModified() and self.duckEntry.GetLineLength(1) > 1):
                stagingDict["duck"] = float(self.duckEntry.GetValue())
                status = status + "& duck "
            else:
                print "NO DUCK ENTERED, NO DUCK WRITTEN"
            
            if(self.unduckEntry.IsModified()  and self.unduckEntry.GetLineLength(1) > 1):
                stagingDict["unduck_duration_offset"] = float(self.unduckEntry.GetValue())
                status = status + "& unduck "
                print stagingDict
            else:
                print "NO UNDUCK ENTERED, NO UNDUCK WRITTEN"

            print stagingDict

            status = "Data entered: " + status
            self.SetStatusText(status)

            print self.finalDict["Audio"][selection]
            self.finalDict["Audio"][selection].append(stagingDict)
            print self.finalDict["Audio"][selection]

            #set all text fields to false
            self.refreshAllFields()
            #2. Append the dict to the list selected from listChoice
            yaml_dump(self.finalDict)
            self.status.SetBackgroundColour("Green")
            status = "DONE Entry Updated "
        else:
            self.status.SetBackgroundColour("Red")
            status = "ERROR: Bad data at field(s): " + status
       
        self.SetStatusText(status)

        #this is a doubly linked list
class CreateDictionaryWindow(wx.Frame):
            #list of nodes
    class MyPanel(ScrolledPanel):
        #node
        class EntryRow(wx.Panel):
            def __init__(self,parentpanel):
                super(parentpanel.EntryRow, self).__init__(parentpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style = wx.TAB_TRAVERSAL )
                #wx.Panel.__init__(parentpanel)
                #self.SetSize(400,50)
               
                #print "making an EntryRow object"
                self.posx = 0
                self.posy = 10
                self.next = None
                self.prev = None
                buttonsizer = wx.BoxSizer(wx.VERTICAL)
                entriesSizer = wx.BoxSizer(wx.HORIZONTAL)
                masterSizer = wx.BoxSizer(wx.HORIZONTAL)
                self.parentpan = parentpanel
                #self.mysizer = wx.FlexGridSizer(5,1,1)
                #self.mysizer.SetMinSize(450,50)

                #set button sizers
                plusBitMap = wx.Bitmap("greenplus1.png", wx.BITMAP_TYPE_PNG)
                xBitmap = wx.Bitmap("redx1.png", wx.BITMAP_TYPE_PNG)
        
                self.addButton = wx.Button(self, 10, pos =(self.posx, self.posy + 18), size = (24,24), name = "addButton")
                self.addButton.SetBitmapLabel(plusBitMap)
                
                self.removeButton = wx.Button(self, 20, pos =(self.posx, self.posy- 5 ), size = (24,24), name = "removeButton")
                self.removeButton.SetBitmapLabel(xBitmap)
                self.addButton.Bind(wx.EVT_BUTTON, self.greenPlus, self.addButton)
                self.removeButton.Bind(wx.EVT_BUTTON, self.redX, self.removeButton)
                #parentpanel.Bind(wx.EVT_BUTTON, self.greenPlus , self.addButton)
                #parentpanel.Bind(wx.EVT_BUTTON, self.redX , self.removeButton)

                buttonsizer.Add(self.addButton,0,0)
                buttonsizer.Add(self.removeButton,0,0)
                
                #set entries sizer
                keyName_SBOX = wx.StaticBox(self, wx.ID_ANY, "Key: ", (self.posx+ 29 ,self.posy-6), (110,50),wx.SUNKEN_BORDER)
                channel_SBOX = wx.StaticBox(self, wx.ID_ANY, "Channel: ",(self.posx+ 144 ,self.posy-6), (110,50),wx.SUNKEN_BORDER)
                delay_SBOX =   wx.StaticBox(self, wx.ID_ANY, "Delay: ", (self.posx+ 259 ,self.posy-6), (110,50),wx.SUNKEN_BORDER)
                action_SBOX =  wx.StaticBox(self, wx.ID_ANY, "Action: ", (self.posx+ 374 ,self.posy-6),(200,50),wx.SUNKEN_BORDER)
                tag_SBOX = wx.StaticBox(self, wx.ID_ANY, "Tag: ", (self.posx + 579,self.posy-6), (110,50),wx.SUNKEN_BORDER)
                
                #create "action" list
                actions = ["ONLY IF CHANNEL AVAILABLE","FORCE","QUEUED", "FRONT OF QUEUE" ]

                #create entries
                self.keyEntry = wx.TextCtrl(keyName_SBOX, wx.ID_ANY, pos = (3,15), size = (100,25),style = wx.RAISED_BORDER ,name = "keyE")
                self.channelEntry = wx.TextCtrl(channel_SBOX, wx.ID_ANY, pos = (3,15), size = (100,25),style = wx.RAISED_BORDER,name = "channelE")
                self.delayEntry = wx.TextCtrl(delay_SBOX, wx.ID_ANY, pos = (3,15), size = (100,25),style = wx.RAISED_BORDER,name = "delayE")
                self.actionEntry = wx.ComboBox(action_SBOX, wx.ID_ANY,"", (3,15), (190,25), actions , wx.RAISED_BORDER|wx.CB_READONLY, wx.DefaultValidator, "actyionE")
                self.tagEntry = wx.TextCtrl(tag_SBOX, wx.ID_ANY, pos = (3,15), size = (100,25),style = wx.RAISED_BORDER,name = "tagE")

                #puyt entries into sizer
                entriesSizer.Add(keyName_SBOX,0,0)
                entriesSizer.Add(channel_SBOX,0,0)
                entriesSizer.Add(delay_SBOX,0,0)
                entriesSizer.Add(action_SBOX,100,wx.EXPAND,100)
                entriesSizer.Add(tag_SBOX,0,0)

                #path up sizers
                masterSizer.AddStretchSpacer(1)
                masterSizer.Add(buttonsizer,0,0)
                masterSizer.Add(entriesSizer,0,0)
                masterSizer.AddStretchSpacer(1)
                self.Layout()


            def clearAllEntries(self):
                self.keyEntry.Clear()
                self.channelEntry.Clear()
                self.delayEntry.Clear()
                #self.actionEntry.Clear()
                self.Refresh()

            def __del__(self):
                print "destroying EntryRow"
                self.Destroy()
                                  
        
            def greenPlus(self, event):
                print "creating new row"
                #parentpanel.pushNew(self)
                object = event.GetEventObject()
                self.parentpan.pushNew(self)

            
            def redX(self, event):
                print "removing exisitng row"
                #parentpanel.popOld(self)
                self.parentpan.popOld(self)

        def __init__(self,parent, id , pos  , size, style ):
            ScrolledPanel.__init__(self, parent, id, pos, size, style)
            self.SetupScrolling(0,1,0,20,1,1)
            self.numberOfNodes = 0
            self.nameOfDict = ""
            self.par = parent
            #self.parStatus = self.par.statusBar
            self.listOfNodes = []
            self.mainsizer = wx.GridBagSizer(5,5)
            self.dictEntryszier = wx.BoxSizer(wx.HORIZONTAL)
            ##intit list
            
            newEntry = self.EntryRow(self)
            dictStatic = wx.StaticBoxSizer(wx.HORIZONTAL, self,"Enter Dictionary Name")
            self.dictName = wx.TextCtrl(self,1,"", wx.DefaultPosition + (0,25), wx.DefaultSize + (100,0),wx.TE_PROCESS_ENTER,wx.DefaultValidator,"chooseName" )
            self.save = wx.Button(self,wx.ID_ANY, "Save && Export",wx.DefaultPosition + (0,100), wx.DefaultSize,wx.BU_EXACTFIT, wx.DefaultValidator, "saveButton")
            self.listOfNodes.append(newEntry)
            self.numberOfNodes += 1

            self.save.Bind(wx.EVT_BUTTON, self.saveNewDict)
            dictStatic.Add(self.dictName, 1, wx.ALL, 1)
            self.dictEntryszier.Add(dictStatic,1,wx.ALL, 1)
            self.dictEntryszier.Add(self.save,1,3, 1)
            self.mainsizer.Add(self.dictEntryszier, (0,1), (0,0), 0,0)
            self.mainsizer.Add(newEntry,(1,1),(0,0),0,5,"node0")
            #self.mainsizer.Add(dictName, (0,2), (0,0),0,5,"textctrl")
            self.SetSizer(self.mainsizer)
            self.mainsizer.Layout()

        def saveNewDict(self, event):
            isWritable = True
            print "entering name"
            if wx.MessageBox("Are you sure?", "All changes are permanent", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
                print "Nothing wirtten to disc"
            else:
                #append a new LIST of DICTS to the [Dictionary] dictionary 

                self.nameOfDict = self.dictName.GetValue()
                finalListofDicts = []
                finalDict = {}
                final_structure = self.par.input_structure
                Dictionaries = final_structure["Audio"]["Dictionaries"]
                print Dictionaries
                
                status = ""
                x = 0
                while x < self.numberOfNodes:
                    node = self.listOfNodes[x]
                    #Robust data check - DID YOU FEED ME BAD DATA??
                    if self.nameOfDict == '':
                        isWritable = False
                        self.dictName.SetBackgroundColour("Red")
                    else:
                        self.dictName.SetBackgroundColour("White")

                    if(type(str(node.keyEntry.GetValue())) is not str) or (node.keyEntry.GetValue() == ''):
                       status = " Keys(str) "
                       node.keyEntry.SetBackgroundColour("Red")
                       isWritable = False
                    else:
                        node.keyEntry.SetBackgroundColour("white")
                        
                    try:
                        if(type(int(node.channelEntry.GetValue())) is not int):
                           status += " Channel(int) "
                           node.channelEntry.SetBackgroundColour("Red")
                           isWritable = False
                        else:
                            print "good channel"
                            node.channelEntry.SetBackgroundColour("white")
                    except:
                        status += " Channel(int) "
                        node.channelEntry.SetBackgroundColour("Red")
                        isWritable = False

                    try:
                        if(type(float(node.delayEntry.GetValue())) is not float):
                            status += " Delay(int) "
                            node.delayEntry.SetBackgroundColour("Red")
                            isWritable = False
                        else:
                            node.delayEntry.SetBackgroundColour("white")
                    except:
                            status += " Delay(int) "
                            node.delayEntry.SetBackgroundColour("Red")
                            isWritable = False
                    try:
                        if(type(float(node.actionEntry.GetValue())) is not float):
                            status += " action(float) "
                            node.actionEntry.SetBackgroundColour("Red")
                            isWritable = False
                        else:
                            node.actionEntry.SetBackgroundColour("white")
                    except:
                        status += " action(float) "
                        node.actionEntry.SetBackgroundColour("Red")
                        isWritable = False

                    if(type(str(node.tagEntry.GetValue())) is not str) or (node.tagEntry.GetValue() == ''):         
                        status += " tag(string) "
                        node.tagEntry.SetBackgroundColour("Red")
                        isWritable = False
                    else:
                        node.tagEntry.SetBackgroundColour("white")

                    if(status is "" and isWritable):
                        node.keyEntry.SetBackgroundColour("white")
                        node.channelEntry.SetBackgroundColour("white")
                        node.delayEntry.SetBackgroundColour("white")
                        node.actionEntry.SetBackgroundColour("white")
                        node.tagEntry.SetBackgroundColour("white")
                        finalDict["key"] = str(node.keyEntry.GetValue())
                        finalDict["channel"] = int(node.channelEntry.GetValue())
                        finalDict["delay"] = float(node.delayEntry.GetValue())
                        finalDict["action"] = float(node.actionEntry.GetValue())
                        finalDict["tag"]    = str(node.tagEntry.GetValue())
                        finalListofDicts.append(copy.deepcopy(finalDict))
                        x +=1
                    else:
                        x += 1

                #real quick, set the first status bar message first
                firstStatus = "Number of Nodes: " + str(self.numberOfNodes)
                if status is "":
                    print finalListofDicts
                    Dictionaries[str(self.nameOfDict)] = finalListofDicts
                    yaml_dump(final_structure)
                    self.par.statusBar.SetBackgroundColour("Green")
                    self.par.SetStatusText(firstStatus +"\t|\t"+ "DONE:Dictionary Entry Added ")
                    node.keyEntry.SetBackgroundColour("white")
                    node.channelEntry.SetBackgroundColour("white")
                    node.delayEntry.SetBackgroundColour("white")
                    node.actionEntry.SetBackgroundColour("white")
                    node.tagEntry.SetBackgroundColour("white")
                else:
                    #self.par.statusBar.SetBackgroundColor("Red")
                    #self.SetBackgroundColour("Red")
                    self.par.statusBar.SetBackgroundColour("Red")
                    self.par.SetStatusText(firstStatus +"\t|\t"+ "ERROR: Bad data at field(s): " + status)
                self.Refresh()
                

        def pushNew(self, entry):
            EntryRowClicked = entry
            targetIndex = self.listOfNodes.index(entry)
            targetPosition = self.mainsizer.GetItemPosition(entry)
            shifterIter = self.listOfNodes[targetIndex]

            #shifter
            #walk the list from the target position to EOL, count total steps, that will be the total # of shifts
            walk = 0
            while shifterIter.next is not None:
                shifterIter = shifterIter.next
                walk += 1
            
            while walk:
                lastPos = self.mainsizer.GetItemPosition(shifterIter)
                lastPos.Row += 1
                self.mainsizer.SetItemPosition(shifterIter, lastPos)
                shifterIter = shifterIter.prev
                walk -= 1
            
            #malloc and push new node into list
            create = self.EntryRow(self)
            if shifterIter.next:
                shifterIter.next.prev = create
                create.next = shifterIter.next
            
            shifterIter.next = create
            create.prev = shifterIter

            #stats and pointer patch
            self.listOfNodes.insert(targetIndex + 1, create)
            self.numberOfNodes += 1
            namestring = "node" + str(self.numberOfNodes)
            targetPosition.Row += 1
            self.mainsizer.Add(create, targetPosition, (0,0),0,1,namestring)
            self.mainsizer.FitInside(self)
            self.ScrollChildIntoView(create)
            self.par.statusBar.SetBackgroundColour("white")
            self.par.SetStatusText("Number of Nodes: " + str(self.numberOfNodes))

        def popOld(self, entry):
            if len(self.listOfNodes) > 1:
                print "red X pressed"
                print "next",entry.next, "prev", entry.prev
                if entry.prev is not None:
                    entry.prev.next = entry.next
                if entry.next is not None:
                    entry.next.prev = entry.prev

                position = self.mainsizer.FindItem(entry)
                gap = position.GetPos()
                iter = entry
                self.mainsizer.Detach(entry)

                #push all the items below the target UP one Unit

                while(iter):
                    if(iter.next is not None):
                        newgap = self.mainsizer.GetItemPosition(iter.next)
                        self.mainsizer.SetItemPosition(iter.next, gap)
                        gap = newgap
                        iter = iter.next
                    else:
                        break
                self.listOfNodes.remove(entry)
                self.mainsizer.FitInside(self)
                self.mainsizer.Layout()
                #entry.Destroy()
                entry.__del__()
                self.SetFocus()
                self.numberOfNodes -=1
                self.par.statusBar.SetBackgroundColour("White")
                self.par.SetStatusText("Number of Nodes: " + str(self.numberOfNodes))
            else:
                print "single node left, clearing only"
                self.par.statusBar.SetBackgroundColour("red")
                self.par.SetStatusText("Number of Nodes: " + str(self.numberOfNodes))
                
                self.Show()
                self.par.statusBar.SetBackgroundColour("red")
                entry.clearAllEntries()

        

    def __init__(self, parent, id=wx.ID_ANY, title="", pos = (250,250), size = (580,350) , style = ~wx.RESIZE_BORDER, name = ""):
        super(CreateDictionaryWindow, self).__init__(parent, title = "Create Dictionary", pos = (250,250), size = (700,350))

        self.SetFocus()
        #self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "panel for edit")
        self.panel = self.MyPanel(self,wx.ID_ANY,pos = wx.DefaultPosition, size = self.GetSize() , style = wx.TAB_TRAVERSAL | wx.VSCROLL)

        box = wx.BoxSizer(wx.VERTICAL)

        box.Add(self.panel,1,wx.GROW)
        self.SetSizerAndFit(box,False)
        self.panel.SetAutoLayout(1)
        self.statusBar = wx.StatusBar(self, 1, wx.STB_DEFAULT_STYLE)
        self.SetStatusBar(self.statusBar)
        self.input_structure  = parent.input_structure
        
        def __del__():
            print "destroying CAE menu"
            parent.refresh()
            parent.Enable()
            parent.SetFocus()
               
        self.Bind(wx.EVT_WINDOW_DESTROY, __del__)
                              
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