import pyaudio
import wave
import os



__FORMAT = pyaudio.paInt16
__CHANNELS = 2
__RATE = 44100
__CHUNKS = 1024
__DEFAULT_RECORD_SECOND = 5
__WAV_OUTPUT_FILE = 'UserNameRecord'





def GetSound(_Seconds = -1):
    _Seconds = _Seconds if _Seconds != -1 else __DEFAULT_RECORD_SECOND

    audio = pyaudio.PyAudio()

    # Start Recording
    stream = audio.open(
        format=__FORMAT,
        channels=__CHANNELS,
        rate=__RATE,
        input=True,
        frames_per_buffer=__CHUNKS
    )
    
    print('Recording...')

    frames = []
    for i in range(0, int(__RATE / __CHUNKS * _Seconds)):
        data = stream.read(__CHUNKS)
        frames.append(data)
    
    print('Finished...')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return (frames, audio)




def Save_Sound(_Sound, _File_Path):
    waveFile = wave.open(_File_Path, 'wb')
    waveFile.setnchannels(__CHANNELS)
    waveFile.setsampwidth(_Sound[1].get_sample_size(__FORMAT))
    waveFile.setframerate(__RATE)
    waveFile.writeframes(b''.join(_Sound[0]))
    waveFile.close()
