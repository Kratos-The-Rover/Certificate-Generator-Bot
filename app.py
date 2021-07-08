import firebase_admin
from firebase_admin import credentials, firestore

from certificate import kratosCertificateBot

#Initialize Firestore
try:
    cred = credentials.Certificate('key/serviceKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print("ERROR: Unable to Initialize the Firestore Client: {}".format(e))


def createCertificate(person):
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
            date = u'for AY {}-{}'.format(person['Team']-2, person['End'])

    if person['Sex'] == "Male":
        name = "Mr. " + person['Name']
    else:
        name = "Ms. " + person['Name']

    bot = kratosCertificateBot()
    bot.run(
        name = name,
        description = description,
        date = date,
        type = type_of_cert,
        qr_data = 'CertificateID: ' + person['Certificate ID'] + ' - Verify at: https://Kratos-The-Rover.github.io/verify',
        output_dir = 'files/certificates/{}/{}'.format(person['Team'], person['Subsystem']),
        fname = '{}_{}.png'.format(person['Name'], person['Certificate ID'][7:])
    )
'''

doc_ref = db.collection(u'Kratians').document(u'f20180608@goa')
doc = doc_ref.get()
person = doc.to_dict()
createCertificate(person)

'''
docs = db.collection(u'Kratians').where(u'Team', u'==', 2022).stream()
for doc in docs:
    print(f'Creating certificate for {doc.id}')
    person = doc.to_dict()
    createCertificate(person)



'''
{'End': '8/1/2021', 'LinkedIn': 'https://www.linkedin.com/in/ithihasmadala/', 
'Personal Email': 'helloithihas@gmail.com', 'Sex': 'Male', 'Team': 2021, 
'Year of Joining': '3/22/2019', 'BITS Mail': 'f20180607@goa.bits-pilani.ac.in', 
'PoR(s)': ['Team Lead', ' Life Detection Subsystem Lead'], 'Subsystem': 'LD', 
'Member status': 'Yes', 'Name': 'Ithihas Madala', 'Certificate ID': 'kratos:f20180607@goa'}
'''