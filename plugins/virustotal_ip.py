from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi

class IPaddrPlugin(WillPlugin):

	def __init__(self):
		self.API_KEY = '87ab79d0a21d9a7ae5c5558969c7d6b38defa1901b77d27796ae466b3823c776'

	@respond_to("ip (?P<ip_addr>[\S*]+)")
	def ip(self, message, ip_addr):
		vt = VirusTotalPublicApi(self.API_KEY)
		try:
			self.reply(message, json.dumps(vt.scan_url(ip_addr), sort_keys=False, indent=4))
			self.reply(message, json.dumps(vt.get_url_report(ip_addr), sort_keys=False, indent=4))
		except Exception as e:
			self.reply(message, "Request for " + ip_addr + " raised an exception!" )


