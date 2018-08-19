from PIL import Image, ImageFont, ImageDraw

# returns 2D array of rgb data [0, 0] corresponding to top left corner of image
def extractRGBdata(image):
    data = list(image.getdata())
    width, height = image.size

    rgbVals = []

    count = 0
    row = []
    for r, g, b in data:
        row.append((r, g, b))
        count += 1

        if count % width == 0:
            rgbVals.append(row)
            row = []

    return rgbVals

def printPixels(rgbVals):
    for row in rgbVals:
        for pixel in row:
            print("{}\t".format(pixel), end="")
        print("")

def unoptimizedCharDict(font):
    charDict= {}

    for i in list(range(33, 127)) + list(range(161, 254)):
        charImage = Image.new('RGB', (70, 110), (255, 255, 255)) # new blank image
        draw = ImageDraw.Draw(charImage) # create ImageDraw object
        draw.text((0, 0), chr(i), fill=(0, 0, 0), font=font) # draw char onto image

        charDict[getBrightnessAverage(extractRGBdata(charImage))] = chr(i) # brightnessAvg:char

    return charDict

# returns average brightness of a specified patch of pixels
def getBrightnessAverage(rgbData):
    width = len(rgbData[0])
    height = len(rgbData)

    bTotal = 0
    for row in rgbData:
        for rgbPixel in row:
            bTotal += (sum(rgbPixel) / 3)
    bAverage = bTotal / (width * height)

    return bAverage

def optimizeCharDict(charDict):
    newCharDict = {}

    min, max = getMinMaxKey(charDict)

    for bAverage, char in charDict.items():
        scaledB = (255 * (bAverage - min)) / (max - min)
        newCharDict[scaledB] = char

    return newCharDict

def getMinMaxKey(charDict):
    keys = list(charDict.keys())
    min = 999
    max = -999
    for key in keys:
        if key < min:
            min = key
        if key > max:
            max = key

    return min, max

def getCharWeightings():
    font = ImageFont.truetype("Fonts/Menlo.ttc", 100)
    chars = unoptimizedCharDict(font)
    optimizedChars = optimizeCharDict(chars)
    
    return optimizedChars

if __name__ == "__main__":
    charWeightings = getCharWeightings()

    img = Image.open("ID_Photo.jpg")
    imgRGBdata = extractRGBdata(img)
    getBrightnessAverage(imgRGBdata)
