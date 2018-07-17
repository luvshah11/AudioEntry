import wx

class Node(wx.TextCtrl):
    def __init__(self, *args, **kw):
        super(Node, self).__init__(*args, **kw)
        print "Node"
        self.nodesizer = wx.FlexGridSizer(cols= 2, vgap = 1, hgap = 1)
        self.popButton = wx.Button(self, wx.ID_ANY, "K", wx.DefaultPosition, (10,10))
        self.next = None
        self.prev = None
        self.val = None
        self.point = self.GetPosition()



class DubList(wx.Frame):
    def __init__(self, *args, **kw):
        super(DubList, self).__init__(*args, **kw)
        self.listWindow = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL, "list window")
        self.listOfNodes = []
        self.mysizer = wx.GridBagSizer(5,5)
        
        button = wx.Button(self.listWindow, wx.ID_ANY, "push new node",wx.DefaultPosition + (150,0), wx.DefaultSize, 0 , wx.DefaultValidator, "make")
        button.Bind(wx.EVT_BUTTON, self.buttonDown, button)

        button0 = wx.Button(self.listWindow, wx.ID_ANY, "pop last node",wx.DefaultPosition + (260,0),wx.DefaultSize,wx.BU_EXACTFIT, wx.DefaultValidator, "take")
        button0.Bind(wx.EVT_BUTTON, self.button0Down, button0)

        print hex(id(button.Sizer))
        print hex(id(button0.Sizer))

        self.mysizer.Add(button, (0,1), (0,0), 0, 1, None)
        self.mysizer.Add(button0,(1,1), (0,0), 0, 0, None)
        self.mysizer.Layout()
        self.mysizer.Fit(self)
        
        

    def buttonDown(self, event):
        print "pressed"
        namestring = "button"
        
        if len(self.listOfNodes) is not 0:
            firstNode = self.listOfNodes[0]
            
            while firstNode.next is not None:
                firstNode = firstNode.next
               
            namestring += str(len(self.listOfNodes))    
            create = Node(self.listWindow, wx.ID_ANY,namestring,firstNode.point + (0,25), wx.DefaultSize, 0, wx.DefaultValidator, namestring)
            firstNode.next = create
        else:
            namestring += str(len(self.listOfNodes))
            create = Node(self.listWindow, wx.ID_ANY,namestring, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, namestring)
            
        
        self.mysizer.Add(create,(len(self.listOfNodes),0))
        self.listOfNodes.append(create)
        self.mysizer.Layout()
        self.mysizer.Fit(self)
  
    def button0Down(self, event):
        print "popping"
        if len(self.listOfNodes) is not 0:
            lastNode = self.listOfNodes[len(self.listOfNodes) - 1] #grab last node
            try:
                lastNode.prev.next = None
            except:
                print"no list"

            self.mysizer.Detach(lastNode)
            self.listOfNodes.remove(lastNode)
            lastNode.Destroy()
            self.mysizer.Layout()





       

def main():
    print "main"
    app = wx.App()
    frame = DubList(None, wx.ID_ANY, "test", wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE, "first window")
    frame.Show()
    app.MainLoop()
if __name__ == '__main__':

    main()
