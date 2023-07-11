import requests
import hashlib
import base64
from datetime import datetime
import json
import credentials

#Private stuff
username = credentials 
password = credentials
customerID = credentials 389849

#Globals
sublist = []
entries = []

#Roughly determine what season it is
def dateconvert():
    #Format date into day of the year
    global year
    global season
    time = datetime.now()
    day_of_year = time.timetuple().tm_yday
    year = str(time).split('-')[0]
    
    if 256<=day_of_year<347:
        season = 4
    elif 165<=day_of_year<256:
        season = 3
    elif 74<=day_of_year<165:
        season = 2
    else:
        season = 1

#Encode password
def encode_pw(username, password):
    initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
    hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
    return hashInBase64

pwValueToSubmit = encode_pw(username, password)

#Send off authentication stuff
def auth():   
    authInfo = {'email': username, 'password': pwValueToSubmit}
    s.post('https://members-ng.iracing.com/auth', data=authInfo)

#Cookies
s = requests.Session()

# Grabs all session data for all official races within current year/season for specific customer id (you)
# Dumps all data to json file. Also dumps car and series info to json file.
def grab():
    sd = {'season_year':year, 'season_quarter':season, 'cust_id':customerID, 'official_only':True, 'event_types':5}
    r = s.get('https://members-ng.iracing.com/data/results/search_series', params=sd).json()
    url = (r['data']['chunk_info']['base_download_url'])
    file = (r['data']['chunk_info']['chunk_file_names'][0])
    url = "".join([url, file])
    r = s.get(url).json()
    try:
        for n in range(len(r[0])): # Fix this bullshit, it's broken
            sublist.append(r[n]['subsession_id'])
    except:
        pass

    for id in sublist:
        param = {'subsession_id':id}
        r = s.get('https://members-ng.iracing.com/data/results/get', params=param).json()
        r = s.get(r['link']).json()
        out_file = open("json//sessions//"+str(id)+".json", "w")
        json.dump(r, out_file, indent = 6) 
        out_file.close()
        print("[INFO] Saved Session", id, "File")

    r = s.get('https://members-ng.iracing.com/data/series/get').json()
    r = s.get(r['link']).json()
    out_file = open("json//series.json", "w")
    json.dump(r, out_file, indent = 6) 
    out_file.close()
    print("[INFO] Saved Series File")       

    r = s.get('https://members-ng.iracing.com/data/car/get').json()
    r = s.get(r['link']).json()
    out_file = open("json//cars.json", "w")
    json.dump(r, out_file, indent = 6) 
    out_file.close()
    print("[INFO] Saved Car File")

# Digs out all of the useful information from all of the session json
# Dumps Entries file
def dig():
    for id in sublist:
        with open("json//sessions//"+str(id)+".json","r") as file:
            d = json.load(file)
            print("[INFO] File",id,"Read")
            try:
                #Not all sessions are practice -> qualy -> race, so we need to find the race session by type
                raceEvent = None
                for event in d['session_results']:
                    if(event['simsession_type']==6):
                        raceEvent=event
                for i in raceEvent['results']:
                    try:
                        if int(i['cust_id']) == int(customerID):
                            entries.append({
                            "series_id":d['series_id'],
                            "car_id":i['car_id'],
                            "sponsor1":i['livery']['sponsor1'],
                            "sponsor2":i['livery']['sponsor2']
                            })
                            print("[INFO] Entry", id, "appended")
                        else:
                            pass
                    except:
                        pass # This is here because of team_id
            except:
                print("[INFO] Skipped", id, ", Not a Race Session")

    out_file = open("json//entries.json", "w")
    json.dump(entries, out_file, indent = 6)
    out_file.close()
    print("[INFO] Saved Entries File")
 
# Cross references contests json against entries json
def check_contests():  
    with open("json//contests.json", "r") as f1, open("json//sponsors.json", "r") as f2, open("json//cars.json", "r") as f3, open("json//series.json", "r") as f4, open("json//entries.json", "r") as f5:
        contestData = json.load(f1)
        sponsorData = json.load(f2)
        carData = json.load(f3)
        seriesData = json.load(f4)
        entryData = json.load(f5)

        for c in contestData:
            print(c['contest_name'], "eligibility:")
            x=0
            draws = 0
            add =0
            for e in entryData:
                eligibility = 0
                if c['series_dependant'] == True and int(c['series']) == int(e['series_id']):
                    pass
                elif c['series_dependant'] == False:
                    pass
                else:
                    eligibility = 1

                if c['car_dependant'] == True and c['car'] == e['car_id']:
                    pass
                elif c['car_dependant'] == False:
                    pass
                else:
                    eligibility = 1
               
                if c['sponsor_dependant'] == True and c['both_locations'] == True and ((e['sponsor1'] == c['sponsor_number']) or (e['sponsor1'] == c['sponsor_number2'])) and ((e['sponsor2'] == c['sponsor_number']) or (e['sponsor2'] == c['sponsor_number2'])):
                    pass
                elif c['sponsor_dependant'] == True and c['primary_location'] == True and e['sponsor1'] == (c['sponsor_number'] or c['sponsor_number2']):
                    pass
                elif c['sponsor_dependant'] == True and c['secondary_location'] == True and e['sponsor2'] == (c['sponsor_number'] or c['sponsor_number2']):
                    pass
                elif c['sponsor_dependant'] == False:
                    pass
                else:
                    eligibility = 1

                if eligibility>0:
                    pass
                else:
                    x=x+1
                
            if x >= c['races_to_enter']:
                draws = draws+1
                if x> c['races_to_enter'] and c['additional_entries'] == True:
                    add = x-int(c['races_to_enter'])
                    draws = draws + add
            else:
                pass

            print("Eligible races:",x)
            print("Draws:",draws,"\n")

                       
auth()
dateconvert()
grab()
dig()
check_contests()
