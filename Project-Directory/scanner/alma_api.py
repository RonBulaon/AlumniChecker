import requests
import json, xmltodict
from .models import Configuration

def getAPI():
    return Configuration.objects.all().first()

def getAlmaRecords(barcode):
    name, email = '', ''
    apikey = str(getAPI())
    URL = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/users/"+str(barcode)+"?apikey="+apikey+"&Content-Type=application/json&accept=application/json" 

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = xmltodict.parse(response.text)
            data = json.dumps(data)
            data = json.loads(data)
            name = data["user"]["last_name"]
            email = data["user"]["contact_info"] \
                ["emails"]["email"]["email_address"]
    except:
        return {
            "name" : '', 
            "email" : ''
        }
    else:
        return {
            "name" : name, 
            "email" : email
        }