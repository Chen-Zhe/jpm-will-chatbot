from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests, json


class threatcrowdemail(WillPlugin):



    @hear("~email(-tc)? (?P<input>.*)")
    def check_email(self, message, input):

        input_list = [input_item.strip() for input_item in input.split(',')]
        for email in input_list:
            result = requests.get("https://www.threatcrowd.org/searchApi/v2/email/report/", params={"email": email})
            j = json.loads(result.text)

            if j['response_code']=="1":

                count = len(j['domains'])

                end = 5
                if len(j["domains"])<5:
                    end = len(j["domains"])
                domainlist = ", ".join(j["domains"][0:end])


                response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".", "[.]") + "\nTotal number of domains: " + str(count) + "\n" +"Most recently registered domains: " + domainlist

            else:
                response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".", "[.]") + "\nTotal number of Domains: 0"

            self.reply(message, response)
        #print response



#s = threatcrowdemail()
#s.check_email("eee","domainregistration@jpmchase.com")

