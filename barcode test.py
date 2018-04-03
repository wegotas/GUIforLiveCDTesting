import barcode
from barcode.writer import ImageWriter

serial = "BR36KX1"

EAN = barcode.get_barcode_class('code39')
ean = EAN(serial)
print(ean)
print(type(ean))

ean2 = EAN(serial, writer=ImageWriter())
print(ean2)
print(type(ean2))
f = open("/home/sopenaclient/Desktop/barcode_test", "wb")
ean.write(f)
