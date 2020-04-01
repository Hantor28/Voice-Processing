from tkinter import Tk, Label, Button, Text
import tkinter as tk
from tkinter import filedialog, Menu, Frame, ttk
from tkinter.font import Font
import sys
import pyaudio
import wave
import os
import re 

#Cat doan van thanh tung cau
def split_text(text):
    pat1 = re.compile(r"[.]\n+|\n")
    pat2 = re.compile(r"[.]+\s|\n")
    with open(text, "r", encoding='utf-8') as f:
        texts = f.read()
    blocks = re.split(pat1, texts)
    result = []
    for block in blocks:
        result += re.split(pat2, block)
    result = [res for res in result if res != '']
    return result

def open_file():
    label_count['text'] = '0'
    save_label['text'] = f"Saved {label_count['text']}.wav"
    save_label.pack_forget()
    file_name = filedialog.askopenfilename(initialdir = "./text", title = "Select file", filetypes = (("text files","*.txt"),("all files","*.*")))
    if file_name:
        text = split_text(file_name)
        total_sens['text'] = str(len(text))
        text_label['text'] = '@@'.join(text)
        lines = [str(i) + ".wav\n" + t for i, t in enumerate(text)]
        if not os.path.isdir(file_name[:-3]): os.mkdir(file_name[:-3])
        save_folder['text'] = file_name[:-3]
        with open(file_name[:-3]+"/Textdata.txt", "w", encoding='utf-8') as f:
            f.write('\n'.join(lines))
        sentence['text'] = label_count['text'] + ".wav >> " + text_label['text'].split('@@')[int(label_count['text'])]

def onExit():
    p.terminate()
    sys.exit()

#Thu am va luu file wav
chunk = 1024  
sample_format = pyaudio.paInt16  
channels = 2
fs = 44100 
p = pyaudio.PyAudio()  
end = False

def record():
    if label_count['text'] != total_sens['text'] and label_count['text'] != '-1':
        save_label.pack_forget()
        buttonRec.pack_forget()
        buttonStop.pack(side='left', padx=3)
        stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
        print('Recording')
        frames = []
        def listen():
            global end
            if not end:
                data = stream.read(chunk)
                frames.append(data)
                window.after(1, listen)
            else:
                stream.stop_stream()
                filename = save_folder['text'] + "/" + label_count['text']
                wf = wave.open(filename+".wav", 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(sample_format))
                wf.setframerate(fs)
                wf.writeframes(b''.join(frames))
                wf.close()
                end = False
        listen()

#Cau tiep     
def next_sentences():
    save_label.pack_forget()
    if label_count['text'] != total_sens['text']:
        label_count['text'] = str(int(label_count['text']) + 1)
        save_label['text'] = f"Saved {label_count['text']}.wav"
    if label_count['text'] == total_sens['text']:
        sentence['text'] = "Done"
    else:
        sentence['text'] = label_count['text'] + ".wav >> " + text_label['text'].split('@@')[int(label_count['text'])]

#Cau truoc
def pre_sentences():
    save_label.pack_forget()
    if label_count['text'] != '-1':
        label_count['text'] = str(int(label_count['text']) - 1)
        save_label['text'] = f"Saved {label_count['text']}.wav"
    else:
        sentence['text'] = label_count['text'] + ".wav >> " + text_label['text'].split('@@')[int(label_count['text'])]

#Dung lai
def stop():
    save_label.pack()
    print(save_label['text'])
    buttonStop.pack_forget()
    buttonRec.pack(side='left', padx=3)
    global end

    print('Finished recording')
    end = True

#Cua so giao dien
window = Tk()
screen_width = window.winfo_screenwidth()
screen_heihgt = window.winfo_screenheight()
window.title("Recorder Speech Processing")
window.geometry(f"800x480+{screen_width//2 - 400}+{screen_heihgt//2 - 250}")
window.resizable(0, 0)
window.configure(background='white')

font = Font(family='Helvetica')

bottomframe0 = Frame(window)
bottomframe0.pack(side='top', pady=1)

buttonOpenfile = Button(bottomframe0, text="Open File", width=15, height=1, relief='solid', fg='black', bg="#008080", command=open_file)
buttonOpenfile['font'] = font
buttonOpenfile.pack(side='left', padx=3)


label_count = Label(text='0')
total_sens = Label(text='0')
save_folder = Label()
text_label = Label()
save_label = Label(window, text=f"Saved {label_count['text']}.wav")

sentence = Label(bg='white', wraplength=780, anchor='w', justify='left', height=12)
sentence['font'] = font
sentence.pack(side='top')

# create button
bottomframe1 = Frame(window)
bottomframe1.pack(side='bottom', pady=2)

buttonRec = Button(bottomframe1, text="Record", width=15, height=1, relief='solid', fg='black', bg="#008080", command=record)
buttonRec['font'] = font
buttonRec.pack(side='left', padx=3)

buttonStop = Button(bottomframe1, text="Stop", width=15, height=1, relief='solid', fg='black', bg="#c0c0c0", command=stop)
buttonStop['font'] = font

bottomframe2 = Frame(window)
bottomframe2.pack(side='bottom', pady=3)

buttonPre = Button(bottomframe2, text="Previous", width=15, height=1, relief='solid', fg='black', bg="#00ff00", command=pre_sentences)
buttonPre['font'] = font
buttonPre.pack(side='left', padx=3)

buttonNext = Button(bottomframe2, text="Next", width=15, height=1, relief='solid', fg='black', bg="#00ff00", command=next_sentences)
buttonNext['font'] = font
buttonNext.pack(side='left', padx=3)

window.mainloop()