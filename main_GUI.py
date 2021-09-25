import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from api import api
from sentiment_Analysis.sentiment import sentiment
import time
# from guiWait import guiWait
import webbrowser
import tltk
from n_gram.prob import prob


sentiment = sentiment()
sentiment.tran()

print("train complete !!")

root = tk.Tk()
print(root.winfo_screenmmwidth() , " ",root.winfo_screenheight())
root.option_add("*Font", "AngsanaUPC 15")
root.geometry("+30+30")
root.title("โปรแกรมตรวจสอบข่าว (Project NLP02)")


contrainer = Frame(root)
contrainer.grid(row=0, column=0,pady=10,padx=40,sticky=NW)

topframe = Frame(contrainer)
topframe.grid(row=0, column=0,pady=10,sticky=NW)
subTopframe = Frame(topframe)
subTopframe.pack(side=BOTTOM)

centerframe = Frame(contrainer)
centerframe.grid(row=1, column=0)

butomframe = Frame(contrainer )
butomframe.grid(row=2, column=0,pady=10,sticky=NW)

righFrame = Frame(root)
righFrame.grid(row=0,column=1,pady=10,sticky=NW)

all_entries=[]
total_subtopfram = []
currectPage = 1
totalResults = 0

def openweb(event):
    do = event.widget["textvariable"]
    print(do)

    if(str(do)=="ok"):
        print("state ok")
    webbrowser.open(str(do))

def doPage(e):
    global currectPage
    do = e.widget["text"]
    if(do=="ก่อนหน้า"):
        if(currectPage <= 1):
            messagebox.showinfo("information","ไม่มีหน้าก่อนหน้าแล้าวจร้า")
        else:
            currectPage = currectPage - 1
            search()
    elif(do =='ถัดไป'):
        if(currectPage*10<totalResults):
            currectPage = currectPage + 1
            search()
        else:
            messagebox.showinfo("information", "อยุ่หน้าสุดท้ายแล้วจร้า")


def switch_tag():

    global check_tag
    if(check_tag==True):
        check_tag = False
        buton_tran.config(text='tran off', fg='red')
    else:
        check_tag = True
        buton_tran.config(text='tran on', fg='green')
    search()

fist = True
changsecondTime =[]
check_tag = True
def search():
    global fist
    if(fist == True):
        btnBefor = Button(butomframe, text='ก่อนหน้า')
        btnBefor.pack(side=LEFT,padx=15)
        btnBefor.bind("<Button-1>",doPage)
        changsecondTime.append(btnBefor)

        page = Label(butomframe, text =currectPage)
        page.pack(side=LEFT,padx=2)
        changsecondTime.append(page)

        btnnext = Button(butomframe, text='ถัดไป')
        btnnext.pack(side=LEFT,padx=15)
        btnnext.bind("<Button-1>", doPage)
        changsecondTime.append(btnnext)

        fist = False
    else:
        for i in changsecondTime:
            i.pack_forget()
        btnBefor = Button(butomframe, text='ก่อนหน้า')
        btnBefor.pack(side=LEFT, padx=15)
        btnBefor.bind("<Button-1>", doPage)
        changsecondTime.append(btnBefor)

        page = Label(butomframe, text=currectPage)
        page.pack(side=LEFT, padx=2)
        changsecondTime.append(page)

        btnnext = Button(butomframe, text='ถัดไป')
        btnnext.pack(side=LEFT, padx=15)
        btnnext.bind("<Button-1>", doPage)
        changsecondTime.append(btnnext)

    keyword = str(e1.get()).strip()
    category = tran[variable.get()]
    print(keyword)
    print(category)
    ss = api()
    data = ss.getAPI(keyword, "10",str(currectPage), category)

    for i in total_subtopfram:
        i.pack_forget()
    total = data['totalResults']
    global totalResults
    totalResults = total

    data_start = ((currectPage - 1) * 10) + 1
    data_stop =data_start + len(data['articles'])-1

    label_total = Label(subTopframe,text="ข่าวที่ "+str(data_start)+
                        "-"+str(data_stop)+" จากทั้งหมด "+str(total)+" ข่าว",justify=LEFT)
    label_total.pack(side=LEFT)
    total_subtopfram.append(label_total)
    # print(json.dumps(data, indent=2, ensure_ascii=False))

    if (data['status'] == 'ok'):

        for i in all_entries:
            i.destroy()

        if(data["articles"]!=[]):
            row = 0
            for data in data['articles']:
                # print(data['title'])

                if(check_tag==True):
                    ss = sentiment.analysis(str(data['description']) + str(data['title']))
                    print(ss[1])
                    if (ss[1] == 'pos'):
                        color = 'green'
                        tag = 'POS'
                    else:
                        color = 'red'
                        tag = 'NEG'

                # print(len(data['title']))
                # numlengt = 90
                # if(len(data['title'])<=numlengt):
                #     data_show = data['title']
                # elif(len(data['title'])>numlengt):
                #     data_show = str(data['title'][0:numlengt])+"..."

                label_news = Label(centerframe , text="- " + data['title'],justify=LEFT, bg='green',
                            wraplength=1000)
                label_news.grid(row=row, column=0,pady=1,sticky=NW)
                all_entries.append(label_news)

                if(check_tag==True):
                    tagnews = Label(centerframe, text=tag,fg=color)
                    tagnews.grid(row=row, column=1,pady=1,sticky=NW)
                    all_entries.append(tagnews)

                btnSearch = Label(centerframe, textvariable=str(data['url']), text=" click",
                                  borderwidth=2,fg='blue',cursor="target")
                btnSearch.grid(row=row, column=2,pady=1,sticky=NW)
                btnSearch.bind("<Button-1>", openweb)
                all_entries.append(btnSearch)

                row =row+1
        else:
            print("null")
            label_news = Label(centerframe, text="ไม่มีข้อมูล", bg='yellow', wraplength=1000)
            label_news.pack(side=TOP, anchor=W, pady=1)
            all_entries.append(label_news)
    elif (data['status'] == 'error'):
        print("Error")
        label_news = Label(centerframe, text=data['message'], bg='yellow', wraplength=1000)
        label_news.pack(side=TOP, anchor=W, pady=1)
        all_entries.append(label_news)

    else:
        print("Error to connect")




label1 = Label(topframe, text='ค้นหา :')
label1.pack(side=LEFT,padx=1)

totol_nextWord= []
def callback(sv):
    # print(sv.get())
    try:
        for i in totol_nextWord:
            i.destroy()

        sentence = str(sv.get())
        subb = tltk.nlp.pos_tag(sentence)[0]
        last = subb[len(subb)-2][0]
        # print(last)

        getNextword = prob().getnextWord(last)
        print(getNextword)
        for word in getNextword:
            nextWord = Label(righFrame, text=word)
            nextWord.pack()
            totol_nextWord.append(nextWord)

        del subb
    except Exception as e:
        print(e)

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))

e1 = Entry(topframe, textvariable=sv)
e1.pack(side=LEFT,padx=1)






tran = {
    "ทั้งหมด": "",
    'ความบันเทิง': "entertainment",
    'ธุรกิจ': "business",
    'วิทยาศาสตร์': "science",
    'สุขภาพ': "health",
    'ทั่วไป': "general",
    'กีฬา': "sports",
    'เทคโนโลยี': "technology"
}

key = [key for key in tran]
variable = tk.StringVar(contrainer)
variable.set(key[0])
opt = tk.OptionMenu(topframe, variable, *key)
opt.config(width=10)
opt.pack(side=LEFT,padx=1)

btn1 = Button(topframe, text='ค้นหา', command=search)
btn1.pack(side=LEFT,padx=1)


time1 = ''
clock = Label(righFrame, fg='green',font=('AngsanaUPC', 20, 'bold'))
clock.pack(padx=15,pady=10)
buton_tran = Button(righFrame,text='tran (on)',fg='green',command=switch_tag)
buton_tran.pack(padx=15,pady=10)

def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(1000, tick)
tick()

contrainer.mainloop()
