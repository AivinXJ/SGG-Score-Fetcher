import json
from sgqlc.endpoint.http import HTTPEndpoint
import tkinter as tk
import urllib.request
from urllib.request import Request
import time
from PIL import Image
import requests
from tkinter import messagebox
import os
versionhere = "Current Version : 0.3"

screen = tk.Tk()
screen.title("Smashgg Auto Score Changer")

screen.resizable(False, False)

link = f"https://aivinxj.github.io/smashgg-score.github.io/"
request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(request).read().decode('utf-8')

if str(versionhere) not in res:
    updatestatus = tk.Label(screen, text= "An update is available, go to https://aivinxj.github.io/smashgg-score.github.io/ and update it")
else:
    updatestatus = tk.Label(screen, text= "No update available, your program is up-to-date")

label1 = tk.Label(text= "Tool Made By @AivinXJ")
label2 = tk.Label(text= "")
label3 = tk.Label(text= "")
keylabel = tk.Label(text= "API Key")
entry1 = tk.Entry(screen)
setidlabel = tk.Label(text= "Set ID")
entry2 = tk.Entry(screen)
# Packing
keylabel.pack()
entry1.pack()
setidlabel.pack()
entry2.pack()
def Startthecode():
    try:
        SMASHGG_API_KEY = entry1.get()
        SetID = entry2.get()
        str(SetID)

        query = '''
        query InProgressSet {{
        set(id: {TheID}) {{
            state
            fullRoundText
            games {{
            selections {{
                selectionValue
            }}
            }}
            event {{
            name
            tournament {{
                name
            }}
            }}
            slots {{
            entrant {{
                name
            }}
            standing {{
                stats {{
                score {{
                    value
                }}
                }}
            }}
            }}
        }}
        }}
        '''.format(TheID = SetID)

        url = 'https://api.smash.gg/gql/alpha'
        headers = {'Authorization': 'Bearer ' + SMASHGG_API_KEY}
        endpoint = HTTPEndpoint(url, headers)
        data = endpoint(query, variables=None)
        thejson = json.dumps(data, indent=2)

        with open('thejson.json', 'w') as f:
            f.write(thejson)

        with open('thejson.json', 'r') as f:
            data = json.load(f)
            json.dumps(data, indent=2)
        
        leftname = data['data']['set']['slots'][0]['entrant']['name']
        leftscore = data['data']['set']['slots'][0]['standing']['stats']['score']['value']
        rightname = data['data']['set']['slots'][1]['entrant']['name']
        rightscore = data['data']['set']['slots'][1]['standing']['stats']['score']['value']
        leftlegend = data['data']['set']['games'][0]['selections'][0]['selectionValue'] or None
        rightlegend = data['data']['set']['games'][0]['selections'][1]['selectionValue'] or None
        request = Request(f"https://api.smash.gg/set/{SetID}", headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(request).read()
        OldApiData = json.loads(res)

        setname = data['data']['set']['fullRoundText']

        if rightscore != None:
            pass
        else:
            rightscore = 0
        
        if leftscore != None:
            pass
        else:
            leftscore = 0
        
        with open('leftname.txt', 'w') as f:
            f.write(str(leftname))

        with open('leftscore.txt', 'w') as f:
            f.write(str(leftscore))

        with open('rightname.txt', 'w') as f:
            f.write(str(rightname))

        with open('rightscore.txt', 'w') as f:
            f.write(str(rightscore))

        with open('setname.txt', 'w') as f:
            try:
                f.write(f"{setname} | BO{OldApiData['entities']['sets']['bestOf']}")
            except:
                f.write(f"{setname}")

        try:
            with open('leftlegend.txt', 'w') as f:
                f.write(str(leftlegend))
        except:
            pass
        
        try:
            with open('rightlegend.txt', 'w') as f:
                f.write(str(rightlegend))
        except:
            pass
        
        link = "https://api.smash.gg/characters"
        request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(request).read()
        data = json.loads(res)
        try:
            var = 0
            with open("leftlegend.txt", 'r') as f:
                contents = f.read()
                for items in data['entities']['character']:
                    legendid = data['entities']['character'][var]['id']
                    legendname = data['entities']['character'][var]['name']
                    gameid = data['entities']['character'][var]['videogameId']
                    url = data['entities']['character'][var]['images'][0]['url']
                    if legendid == int(contents):
                        if gameid == 15:
                            link = f"https://aivinxj.github.io/smashgg-bh-images.github.io/data/data.json"
                            request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                            res = urllib.request.urlopen(request).read().decode()
                            bhimagedata = json.loads(res)
                            img = Image.open(requests.get(bhimagedata[str(legendid)], stream=True).raw)
                            # resized_img = img.resize((int(img.size[0] / 10), int(img.size[1] / 10)))
                            resized_img = img.resize((100, 100))
                            resized_img.save("leftlegend.png")
                        else:
                            img = Image.open(requests.get(url, stream=True).raw)
                            img.save("leftlegend.png")

                    var += 1
        except:
            try:
                os.remove("leftlegend.png")
            except:
                pass

        try:     
            var = 0
            with open("rightlegend.txt", 'r') as f:
                contents = f.read()
                for items in data['entities']['character']:
                    legendid = data['entities']['character'][var]['id']
                    legendname = data['entities']['character'][var]['name']
                    gameid = data['entities']['character'][var]['videogameId']
                    url = data['entities']['character'][var]['images'][0]['url']
                    if legendid == int(contents):
                        if gameid == 15:
                            link = f"https://aivinxj.github.io/smashgg-bh-images.github.io/data/data.json"
                            request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                            res = urllib.request.urlopen(request).read().decode()
                            bhimagedata = json.loads(res)
                            img = Image.open(requests.get(bhimagedata[str(legendid)], stream=True).raw)
                            # resized_img = img.resize((int(img.size[0] / 10), int(img.size[1] / 10)))
                            resized_img = img.resize((100, 100))
                            hori_flippedImage = resized_img.transpose(Image.FLIP_LEFT_RIGHT)
                            hori_flippedImage.save("rightlegend.png")
                        else:
                            img = Image.open(requests.get(url, stream=True).raw)
                            hori_flippedImage = img.transpose(Image.FLIP_LEFT_RIGHT)
                            hori_flippedImage.save("rightlegend.png")

                    var += 1

        except:
            try:
                os.remove("rightlegend.png")
            except:
                pass 
        

    except:
        messagebox.showerror("Error (Smashgg Auto Score Changer)", "Make sure you filled all the required boxes and that these numbers are valid.")

        
btn1 = tk.Button(screen, text= "Call The API", command = Startthecode)
label3.pack()
btn1.pack()
label2.pack()
label1.pack()
updatestatus.pack()

screen.mainloop()
