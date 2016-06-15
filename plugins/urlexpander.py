from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests
import json
import re

class UrlExpanderPlugin(WillPlugin):

    @respond_to("exp (?P<input>[\S*]+)")
    def expand_url(self, message, input):

        try:
            bit_pattern = re.compile("(http:\/\/)?bit.ly\/[a-zA-Z0-9]*")
            goo_pattern = re.compile("(http:\/\/)?goo.gl\/[a-zA-Z0-9]*")
            if goo_pattern.match(input):
                if (input.find("https://")==-1):
                    input = "https://" + input
                response = requests.get('https://www.googleapis.com/urlshortener/v1/url',
                                        params={'shortUrl': input, 'key': 'AIzaSyBMDM8HM2_K5FHQH14SZIW2sRsvBb3QIo0'})
                self.reply(message, "URL Expansion Result \n"
                                    "Short URL: {short_url} \n"
                                    "Long URL: {long_url}".format(short_url=input, long_url=json.loads(response.text).get('longUrl')))
            elif bit_pattern.match(input):
                if (input.find("http://") == -1):
                    input = "http://" + input
                response = requests.get('https://api-ssl.bitly.com/v3/expand',
                                        params={'shortUrl': input, 'access_token': '369ebc3d0584dceac891e5fcc457eada2d24c1a3', 'format': 'txt'})
                self.reply(message, "URL Expansion Result \n"
                                "Short URL: {short_url} \n"
                                "Long URL: {long_url}".format(short_url=input, long_url=response.text))

            else:
                raise Exception()

        except Exception as e:
            self.reply(message, "Request for " + input + " raised an exception!")