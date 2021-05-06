import tkinter
from PIL import Image, ImageTk
import time




class LockScreen:

    __Is_Active = True
    __Logo = None

    def __init__(self, Window):
        self.__Window = Window
        self.__PanelWindow = tkinter.PanedWindow(self.__Window, bd=4, orient=tkinter.VERTICAL, relief='raised')

        #self.__Name_Label = tkinter.Label(self.__PanelWindow, justify='center')
        #self.__Name_Label.config(text='المعهد الفنى للقوات المسلحة', font='times 50')
        #self.__Name_Label.pack()

        self.__Logo = ImageTk.PhotoImage( Image.open("Logo.png") )
        self.__Logo_Label = tkinter.Label(self.__PanelWindow, image=self.__Logo, justify='center')
        
        
        #self.__Date_Label = tkinter.Label(self.__PanelWindow, justify='center')
        #self.__Date_Label.pack()

        self.__Time_Label = tkinter.Label(self.__PanelWindow, width=60, fg='#952E18')
        

        #self.__PanelWindow.add(self.__Name_Label)
        self.__PanelWindow.add(self.__Logo_Label)
        #self.__PanelWindow.add(self.__Date_Label)
        self.__PanelWindow.add(self.__Time_Label)




    def Start(self):
        self.__Logo_Label.pack()
        self.__Time_Label.pack()

        self.RaiseEvent('LockScreen')

        self.__UpdateClock()
    

    def __UpdateClock(self):
        Time = time.strftime('%I:%M:%S',time.localtime())
        if Time != "":
            self.__Time_Label.config(text=Time, font='times 50')
            #self.__Date_Label.config(text=today.strftime("%d/%m/%Y"), font='times 50')
        
        self.__PanelWindow.after(100, self.__UpdateClock)
    

    def Add(self):
        self.__Is_Active = True
        self.__PanelWindow.pack(fill=tkinter.BOTH, expand=1)


    def Remove(self):
        self.__Is_Active = False
        self.__PanelWindow.pack_forget()
