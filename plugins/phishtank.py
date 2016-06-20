from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

import json
import base64

class PTPlugin(WillPlugin):

    @hear("~url(-pt)? (?P<input>.*)")
    def check_phishing(self, message, input):

        input_list = [input_item.strip() for input_item in input.split(',')]

        for site in input_list:
            if site.find("http://")==-1:
                site = "http://"+ site

            response = requests.post("http://checkurl.phishtank.com/checkurl/",
                                     data={"url":base64.b64encode(site.encode("utf-8")), "format": "json",
                                           "app_key": "a44346b8167abe4ab6e177f0afe21f0628c57facaba5699085a7a1400b3e2789"}
                                    ).text

            json_response = json.loads(response)
            success=json_response["meta"]["status"]
            reply="PhishTank Scan Result \n" \
                  "URL: {site} \n" \
                  "Timestamp: {timestamp} \n".format(site = site.replace(":", "[:]").replace(".", "[.]"), timestamp = str(json_response["meta"]["timestamp"]))

            if success:
                reply += "Is phishing site: " + str(json_response["results"]["in_database"])

            self.reply(message, reply)