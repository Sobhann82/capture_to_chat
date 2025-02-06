import cv2
import pytesseract as ps
from ollama import Client
import tkinter as tk
from tkinter import scrolledtext, ttk, Label
from PIL import Image, ImageTk

ps.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
imagePath = "Screenshot 2024-12-29 211103.png"
def text_recognition(image_path):
   image = cv2.imread(image_path)
   resized_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
   resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
   config = r'--oem 3 --psm 6 -l fas'
   text = ps.image_to_string(resized_image, lang='fas')
   return text

def take_picture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():  # بررسی اینکه آیا دوربین باز شده است
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()  # گرفتن یک فریم تصویر

    if not ret:  # بررسی اینکه آیا فریم با موفقیت گرفته شده است
        print("Error: Could not read frame.")
        cap.release()
        return

    cv2.imwrite('captured_image.jpg', frame)  # ذخیره عکس
    print("Image saved as 'captured_image.jpg'")
    return 'captured_image.jpg'

output = ''
def image_to_text():
    text = text_recognition(take_picture())
    print(text)
    return text

def response_to_picture():

    output_text.delete('1.0', tk.END)
    client = Client(host="http://localhost:11434")
    response = client.chat(model='qwen2.5', messages=[
        {
            'role': 'user',
            'content': str(image_to_text()),
        }
    ])
    output = response['message']['content']
    print(output)
    output_text.insert(tk.END, output+'\n', 'right')


window = tk.Tk()
window.title("Camera Capture and Text Extractor")
window.geometry("400x500")  # اندازه پنجره
window.configure(bg="#f0f0f0")  # رنگ پس زمینه

# عنوان
title_label = Label(window, text="Image Capture and Text Extraction", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

video_label = Label(window, width=320, height=240, bg="black")  # پس‌زمینه مشکی برای نشان دادن ویدیو بهتر
video_label.pack(pady=10)

# استایل دکمه
style = ttk.Style()
style.configure("TButton", borderwidth=1, relief="flat", padding=10, background="#ADD8E6")  # آبی ملایم
style.map("TButton", background=[("active", "#87CEEB"), ("pressed", "#4682B4")])  # تغییر رنگ در حالت‌های مختلف

button = ttk.Button(window, command=response_to_picture, text="Capture Image")
button.pack(pady=10)

output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=8,font=("Calibri", 12))  # تغییر فونت به Calibri
output_text.pack(pady=10)
output_text.tag_configure('right', justify='right')

# ایجاد دوربین و نمایش ویدیو
video_source = 0
vid = cv2.VideoCapture(video_source)

def update():
    # خواندن فریم از دوربین
    ret1, frame = vid.read()
    if ret1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        frame = cv2.resize(frame, (320, 240))

        # تبدیل فریم به تصویر PIL
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        # نمایش تصویر در برچسب
        video_label.config(image=photo)
        video_label.image = photo
    video_label.after(10, update)


update()

window.mainloop()

if vid.isOpened():
    vid.release()
