from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

import json

class PTPlugin(WillPlugin):

    @respond_to("url (?P<url>.*)")
    def check_phishing(self, message, url):
        if url.find("http://")==-1:
            url = "http://"+ url

        response = requests.post("http://checkurl.phishtank.com/checkurl/",
                            data={"url":encoded, "format": "json",
                                  "app_key": "a44346b8167abe4ab6e177f0afe21f0628c57facaba5699085a7a1400b3e2789"}
                                 ).text

        json_response = json.loads(response)

        success=json_response["meta"]["success"]

        reply="\nPhishtank Report\nURL/URI: "+url\
              +"\nTimestamp"+str(json_response["meta"]["timestamp"])\
              +"\nSuccess: "+str(success)

        if success:


        self.reply(message, response)