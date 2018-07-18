import wx
from wx.lib.scrolledpanel import ScrolledPanel

class DubList(wx.Frame):

    class Node(wx.TextCtrl):
               def __init__(self, parent, id, value, pos, size, style, validator, name, listPtr):
                   super(DubList.Node, self).__init__(parent, id, value, pos, size, style, validator, name)
                   print "Node"

                   self.nodesizer = wx.FlexGridSizer(cols= 2, vgap = 1, hgap = 1)
                   self.popButton = wx.Button(self, wx.ID_ANY, "K", wx.DefaultPosition, (11,11))
                   self.pushButton = wx.Button(self, wx.ID_ANY, "P", wx.DefaultPosition + (0,13), (11,11))
                   self.listManager = listPtr
                   self.next = None
                   self.prev = None
                   self.val = None
                   self.point = self.GetPosition()
           
                   self.Bind(wx.EVT_BUTTON, listPtr.onRemove,self.popButton)
                   self.Bind(wx.EVT_BUTTON, listPtr.onPush, self.pushButton)
        

    def __init__(self,parent, id, title, pos, size, style, name):
        super(DubList, self).__init__(parent, id, title, pos, size, style, name)
       
        masterSizer = wx.BoxSizer(wx.VERTICAL)
        #self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        #self.listWindow = scrolledpanel(self, wx.ID_ANY, self.Position, self.Size, wx.VSCROLL, "list window")
        self.listWindow = ScrolledPanel(self,wx.ID_ANY, self.GetPosition(),self.GetSize(),wx.TAB_TRAVERSAL | wx.VSCROLL, "list window")
        self.listWindow.SetupScrolling(0,1,0,20,1,1)
        
        #self.listWindow.SetScrollRate(5,5) not needced
        self.listOfNodes = []
        self.mysizer = wx.GridBagSizer(5,5)
        #self.mysizer = wx.BoxSizer(wx.VERTICAL)       

        button = wx.Button(self.listWindow, wx.ID_ANY, "push new node",wx.DefaultPosition + (150,0), wx.DefaultSize, 0 , wx.DefaultValidator, "make")
        button.Bind(wx.EVT_BUTTON, self.buttonDown, button)

        button0 = wx.Button(self.listWindow, wx.ID_ANY, "pop last node",wx.DefaultPosition + (260,0),wx.DefaultSize,wx.BU_EXACTFIT, wx.DefaultValidator, "take")
        button0.Bind(wx.EVT_BUTTON, self.button0Down, button0)

        #layout
        #self.mysizer.SetSizeHints(self.listWindow) not needed
        #self.mysizer.Add(button, 0,0,1,None)
        #self.mysizer.Add(button0, 0,0,1,None)

        self.mysizer.Add(button,(0,2),(0,0),0, 1,"addButton")
        self.mysizer.Add(button0,(2,2),(0,0),0, 1,"removeButton")

        self.listWindow.SetSizer(self.mysizer)
        self.mysizer.Fit(self.listWindow)
        
        self.listWindow.SetAutoLayout(1)


    def onRemove(self, event):
        button = event.GetEventObject()
        button = button.GetParent()
        print "middle pop", button.val
        self.listOfNodes.remove(button)
        self.mysizer.FitInside(self.listWindow)
        self.mysizer.Remove(button)
        button.Destroy()
        self.mysizer.Layout()



    def onPush(self,event):
        button = event.GetEventObject()
        button = button.GetParent()
        print "middle push", button.val
          
        

    def buttonDown(self, event):
        print "pressed"
        namestring = "button"
        # a list
        if len(self.listOfNodes) is not 0:
            firstNode = self.listOfNodes[0] # head of list
            
            while firstNode.next is not None: #iter until eol
                prev = firstNode.prev
                firstNode = firstNode.next
                
            namestring += str(len(self.listOfNodes))    
           #create = Node(self.listWindow, wx.ID_ANY,namestring,firstNode.point + (0,25), wx.DefaultSize, 0, wx.DefaultValidator, namestring)
            create = self.Node(self.listWindow, wx.ID_ANY,namestring,firstNode.point, wx.DefaultSize, 0, wx.DefaultValidator, namestring, self)
            create.val = len(self.listOfNodes)

            firstNode.next = create
            create.prev= firstNode
            # no list
        else:
            namestring += str(len(self.listOfNodes))
            create = self.Node(self.listWindow, wx.ID_ANY,namestring, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, namestring, self)
            create.val = len(self.listOfNodes)
            create.parent = self
        
        #self.mysizer.Add(create,0,0,1,namestring) #boxsizer add
        self.mysizer.Add(create,(1+ len(self.listOfNodes),1 ),(0,0),0,1, namestring)
        self.listOfNodes.append(create)
        self.mysizer.FitInside(self.listWindow)
        #self.listWindow.SetFocus()not needed 
        self.listWindow.ScrollChildIntoView(create)
        #self.listWindow.Refresh() not needed
        #self.listWindow.Update()  not needed
        #self.mysizer.Layout()     not needed


    def button0Down(self, event):
        print "popping"
        if len(self.listOfNodes) is not 0: 
            lastNode = self.listOfNodes[len(self.listOfNodes) - 1] #grab last node
            try:
                prev = lastNode.prev
                prev.next = None
            except:
                print"last node"

            self.mysizer.Detach(lastNode)
            self.listOfNodes.remove(lastNode)
            lastNode.Destroy()
            self.mysizer.FitInside(self.listWindow)
            self.mysizer.Layout()
        else:
            print "no list"





       

def main():
    print "main"
    app = wx.App()
    frame = DubList(None, wx.ID_ANY, "test", (50,50), (500,150), wx.DEFAULT_FRAME_STYLE, "first window")
    frame.Show()
    app.MainLoop()
if __name__ == '__main__':

    main()
