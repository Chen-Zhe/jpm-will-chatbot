from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class report:
    def __init__(self, id, indicators, date, url):
        self.id = id
        self.indicator = indicators
        self.date = date
        self.url = url

class intelme(WillPlugin):

    @hear("~intelme? (?P<ioc>.*)")
    def pull_report(self, message, ioc):
        reply = ""
        database = [report(12345,"123.123.123.123", "2016-6-24", "https://www.fireeye.com/blog/threat-research/2016/06/red-line-drawn-china-espionage.html"),
                    report(12346, "d41d8cd98f00b204e9800998ecf8427e", "2016-4-23", "https://www.fireeye.com/blog/threat-research/2016/06/automatically-extracting-obfuscated-strings.html"),
                    report(12347, "123.123.123.123", "2015-2-4", "https://www.fireeye.com/blog/threat-research/2016/06/resurrection-of-the-evil-miner.html"),

                    ]

        for rep in database:
            if rep.indicator == ioc:
                reply+="\n ID: "+str(rep.id)+" URL: "+rep.url

        if reply=="":
            reply="I can't find any reports related to this IOC"
        else:
            reply="I found the following reports related to this IOC"+reply

        self.reply(message, reply)