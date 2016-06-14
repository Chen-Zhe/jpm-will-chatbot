from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import simplejson
import urllib
import urllib2


class VirusTotalPlugin(WillPlugin):

    @respond_to("url (?P<url_rq>.*)")
    def check_url(self, message, url_rq):
	url = "https://www.virustotal.com/vtapi/v2/url/report"
	parameters = {"resource": url_rq, "apikey": "87ab79d0a21d9a7ae5c5558969c7d6b38defa1901b77d27796ae466b3823c776"}
	data = urllib.urlencode(parameters)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()
	response_dict = simplejson.loads(json)
        self.reply(message, "Detection rate: " + str(response_dict.get('positives')) + " out of " + str(response_dict.get('total') ))



