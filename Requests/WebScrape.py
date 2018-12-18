import requests
import re

# get the data
data = requests.get('https://www.munichre.com/HSB/hsb-contact/index.html')

# extract the phone numbers and emails using regex expressions
phones = re.findall(r'(\(?[0-9]{3}\)?(?:\-|\s|\.)?[0-9]{3}(?:\-|\.)[0-9]{4})', data.text)
emails = re.findall(r'([\d\w.]+@[\d\w\.\-]+\.\w+)', data.text)

print("phones: {}".format(phones))
print("emails: {}".format(emails))

