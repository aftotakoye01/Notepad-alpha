import tkinter as tk
import os
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write, read
import numpy as np
from pathlib import Path
import time
import threading
import soundfile as sf
workspaceph = None
mainfield = ""
is_recording = False
recording_frames = []
sample_rate = 16000
rec_file = ''


#update visual status
def reset_status():
    status_label.config(text="Listening", fg="gray")
#info from notebook
def getinfo():
    global mainfield
    mainfield = field.get("1.0", tk.END).strip()
    print(mainfield)
#save button
def save():
    global statustxt, workspaceph, mainfield

    if not mainfield:
        statustxt = "write something first"
        update_status(statustxt, is_error=True)
        return
    userfolder = field2.get("1.0", tk.END).strip()
    filename = field3.get("1.0", tk.END).strip()

    if not userfolder:
        update_status("Enter folder path", is_error=True)
        return

    if not filename:
        update_status("Enter file name", is_error=True)
        return
    userfolder = userfolder.strip('"\'').strip()
    filename = filename.strip('"\'').strip()

    if not filename.endswith('.txt'):
        filename = filename + '.txt'

    workspaceph = Path(userfolder)

    path = workspaceph / filename

    try:
        if not workspaceph.exists():
            update_status(f"Folder does not exist: {workspaceph}", is_error=True)
            return

        if not os.access(workspaceph, os.W_OK):
            update_status(f"No permission to write to: {workspaceph}", is_error=True)
            return

        with open(path, "w", encoding="utf-8") as file:
            file.write(mainfield)

        statustxt = f"File saved:\n{path}"
        update_status(statustxt, is_error=False)
        print(f"saved in: {path}")

    except PermissionError:
        update_status(f"Permission denied!\n{workspaceph}", is_error=True)
    except Exception as e:
        update_status(f"error: {e}", is_error=True)
        print(f"error: {e}")
#visual status
def update_status(message, is_error=False):
    if is_error:
        status_label.config(text=message, fg="red")
    else:
        status_label.config(text=message, fg="green")

    window.after(3000, reset_status)
#keybinds
def handle_combos(event):
    if not (event.state & 0x4):
        return

    widget = event.widget

    if event.keycode == 65:
        widget.tag_add('sel', '1.0', 'end')
        return "break"

    if event.keycode == 67:
        try:
            selected = widget.get('sel.first', 'sel.last')
            window.clipboard_clear()
            window.clipboard_append(selected)
        except:
            pass
        return "break"

    if event.keycode == 86:
        try:
            text = window.clipboard_get()
            text = text.rstrip('\n\r')
            widget.insert('insert', text)
        except:
            pass
        return "break"

    if event.keycode == 88:
        try:
            selected = widget.get('sel.first', 'sel.last')
            window.clipboard_clear()
            window.clipboard_append(selected)
            widget.delete('sel.first', 'sel.last')
        except:
            pass
        return "break"
    return
def playsound():
    global workspaceph
    for_read = workspaceph / rec_file
    if for_read.exists():
        sample_rate, data = read(str(for_read))
        sd.play(data, sample_rate)
        status_label.config(text="Playing", fg="blue")
        window.after(3000, reset_status)
    else:
        status_label.config(text="Dont exist", fg="red")
        window.after(3000, reset_status)
def setupactivate():
    global workspaceph
    global rec_file
    recordwindow = tk.Toplevel(window)
    recordwindow.geometry("300x300")
    recordwindow.resizable(width=False, height=False)
    recordwindow.title("RECORD")
    recordwindow.grab_set()
    recordwindow.transient(window)

    microimage = Image.open(r"C:\Users\helpp\OneDrive\Рабочий стол\NotePad++\Assets\Icons\microphone_800309.png")
    microimage = microimage.resize((80, 80))
    playimage = Image.open(r"C:\Users\helpp\OneDrive\Рабочий стол\NotePad++\Assets\Icons\free-icon-play-button-arrowhead-27223.png")
    playimage = playimage.resize((60, 60))

    micicon = ImageTk.PhotoImage(microimage)
    micbutton = tk.Button(recordwindow, image=micicon, bd=0, highlightthickness=0, command=start_stop_recording)
    micbutton.image = micicon
    micbutton.place(x=17, y=95)

    playicon = ImageTk.PhotoImage(playimage)
    play_button = tk.Button(recordwindow, image=playicon, bd=0, highlightthickness=0, command=playsound)
    play_button.image = playicon
    play_button.place(x=125, y=104)

    field4 = tk.Text(recordwindow, height=1, width=15)
    field4.place(x=90,y=200)
    rec_file = field4.get("1.0",tk.END).strip()
    rec_file = rec_file + ".wav"
#voice record
def start_stop_recording():
    global rec_file
    global workspaceph
    global is_recording, recording_data

    if not is_recording:
        is_recording = True
        recording_data = []
        print("started")
        status_label.config(text="Recording", fg="red")
        recording_data = sd.rec(int(10 * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    else:
        is_recording = False
        status_label.config(text="Saving", fg="orange")

        sd.stop()

        if len(recording_data) > 0:
            workspaceph.mkdir(parents=True, exist_ok=True)
            file_path = workspaceph / rec_file
            write(str(file_path), sample_rate, recording_data)
            print(f"saved in {file_path}")
            status_label.config(text="Saved: rectest.wav", fg="green")
            window.after(3000, reset_status)
        else:
            status_label.config(text="Nothing recorded", fg="red")
            window.after(3000, reset_status)

window = tk.Tk()
window.title("TEST")
window.geometry("450x700")
window.resizable(width=False, height=False)

label = tk.Label(window, text="TEXTBOOK", font=('Arial', 14, 'bold'))
label.place(x=220, y=10, anchor="n")

field = tk.Text(window, height=10, width=50)
field.place(x=25, y=50, width=400, height=162)

scroll = tk.Scrollbar(window, command=field.yview)
scroll.place(x=425, y=60, height=162)
field.config(yscrollcommand=scroll.set)

button2 = tk.Button(window, text="WRITE", command=getinfo, bg="lightblue", width=15)
button2.place(x=25, y=235)

button1 = tk.Button(window, text="SAVE", command=save, bg="lightgreen", width=15)
button1.place(x = 166, y = 235)

pathtext = tk.Label(window, text="Enter folder path:", font=('Arial', 10))
pathtext.place(x=25, y=280)
field2 = tk.Text(window, height=1, width=50)
field2.place(x=25, y=305, width=400, height=25)


filenametxt = tk.Label(window, text="Enter text file name:", font=('Arial', 10))
filenametxt.place(x=25, y=345)

field3 = tk.Text(window, height=1, width=50)
field3.place(x=25, y=370, width=400, height=25)

status_label = tk.Label(window, text="Listening", fg="gray", wraplength=400)
status_label.place(x=225, y=420, anchor="n")

betabutton = tk.Button(window, text="RECORD", command=setupactivate, bg = "red", width=15)
betabutton.place(x=365, y=235, anchor="n")


window.geometry("450x700")
window.resizable(width=False, height=False)

field.bind('<KeyPress>', handle_combos)
field2.bind('<KeyPress>', handle_combos)
field3.bind('<KeyPress>', handle_combos)

def focus_field2(event):
    field2.focus_set()

def focus_field3(event):
    field3.focus_set()

field2.bind('<Button-1>', focus_field2)
field3.bind('<Button-1>', focus_field3)
window.mainloop()
