import pyqrcode
from pyqrcode import QRCode

v=input("Enter your data to generate QR CODE: ")
url=pyqrcode.create(v)
url.svg("myqr.svg",scale=8)