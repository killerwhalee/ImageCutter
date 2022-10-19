## Client for Linux

import os
from pdf2image import convert_from_path as pdf
from ImageCutter import *

## STANDARD KICE FORM

leftFirstImageCropPercentage  = (0.1006, 0.2086, 0.4983, 0.9068)
rightFirstImageCropPercentage = (0.5147, 0.2086, 0.9125, 0.9068)

leftImageCropPercentage  = (0.1006, 0.1250, 0.4983, 0.9068)
rightImageCropPercentage = (0.5147, 0.1250, 0.9125, 0.9068)


## Start output
print("""ImageCutter by KillerWhalee

Add file to search.
Press Enter to execute.
:q to exit.""")

def run(srcList):
    success, fail = (0, 0)
    for src in srcList:
        print(f"Cutting [{src}]")
        try:
            pageNum = 1
            pdfFile = pdf(src, dpi = 600)
            fileName, fileExt = os.path.splitext(src)

            for pdfImage in pdfFile:
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-L.png")
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-R.png")

                if pageNum % 4 == 1:
                    leftCropRange  = leftFirstImageCropPercentage
                    rightCropRange = rightFirstImageCropPercentage
                else:
                    leftCropRange  = leftImageCropPercentage
                    rightCropRange = rightImageCropPercentage
                
                imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-L.png", cropRange = leftCropRange, cropCheckRange = (0.0420, 0.095))
                imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-R.png", cropRange = rightCropRange, cropCheckRange = (0.0420, 0.095))

                os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
                os.remove(f"{fileName}-PAGE#{pageNum}-R.png")

                pageNum += 1
            
            print(f"Successfully cut source [{src}]")
            success += 1

        except Exception as e:
            print(f"Error in source [{src}] - {e}")
            fail += 1
        
    print(f"Process Done: Success {success} / Fail {fail}")


srcList = []

while (True):
    src = input(">> ")
    if src == "":
        print(f"Running {len(srcList)} files...")
        run(srcList)
        srcList = []
    elif src == ":q":
        break
    else: 
        srcList.append(src)