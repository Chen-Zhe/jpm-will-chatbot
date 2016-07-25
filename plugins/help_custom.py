from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class HelpPlugin(WillPlugin):

    @hear("^~help")
    def help_reply(self, message):

		self.reply(message,"\nNoblesse oblige:\n" \
							"\t ~help \n" \
							"\t ~ip \t< ip_addr > \n" \
							"\t ~url \t< url >\n" \
							"\t ~hash \t< md5 >\n" \
							"\t ~exp \t< shorten-url >\n" \
							"\t ~find \t< IOC >\n" \
							"\t ~email \t< example@example.com >\n" \
							"\t ~b64 < encode/decode > < text > \n" \
				            "\t ~arcme \t< IOC(s) > \n" \
				            "\t ~intelme \t< IOC(s) >\n" )
