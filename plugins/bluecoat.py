from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

import json
import sys

import re


class SiteReview(object):
    def __init__(self):
        self.baseurl = "http://sitereview.bluecoat.com/rest/categorization"
        self.useragent = {"User-Agent": "Mozilla/5.0"}
        self.category = ""
        self.date = ""

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
            self.category = re.match(r"<a.*>(.*)</a>", response["categorization"]).group(1)
            self.date = re.match(r".*Last Time Rated\/Reviewed:(.*)<img", response["ratedate"]).group(1)


class BCPlugin(WillPlugin):

    @hear("~(ip|url) (?P<site_address>.*)")
    def check_bc(self, message, site_address):

        s = SiteReview()
        response = s.sitereview(site_address)

        reply = "This site has not yet been rated!"

        if not response["unrated"]:
            s.check_response(response)
            reply = "Category: " + s.category + "\nLast Time Rated/Reviewed:"+ s.date

        self.reply(message, "\nBluecoat site review:\n"+reply)