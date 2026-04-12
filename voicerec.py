import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pathlib import Path
import time
frames = []
stop = False
print("MICROPHONE TEST")
print("1. start recording\n2. settings\n3. exit")

sample_rate = 16000

def recordingtime():
    print("recording was started")
    rec = sd.rec(int(time*sample_rate), samplerate=sample_rate, channels=1)

    sd.wait()
    print("recording was finished")
    file_name = input("enter the file name: ")
    if not file_name.endswith('.wav'):
        file_name = file_name + '.wav'
    done = path / file_name
    write(done, sample_rate, rec)
def recordingwout():
    frames = []
    stop = False
    def call(indata, *args):
        nonlocal stop
        if not stop:
            frames.append(indata.copy())

    print("recording was started")

    stream = sd.InputStream(samplerate=sample_rate, channels=1, callback=call, dtype='int16')
    stream.start()
    input()
    stop = True
    stream.stop()
    stream.close()

    if frames:
        result = np.concatenate(frames)
        duration = len(result) / sample_rate

        file_name = input("\nEnter file name: ")
        if not file_name.endswith('.wav'):
            file_name += '.wav'

        file_path = path / file_name
        write(str(file_path), sample_rate, result)

        print(f"\nSaved: {file_path}")
        print(f"Duration: {duration:.1f} seconds")
    else:
        print("Nothing was recorded!")
    print("recording was finished")

def settingup():
    print("\n1. chose your devise\n2. change sample\n3. exit")
    setinp = int(input("\nenter the setting: "))
    if setinp == 1:
        print("\nfind your input device in the list below: ")
        time.sleep(1)
        print(sd.query_devices())
        chose1 = int(input("\nenter your device number: "))
        sd.default.device = chose1
    elif setinp == 2:
        global sample_rate

        print("\nNOTE: 8000 is low quality\n16000 is medium quality\n22050 is high quality\n44100 is very high quality")
        print(f"your current sample rate is: {sample_rate}")
        time.sleep(0.5)
        sample_rate = int(input("\nenter new sample rate: "))
    elif setinp == 3:
        return
def pathcheck():
    global path
    try:
        path = Path(input("\nenter the file path: "))
    except:
        return

x = 0
while x == 0:
    userinput = int(input("\nenter your choice: "))
    if userinput == 1:
        pathcheck()

        time = int(input("enter the time: "))
        if time > 0:
            recordingtime()
        elif time <= 0:
            recordingwout()
    elif userinput == 2:
        settingup()
    elif userinput == 3:
        exit()
    print("1. start recording\n2. settings\n3. exit")

