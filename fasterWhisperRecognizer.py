### Same test rendition as whisperRecognizer.py but with the faster_whisper library
### They boast better performance by 4x
from faster_whisper import WhisperModel
import os as os
import pyaudio
from colorama import Fore
import wave

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

model = WhisperModel('tiny', device='cuda', compute_type='float16')
FORMAT = pyaudio.paInt16 #audio encoding format 16 bit signed int
RATE = 16000 # sample rate, 16000-22000 is good enough for speech
CHANEL = 1 # The number of audio channels being managed
CHUNK = 1024 # Number of audio frames before buffer creation
temp_file_location = "C:/Users/JWald/Documents/PythonProjects/deleteme.wav"

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
    
    wvfile = wave.open(temp_file_location, "wb")
    wvfile.setnchannels(1)
    wvfile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wvfile.setframerate(RATE)
    wvfile.writeframes(b''.join(frames))
    wvfile.close()

def transcribe_audio():
    segments, _ = model.transcribe(temp_file_location, beam_size=5, language='en', prefix="You said:\n")
    transcription = ""
    for segment in segments:
        transcription += segment.text + " "
    return transcription.strip()

def transcribe_frankestein():
    segments = model.transcribe("C:/Users/JWald/Downloads/Frankenstein.mp3", beam_size=5, language="en")
    for segment in segments:
        print(segment)

def main():
    # transcribe_frankestein()
    try:  
        while True:
            record_audio()
            words = transcribe_audio()
            print(words)
            if len(words) != 0 and words[-1] == 'Okay.':
                print("we did the okay spam stopping the program")
                break
            os.remove(temp_file_location)
    except KeyboardInterrupt:
        print("Pressed a button")
        pass
    finally:
        print("Completed")
    
        
if __name__ == "__main__":
    main()