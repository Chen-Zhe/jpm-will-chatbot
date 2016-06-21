from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests
import re
class WhoisIP(WillPlugin):

    @hear("~ip(-whois)? (?P<ip>.*)")
    def check_whois(self, message, ip):
        result_text = requests.get("https://who.is/whois-ip/ip-address/"+ip,headers= {"User-Agent": "Mozilla/5.0"}).text
        whois_text = re.match('.*<div class="col-md-12 queryResponseBodyKey"><pre>(.*)</pre></div>',result_text, re.DOTALL).group(1)
        return self.reply(message,whois_text)