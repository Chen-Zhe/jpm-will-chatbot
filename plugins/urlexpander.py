from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests
import json
import re

class UrlExpanderPlugin(WillPlugin):

    @hear("~exp (?P<input>.*)")
    def expand_url(self, message, input):

        try:
            input_list = [input_item.strip() for input_item in input.split(',')]
            bit_pattern = re.compile("(http:\/\/)?bit.ly\/[a-zA-Z0-9]*")
            goo_pattern = re.compile("(http:\/\/)?goo.gl\/[a-zA-Z0-9]*")

            for shortened_url in input_list:
                if goo_pattern.match(shortened_url):
                    if (shortened_url.find("https://")==-1):
                        shortened_url = "https://" + shortened_url
                    response = requests.get('https://www.googleapis.com/urlshortener/v1/url',
                                            params={'shortUrl': shortened_url, 'key': 'AIzaSyBMDM8HM2_K5FHQH14SZIW2sRsvBb3QIo0'})
                    self.reply(message, "URL Expansion Result \n"
                                        "Short URL: {short_url} \n"
                                        "Long URL: {long_url}".format(short_url=shortened_url.replace(":", "[:]").replace(".", "[.]"), long_url=json.loads(response.text).get('longUrl').replace(":", "[:]").replace(".", "[.]")))
                elif bit_pattern.match(shortened_url):
                    if (shortened_url.find("http://") == -1):
                        shortened_url = "http://" + shortened_url
                    response = requests.get('https://api-ssl.bitly.com/v3/expand',
                                            params={'shortUrl': shortened_url, 'access_token': '369ebc3d0584dceac891e5fcc457eada2d24c1a3', 'format': 'txt'})
                    self.reply(message, "URL Expansion Result \n"
                                    "Short URL: {short_url} \n"
                                    "Long URL: {long_url}".format(short_url=shortened_url.replace(":", "[:]").replace(".", "[.]"), long_url=response.text.replace(":", "[:]").replace(".", "[.]")))

                else:
                    raise Exception()

        except Exception as e:
            self.reply(message, "Request for " + input + " raised an exception!")