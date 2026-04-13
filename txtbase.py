import tkinter as tk
import os

userinfo = ""


def getinfo():
    global userinfo
    userinfo = field.get("1.0", tk.END).strip()
    print(userinfo)


def save():
    global statustxt

    if not userinfo:
        statustxt = "write something first"
        update_status(statustxt, is_error=True)
        return

    folder_path = field2.get("1.0", tk.END).strip()
    filename = field3.get("1.0", tk.END).strip() + ".txt"

    if not folder_path:
        update_status("Enter folder path", is_error=True)
        return

    if not filename:
        update_status("Enter file name", is_error=True)
        return

    folder_path = folder_path.strip('"\'').strip()
    filename = filename.strip('"\'').strip()

    if not filename.endswith('.txt'):
        filename = filename + '.txt'

    path = os.path.join(folder_path, filename)


    try:

        if not os.path.exists(folder_path):
            update_status(f"Folder does not exist: {folder_path}", is_error=True)
            return

        if not os.access(folder_path, os.W_OK):
            update_status(f"No permission to write to: {folder_path}", is_error=True)
            return

        with open(path, "w", encoding="utf-8") as file:
            file.write(userinfo)

        statustxt = f"File saved:\n{path}"
        update_status(statustxt, is_error=False)
        print(f"saved in: {path}")

    except PermissionError:
        update_status(f"Permission denied!\n{folder_path}", is_error=True)
    except Exception as e:
        update_status(f"error: {e}", is_error=True)
        print(f"error: {e}")


def update_status(message, is_error=False):
    if is_error:
        status_label.config(text=message, fg="red")
    else:
        status_label.config(text=message, fg="green")

    window.after(3000, reset_status)


def reset_status():
    status_label.config(text="Listening", fg="gray")


window = tk.Tk()
window.title("test")
window.geometry("450x700")
window.resizable(width=False, height=False)


label = tk.Label(window, text="TEXTBOOK", font=('Arial', 14, 'bold'))
label.pack(pady=10)

field = tk.Text(window, height=10, width=50)
field.pack(pady=10)

button2 = tk.Button(window, text="WRITE", command=getinfo, bg="lightblue", width=15)
button2.pack(pady=5)

button1 = tk.Button(window, text="SAVE", command=save, bg="lightgreen", width=15)
button1.pack(pady=5)

pathtext = tk.Label(window, text="Enter folder path:", font=('Arial', 10))
pathtext.pack(pady=(20, 5))

field2 = tk.Text(window, height=1, width=50)
field2.pack(pady=5)


filenametxt = tk.Label(window, text="Enter file name:", font=('Arial', 10))
filenametxt.pack(pady=(10, 5))

field3 = tk.Text(window, height=1, width=50)
field3.pack(pady=5)

status_label = tk.Label(window, text="listening", fg="gray", wraplength=400)
status_label.pack(pady=20)

window.mainloop()
