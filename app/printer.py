from PIL import Image, ImageDraw
from app.PDF_Generator import generatePDF
import pyap

class Print:
    def __init__(self):
        self._chosenAddress = ["X", "X", "X"]
        self._firstLine = ""
        self._stickerLocation = 0

    def getAddLine0(self):
        return self._chosenAddress[0]

    def getAddLine1(self):
        return self._chosenAddress[1]
    
    def getAddLine2(self):
        return self._chosenAddress[2]

    # Getter and setter for chosenAddress
    def get_chosenAddress(self):
        return self._chosenAddress

    def set_chosenAddress(self, inputAddress):
        addressBuilder = []
        inputAddress = str(inputAddress)
        if inputAddress == "PRESS HERE TO CHOOSE":
            addressBuilder = [" ", " ", " "]
        else:
            for i in inputAddress.split(' | '):
                i.lstrip()
                addressBuilder.append(i)
        
        self._chosenAddress = addressBuilder

    # Getter and setter for firstLine
    def get_firstLine(self):
        return self._firstLine

    def set_firstLine(self, firstLine):
        self._firstLine = firstLine
        if self._chosenAddress[0] == " ":
            if '.' in firstLine:
                lines = firstLine.split('.')
                if len(lines) < 3:
                    self._chosenAddress[1] = "ERROR"
                else:
                    self._firstLine = lines[0].rstrip().lstrip()
                    self._chosenAddress[1] = lines[1].rstrip().lstrip()
                    self._chosenAddress[2] = lines[2].rstrip().lstrip()
            else:
                addressString = firstLine
                parsedAddresses = pyap.parse(addressString, country = 'US')
                if parsedAddresses:
                    addressDict = parsedAddresses[0].as_dict()
                    self._firstLine = addressString[:addressDict['match_start']]
                    self._chosenAddress[1] = addressDict['full_street']
                    self._chosenAddress[2] = addressDict['full_address'].lstrip(addressDict['full_street'])
                else:
                    self._chosenAddress[1] = "ERROR"


    # Getter and setter for stickerLocation
    def get_stickerLocation(self):
        return self._stickerLocation

    def set_stickerLocation(self, stickerLocation):
        self._stickerLocation = stickerLocation

    def __str__(self):
        return f"Chosen Address: {self._chosenAddress}\nFirst Line: {self._firstLine}\nSticker Location: {self._stickerLocation}"

    coords = {1 : [(17, 28), (201, 97)],
            2 : [(202, 28), (384, 97)],
            3 : [(385, 28), (568, 97)],
            4 : [(17, 98), (201, 167)],
            5 : [(202, 98), (384, 167)],
            6 : [(385, 98), (568, 167)],
            7 : [(17, 168), (201, 237)],
            8 : [(202, 168), (384, 237)],
            9 : [(385, 168), (568, 237)],
            10 : [(17, 238), (201, 307)],
            11 : [(202, 238), (384, 307)],
            12 : [(385, 238), (568, 307)],
            13 : [(17, 308), (201, 377)],
            14 : [(202, 308), (384, 377)],
            15 : [(385, 308), (568, 377)],
            16 : [(17, 378), (201, 447)],
            17 : [(202, 378), (384, 447)],
            18 : [(385, 378), (568, 447)],
            19 : [(17, 448), (201, 517)],
            20 : [(202, 448), (384, 517)],
            21 : [(385, 448), (568, 517)],
            22 : [(17, 518), (201, 587)],
            23 : [(202, 518), (384, 587)],
            24 : [(385, 518), (568, 587)],
            25 : [(17, 588), (201, 657)],
            26 : [(202, 588), (384, 657)],
            27 : [(385, 588), (568, 657)],
            28 : [(17, 658), (201, 727)],
            29 : [(202, 658), (384, 727)],
            30 : [(385, 658), (568, 727)]}
    
    def genChosenSticker(self):
        with Image.open(r"app/static/stickers.png") as sImg:
            sImg.convert("RGBA")
            draw = ImageDraw.Draw(sImg, "RGBA")
            draw.rectangle(Print.coords[self._stickerLocation], fill=(204, 248, 194, 300))
            sImg.save("app/static/chosen_sticker.png")

    def startPrint(self):
        print("Print function called")
        addressDataForPDF = {
        'line1':self.get_firstLine(),
        'line2':self.get_chosenAddress()[1],
        'line3':self.get_chosenAddress()[2],
        'stickerpos':self.get_stickerLocation()
        }
        generatePDF(addressDataForPDF)
        # print using lpr command
        #subprocess.run()




# Example usage:
if __name__ == "__main__":
    print_obj = Print()
    print_obj.set_chosenAddress(["123 Main St", "Apt 3B", "City"])
    print_obj.set_firstLine("Hello, World!")
    print_obj.set_stickerLocation(11)
    
    print("Chosen Address:", print_obj.get_chosenAddress())
    print("First Line:", print_obj.get_firstLine())
    print("Sticker Location:", print_obj.get_stickerLocation())

    print_obj.genChosenSticker()

