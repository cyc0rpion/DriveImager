try:
    from tkinter import *
    import subprocess
    from browse import browse_file
    from tkinter import messagebox
    import shutil
    import os
    from os import path
    import webbrowser

    def infobox():
        messagebox.showinfo("Won't work in FAT32", "If destination File System is FAT32, A file having size more than 4.3 GB cannot be created.\nEither convert FAT32 to NTFS, or use another NTFS drive as destination.")

    def destname():
        destEntry.delete(0,END)
        lname = (li[choice.get()].split(':')[0]).replace("/","_")
        dname = "/root/Image"+ lname
        destEntry.insert(END,dname)

    def select_file():
    	fileName = browse_file()
    	destEntry.delete(0,END)
    	destEntry.insert(END,fileName)

    def imager():
        try:
            drive = li[choice.get()].split(':')[0]
            dest = destEntry.get()  
            
            drive = path.realpath(drive)
            dest = path.realpath(dest)

            #print(drive,dest)

            with open(drive,'rb') as z:
                z.seek(0, os.SEEK_END)
                size = z.tell()
                size = size // 1000000000
                #print(size)
                z.close()

            with open(drive,'rb') as f:
                with open(dest, 'wb') as j:
                    procLabel = Label(rightFrame,text="Creating Image. Please wait...",width="65",bg="pink")
                    procLabel.grid(row=5,column=1,pady=20,columnspan=6)
                    x = 0
                    while True:
                        x+=1024
                        progress = x / 1000000000
                        fprogress = format(progress,'.8f')
                        pdone = format((float(fprogress)/size * 100),'.2f')
                        if j.write(f.read(1024)) == 0:
                            break
                        procLabel['text'] = "Drive Size: " + str(size) + " GB.\nCreating Image. Please wait... " + pdone + "%"
                        drimager.update()
            shutil.copystat(drive,dest)
            messagebox.showinfo("Image Created", "Image Created succesfully.\nLocation: "+dest)
            
            compLabel = Label(rightFrame,text="Image Created",width="65",bg="light green")
            compLabel.grid(row=7,column=1,pady=10,columnspan=6)
        except IsADirectoryError:
            messagebox.showwarning("Not a directory","Please choose destination as a file not a folder.")

    proc = subprocess.Popen("sudo blkid", stdout=subprocess.PIPE, shell=True)
    output, err = proc.communicate()

    li = output.decode("utf-8").strip("\n").split("\n")
    tdrives = len(li)


    drimager = Tk()
    drimager.geometry("830x530")
    drimager.title("Open Forensic Toolkit Drive Imager")
    drimager.resizable(0,0)

    nameLabel = Label(drimager,text="Drive Imager",font="Helevetica 20 bold",fg="blue")
    nameLabel.grid(row=1,column=2,padx=10,pady=10,sticky=W)

    leftFrame = Frame(drimager, height="450", width="280",bd="2",relief=SUNKEN)
    leftFrame.grid(row=2,column=1,padx=10,pady=10,rowspan=10)

    leftFrame.configure(height=leftFrame["height"],width=leftFrame["width"])
    leftFrame.grid_propagate(0)

    sourceLabel = Label(leftFrame,text="Select Drive (Source):",font="Helevetica 14 bold",fg="black",bg="light yellow")
    sourceLabel.grid(row=1,column=1,sticky=W)

    empLabel = Label(leftFrame,height="1")
    empLabel.grid(row=2,column=1)

    choice = IntVar()
    i=0
    while(i<tdrives):
        dname = li[i].split(':')[0]
        temp0 = li[i].split(':')[1]
        if "LABEL" in (temp0):
            #print(temp0)
            temp1 = temp0.split(':')[0]
            #print(temp1)
            temp2 = temp1.split('=')[1]
            #print(temp2)
            temp3 = temp2.split(' ')
            j=0
            lname = ""
            while(j<len(temp3)-1):
                lname +=" " + temp3[j]
                j+=1

            lname = lname.strip()
            lname = lname.strip('"')
            dname +=" :: "+lname

        dButtons = Radiobutton(leftFrame, text=dname,value=i,variable=choice,command=destname)
        dButtons.grid(row=i+3,column=1,padx=20,pady=5,sticky=W)
        i+=1

    rightFrame = Frame(drimager, height="400", width="500",bd="4")
    rightFrame.grid(row=2,column=2,padx=10,pady=10)

    rightFrame.configure(height=rightFrame["height"],width=rightFrame["width"])
    rightFrame.grid_propagate(0)

    destLabel = Label(rightFrame,text="Select Destination File:",font="Helevetica 14 bold",fg="black",bg="light green")
    destLabel.grid(row=1,column=1,sticky=W)

    destEntry = Entry(rightFrame,width="40")
    destEntry.grid(row=2,column=1,padx=10,pady=10)

    browseButton = Button(rightFrame,text="Browse",width="10",command=select_file)
    browseButton.grid(row=2,column=2)

    imageButton = Button(rightFrame,text="Create Image",width="12",height="1",bg="yellow",font="Helvetica 12 bold",command=imager)
    imageButton.grid(row=3,column=1,padx=20,sticky=E)

    infoFrame = Frame(drimager)
    infoFrame.grid(row=6,column=2,sticky=W)

    infoPhoto=PhotoImage(file="info.png")

    infoLabel=Label(infoFrame,text="Drive size more than 4.3 GB?")
    infoLabel.grid(row=1,column=1,sticky=W,padx=10)

    infoButton = Button(infoFrame,image=infoPhoto,height="15",width="15",command=infobox)
    infoButton.grid(row=1,column=2,sticky=W)

    empLabel = Label(infoFrame,width="8")
    empLabel.grid(row=1,column=3)

    def callback(event):
    	webbrowser.open("https://github.com/mohitbalu/")

    footerLabel = Label(infoFrame,text="Developed by @mohitbalu\nunder Project OFTK",bg="black",fg="white",relief=RAISED,bd="2")
    footerLabel.grid(row=1,column=4,sticky=E,ipadx=2,ipady=2)
    footerLabel.bind("<Button-1>", callback)

    drimager.mainloop()

except (ValueError,TypeError):
    try:
        messagebox.showinfo("Value Error","Please provide correct values. If not resolved mailto: mohit.balu@outlook.com")
    except:
        print("Please provide Correct values in the fields. If not resolved mailto: mohit.balu@outlook.com")

except (IOError,EOFError):
    try:
        messagebox.showinfo("Input Output/File Error","Please check file name and permissions. If not resolved mailto: mohit.balu@outlook.com")
    except:
        print("Please check file names and permissions. If not resolved mailto: mohit.balu@outlook.com")

except (ImportError):
    try:
        messagebox.showinfo("Import Error","Cannot import package/s. Make sure you are using correct version (python3.x), If not resolved mailto: mohit.balu@outlook.com")
    except:
        print("Cannot import package/s. Make sure you are using correct version (python3.x). If not resolved mailto: mohit.balu@outlook.com")

except:
    messagebox.showwarning("Error!","An unexpected error has occured. Make sure Drive Imager Tool is running on linux platform and requires root(sudo) permissions.")
    try:
        drimager.destroy()
    except:
        pass
