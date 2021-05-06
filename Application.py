from LockScreen import LockScreen
from MainScreen import MainScreen
import tkinter




class Application:

    __FullScreenState = True

    
    def __init__(self):
        self.__Window = tkinter.Tk()
        self.__Window.attributes('-fullscreen', self.__FullScreenState)
        self.__Window.title('Identity Check')

        self.__Window.bind("<F11>", self.__ToggleFullScreen)
        self.__Window.bind("<Escape>", self.__QuitFullScreen)
        self.__Window.bind('<q>', self.__QuitApplication)


        self.__LockScreen = LockScreen(self.__Window)
        self.__LockScreen.RaiseEvent = self.RaiseEvent

        
        self.__MainScreen = MainScreen(self.__Window)
        self.__MainScreen.RaiseEvent = self.RaiseEvent
    

    def RaiseEvent(self, _Event):
        if _Event == 'LockScreen':
            self.__MainScreen.Remove()
            self.__LockScreen.Add()
        else:
            self.__LockScreen.Remove() 
            self.__MainScreen.Add()
    

    def __ToggleFullScreen(self, _Event):
        self.__FullScreenState = not self.__FullScreenState
        self.__Window.attributes('-fullscreen', self.__FullScreenState)
    

    def __QuitFullScreen(self, _Event):
        self.__Window.attributes('-fullscreen', False)
    

    def __QuitApplication(self, _Event):
        exit()


    def Start(self):
        self.__LockScreen.Start()
        self.__MainScreen.Start()
        self.__Window.mainloop()
