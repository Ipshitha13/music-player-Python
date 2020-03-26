import os
import sys
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import threading
from mutagen.mp3 import MP3
from pygame import mixer
import playsound
import time
import datetime


win=tk.ThemedTk()
win.get_themes()
win.set_theme("clearlooks")

#Fonts- Arial,(corresponds to Helvetical), Courier New(Courier), Comic Sans MS, Fixedsys, MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana 
#Styles-bold, italic, overstrike styles

statusbar=ttk.Label(win,text="Welcome to Melody",relief=SUNKEN,anchor=W,font='Times 15 italic bold')
statusbar.pack(side=BOTTOM, fill=X)#side takes top,left,top,bottom, X=x-axis it covers

#create menu
menubar=Menu(win)
win.config(menu=menubar) #config=used to stick to top of the page 

#create sub-menu
subMenu=Menu(menubar,tearoff=0)

playlist=[] 
#it contains the fullpath+filename  #playlist box-it contains just the filenmae
#fullpath+filename is required to play inside play_music load function
#filename-- contains poathof the file
#f-- filename

def browse_file():
    global filename
    filename=filedialog.askopenfilename()
    add_to_palylist(filename)

def add_to_palylist(f):
    f=os.path.basename(f)
    index=0
    playlistbox.insert(index,f)
    playlist.insert(index,filename)
    playlistbox.pack()
    #index++


menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open", command= browse_file)
subMenu.add_command(label="Exit", command=win.destroy)

def about_us():
    tkinter.messagebox.showinfo("About Melody","This is a music player using python tkinter by Ipshitha...")
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init() #initializing
win.title('Melody')
win.iconbitmap(r'melody.ico')#r=raw file


#win - statusbar, leftframe, rightframe
#leftframe- listbox
#rightframe- topframe, middleframe, bottomframe

leftframe=Frame(win)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox=Listbox(leftframe)
playlistbox.pack()

addbtn=ttk.Button(leftframe, text="+ Add", command=browse_file)
addbtn.pack(side=LEFT)

def del_song():
    slected_song=playlistbox.curselection()
    selected_song=int(slected_song[0])
    playlistbox.delete(slected_song)
    playlist.pop(selected_song)

deletebtn=ttk.Button(leftframe,text="-Delete",command=del_song)
deletebtn.pack(side=RIGHT)

rightframe=Frame(win)
rightframe.pack(pady=10)

topframe=Frame(rightframe)
topframe.pack()

#.wav files
lengthlabel=ttk.Label(topframe,text='Total length: --:--', font='Verdana 14 overstrike')
lengthlabel.pack(pady=10)

currenttimelabel=ttk.Label(topframe,text='Current time: --:--',relief=GROOVE, font='Verdana 13 overstrike')
currenttimelabel.pack()


def show_details(play_song):
    file_data=os.path.splitext(play_song)
    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.sound(play_song)
        total_length=a.get_length()

    #div- total_length/60, mod-total_length%60
    mins,secs= divmod(total_length,60)  
    mins=round(mins)
    secs=round(secs)
    timef='[:02d]:[:02d]'.format(mins,secs)
    lengthlabel['text']="Total length"+'-'+timef
    
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    #current_time=0
    #mixer.music.get_busy()-returns false when we press the stop button and music stops palying
    #continue- Ignores all of the statements below it. We check if music is paused ot not.
    while t and mixer.music.get_busy(): #current_time<=t -- for music coming from back
        if paused:
            continue
        else:
            mins,secs= divmod(t,60)
            mins=round(mins)
            secs=round(secs)
            timef='[:02d]:[:02d]'.format(mins,secs)
            currenttimelabel['text']="Current time"+'-'+timef
            time.sleep(1)
            t-=1 # music come back 
            #current_time+=1- music starts from 00:00

    

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text']="Music resumed"
        paused=FALSE
    else: 
        try:
            stop_music()
            time.sleep(1)
            slected_song=playlistbox.curselection()
            selected_song=int(slected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Playing music: "+''+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("File not found", "Melody not found. please check again...")


def stop_music():
    mixer.music.stop()
    statusbar['text']="Music stopped"

paused=FALSE

def pause_music(): 
    global paused
    paused=TRUE
    mixer.music.pause()
    statusbar['text']="Music paused"

def rewind_music():
    play_music()
    statusbar['text']="Music rewinded"

def set_vol(val):
    volume=int(float(val)/100)
    mixer.music.set_volume(volume)

muted=FALSE

def mute_music():
    global muted
    if muted:  #unmute the music 
        mixer.music.set_volume(0.7)
        volumebtn.configure(image=volumephoto)
        scale.set(70)
        statusbar['text']="Music is set to minimum volume"
        muted=FALSE
    else: #mute the music 
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        scale.set(0)
        statusbar['text']="Music muted"
        muted=TRUE

#back layout manager- arranging buttons,padding, division of frames
#grid layout manager- arrange widgets, buttons in th rows and columns..
#back and grid layout manager cannot be used at the same time.. But we can use both at the same time by using FRAMES...

middleframe=Frame(rightframe)#,relief=RAISED, borderwidth=1)#for division of the three buttons below
middleframe.pack(padx=10,pady=30)

playphoto=ImageTk.PhotoImage(file='run.png')
playbtn=Button(middleframe,image=playphoto,command=play_music)
playbtn.grid(row=0,column=0,padx=10)

stopphoto=ImageTk.PhotoImage(file='stop.png')
stopbtn=Button(middleframe,image=stopphoto,command=stop_music)
stopbtn.grid(row=0,column=1,padx=10)

pausephoto=ImageTk.PhotoImage(file='pause.png')
pausebtn=Button(middleframe,image=pausephoto,command=pause_music)
pausebtn.grid(row=0,column=2,padx=10)

bottomframe=Frame(rightframe)
bottomframe.pack()

rewindphoto=ImageTk.PhotoImage(file='rewind.png')
rewindbtn=Button(bottomframe,image=rewindphoto,command=rewind_music)
rewindbtn.grid(row=0,column=0)

mutephoto=ImageTk.PhotoImage(file='mute.png')
volumephoto=ImageTk.PhotoImage(file='volume.png')
volumebtn=Button(bottomframe,image=volumephoto,command=mute_music)
volumebtn.grid(row=0,column=1)


scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(70) #70-this is to implement the default value
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,padx=30,pady=15)


def on_closing():
    stop_music()
    tkinter.messagebox.showinfo('Note',"You want to exit")
    win.destroy()
win.protocol("WM_DELETE_WINDOW",on_closing)
win.mainloop()  