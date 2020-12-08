import json
from sgqlc.endpoint.http import HTTPEndpoint
import tkinter as tk

screen = tk.Tk()
screen.title("Smashgg Auto Score Changer")
screen.geometry('400x250')

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

def log_scores():
    SMASHGG_API_KEY = entry1.get()
    SetID = entry2.get()
    str(SetID)

    query = '''
    query InProgressSet {{
    set(id: {TheID}) {{
        state
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

    with open('thejson.json', 'r') as f:  # Remove this line if you only want to write into a JSON file
        data = json.load(f)  # Remove this line if you only want to write into a JSON file
        json.dumps(data, indent=2)  # Remove this line if you only want to write into a JSON file
    
    leftname = data['data']['set']['slots'][0]['entrant']['name']  # Remove this line if you only want to write into a JSON file
    leftscore = data['data']['set']['slots'][0]['standing']['stats']['score']['value']  # Remove this line if you only want to write into a JSON file
    rightname = data['data']['set']['slots'][1]['entrant']['name']  # Remove this line if you only want to write into a JSON file
    rightscore = data['data']['set']['slots'][1]['standing']['stats']['score']['value']  # Remove this line if you only want to write into a JSON file

    with open('leftname.txt', 'w') as f:  # Remove this line if you only want to write into a JSON file
        f.write(str(leftname))  # Remove this line if you only want to write into a JSON file

    with open('leftscore.txt', 'w') as f:  # Remove this line if you only want to write into a JSON file
        f.write(str(leftscore))  # Remove this line if you only want to write into a JSON file

    with open('rightname.txt', 'w') as f:  # Remove this line if you only want to write into a JSON file
        f.write(str(rightname))  # Remove this line if you only want to write into a JSON file

    with open('rightscore.txt', 'w') as f:  # Remove this line if you only want to write into a JSON file
        f.write(str(rightscore))  # Remove this line if you only want to write into a JSON file





btn1 = tk.Button(screen, text= "Fetch Scores", command = log_scores)
label3.pack()
btn1.pack()
label2.pack()
label1.pack()


screen.mainloop()
