from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

class WhoisURL(WillPlugin):

    @hear("~url(-whois)? (?P<url>.*)")
    def check_whois(self, url):
        result = requests.get("http://api.whoapi.com/?apikey=3fb4ea768efd677bfbed2d705bc6f47a&r=whois&domain="+url,headers= {"User-Agent": "Mozilla/5.0"})