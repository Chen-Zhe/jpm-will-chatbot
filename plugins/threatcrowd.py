from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests, json

import base64
import config
class threatcrowdemail(WillPlugin):

    @hear("~email(-tc)? (?P<input>.*)")
    def check_email(self, message, input):

        input_list = [input_item.strip() for input_item in input.split(',')]
        for email in input_list:
            result = requests.get("https://www.threatcrowd.org/searchApi/v2/email/report/", params={"email": email})
            j = json.loads(result.text)

            if j['response_code']=="0":

                response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".",
                                                                                   "[.]") + "\nTotal number of Domains: 0"

            else:
                count = len(j['domains'])

                end = 5
                if len(j["domains"]) < 5:
                    end = len(j["domains"])
                domainlist = ", ".join(j["domains"][0:end])

                response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".",
                                                                                   "[.]") + "\nTotal number of domains: " + str(
                    count) + "\n" + "Most recently registered domains: " + domainlist

                if count >= 3:

                    encoded_email_key = base64.b64encode(email)

                    self.save(email, j["domains"])

                    response += "\nurl: http://localhost:"+config.HTTPSERVER_PORT+"/visualize/"+encoded_email_key


            self.reply(message, response)


