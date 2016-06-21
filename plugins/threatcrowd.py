from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests, json


class threatcrowdemail(WillPlugin):



    @respond_to("email (?P<input>.*)")
    def check_email(self, message, input):
        result = requests.get("https://www.threatcrowd.org/searchApi/v2/email/report/", params={"email": input})
        j = json.loads(result.text)

        if j['response_code']=="1":

            count = len(j['domains'])

            end = 5
            if len(j["domains"])<5:
                end = len(j["domains"])
            domainlist = "\n".join(j["domains"][0:end])

            response = "Threatcrowd result: \n" + "Total number of Domain = " + str(count) + "\n" +"Most recently registered domain: \n" + domainlist

        else:
            response = "Threatcrowd result: \n" + "Total number of Domain = 0"

        self.reply(message, response)



s = threatcrowdemail()
s.check_email("eee","domainregistration@jpmchase.com")

