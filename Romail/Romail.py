from email import message
import imghdr
from msilib.schema import File
from tkinter import *
import smtplib
from email.message import EmailMessage
from tkinter import filedialog
import ssl
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
buttons_visible = False
def vali_pilt():
    global File
    File = filedialog.askopenfilename()
    l_lisatud.config(text=File)
    return File

def saada_kiri():
    kellele = email_entry.get("1.0", END).strip()
    kiri = kiri_entry.get("1.0", END)
    teema = teema_entry.get("1.0", END).strip()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "ihavearm0@gmail.com"
    password = "kavf mpsp qxje cmat"

    context = ssl.create_default_context()

    msg = EmailMessage()
    msg.set_content(kiri)
    msg["Subject"] = teema
    msg["From"] = sender_email
    msg["To"] = kellele


    progress_label.config(text="Sending...")
    progress_bar.place(x=130, y=342)  
    progress_label.place(x=131, y=315) 
    progress_bar.start(10)    

    try:
        if File:
            with open(File, "rb") as f:
                file_data = f.read()
                file_type = imghdr.what(None, file_data)
                file_name = File.split("/")[-1]
                msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(sender_email, password)
            smtp.send_message(msg)
            messagebox.showinfo("Informatsioon", "Kiri oli saadetud!")

    except Exception as e:
        messagebox.showerror("Error", f"Viga: {e}")

    finally:
        progress_bar.stop()  
        progress_label.config(text="")  

def open_secret_mode():
    
    secret_window = Toplevel()  
    secret_window.title("Secret Mode")
    secret_window.geometry("700x700")

    
    gif_image = Image.open("ultra_secret.jpg") 
    gif_photo = ImageTk.PhotoImage(gif_image)

    gif_label = Label(secret_window, image=gif_photo)
    gif_label.image = gif_photo  
    gif_label.pack()

def clear_form():
    email_entry.delete("1.0", END)
    teema_entry.delete("1.0", END)
    kiri_entry.delete("1.0", END)
    global File
    File = ""
    l_lisatud.config(text="No file selected")

def toggle_theme():
    current_color = aken.cget("bg")
    if current_color == "lightblue":
        new_bg = "lightgray"
        button_color = "lightcoral"
    else:
        new_bg = "lightblue"
        button_color = "SystemButtonFace" 

    aken.configure(bg=new_bg)
    for widget in aken.winfo_children():
        if isinstance(widget, (Button, ttk.Button, Label, Text)):
            try:
                widget.configure(bg=new_bg)
            except:
                pass
        if isinstance(widget, Button):
            widget.configure(bg=button_color)

def toggle_extra_buttons():
    global buttons_visible
    if not buttons_visible:
        clear_button.place(x=5, y=340)
        secret_mode.place(x=5, y=370)
        theme_button.place(x=5, y=310)
        toggle_button.config(text="Скрыть доп. кнопки")
        buttons_visible = True
    else:
        clear_button.place_forget()
        secret_mode.place_forget()
        theme_button.place_forget()
        toggle_button.config(text="Показать доп. кнопки")
        buttons_visible = False

aken = Tk()
aken.title("E-kirja saatmine")
aken.geometry("400x400")
aken.configure(bg="lightblue")
aken.resizable(width=False, height=False)
aken.iconbitmap("mail.ico")


email = Label(aken, text="  Email:", bg="lightgreen", font=("Arial", 16), fg="black", width=10)
email_entry = Text(aken, bg="lightgreen", font=("Arial", 16), fg="black", width=21, height=1)

teema = Label(aken, text="  Teema:", bg="lightgreen", font=("Arial", 16), fg="black", width=10)
teema_entry = Text(aken, bg="lightgreen", font=("Arial", 16), fg="black", width=21, height=1)

lisa = Label(aken, text="  Lisa:", bg="lightgreen", font=("Arial", 16), fg="black", width=10)
kiri = Label(aken, text="  Kiri:", bg="lightgreen", font=("Arial", 16), fg="black", width=10)
kiri_entry = Text(aken, bg="lightgreen", font=("Arial", 16), fg="black", width=21, height=10)

lisa_pilt = ttk.Button(aken, text="Lisa Pilt", command=vali_pilt)
saada = ttk.Button(aken, text="Saada", command=saada_kiri)

l_lisatud = Label(aken, text="No file selected", font=("Arial", 8), bg="lightgreen")


progress_label = Label(aken, text="", bg="lightgreen", font=("Arial", 12), fg="black")
progress_bar = ttk.Progressbar(aken, orient="horizontal", length=200, mode="indeterminate")

secret_mode=Button(aken, text="Secret mode", command=open_secret_mode,bg="green",fg="white")#FIUwHNEIUEBWIUGBEWIUB
clear_button = Button(aken, text="Очистить форму", command=clear_form,bg="green",fg="white")

theme_button = Button(aken, text="Сменить тему", command=toggle_theme,bg="green",fg="white")
toggle_button = Button(aken, text="Показать доп. кнопки", command=toggle_extra_buttons, bg="lightgreen")


toggle_button.place(x=1, y=280)
l_lisatud.place(x=150, y=80)
saada.place(x=250, y=370)
lisa_pilt.place(x=150, y=370)
kiri_entry.place(x=130, y=120)
kiri.place(x=1, y=160)
lisa.place(x=1, y=80)
email_entry.place(x=130, y=3)
email.place(x=1, y=1)
teema_entry.place(x=130, y=40)
teema.place(x=1, y=40)


progress_bar.place_forget()
progress_label.place_forget()
aken.mainloop()


