from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

arcsight_db = [{"case_id": "AS-3233", "sid": "R601601", "severity": "medium", "ip": ["123.123.123.123", "69.69.69.69"],
                 "md5": ["md5md5md5md5oooooo"], "c2": ["secret.myftp.org"]},
               {"case_id": "AS-3222", "sid": "D525656", "severity": "high", "ip": ["123.23.3.3", "8.8.8.9"],
                 "md5": ["md5md5md5mdexample"], "c2": ["my.c2.cnc"]},
               {"case_id": "AS-3221", "sid": "G596556", "severity": "low", "ip": ["169.8.3.3", "63.12.10.3"],
                 "md5": ["md5md5md5lolllllll"], "c2": ["my.c3.sg"]},
               ]

class ArcMePlugin(WillPlugin):

    @hear("~arcme (?P<input>.*)")
    def find_IOC(self, message, input):
        input_list = [input_item.strip() for input_item in input.split(',')]
        match_cases = []
        for case in arcsight_db:
            match = False
            for input_item in input_list:
                for key in case:
                    if input_item in case.get(key):
                        match = True
                        break
            if match:
                match_cases.append(case)
        if (len(match_cases) == 0):
            self.reply(message, "There are no matched past cases.")
        else:
            if len(match_cases) == 1:
                reply = "There is 1 matched case. \n"
            else:
                reply = "There are {num_of_matches} matched cases. \n".format(num_of_matches=len(match_cases))
            for match_case in match_cases:
                reply = reply +  "Case ID: {case_id} \n" \
                        "SID: {sid} \n" \
                        "Severity: {severity} \n" \
                        "IP: {ip} \n" \
                        "MD5: {md5} \n" \
                        "C2: {c2} \n \n".format(case_id = match_case.get("case_id"),
                                          sid = match_case.get("sid"),
                                          severity = match_case.get("severity"),
                                          ip = match_case.get("ip"),
                                          md5 = match_case.get("md5"),
                                          c2 = match_case.get("c2"))
            self.reply(message, reply)








