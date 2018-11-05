from __future__ import absolute_import
from __future__ import print_function
import six

import language_check

from tkinter import *
from tkinter import messagebox


import rake
import operator
import io

counter=1
file=open("questions.txt","r")
q=[line.rstrip('\n') for line in file]
totmark=[0,0,0,0,0,0]

def nex():
    global counter
    if(counter<6):
        counter=counter+1
        ques.set(str(q[counter-1]))
        
    else:
        messagebox.showwarning("Limit Exceeded","Sorry, No more questions available!")
    #print(counter)

def prev():
    global counter
    if(counter>1):
        counter=counter-1
        ques.set(str(q[counter-1]))
    else:
        messagebox.showwarning("Limit Exceeded","This is the first question!")
    #print(counter)

def finish():
    
    s=0
    for i in totmark:
        s=s+i
    messagebox.showinfo("Total Score","The total score obtained in the test="+str(s)+"/40")
        

def enFunc():
    
    global counter
    
    ans = entry.get('1.0','end')
    n=0
    for line in ans:
        words=[line.split(' ') for line in ans]
    n=len(words)
    if(counter==1 or counter==2):
        if(n>=850):
            marks1=10
        elif(n>=400):
            marks1=5
        else:
            marks1=3
            
    else:
        if(n>=250):
            marks1=10
        elif(n>=100):
            marks1=5
        else:
            marks1=3
    a=marks1
    
    fname="data/docs/mp"+str(counter)+".txt"


    stoppath = "data/stoplists/SmartStoplist.txt"

    rake_object = rake.Rake(stoppath)
    sample_file = io.open(fname, 'r',encoding="iso-8859-1")
    text = ans

    sentenceList = rake.split_sentences(text)

    #for sentence in sentenceList:
     #   print("Sentence:", sentence)

    stopwords = rake.load_stop_words(stoppath)
    stopwordpattern = rake.build_stop_word_regex(stoppath)
    phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern, stopwords)
    #print("Phrases:", phraseList)

    wordscores = rake.calculate_word_scores(phraseList)

    keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
    """for candidate in keywordcandidates.keys():
        print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))

    sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
    totalKeywords = len(sortedKeywords)

    for keyword in sortedKeywords[0:int(totalKeywords/3)]:
        print("Keyword: ", keyword[0], ", score: ", keyword[1])"""

    keyw=dict(rake_object.run(text))
    print(keyw)
    #l1=len(keyw)
    
    
    print(fname)
    f1=io.open(fname, 'r',encoding="iso-8859-1")
    text1=f1.read()
    que=text1.split("\n")
    print(que[0])
    l=text1.split("\n\n")
    kw=l[2].split("\n")
    print("keyword in original file=",kw)
    total=len(kw)
    print("No of keywords in original file=",total)

    c=0
    for i in keyw:
        for j in range(0,total):
            if(kw[j].lower() in i.lower()):
                print("Detected= " +str(i))
                c=c+1
    print("count=",c)

    
    percentage=(c/total)*100

    if(percentage>=90):
        marks2=30
        message = "Marks obtained for keyword:" + str(marks2) + "/30"

    elif(percentage>=80 and percentage<90):
        marks2=28
        message = "Marks obtained for keyword:"+ str(marks2) + "/30"

    elif(percentage>=70 and percentage<80):
        marks2=26
        message = "Marks obtained for keyword:" + str(marks2) + "/30"

    elif(percentage>=60 and percentage<80):
        marks2=24
        message = "Marks obtained for keyword:" + str(marks2) + "/30"

    elif(percentage>=50 and percentage<60):
        marks2=28
        message = "Marks obtained for keyword:" + str(marks2) + "/30"

    elif(percentage>=40 and percentage<50): 
        marks2=25
        message = "Marks obtained for keyword:" + str(marks2) + "/30"
        
    else:
        marks2 = 0
        message = "Marks obtained for keyword:" + str(marks2) + "/30"
   
    mes2text = "\nMarks for length = " + str(a) + "/10" + "\nLength = " + str(n)
    print(mes2text)
    print(message)
    b=marks2



    tool=language_check.LanguageTool('en-US')

    count=0
    text=str(ans)
    txtlen=len(text.split())
    setxt = set(text.split())
    setlen = len(setxt)
    matches=tool.check(text)
    #print("Error:",matches)
    print("No. of Errors=",len(matches))
    noOfError=len(matches)
    for i in range (0,noOfError):
        print(matches[i].msg)
    
    if (noOfError<=3 and n>0):
        marks3=10
    elif (noOfError<=5):
        marks3=8
    elif (noOfError<=8):
        marks3=5
    else:
        marks3=3
    print("Marks obtained after parsing=",marks3,"/10")
    c=marks3
    d=a+b+c

    print("Marks obtained out of 50 is=",d,"/50")
    if(counter==1 or counter==2):
        tot=(d/50)*12
    else:
        tot=(d/50)*4
    m="\nMarks obtained for this question is"+str(tot)
    messagebox.showinfo("Result",m)
    global totmark
    totmark[counter-1]=tot


root = Tk()
root.geometry('800x1800')
label= Label(root,text="ANSWER ALL THE FOLLOWING QUESTIONS",bg="lightyellow",bd=20)
label.place(x=300,y=10)

ques= StringVar()
ques.set(str(q[counter-1]))
labelQ=Label(root,textvariable=ques,text=str(q[0]),width=100, bg="lightyellow", bd=20)
labelQ.place(x=10,y=100)

entry= Text(root)
entry.place(x=100,y=200)

prevBtn= Button(root, text = '<', command = prev)
prevBtn.place(x=120,y=600)

button1= Button(root, text = 'Submit', command = enFunc)
button1.place(x=400,y=600)

nextBtn= Button(root, text = '>', command = nex)
nextBtn.place(x=700,y=600)

finishbtn=Button(root,text='Finish',command=finish)
finishbtn.place(x=400,y=650)

root.mainloop()

