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
import webbrowser

versionhere = "Current Version : 0.3"

screen = tk.Tk()
screen.title("SGG Score Fetcher")

screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()
the_geometry = "{}x{}+{}+{}".format((550), (250), (int(screen.winfo_screenwidth() / 2) - screen.winfo_reqwidth() - 80), (int(screen.winfo_screenheight() / 2) - screen.winfo_reqheight()))
screen.geometry(the_geometry)
screen.resizable(False, False)


link = f"https://aivinxj.github.io/smashgg-score.github.io/"
request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(request).read().decode('utf-8')

if str(versionhere) not in res:
    def callback(url):
        webbrowser.open_new(url)

    updatestatus = tk.Label(screen, text= "An update is available, go to https://aivinxj.github.io/smashgg-score.github.io/ and update it", fg ="#0000ff")
    updatestatus.bind("<Button-1>", lambda e: callback("https://aivinxj.github.io/smashgg-score.github.io/"))
else:
    updatestatus = tk.Label(screen, text= "No update available, your program is up-to-date")

label1 = tk.Label(text= "Tool Made By @AivinXJ")
label2 = tk.Label(text= "")
label3 = tk.Label(text= "")
keylabel = tk.Label(text= "API Key")
api_key_entry = tk.Entry(screen)

try:
    f = open('api_key.txt', 'r')
    api_key_entry.insert(0, f.read())
    f.close()
except:
    pass


setidlabel = tk.Label(text= "Set ID")
set_id_entry = tk.Entry(screen)

keylabel.pack()
api_key_entry.pack()
setidlabel.pack()
set_id_entry.pack()

def Startthecode():
    try:
        SMASHGG_API_KEY = api_key_entry.get()
        SetID = set_id_entry.get()
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
        try:
            leftlegend = data['data']['set']['games'][0]['selections'][0]['selectionValue']
        except:
            pass
        try:
            rightlegend = data['data']['set']['games'][0]['selections'][1]['selectionValue']
        except:
            pass
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
        
        with open('speadsheet.csv', 'w') as speadsheet:
            ss_data.write(f"{leftname},{leftscore},{setname},{rightscore},{rightname}")

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
                url = "https://cdn.discordapp.com/attachments/804753013410496552/808587264740294656/100x100Transparent.png"
                img = Image.open(requests.get(url, stream=True).raw)
                img.save("leftlegend.png")
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
                url = "https://cdn.discordapp.com/attachments/804753013410496552/808587264740294656/100x100Transparent.png"
                img = Image.open(requests.get(url, stream=True).raw)
                img.save("rightlegend.png")
            except:
                pass 
        

    except:
        try:
            SMASHGG_API_KEY = api_key_entry.get()
            SetID = set_id_entry.get()
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

        except:
            messagebox.showerror("Error (Smashgg Auto Score Changer)", "Make sure you filled all the required boxes and that these numbers are valid.")

        
btn1 = tk.Button(screen, text= "Call The API", command = Startthecode, bg = "#CB333B", fg = "#FFFFFF")
label3.pack()
btn1.pack()
label2.pack()
label1.pack()
updatestatus.pack()


screen.mainloop()
