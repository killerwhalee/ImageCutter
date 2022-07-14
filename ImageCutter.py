import os
from pdf2image import convert_from_path as pdf
from PIL import Image
from tkinter import filedialog
    
def imgBinaryCrop(src, cropRange = (0, 0, 1, 1), cropCheckRange = (0, 0), startNum = 1, numDigit = 0):

    image = Image.open(src)
    width, height = image.size
    
    ## Crop Image
    imageCropArea = (int(cropRange[0] * width), int(cropRange[1] * height), int(cropRange[2] * width), int(cropRange[3] * height))
    croppedImage = image.crop(imageCropArea)
    width, height = croppedImage.size
    whiteSpace = int(height * 0.005)

    ## Variable Set
    imageCount = startNum
    boundRange  = [0, 0]
        
    #Cut Each Paragraph in Cropped Page
    for heightPixel in range(height):
        for widthPixel in range(int(width * cropCheckRange[1])):
            if croppedImage.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                if widthPixel < width * cropCheckRange[0]:
                    if boundRange[1]:
                        recroppedRegion = 0, boundRange[0] - whiteSpace, width, boundRange[1] + whiteSpace * 2

                        imageStr = str(imageCount)
                        if numDigit:
                            imageStr = "0" * (numDigit - len(str(imageCount))) + str(imageCount)

                        outputImage = croppedImage.crop(recroppedRegion)
                        outputImage.save(f"{os.path.splitext(src)[0]}_{imageStr}.png")

                        imageCount += 1
                        boundRange = [0, 0]
                    
                    if not boundRange[0]:
                        boundRange[0] = heightPixel
                    
                else:
                    boundRange[1] = heightPixel
                
                break

    if not boundRange[1]:
        return

    recroppedRegion = 0, boundRange[0] - whiteSpace, width, boundRange[1] + whiteSpace * 2
    
    imageStr = str(imageCount)
    if numDigit:
        imageStr = "0" * (numDigit - len(str(imageCount))) + str(imageCount)

    outputImage = croppedImage.crop(recroppedRegion)
    outputImage.save(f"{os.path.splitext(src)[0]}_{imageStr}.png")

    imageCount += 1

    return imageCount


## ImageCutter as Main function
## This is for developer mode, not for client!

if __name__ == "__main__":
    # Temporary set
    leftFirstCropRange  = (0.1006, 0.2086, 0.4983, 0.9068)
    rightFirstCropRange = (0.5147, 0.2086, 0.9125, 0.9068)

    leftCropRange  = (0.1006, 0.1250, 0.4983, 0.9068)
    rightCropRange = (0.5147, 0.1250, 0.9125, 0.9068)

    srcList = filedialog.askopenfilenames(title = "Select PDF files to cut", filetypes = [("PDF Files", ".pdf")])

    for src in srcList:

        pageNum = 1
        imageCount = 1
        pdfFile = pdf(src, dpi = 600)
        fileName, fileExt = os.path.splitext(src)

        for pdfImage in pdfFile:
            pdfImage.save(f"{fileName}.png")

            if pageNum % 4 == 1:
                left  = leftFirstCropRange
                right = rightFirstCropRange
            else:
                left  = leftCropRange
                right = rightCropRange
            
            imageCount = imgBinaryCrop(f"{fileName}.png", cropRange = left, cropCheckRange = (0.0358, 0.0645), startNum = imageCount, numDigit = 2)
            imageCount = imgBinaryCrop(f"{fileName}.png", cropRange = right, cropCheckRange = (0.0358, 0.0645), startNum = imageCount, numDigit = 2)

            os.remove(f"{fileName}.png")
            pageNum += 1

