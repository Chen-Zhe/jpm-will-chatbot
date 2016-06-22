from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests
import re
import json
class whois(WillPlugin):

    @hear("~whois (?P<text>.*)")
    def check_whois(self, message, text):

        check_ip = text.split(".")[-1]
        try:
            int(check_ip) #if success, it's an ip
            result_text = requests.get("https://who.is/whois-ip/ip-address/"+text,headers= {"User-Agent": "Mozilla/5.0"}).text
            whois_text = re.match('.*<div class="col-md-12 queryResponseBodyKey"><pre>(.*)</pre></div>',result_text, re.DOTALL).group(1)
            return self.reply(message,whois_text)
        # it's a url
        except:
            result_text = requests.get("http://api.whoapi.com/?apikey=3fb4ea768efd677bfbed2d705bc6f47a&r=whois&domain=" + text,
                                       headers={"User-Agent": "Mozilla/5.0"}).text

            try:
                whois_dict = json.loads(result_text)
                if whois_dict["status"] == "0":

                    for contact in whois_dict["contacts"]:
                        if contact["type"] == "admin":
                            admin_info="Name: {name} \n" \
                                "Organization: {org} \n" \
                                "Address: {address} \n" \
                                "Phone: {phone} \n" \
                                "Fax: {fax} \n" \
                                "Email: {email}".format(
                                name=contact["name"],
                                org=contact["organization"],
                                address=contact["full_address"].replace("\n", " "),
                                phone=contact["phone"],
                                fax=contact["fax"],
                                email=contact["email"].replace(".", "[.]"),
                                )
                            break
                        else:
                            admin_info="NIL"

                    reply = "Whois domain record\n" \
                            "URL: {site}\n" \
                            "Date Created: {date_created}\n" \
                            "Date Updated: {date_updated}\n\n" \
                            "Site Admin Information:\n".format(site=text.replace(":", "[:]").replace(".", "[.]"),
                                       date_created=str(whois_dict["date_created"]),
                                       date_updated=str(whois_dict["date_updated"])
                                       ) + admin_info
                else:
                    reply="API source error, possible API usage limit exceed!"
            except:
                reply = "Error: domain not in database or something else is wrong!"

            return self.reply(message, reply)
