from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi

class VT_UrlPlugin(WillPlugin):

	def __init__(self):
		self.API_KEY = '87ab79d0a21d9a7ae5c5558969c7d6b38defa1901b77d27796ae466b3823c776'

	@respond_to("url (?P<input>[\S*]+)")
	def check_url(self, message, input):
		vt = VirusTotalPublicApi(self.API_KEY)
		try:
			scan_report = vt.get_url_report(input)
			self.reply(message, "VirusTotal Scan Result \n"
					   			"URL: {url_request} \n"
								"Scan date: {scan_date} \n"
								"Detection rate: {positives} out of {total} \n"
								"Permalink: {permalink}".format(url_request=scan_report.get("results").get("url"),
																scan_date=scan_report.get("results").get("scan_date"),
																positives=scan_report.get("results").get("positives"),
																total=scan_report.get("results").get("total"),
																permalink=scan_report.get("results").get("permalink")))

		except Exception as e:
			self.reply(message, "Request for " + input + " raised an exception!")


class VT_HashPlugin(WillPlugin):

	def __init__(self):
		self.API_KEY = '87ab79d0a21d9a7ae5c5558969c7d6b38defa1901b77d27796ae466b3823c776'

	@respond_to("hash (?P<input>[\S*]+)")
	def check_url(self, message, input):
		vt = VirusTotalPublicApi(self.API_KEY)
		try:
			scan_report = vt.get_file_report(input)
			self.reply(message, "VirusTotal Scan Result \n"
								"Scan date: {scan_date} \n"
								"Detection rate: {positives} out of {total} \n"
								"SHA1: {sha1} \n"
								"MD5: {md5} \n"
								"Permalink: {permalink}".format(scan_date=scan_report.get("results").get("scan_date"),
																positives=scan_report.get("results").get("positives"),
																total=scan_report.get("results").get("total"),
																sha1=scan_report.get("results").get("sha1"),
																md5=scan_report.get("results").get("md5"),
																permalink=scan_report.get("results").get("permalink")))

		except Exception as e:
			self.reply(message, "Request for " + input + " raised an exception!")