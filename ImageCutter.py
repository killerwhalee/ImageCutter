import os
from pdf2image import convert_from_path as pdf
from PIL import Image
from tkinter import filedialog
    
def imgBinaryCrop(src, cropRange = (0, 0, 1, 1), cropCheckRange = (0, 0)):
    #Crop one image
    fileName, fileExt = os.path.splitext(src)
    print(f"cropping {fileName}...")

    image = Image.open(src)
    width, height = image.size

    ## Temp image cutting area setting - SURV
    imageCropPercentage = cropRange
    imageCropCheckingRange = cropCheckRange
    
    ## Crop Image
    imageCropArea = (int(imageCropPercentage[0] * width), int(imageCropPercentage[1] * height), int(imageCropPercentage[2] * width), int(imageCropPercentage[3] * height))
    croppedImage = image.crop(imageCropArea)
    width, height = croppedImage.size
    whiteSpace = int(height * 0.005)

    ## Variable Set
    imageCount  = 1
    boundRange  = [0, 0]
        
    #Cut Each Paragraph in Cropped Page
    for heightPixel in range(height):
        for widthPixel in range(int(width * imageCropCheckingRange[1])):
            if croppedImage.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                if widthPixel < width * imageCropCheckingRange[0]:
                    if boundRange[1]:
                        recroppedRegion = 0, boundRange[0] - whiteSpace, width, boundRange[1] + whiteSpace
                        outputImage = croppedImage.crop(recroppedRegion)
                        outputImage.save(f"{os.path.splitext(src)[0]}-{imageCount}.png")
                        imageCount += 1

                        boundRange = [0, 0]
                    
                    if not boundRange[0]:
                        boundRange[0] = heightPixel
                    
                else:
                    boundRange[1] = heightPixel
                
                break

    if not boundRange[1]:
        return

    recroppedRegion = 0, boundRange[0] - whiteSpace, width, boundRange[1] + whiteSpace
    outputImage = croppedImage.crop(recroppedRegion)
    outputImage.save(f"{os.path.splitext(src)[0]}-{imageCount}.png")
    imageCount += 1

##Start SAC
if __name__ == "__main__":
    try:

        # Temporary set
        leftFirstImageCropPercentage  = (0.1006, 0.2086, 0.4983, 0.9068)
        rightFirstImageCropPercentage = (0.5147, 0.2086, 0.9125, 0.9068)

        leftImageCropPercentage  = (0.1006, 0.1250, 0.4983, 0.9068)
        rightImageCropPercentage = (0.5147, 0.1250, 0.9125, 0.9068)

        srcList = filedialog.askopenfilenames(title = "Select PDF files to cut", filetypes = [("PDF Files", ".pdf")])

        for src in srcList:

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
                
                imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-L.png", cropRange = leftCropRange, cropCheckRange = (0.0420, 0.120))
                imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-R.png", cropRange = rightCropRange, cropCheckRange = (0.0420, 0.120))

                os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
                os.remove(f"{fileName}-PAGE#{pageNum}-R.png")
                pageNum += 1
        
    except Exception as e:
        print(f"Exception Occurred!: {e}")

