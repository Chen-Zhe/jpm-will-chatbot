from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

import json
import sys

class SiteReview(object):
    def __init__(self):
        self.baseurl = "http://sitereview.bluecoat.com/rest/categorization"
        self.useragent = {"User-Agent": "Mozilla/5.0"}

    def sitereview(self, url):
        payload = {"url": url}

        try:
            self.req = requests.post(
                                    self.baseurl,
                                    headers=self.useragent,
                                    data=payload
                                    )
        except requests.ConnectionError:
            sys.exit("[-] ConnectionError: " \
                     "A connection error occurred")

        return json.loads(self.req.content)

    def check_response(self, response):

        if self.req.status_code != 200:
            sys.exit("[-] HTTP {} returned".format(req.status_code))

        elif "error" in response:
            sys.exit(response["error"])

        else:
            begin = response["categorization"].find("\">")
            end = response["categorization"].find("</a>")
            self.category = response["categorization"][begin+2:end]
            end = response["ratedate"].find("<")
            self.date = response["ratedate"][:end]


class BCPlugin(WillPlugin):

    @respond_to("ip (?P<ip_addr>.*)")
    def check_bc(self, message, ip_addr):

        s = SiteReview()
        response = s.sitereview(ip_addr)

        reply = "This site has not yet been rated!"

        if not response["unrated"]:
            s.check_response(response)
            reply = "Category: " + s.category + "\n"+ s.date

        self.reply(message, "\nBluecoat site review:\n"+reply)