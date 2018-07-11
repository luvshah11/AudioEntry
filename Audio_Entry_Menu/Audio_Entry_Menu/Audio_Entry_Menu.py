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
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "mainPanel")
        #self.SetScrollbar(self)
        #members
        self.holding_list = []
        self.channelList = []
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
        self.holding_list = self.holding_list[:-1]
        self.makeAudioPanel(self.holding_list)
        self.makeToolBar()
        self.makeButtons()
    

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
        dictWindow = CreateDictionaryWindow(self)
        dictWindow.Show()
        print "creating dictionary"

    def onExit(self,event):
        self.Close()

    def onSave(self, event):
        print "saving"
        yaml_dump(self.input_structure)

    def makeAudioPanel(self, in_string):
        choicebox_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (430,36), (390,45))
        channel_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Channel: ", (20,36), (390,45))
        self.channelbox = wx.Choice(self.panel,1, (25,50), (380,25), in_string)
        self.choicebox = wx.Choice(self.panel,1,(435,50), (380,25))
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
        print "\nYou selected: ",self.finalFileList[self.choicebox.GetCurrentSelection()]
        print self.choicebox.GetSelection()
        self.finalFileSelection = self.finalFileList[self.choicebox.GetSelection()]
        #print sub_list[self.finalFileSelection]

    def makeButtons(self):
        print "making buttons"
        playButton = wx.Button(self.panel, 1, "Play", (830,50), (35,25), name = "playButton")
        editButton = wx.Button(self.panel, 1, "Edit", (875,50), (35,25), name = "editButton")
        deleteBttn = wx.Button(self.panel, 1, "Delete", (920,50), (45,25), name = "deleteBttn")        

        #bind script to buttons
        self.Bind(wx.EVT_BUTTON, self.buttonEventHandler, playButton)
    
    def refresh(self):
        self.choicebox.Clear()
        self.finalFileList = []
        x = 0
        key_list = self.input_structure["Audio"].keys()
        key_list = key_list[:-1]
        sub_list = self.input_structure["Audio"][key_list[self.channelbox.GetCurrentSelection()]]
        displayString = []
        while x < len(sub_list):
            self.finalFileList.append(sub_list[x]["file"])
            x += 1
        print "sucess"
        self.finalFileList.sort()
        self.choicebox.SetItems(self.finalFileList)
        self.channelbox.SetSelection(wx.NOT_FOUND)
        self.choicebox.SetSelection(wx.NOT_FOUND)
        self.choicebox.Clear()
        print "end"

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
            self.dletBttnFunc(self.finalFileList[self.choicebox.GetCurrentSelection()])  


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
        super(CreateAudioEntryWindow, self).__init__(parent, title = "Create Audio Entry", pos = (250,250), size = (580,350))
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "panel for edit")

        self.SetBackgroundColour('Gray')
        parent.Disable()
        self.SetFocus() 
        self.finalDict = parent.input_structure
        temp = self.finalDict["Audio"]
        self.key_list = self.finalDict["Audio"].keys()
        self.key_list = self.key_list[:-1]

        #list
        self.listChoice = wx.Choice(self.panel,1, (125,30), (350,25), self.key_list)

        #entries
        
        self.keyEntry = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (125,66), size = (350,25),name = "keyE")
        self.fileEntry = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (125,121), size = (350,25), name= "fileE")
        self.VolEntry = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (125,176), size = (90,25))
        self.duckEntry = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (125,231), size = (90,25))
        self.unduckEntry = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (255,231), size = (220,25))
        
        #disable for now, enable once you make a selection in listCHoice
        self.keyEntry.Disable()
        self.fileEntry.Disable()
        self.VolEntry.Disable()
        self.duckEntry.Disable()
        self.unduckEntry.Disable()

        #text labels
        list_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "List: ", (120,16), (360,45))
        keyName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (120,52), (360,45))
        fileName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "File: ", (120,107), (360,45))
        volume_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Volume: ", (120,162), (100,45))
        duck_SBOX= wx.StaticBox(self.panel, wx.ID_ANY, "Duck: ", (120,217), (100,45))
        unduck_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Unduck Duration Offset: ", (250,217), (230,45))

        #buttons
        self.okButton = wx.Button(self.panel, 1, "OK", (425,176), (50,25), name = "okButton")
        self.okButton.Disable()

        #Status Bar
        self.isKeyEntered = False
        self.isFileEntered = False
        status = wx.StatusBar(self, 1, wx.STB_DEFAULT_STYLE, "helooooo")
        self.SetStatusBar(status)
        self.SetStatusText("Enter data and press OK | Key/File are required, other data fields can be left blank")


        #bind list box to function, to enable text feilds 
        self.Bind(wx.EVT_CHOICE, self.enableTextCtrl, self.listChoice)
        self.Bind(wx.EVT_BUTTON, self.addToDict, self.okButton)

        def __destroy(_):
                print "destroying CAE menu"
                parent.refresh()
                parent.Enable()
                parent.SetFocus()
               
        self.Bind(wx.EVT_WINDOW_DESTROY, __destroy)  
        self.Bind(wx.EVT_TEXT,self.enableButton, self.keyEntry)
        self.Bind(wx.EVT_TEXT,self.enableButton, self.fileEntry)
        #disable OK button until Key and File are modified
        
    def enableButton(self, event):
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

        if(self.isKeyEntered and self.isFileEntered):
            self.okButton.Enable()
        else:
            self.okButton.Disable()

    def enableTextCtrl(self, event):
        self.keyEntry.Enable()
        self.fileEntry.Enable()
        self.VolEntry.Enable()
        self.duckEntry.Enable()
        self.unduckEntry.Enable()


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

class CreateDictionaryWindow(wx.Frame):

    def __init__(self, parent, id=1, title="", pos= wx.DefaultPosition, size = wx.DefaultSize, style = ~wx.RESIZE_BORDER, name = ""):
        super(CreateDictionaryWindow, self).__init__(parent, title = "Create Dictionary", pos = (250,250), size = (580,350))
        self.panel = wx.Panel(self, 1,pos = wx.DefaultPosition, size= self.GetSize(), style = wx.TAB_TRAVERSAL, name= "panel for edit")
        self.NodeList = []

        class EntryRow:
            def __init__(self, xpos, ypos, parentpanel):
                print "making an EntryRow object"
                self.posx = xpos
                self.posy = ypos
                self.next = None
                self.prev = None
                self.renderPanel = parentpanel

                plusBitMap = wx.Bitmap("greenplus1.png", wx.BITMAP_TYPE_PNG)
                xBitmap = wx.Bitmap("redx1.png", wx.BITMAP_TYPE_PNG)

                self.addButton = wx.Button(self.renderPanel, 1, pos =(self.posx-4, self.posy + 9), size = (14,14), name = "addButton")
                self.addButton.SetBitmapLabel(plusBitMap)

                self.removeButton = wx.Button(self.renderPanel, 2, pos =(self.posx-4, self.posy + 22), size = (14,14), name = "removeButton")
                self.removeButton.SetBitmapLabel(xBitmap)



                self.keyEntry = wx.TextCtrl(self.renderPanel, wx.ID_ANY, pos = (self.posx + 10, self.posy + 10), size = (100,25),name = "keyE")
                self.channelEntry = wx.TextCtrl(self.renderPanel, wx.ID_ANY, pos = (self.posx + 120, self.posy + 10), size = (100,25),name = "channelE")
                self.delayEntry = wx.TextCtrl(self.renderPanel, wx.ID_ANY, pos = (self.posx + 230, self.posy + 10), size = (100,25),name = "delayE")
                self.actionEntry = wx.TextCtrl(self.renderPanel, wx.ID_ANY, pos = (self.posx + 340, self.posy + 10), size = (100,25),name = "actyionE")

                print "success"


        newEntry = EntryRow(40,10,self.panel)
        
        self.NodeList.append(newEntry)
        #sec = EntryRow(40,45,self.panel)#down (25{heigt of textctr} + 10 for space)
        #thi = EntryRow(40,80,self.panel)
        #fou = EntryRow(40,115,self.panel)


        self.SetFocus()
        #keyName_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Key: ", (30,30), (150,45))
        #channel_SBOX = wx.StaticBox(self.panel, wx.ID_ANY, "Channel: ", (190,30), (150,45))
        #delay_SBOX =   wx.StaticBox(self.panel, wx.ID_ANY, "Delay: ", (350,30), (150,45))
        def pushNew(self, prevNode_x, prevNode_y):
            print "creating new row"



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