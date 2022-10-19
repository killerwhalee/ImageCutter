import os
from pdf2image import convert_from_path as pdf
from PIL import Image
    
def imgBottomTrim(image, whiteSpace):
    #Image Bottom Trimming
    bottomLine = 0
    width, height = image.size
    
    for heightPixel in range(height):
        for widthPixel in range(int(width * 0.5)):
            if image.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                bottomLine = heightPixel
                break

    recroppedRegion = 0, 0, width, bottomLine + 2 * whiteSpace
    image = image.crop(recroppedRegion)
    return image

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
                        recroppedRegion = 0, boundRange[0] - whiteSpace, width, heightPixel - whiteSpace

                        imageStr = str(imageCount)
                        if numDigit:
                            imageStr = "0" * (numDigit - len(str(imageCount))) + str(imageCount)

                        unTrimmedImage = croppedImage.crop(recroppedRegion)
                        outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
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

    recroppedRegion = 0, boundRange[0] - whiteSpace, width, heightPixel - whiteSpace
    
    imageStr = str(imageCount)
    imageStr = "0" * (numDigit - len(str(imageCount))) + str(imageCount)

    unTrimmedImage = croppedImage.crop(recroppedRegion)
    outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
    outputImage.save(f"{os.path.splitext(src)[0]}_{imageStr}.png")

    imageCount += 1

    return imageCount


## Block user to use module in itself

if __name__ == "__main__":
    pass
