## Client for Windows

import os
import json
import time
from tkinter import filedialog

from ImageCutter import *

# Main function starts from here
INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(INSTALL_PATH)
srcList = []

with open("json/cropData.json", "r") as cropJson:
    cropData = json.load(cropJson)
    modeList = list(cropData.keys())

# Basically it is infinite loop
while True:
    srcInput = filedialog.askopenfilenames(title = "Select PDF file to cut", filetypes = [("PDF file", ".pdf")])
    if not srcInput:
        break
    
    for src in srcInput:
        print(f"Appending {os.path.basename(src)}...")
        srcList.append(src)

print("<Cropping Mode List>\n")
for index in range(len(modeList)):
    print(f"{index + 1}. {modeList[index]}")

while True:
    try:
        index = int(input("\nSelect Cropping Mode (in number) : "))
        cropMode = modeList[index - 1]
        break
    except:
        print("Wrong input! Try again.")
        continue
    
print(f"Running {len(srcList)} files with {cropMode}...")
start = time.time()
run(srcList, cropMode = cropMode)
end = time.time()
input(f"Process Done({end - start:.1f}s)! Press Enter to exit...")