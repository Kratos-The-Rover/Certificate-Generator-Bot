from PIL import Image, ImageDraw, ImageFont
import os

import firebase_admin
from firebase_admin import credentials, firestore

import qrcode

from fire import add_to_database

class kratosCertificateBot:
    def __init__(self, template_path, font_dir='files'):

        #Fonts & sizes
        self.name_font = ImageFont.truetype(os.path.join(font_dir, "CooperHewitt-Semibold.otf"), 140)
        self.description_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Medium.ttf"), 50)
        self.year_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Medium.ttf"), 50)
        self.banner_font = ImageFont.truetype(os.path.join(font_dir, "HKGrotesk-Bold.ttf"), 50)

        #Certificate template path
        self.template = Image.open(template_path)

        #Configure the size and border, etc., of the QR Code
        self.qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=7,
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

    def export_certificate(self, path, fname):
        if not os.path.exists(path):
            os.makedirs(path)
        #print(os.path.join(path, fname))
        #self.template.show()
        self.template.save(os.path.join(path, fname), quality=100)

    def run(self, name, description, date, type, qr_data, output_dir, fname):
        self.draw_text(name, description, date, type)
        self.add_QR(qr_data)
        self.export_certificate(output_dir, fname)

    def createCertificate(self, person):
        if 'lead' in person['PoR(s)'][0].lower() or 'head' in person['PoR(s)'][0].lower():
            type_of_cert = u'CERTIFICATE OF LEADERSHIP'
            if person['Member status'] == u'Yes':
                description = u'is "{}" of Project Kratos'.format(person['PoR(s)'][0])
                date = u'for AY {}-{}'.format(person['Team']-1, person['Team'])
            else:
                description = 'was "{}" of Project Kratos'.format(person['PoR(s)'][0])
                date = u'for AY {}-{}'.format(person['Team']-1, person['Team'])
        else: 
            type_of_cert = u'CERTIFICATE OF Membership'
            if person['Member status'] == u'Yes':
                description = u'is "{}" in {} Subsystem of Project Kratos'.format(person['PoR(s)'][0], person['Subsystem'])
                date = u'for AY {}-Present'.format(person['Team']-2)
            else:
                description = u'was "{}" in {} Subsystem of Project Kratos'.format(person['PoR(s)'][0], person['Subsystem'])
                date = u'for AY {}-{}'.format(person['Team']-2, person['End'][-2:])

        if person['Sex'] == "Male":
            name = "Mr. " + person['Name']
        else:
            name = "Ms. " + person['Name']

        self.run(
            name = name,
            description = description,
            date = date,
            type = type_of_cert,
            qr_data = 'CertificateID: ' + person['Certificate ID'] + ' - Verify at: https://Kratos-The-Rover.github.io/verify',
            output_dir = 'files/certificates/{}/{}'.format(person['Team'], person['Subsystem']),
            fname = '{}_{}.png'.format(person['Name'], person['Certificate ID'][7:])
        )

    def createSingleCertificate(self, documentID):
        doc_ref = db.collection(u'Kratians').document(u'{}'.format(documentID))
        doc = doc_ref.get()
        person = doc.to_dict()
        self.createCertificate(person)

    def createMultipleCertificate(self, team):
        docs = db.collection(u'Kratians').where(u'Team', u'==', team).stream()
        for doc in docs:
            print(f'Creating certificate for {doc.id}')
            person = doc.to_dict()
            self.createCertificate(person)



if __name__ == "__main__":

    try:
        cred = credentials.Certificate('files/serviceKey.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        print("ERROR: Unable to Initialize the Firestore Client: {}".format(e))

    add_to_database(db)

    #bot = kratosCertificateBot(template_path='files/Certificate_Template_2021.png')
    #bot.createMultipleCertificate(team = 2022)