import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

number = input("Enter number with country code without +:")
number = "+" + number

ch_number = phonenumbers.parse(number,"CH")
country = geocoder.description_for_number(ch_number,"en")

service_number = phonenumbers.parse(number,"RO")
service_name = carrier.name_for_number(ch_number,'en')

print("Country Name:{0}\nProvider Name:{1}".format(country,service_name))
