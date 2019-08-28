# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:47:59 2019

@author: PRAVEEN
"""

from ftplib import FTP

files = []

def traverse():
    """
    return a recursive listing of an ftp server contents (starting
    from the current directory)

    listing is returned as a recursive dictionary, where each key
    contains a contents of the subdirectory or None if it corresponds
    to a file.

    @param ftp: ftplib.FTP object
    """
    locs=[]
    paths=["/"]
    while paths!=[]:
        path=paths.pop(0)
        try:
            curr=ftp.pwd()
            ftp.cwd(path)
            ftp.cwd(curr)
            files = ftp.nlst(path)
            for j in files:
                paths.append(path+"/"+j)
        except:
            locs.append((path, path[path.rfind("/")+1:]))
    return locs[:]

def ls(dirname="/"):
    ftp.dir(dirname)

def uploadFile(localpath, filename):
    global files
    ftp.storbinary('STOR '+filename, open(localpath+"/"+filename, 'rb'))
    files=traverse()
    ls()

def downloadFile(localpath, filename):
    localfile = open(localpath+"/"+filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    localfile.close()

def rename(fromname, toname):
    global files
    ftp.rename(fromname, toname)
    files=traverse()
    ls()
    
def delete(filename):
    global files
    ftp.delete(filename)
    files=traverse()
    ls()
    
def cd(dirname="/"):
    ftp.cwd(dirname)
    ls()
    
def mkdir(dirname):
    ftp.mkd(dirname)
    ls()
    
def pwd():
    return ftp.pwd()

def rmd(dirname):
    ftp.rmd(dirname)
    ls()
    
def close():
    ftp.quit()
    print("Connection Closed.....")

def search(keyword):
    flag = False
    for (path, filename) in files:
        if keyword in filename:
            print(path)
            flag = True
    if not flag:
        print("No matching file found...")
def help():
    print(" QUIT   >>> Closses the ftp connection. Accepts no Parameter. ")
    print(" EXIT   >>> Closses the ftp connection. Accepts no Parameter. ")
    print(" CLOSE  >>> Closses the ftp connection. Accepts no Parameter. ")
    print(" UPLD   >>> Uploades file on the server.")
    print(" DWNLD  >>> Dowloades file to the local system. ")    
    print(" RENAME >>> Renames the file on the server. Accepts two parametrers as Oldname and Newname. ")
    print(" DELETE >>> DELETES the file on the server. Accepts one parameter as the filname on the server.")
    print(" LS     >>> Lits Directories and Files in the current directory. Accepts no parameter. ")
    print(" CD     >>> Changes current Working directory. Changes to root if no path provided. ")
    print(" MKDIR  >>> Creates new directory nder current working directory.")
    print(" PWD    >>> Displays current working directory. Accepts no argument. ")
    print(" RMD    >>> To delete a directory. Accepts one argumet as a directory name")
    print(" SEARCH >>> Searches for the file wwith the matching keyword. ")
    print(" HELP   >>> Displays information about some commands. ")
def parser():
    while True:
        line=input("root" + pwd() + ":~$ ")
        token = line.split("  ")
        try:
            length = len(token)
            if  line != "":
                cmd = token[0].lower()
                if cmd == "quit" or cmd == "exit" or cmd == "close":
                    close()
                    break
                elif cmd == "upld":
                    uploadFile(token[1], token[2])
                elif cmd == "dwnld":
                    downloadFile(token[1], token[2])
                elif cmd == "rename":
                    rename(token[1], token[2])
                elif cmd == "delete":
                    delete(token[1])
                elif cmd == "ls":
                    if length > 1:
                        ls(token[1])
                    else:
                        ls()
                elif cmd == "cd":
                    if length > 1:
                        cd(token[1])
                    else:
                        cd()
                elif cmd == "mkdir":
                    mkdir(token[1])
                elif cmd == "pwd":
                    pwd()
                elif cmd == "rmd":
                    rmd(token[1])
                elif cmd == "search":
                    search(token[1])
                elif cmd == "help":
                    help()
                else:
                    print(token[0],"not recognized as any supported command. Type HELP to know more.")
        except:
            print("Invalid set(s) of arguments for "+token[0]+" command")


ip = input("IP Address : ")
port = input("Port Number : ")
user = input("Username : ")
password = input("Password : ")

ftp = FTP()
ftp.connect(ip,int(port))
ftp.login(user, password)
print(ftp.getwelcome())
files=traverse()
parser()
