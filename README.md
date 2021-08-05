# Certificate-Generator-Bot

A simple python script to generate certificates with QR Code in a loop. QR Codes are tied to a Firebase Firestore database.

## Steps involved

- Create a template on Canva with spaces provided for different fields like Name, Date, etc.
- Export as .png file.
- Download the necessary font files
- Create a ```/files``` folder in the same directory and add all the .png and font files
- Make sure python is installed
- ```pip install -r requirements.txt```
- ```certificate.py``` has the necessary functions to generate a certificate, modify it according to your needs.
