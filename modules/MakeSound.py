from gtts import gTTS
from playsound import playsound


MyObj = gTTS(text='تم إلتقاط صورة تحقيق الشخصية بنجاح', lang='ar', slow=False, lang_check=True)

MyObj.save('DoneIdCardCapture.mp3')
