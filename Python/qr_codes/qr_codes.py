import zbarlight
from PIL import Image
from qrcode import QRCode

subject = "Science"
yearLevel = "07"
pageNumber = 0000
createdCodes = []

while pageNumber < 11:
    pageNumber += 1
    fileNumber = "{0} - Year{1} - Page{2}".format(subject, yearLevel, pageNumber)
    qr = QRCode(version=1, error_correction=ERROR_CORRECT_H)
    qr.add_data(fileNumber)
    qr.make()  # Generate the QRCode itself

    # im contains a PIL.Image.Image object
    im = qr.make_image()

    # To save it
    im.save("./qrcodes/%s.png" % fileNumber)
    createdCodes.append(fileNumber)


def load_from_file(file_path="filename.png"):
    with open(file_path, "rb") as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes("qrcode", image)
    codes = codes[0].decode("ascii")
    print("QR codes: %s" % codes)
