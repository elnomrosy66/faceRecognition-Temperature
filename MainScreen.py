import tkinter
from PIL import Image, ImageTk
import cv2
import imutils
import face_recognition
import threading
from playsound import playsound
from time import sleep
from modules import ImageProcessing
import numpy as np
from modules import Sound
from modules import Temperature
from modules import SoundProccessing
from modules import fingerprint
import random
from modules import Database
import imutils
import os
from modules.card_detection.id_card_detection_camera import Detect_Card
import string





class MainScreen:
    #exec(open("modules/card_detection/id_card_detection_camera.py").read())
    __Photo = None
    __Is_Active = False
    __Frame_Counter = 0

    __Instructions = False
    __Captured = ()
    __Origin_Frame = None

    __User_Image = None
    __User_Name = None
    __ShowPicture_Sound = False

    __FramesCounter = 0

    __SleepModeCounter = 0

    __Counter = 0



    __Capture_Image = 0
    __Front_Image = None
    __Left_Image = None
    __Right_Image = None


    __Capture_Id_Card_Image = False
    __Captured_Id_Card_Image = False
    __Id_Card_Image = None


    __Break_All_Instructions = False


    __Current_Dir = os.path.dirname(os.path.abspath(__file__))


    def __init__(self, Window):

        self.__Window = Window

        self.__PanelWindow = tkinter.PanedWindow(self.__Window, bd=4, orient=tkinter.VERTICAL, relief='raised')

        self.__Camera = cv2.VideoCapture(0)
        
        # TOP Frame
        self.__Top_Frame = tkinter.Frame(self.__PanelWindow)
        self.__Top_Frame.grid(column=0 , row = 0)

        # Logo Image
        self.__Photo = ImageTk.PhotoImage( Image.open("Logo.png").resize((70, 70), Image.ANTIALIAS) )## The (250, 250) is (height, width)
        self.__Logo_Label = tkinter.Label(self.__Top_Frame, image=self.__Photo )
        self.__Logo_Label.grid(column = 1 , row =  0 , sticky="W")

        # Title
        self.__Title_Label = tkinter.Label(self.__Top_Frame, text='المعهد الفني للقوات المسلحة', font='times 50')
        self.__Title_Label.grid(column = 0 , row =  0)


        # Body Frame
        self.__Body_Frame = tkinter.Frame(self.__PanelWindow)
        self.__Body_Frame.grid(column = 0 , row = 1)

        # Image Screen
        self.__ImagePicture = tkinter.Label(self.__Body_Frame)
        self.__ImagePicture.grid(column=0, row=0, sticky="W")
    


    def __Update_Frame(self):
        _, frame = self.__Camera.read()

        frame = self.__ProccessImage(frame)

        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)


        self.__ImagePicture.configure(image=frame)
        self.__ImagePicture.image = frame
        self.__ImagePicture.after(1, self.__Update_Frame)
    

    def __ProccessImage(self, _frame):

        #### Take User Image Proccess ####
        if self.__Capture_Image != 0:
            
            if self.__Capture_Image == 1:
                self.__Front_Image = _frame
            elif self.__Capture_Image == 2:
                self.__Left_Image = _frame
            else:
                self.__Right_Image = _frame

            self.__Capture_Image = 0
        

        #### Take User Card Id Image ####
        if self.__Capture_Id_Card_Image:
            self.__Id_Card_Image = _frame
            self.__Captured_Id_Card_Image = True
        

        _Origin_Frame = _frame.copy()
        _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
        (_frame, Faces_Loc) = ImageProcessing.DetectFacesAndDrow(_frame)


        if not self.__Is_Active:
            if len(Faces_Loc) > 0:
                self.__Frame_Counter = 1
                self.__Is_Active = True
                self.RaiseEvent('Camera')
        else:
            if not self.__Instructions:
                if len(Faces_Loc) > 0:
                    if self.__Frame_Counter < 5:
                        self.__Frame_Counter += 1
                    else:
                        self.__Frame_Counter = 0
                        self.__Instructions = True
                        self.__Break_All_Instructions = False
                        self.__Captured = (_frame, Faces_Loc)
                        self.__Origin_Frame = _Origin_Frame
                        threading.Thread(target=self.__StartInstructions).start()
                else:
                    self.__Frame_Counter = 0
                    if self.__SleepModeCounter < 30:
                        self.__SleepModeCounter += 1
                    else:
                        self.__SleepModeCounter = 0
                        self.__Is_Active = False
                        self.RaiseEvent('LockScreen')

        _frame = cv2.resize(_frame, (1900, 980), interpolation=cv2.INTER_AREA)
        

        #### User Is Authenticated ####
        if self.__User_Name:
            if not self.__ShowPicture_Sound:
                self.__ShowPicture_Sound = True
                #Sound.ShowPicture_Sound()
            
            CamFrame = cv2.resize(_frame.copy(), (950, 980))

            Card_Image = cv2.imread(self.__User_Image)
            Card_Image = cv2.cvtColor(Card_Image, cv2.COLOR_BGR2RGB)
            Card_Image = cv2.resize(Card_Image, (950, 980))

            _frame[0: 980, 0: 950] = CamFrame
            _frame[0: 980, 950: 1900] = Card_Image

        return _frame

    


    def Start(self):
        self.__Update_Frame()

    def Add(self):
        self.__Is_Active = True
        self.__PanelWindow.pack(fill=tkinter.BOTH, expand=1)

    def Remove(self):
        self.__Is_Active = False
        self.__PanelWindow.pack_forget()


    def __StartInstructions(self):
        #### Begin Instructions ####
        #Sound.Wait_Instructions()
        #start recognizing after 20 frame with face detection
        _User, _Image = ImageProcessing.Recognize(self.__Captured)

        sleep(2)

        #_User = 'UnKnown User'
        self.__Authenticated_User_Instructions(_User, _Image) if _User != 'UnKnown User' else self.__UnAuthenticated_User_Instructions()
        sleep(5)

        #### End Instructions ####
        self.__Instructions = False
    

    def __Authenticated_User_Instructions(self, _User, _Image):
        #### Take Finger Print ####
        Sound.FingerPrint_Instructions()
        sleep(3)
        if fingerprint.Get_FingerPrint() == _User:

            #sound 'لم تتم المطابقة'
            Sound.FingerPrintAuthFaild()
            return
            #start to recognize face again (start from begining)
        else:

            #### Put User Image ####
            self.__User_Name = _User
            self.__User_Image = _Image

            #### Authenticated User confirmed ####
            Sound.AuthenticatedUser_Instructions()

            sleep(1.5)

            #### Take Temperature ####
            Sound.Temperature_Instructions()
            _Temp = Temperature.GetTemperature()

            #### Save Into Database ####
            Db = Database.GetDatabase("SqlServer")
            Db.Connect()
            Db.Insert("INSERT INTO Attendence (User_Card_id, Temperature) VALUES(?, ?)", _User, _Temp)


            #### Handle Temperature ####
            if Temperature.Is_Normal(_Temp):
                Sound.NormalTemp_Instructions()
                Sound.WelcomeMessage_Instructions()
            else:
                Sound.NotNormalTemp_Instructions()
                
            
            #### Print User ####
            print(_User)
            sleep(5)


            #### Restart Configurations ####
            self.__User_Name = None
            self.__User_Image = None
            self.__ShowPicture_Sound = False


    def __UnAuthenticated_User_Instructions(self):
        Visitor_id = ''.join(random.choice(string.digits) for i in range(13))
        Visitor_Dir = self.__Current_Dir + '/images/' + str(Visitor_id)
        os.mkdir(Visitor_Dir)
        ImageProcessing.Save_Image(self.__Origin_Frame, Visitor_Dir + '/Image.jpg')


        #### Not Authenticated User ####
        Sound.UnAuthenticatedUser_Instructions()


        #### Take Front Image ####
        Sound.GetUserFrontPicture_Instructions()            
        Sound.Alarm_Sound()
        sleep(3)

        self.__Capture_Image = 1
        while self.__Capture_Image != 0: pass
        ImageProcessing.Save_Image(self.__Front_Image, Visitor_Dir + '/Front_Image.jpg')
        self.__Front_Image = None
        
        Sound.CameraCapture_Sound()
        sleep(0.5)
        


        #### Take Right Image ####
        Sound.GetUserRightPicture_Instructions()
        #Sound.Alarm_Sound()
        sleep(2)

        self.__Capture_Image = 3
        while self.__Capture_Image != 0: pass
        ImageProcessing.Save_Image(self.__Right_Image, Visitor_Dir + '/Right_Image.jpg')
        self.__Right_Image = None

        Sound.CameraCapture_Sound()
        sleep(0.5)
        

        
        #### Take Left Image ####
        Sound.GetUserLeftPicture_Instructions()
        #Sound.Alarm_Sound()
        sleep(2)

        self.__Capture_Image = 2
        while self.__Capture_Image != 0: pass
        ImageProcessing.Save_Image(self.__Left_Image, Visitor_Dir + '/Left_Image.jpg')
        self.__Left_Image = None

        Sound.CameraCapture_Sound()
        sleep(0.5)
        


        #### Done Image Capture ####
        Sound.DoneImageCapture_Instructions()
        sleep(0.5)


        #### Take Finger Print ####
        Sound.RegisterFingerPrint_Instructions()
        sleep(2)
        Sound.PutYourFingerAgain()
        fingerprint.Enrol_New(id = Visitor_id)

        sleep(3.5)
        

        #### Done Saving Finger Print ####
        Sound.FingerPrintRegistered_Instructions()
        sleep(2)



        #### Take Card Picture ####
        Sound.CardIdImage_Instruction()

        self.__Capture_Id_Card_Image = True
        threading.Thread(target=self.__TakeIdCardImage_Break).start()
        while True:
            if self.__Captured_Id_Card_Image and Detect_Card(self.__Id_Card_Image, Visitor_Dir + '/Id_Card.jpg'):
                break
            elif self.__Break_All_Instructions:
                return
        
        self.__Captured_Id_Card_Image = False
        self.__Capture_Id_Card_Image = False
        self.__Id_Card_Image = None
        Sound.DoneIdCardCapture_Instruction()



        #### Say Your Name ####
        Sound.SayYourName_Instructions()
        SoundProccessing.Save_Sound( SoundProccessing.GetSound(5), Visitor_Dir + '/UserNameSound.wav')
        Sound.YourNameRegistered_Instructions()
        


        #### Take Temperature ####
        Sound.Temperature_Instructions()
        sleep(2)
        _Temp = Temperature.GetTemperature()
        


        #### Handle Temerature ####
        if Temperature.Is_Normal(_Temp):
            Sound.NormalTemp_Instructions()
            Sound.WelcomeMessage_Instructions()
        else:
            Sound.NotNormalTemp_Instructions()
        

        
        #### Save Into Database ####
        Db = Database.GetDatabase('SqlServer')
        Db.Connect()
        Db.Insert('INSERT INTO [User]([Is_Visitor], [User_Card_id]) VALUES(?, ?)', 1, Visitor_id)
        Db.Insert('INSERT INTO [Attendence]([User_Card_id], [Temperature]) VALUES(?, ?)', Visitor_id, _Temp)
        

    

    def __TakeIdCardImage_Break(self):

        _Counter = 5

        while _Counter > 0:
            print(_Counter)
            sleep(5)
            if not self.__Capture_Id_Card_Image:
                return
            Sound.CardIdImage_Instruction()
            _Counter -= 1
        
        self.__Break_All_Instructions = True
        
