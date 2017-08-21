import os
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import shutil

lastdocument = "UNKNOWN"

test = False

def gentempfolder(directory):
    tempfolder = directory + "\\temp"

    if test: print("GenTempFolder Test Case: " + tempfolder)

    #this code should always run but if statement here as precaution
    if not os.path.isdir(tempfolder):
        os.makedirs(tempfolder)
    return

def geninputarray(workingdirectory):
    print("Generating Input Array...")
    #function gets list of directory
    genarray = os.listdir(workingdirectory)
    if test:
        print(workingdirectory)
        print(genarray)
    print("Done!")
    return genarray

def convimgstotxts(workingdirectory):
    # function gets list of directory
    dirarray = os.listdir(workingdirectory)
    print(dirarray)
    for file in dirarray:
        if (file.endswith(".tif")):
            convimgtotxt(workingdirectory, file)

def convimgtotxt(workingdirectory, filename):
    print("Converting " + filename + " to text...")
    tifImage =  Image.open(workingdirectory + "\\" + filename)

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 4'

    tempText = pytesseract.image_to_string(tifImage, config=tessdata_dir_config)
    tempTextShort = tempText[0:56]
    #print(tempTextShort)

    tempTXTFileName = workingdirectory + "\\temp\\" + filename
    #print(tempTXTFileName)
    tempTXTFileName = tempTXTFileName.rstrip('.tif')
    #print(tempTXTFileName)
    tempTXTFileName = tempTXTFileName + ".txt"
    #print(tempTXTFileName)
    tempTXTFile = open(tempTXTFileName, "w")

    try:
        tempTXTFile.write(tempTextShort)
        tempTXTFile.close()
    except UnicodeEncodeError:
        tempTXTFile.write("UNREADABLE")
        tempTXTFile.close()
    print("Done!")

def convimgtotxtlong(workingdirectory, filename):
    print("Converting " + filename + " to text...")
    tifImage =  Image.open(workingdirectory + "\\" + filename)

    tesseractConfig = '--psm 4'
    tempText = pytesseract.image_to_string(tifImage, config = tesseractConfig)
    #print(tempText)

    tempTXTFileName = workingdirectory + "\\temp\\" + filename
    #print(tempTXTFileName)
    tempTXTFileName = tempTXTFileName.rstrip('.tif')
    #print(tempTXTFileName)
    tempTXTFileName = tempTXTFileName + ".txt"
    #print(tempTXTFileName)
    tempTXTFile = open(tempTXTFileName, "w")

    try:
        tempTXTFile.write(tempText)
        tempTXTFile.close()
    except UnicodeEncodeError:
        tempTXTFile.write("UNREADABLE")
        tempTXTFile.close()
    print("Done!")

def renameFiles(workingdirectory):
    workingtempdirectory = workingdirectory + "\\temp"
    tempdirarray = os.listdir(workingtempdirectory)
    for txt in tempdirarray:

        ticket = parseforincidentnumber(workingtempdirectory, txt)
        docname = txt.rstrip(".txt") + ".tif"
        if ticket == "UNKNOWN":
            convimgtotxtlong(workingdirectory, docname)
            ticket = parseforincidentnumber(workingtempdirectory, txt)
            docname = txt.rstrip(".txt") + ".tif"
        print("Renaming " + docname + " to : " + ticket)
        index = 1
        while os.path.isfile(workingdirectory + "\\" + str(ticket) + ".tif"):
            ticket = ticket + " (" + str(index) + ")"
            index = index + 1
        try:
            os.rename(workingdirectory + "\\" + docname, workingdirectory + "\\" + ticket + ".tif")
        except FileExistsError:
            print(docname + " rename failed!")

def parseforincidentnumber(workingtempdirectory, textfilename):
    global lastdocument
    #print("sss " + workingtempdirectory + "\\" + textfilename)
    incident = "NA"
    firstincfound = False
    with open(workingtempdirectory + "\\" + textfilename, 'r') as file:
        words = file.read().replace("\n", " ")
        words = words.split(" ")
        index = 0
        for word in words:
            index = index + 1
            if word == "INC" or word == "1NC" or word == 'INC#:':
                if firstincfound:
                    incident = word + words[index]
                    lastdocument = incident
                    return incident
                else:
                    firstincfound = True
            if not word == "INC" and not word == "1NC" and not word == 'INC#:':
                if word[0:3] == "INC":
                    word = word.replace("o", "0").replace("O", "0")
                    #print("1: " + word)
                    incident = word
                elif word[0:5] == "LTASK":
                    word = word.replace("o", "0").replace("O", "0")
                    #print("2: " + word)
                    incident = word
                elif word[0:4] == "RITM":
                    word = word.replace("o", "0").replace("O", "0")
                    #print("3: " + word)
                    incident = word
                elif word[0:4] == "TASK":
                    word = word.replace("o", "0").replace("O", "0")
                    #print("4: " + word)
                    incident = word
                elif word[0:3] == "LNR":
                    word = word.replace("o", "0").replace("O", "0")
                    #print("5: " + word)
                    incident = word
    if not incident == "NA":
        lastdocument = incident
        return incident
    else:
        if incident == "UNKNOWN":
            return incident
        else:
            incident = lastdocument
            lastdocument=incident
            return incident

def cleanup(tempdirectory):
    print("Cleaning...")
    shutil.rmtree(tempdirectory)
    print("Done!")

#Gets the root directory of the program (folder of the .py executable)
workingdirectory = os.getcwd()

#Generates an array of the files in the "toConvert" directory
inputarray = geninputarray(workingdirectory)

#generates the temp folder for use by the program
#TODO: write code at cleanup to delete this folder and its contents
gentempfolder(workingdirectory)
if test: print("Working Directory: " + workingdirectory)

#generates temp working directory path (root\toConvert\temp)
workingtempdirectory = workingdirectory + "\\temp"
if test: print("Temp Directory: " + workingtempdirectory)

#Use only one
#Convert all Images in temp directory to TXT files and store in Temp Directory
convimgstotxts(workingdirectory)

#Use TXT files in temp directory to rename the files in the workingdirectory
renameFiles(workingdirectory)

#Delete temp folder and its contents
cleanup(workingtempdirectory)

print("Renaming Process Complete!")