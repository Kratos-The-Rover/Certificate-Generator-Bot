from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

import qrcode

class kratosCertificateBot:
    def __init__(self, template_path='files/Certificate_Template.png', font_dir='files'):

        #Fonts & sizes
        self.name_font = ImageFont.truetype(os.path.join(font_dir, "CooperHewitt-Semibold.otf"), 140)
        self.description_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Medium.ttf"), 60)
        self.year_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Medium.ttf"), 50)
        self.banner_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Bold.ttf"), 50)

        #Certificate template path
        self.template = Image.open(template_path)

        #Configure the size and border, etc., of the QR Code
        self.qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=10,
                                border=2,
                            )

    def draw_text(self, name, description, date, type):
        certificate = ImageDraw.Draw(self.template)

        #Adjust the coordinates and fields accordingly
        certificate.text(xy=(210, 570), text=name, fill = (255, 255, 255), font=self.name_font)
        certificate.text(xy=(210, 710), text=description, fill = (255, 255, 255), font=self.description_font)
        certificate.text(xy=(210, 780), text=date, fill = (255, 255, 255), font=self.year_font)
        certificate.text(xy=(1180, 130), text=type.upper(), fill = (0, 0, 0), font=self.banner_font)

    def add_QR(self, data):

        self.qr.add_data(data)
        self.qr.make(fit=True)

        QR = self.qr.make_image(fill_color="black", back_color="white")
        self.template.paste(QR, (145, 965))

    def export_certificate(self, path):
        self.template.save(path, quality=100)

    def run(self, name, description, date, type, qr_data, output_path):
        self.draw_text(name, description, date, type)
        self.add_QR(qr_data)
        self.export_certificate(output_path)


if __name__ == "__main__":
    bot = kratosCertificateBot()
    bot.run(
        name = 'Mr. John Doe',
        description = 'is "Random Subsystem Lead" of Project Kratos',
        date = 'for AY 2021-22',
        type = 'CERTIFICATE OF LEADErSHIP',
        qr_data = 'h0iehwken0v0weklwmnds[',
        output_path = 'files/certificates/johndoe.png'
    )