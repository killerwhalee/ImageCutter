## Client for Linux

import os
import json
from pdf2image import convert_from_bytes as pdf
from ImageCutter import *

## Start output
print("""ImageCutter by KillerWhalee

Add file or folder to search.
* only PDF file is accepted
Press Enter to execute.
:q to exit.""")

# Main function starts from here
srcList = []

with open("json/cropData.json", "r") as cropJson:
    cropData = json.load(cropJson)
    modeList = list(cropData.keys())

# Basically it is infinite loop
while True:
    src = input(">> ")
    if src == "":
        print("<Cropping Mode List>\n")
        for index in range(len(modeList)):
            print(f"{index + 1}. {modeList[index]}")

        while True:
            try:
                index = int(input("\nSelect Cropping Mode : "))
                cropMode = modeList[index - 1]
                break
            except:
                print("Wrong input! Try again.")
                continue
            
        print(f"Running {len(srcList)} files with {cropMode}...")
        run(srcList, cropMode = cropMode)
        srcList = []

    elif src == ":q":
        break
    else: 
        try:
            # Case for folder input
            if os.path.isdir(src):
                counter = 0
                for file in os.listdir(src):
                    if os.path.splitext(file)[-1] in [".pdf", ".PDF"]:
                        srcList.append(f"{src}/{file}")
                        print(f"Appending {file}...")
                        counter += 1
                
                print(f"appended {counter} files.")
            
            # Case for file input
            else:
                if os.path.splitext(src)[-1] in [".pdf", ".PDF"]:
                    srcList.append(src)
                else:
                    print("warning : wrong file type. Try again.")

        except FileNotFoundError:
            print("error : No such file or directory. Try again.")
            
