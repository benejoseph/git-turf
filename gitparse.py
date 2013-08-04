#!/usr/bin/python

import re

def parserecord(log):
    regexhash = 'commit[\s]+[a-f0-9]{20,}[^\n]'
    regexauthor = 'Author.*[^\n]'
    regexdate = 'Date.*[^\n]'

    temp = re.search(regexhash,log).group()
    temp = temp.split(' ')
    myhash = temp[1]

    temp = re.search(regexauthor,log).group()
    temp = temp.split(': ')[1]
    myauthor = temp.split('<')[0]

    temp = re.search(regexdate,log).group()
    temp = temp.split(': ')[1].strip()
    mydate = temp

    temp = re.search(mydate + '[\s\S]*',log).group()
    comments = temp.split(mydate)[1]

    lines = comments.split('\n')
    mycomment = ''
    mymods = []
    isfirst = True
    for line in lines:
        if line is not '':
            if isfirst:
                mycomment = line.strip()
                isfirst = False
            else:
                mymods.append(line)         
            

    data = {'hash' : myhash, 'author' : myauthor, 'date' : mydate, 'comment' : mycomment, 'mods' : mymods}

    return data


def parsegitlog(txt):
    regexheader = 'commit[\s]+[a-f0-9]{20,}\nAuthor.*\nDate.*\n'

    iter = re.finditer(regexheader,txt)
    indices = [m.start(0) for m in iter]
    indices.append(len(txt))

    records = []
    for j in range(len(indices)-1):
        records.append(txt[indices[j]:indices[j+1]])

    data = []
    for record in records:
        data.append(parserecord(record))


    return data




