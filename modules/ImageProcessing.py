import cv2
import numpy as np
import face_recognition
import os
import pickle




_Main_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_Encodes = []

_Encode_List_Known = []
_Class_Names = []
_Training_Images_Paths = []
_Front_Images_Paths = []


with open(_Main_Dir + '/Faces_Encodings.enc', 'rb') as file:
    _Encodes = pickle.load(file)


for Item in _Encodes:
    _Encode_List_Known.append(Item['Encode'])
    _Class_Names.append(Item['ClassName'])
    _Training_Images_Paths.append(Item['TrainingImagePath'])
    _Front_Images_Paths.append(Item['ImagePath'])



def Training():

    global _Main_Dir

    _Traning = []
    
    with open( _Main_Dir + '/Faces_Encodings.enc', 'wb') as file:

        for Dir in os.listdir(_Main_Dir + '/images'):

            _Training_Image_Path = _Main_Dir + '/images/' + Dir + '/Image.jpg'
            _Image_Path = _Main_Dir + '/images/' + Dir + '/Front_Image.jpg'
            _Image = cv2.imread(_Training_Image_Path)
            _ClassName = Dir

            _Image = cv2.cvtColor(_Image, cv2.COLOR_BGR2RGB)
            _Encode = face_recognition.face_encodings(_Image)[0]

            _Traning.append({
                'ClassName': _ClassName,
                'Encode' : _Encode,
                'TrainingImagePath': _Training_Image_Path,
                'ImagePath': _Image_Path
            })
        
        pickle.dump(_Traning, file)

#Training()


def Recognize(_Captured):

    global _Encode_List_Known, _Class_Names, _Front_Images_Paths

    imgS = _Captured[0]
    Frame_Face_Loc = _Captured[1]
    Frame_Encode = face_recognition.face_encodings(imgS, Frame_Face_Loc)

    for encodeface, faceloc in zip(Frame_Encode, Frame_Face_Loc):
        matches = face_recognition.compare_faces( _Encode_List_Known, encodeface)
        faceDistance = face_recognition.face_distance( _Encode_List_Known, encodeface)
        #print(faceDistance)

        matchIndex = np.argmin(faceDistance)
        return (
            _Class_Names[matchIndex] if matches[matchIndex] else 'UnKnown User',
            _Front_Images_Paths[matchIndex] if matches[matchIndex] else None
        )



def DetectFacesAndDrow(_Frame):

    Faces_Loc = face_recognition.face_locations(_Frame)

    for faceloc in Faces_Loc:
        y1, x2, y2, x1 = faceloc
        cv2.rectangle(_Frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return (_Frame, Faces_Loc)



def Save_Image(_Frame, _Path):
    cv2.imwrite(_Path, _Frame)
