import pyqrcode
from pyqrcode import QRCode

v="www.google.com"
url=pyqrcode.create(v)
url.svg("myqr.svg",scale=8)