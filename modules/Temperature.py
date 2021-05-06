import random
import serial

#__Ser = serial.Serial('COM3', 9600)



def GetTemperature():
    return __Real_Temperature() if False else __Fake_Temprature()



def Is_Normal(_Temp):
    return True if 38 >= float(_Temp) >= 33 else False



def __Real_Temperature():
    global __Ser

    try:
        if not __Ser.isOpen():
            __Ser.open()
        __Ser.write(b'#')
        __Ser.flushInput()
        return str(__Ser.readline().decode()[1:])

    except Exception as e:
        print(e)



def __Fake_Temprature():
    return 36
