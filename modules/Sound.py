from playsound import playsound
import os


__Sound_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Sounds/'



def Wait_Instructions():
    playsound(__Sound_Dir + 'Wait.mp3', True)



def FingerPrint_Instructions():
    playsound(__Sound_Dir + 'PutYourFinger.mp3', True)


def FingerPrintAuthFaild():
    playsound(__Sound_Dir + 'FingerPrintAuthFaild.mp3')


def PutYourFingerAgain():
    playsound(__Sound_Dir + 'PutYourFingerAgain.mp3')


def Temperature_Instructions():
    playsound(__Sound_Dir + 'Temprature.mp3', True)



def AuthenticatedUser_Instructions():
    playsound(__Sound_Dir + 'AuthenticatedUser.mp3')



def UnAuthenticatedUser_Instructions():
    playsound(__Sound_Dir + 'UnAuthenticatedUser.mp3')


def GetUserFrontPicture_Instructions():
    playsound(__Sound_Dir + 'GetUserFrontPicture.mp3')


def GetUserRightPicture_Instructions():
    playsound(__Sound_Dir + 'GetUserRightPicture.mp3')


def GetUserLeftPicture_Instructions():
    playsound(__Sound_Dir + 'GetUserLeftPicture.mp3')


def DoneImageCapture_Instructions():
    playsound(__Sound_Dir + 'DoneImageCapture.mp3')


def Alarm_Sound():
    playsound(__Sound_Dir + 'AlarmSound.mp3')


def CameraCapture_Sound():
    playsound(__Sound_Dir + 'CameraCaptureSound.mp3')


def RegisterFingerPrint_Instructions():
    playsound(__Sound_Dir + 'RegisterFingerPrint.mp3')


def SayYourName_Instructions():
    playsound(__Sound_Dir + 'SayYourName.mp3')


def WelcomeMessage_Instructions():
    playsound(__Sound_Dir + 'WelcomeMessage.mp3')



def NormalTemp_Instructions():
    playsound(__Sound_Dir + 'NormalTemp.mp3')


def NotNormalTemp_Instructions():
    playsound(__Sound_Dir + 'NotNormalTemp.mp3')


def FingerPrintRegistered_Instructions():
    playsound(__Sound_Dir + 'FingerPrintRegistered.mp3')


def YourNameRegistered_Instructions():
    playsound(__Sound_Dir + 'YourNameRegistered.mp3')


def ShowPicture_Sound():
    playsound(__Sound_Dir + 'ShowPicture.mp3', False)


def CardIdImage_Instruction():
    playsound(__Sound_Dir + 'CardIdImage.mp3')


def DoneIdCardCapture_Instruction():
    playsound(__Sound_Dir + 'DoneIdCardCapture.mp3')
