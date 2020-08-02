import os

from fingerprint.common import *
from fingerprint.jieba_cut import *

print(os.getcwd())

db=make_original_dataset()
init=False

aset=''
while True:
    change = False

    if init:
        print("Working on " + aset)
        ifchange=input("Change set? [yes]: ")
        if ifchange in "YyYesyesYES":
            change=True
        else:
            change=False


    if not init or change:
        aset0=input("Set:")

        if aset0 not in db:
            print("Wrong set name!")

            continue
        else:
            aset=aset0
            init = True
            change=False

    alist=db[aset]

    command=input('Command:')

    clist=command.split()
    try:
        if clist[0]=='url':
            for i in alist:
                if i[0]==clist[1]:
                    print(i[1])
                    break
        elif clist[0]=='title':
            for i in alist:
                if i[0]==clist[1]:
                    print(i[2])
                    break
        elif clist[0]=='txt':
            for i in alist:
                if i[0]==clist[1]:
                    print(i[3])
                    break
        elif clist[0]=='search':
            for i in alist:
                if clist[1] in i[3]:
                    print(i[0])
            print('Complete')
    except:
        print("Ignored")

