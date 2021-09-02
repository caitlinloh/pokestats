from dotenv import load_dotenv
from flask import Flask, request
import json
import requests
import os

load_dotenv()
app = Flask('bootcamp')

# app
@app.route("/pokemon", methods=['GET', 'POST'])
def pokemon():
    # make request to pokeapi
    name = request.values['Body'].lower().strip()
    reqPath = "http://pokeapi.co/api/v2/pokemon/" + name
    response = requests.get(reqPath)

    # check to make sure response exists
    if response.status_code != 200:
        print("error: status code not 200")
        errorTemplate = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>{}</Message>
        </Response>"""
        return errorTemplate.format("Pokemon not found")

    data = json.loads(response.content)

    # get image
    # idNum = data["id"]
    # imgLink = "https://pokeres.bastionbot.org/images/pokemon/" + str(idNum) + ".png"
    # print(imgLink)
    imgLink = "https://img.pokemondb.net/artwork/" + name + ".jpg"
    print(imgLink)

    # get stats
    totalStats = 0
    statString = "STATS\n"
    statTemplate = "{}: {}\n"
    pokestats = data["stats"]
    for i in range(len(pokestats)):
        statVal = pokestats[i]["base_stat"]
        statName = pokestats[i]["stat"]["name"]
        statString += statTemplate.format(statName, statVal)
        totalStats += statVal
    statString += "TOTAL: " + str(totalStats)

    # format and send response
    respTemplate = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>
            <Media>{}</Media>
            <Body>{}</Body>
        </Message>
    </Response>"""
    ret = respTemplate.format(imgLink, statString)
    print(ret)
    return ret
    # return respTemplate.format(imgLink, statString)

    ## no image version
    # respTemplate = """<?xml version="1.0" encoding="UTF-8"?>
    #     <Response>
    #     <Message>
    #         <Body>{}</Body>
    #     </Message>
    #     </Response>"""
    # return respTemplate.format(statString)

if __name__ == "__main__":
    ## SETUP BEFOREHAND
    #  1. run `ngrok http 5000` in terminal
    #  2. copy the forwarding link, paste it into Twilio console for SMS, click Save
    #  3. run `source venv/bin/activate` in terminal
    #  4. run `python3 app.py` in terminal
    app.run(debug=True)