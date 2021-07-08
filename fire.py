from io import BytesIO
import requests
import pandas as pd

def add_to_database(db, sheet_link='https://docs.google.com/spreadsheet/ccc?key=16t5LRWRfUIY-FVj1yibx1kRbdyo5PNF0LbWZ-qHCCv0&output=csv'):
    #Get the Data from Google Sheets
    r = requests.get(sheet_link)
    data = r.content
    df = pd.read_csv(BytesIO(data), index_col=0,parse_dates=['Timestamp'])

    for index, row in df.iterrows():

        print("Adding ", row['Full Name'], "...")
        person = db.collection(u'Kratians').document(u'{}'.format(row['BITS Mail'][:13]))

        data = {
            u'Name': u'{}'.format(row['Full Name']),
            u'Personal Email': u'{}'.format(row['Personal Email']),
            u'BITS Mail': u'{}'.format(row['BITS Mail']),
            u'Certificate ID': u'kratos:{}'.format(row['BITS Mail'][:13]),
            u'Team': int(row['Which Team?']),
            u'Subsystem': u'{}'.format(row['Subsystem?']),
            u'PoR(s)': u'{}'.format(row['Any PoRs or specific title held (comma separated, for multiple)?']).split(','),
            u'LinkedIn': u'{}'.format(row['LinkedIn link']),
            u'Sex': u'{}'.format(row['Sex']),
            u'Year of Joining': u'{}'.format(row['Start date']),
            u'End': u'{}'.format(row['End date']),
            u'Member status': u'{}'.format(row['Are you currently in the team?'])
        }

        person.set(data, merge=True)


