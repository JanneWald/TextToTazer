# Basic translation test bed for the whisper library


import whisper
import pyaudio
from colorama import Fore
import wave
import os


# Model Setup
model = whisper.load_model("base.en")
FORMAT = pyaudio.paInt16 #audio encoding format 16 bit signed int
RATE = 16000 # sample rate, 16000-22000 is good enough for speech
CHANEL = 1 # The number of audio channels being managed
CHUNK = 1024 # Number of audio frames before buffer creation

temp_file = "C:/Users/JWald/Documents/PythonProjects/deleteme.wav"

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANEL, rate=RATE, frames_per_buffer=CHUNK, input=True)
    
    print(Fore.RED + "Recording" + Fore.WHITE)
    
    frames = []
    for _ in range(0, int(RATE/CHUNK)): # amount of frames captured in one second
        data = stream.read(CHUNK)
        frames.append(data)
    
    print(Fore.GREEN + "Completed Recording" + Fore.WHITE)
    
    # Stream management
    # stream.stop_stream()
    # stream.close()
    # audio.terminate()
    
    wvfile = wave.open(temp_file, "wb")
    wvfile.setnchannels(1)
    wvfile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wvfile.setframerate(RATE)
    wvfile.writeframes(b''.join(frames))
    wvfile.close()

def transcribe_audio():
    words =  model.transcribe(temp_file)
    return words

# Do anthing with this
def main():
    try:  
        while True:
            record_audio()
            words = transcribe_audio().get('text')
            print(words)
            if len(words) != 0 and words[-1] == 'Okay.':
                print("we did the okay spam stopping the program")
                break
            os.remove(temp_file)
    except KeyboardInterrupt:
        pass
    finally:
        print("pressed a button")
    
        
if __name__ == "__main__":
    main()