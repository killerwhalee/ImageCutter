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

def run(srcList, cropMode = "standard_type_B2"):
    success, fail = (0, 0)

    # Load cropMode from cropData JSON file
    with open("json/cropData.json", "r") as cropJson:
        cropData = json.load(cropJson)
        leftFirstImageCropPercentage = cropData[cropMode]["leftFirstImageCropPercentage"]
        rightFirstImageCropPercentage = cropData[cropMode]["rightFirstImageCropPercentage"]

        leftImageCropPercentage = cropData[cropMode]["leftImageCropPercentage"]
        rightImageCropPercentage = cropData[cropMode]["rightImageCropPercentage"]

        cropCheckRange = cropData[cropMode]["cropCheckRange"]

    # Iterate for every source path in source list
    for src in srcList:
        print(f"Cutting [{src}]")

        '''
        if os.path.isdir(src):
            s, f = run(os.listdir(src))
            success, fail = success + s, fail + f
        '''

        # Catch every error/exception occur while running function
        try:
            pageNum = 1
            startNum = 1
            pdfFile = pdf(src, dpi = 600)
            fileName, fileExt = os.path.splitext(src)

            for pdfImage in pdfFile:
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-L.png")
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-R.png")
                #pageNum += 1; continue # For raw extraction

                # Typically first page has different form (case specific).
                # If not, FirstImageCropPercentage would be same with ImageCropPercentage in JSON file
                if pageNum % 4 == 1:
                    leftCropRange  = leftFirstImageCropPercentage
                    rightCropRange = rightFirstImageCropPercentage
                else:
                    leftCropRange  = leftImageCropPercentage
                    rightCropRange = rightImageCropPercentage
                
                # This is for Binary Cropping
                startNum += imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-L.png", dest = fileName, cropRange = leftCropRange, cropCheckRange = cropCheckRange, startNum = startNum, numDigit = 2)
                startNum += imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-R.png", dest = fileName, cropRange = rightCropRange, cropCheckRange = cropCheckRange, startNum = startNum, numDigit = 2)

                # This is for Raw Cropping
                #startNum += imgRawCrop(f"{fileName}-PAGE#{pageNum}-L.png", dest = f"{fileName}-halfcrop", cropRange = leftCropRange, startNum = startNum, numDigit = 2)
                #startNum += imgRawCrop(f"{fileName}-PAGE#{pageNum}-R.png", dest = f"{fileName}-halfcrop", cropRange = rightCropRange, startNum = startNum, numDigit = 2)

                # Remove temporal file created
                os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
                os.remove(f"{fileName}-PAGE#{pageNum}-R.png")

                pageNum += 1
            
            print(f"Successfully cut source [{src}]")
            success += 1

        # We caught some error/exception here.
        # Print error message and exit
        except Exception as e:
            print(f"Error in source [{src}] - {e}")
            fail += 1
    
    # Print result message then return with success/fail count
    print(f"Process Done: Success {success} / Fail {fail}")
    return success, fail


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
            
