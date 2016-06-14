from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class BonjourPlugin(WillPlugin):

    @respond_to("bonjour")
    def say_bonjour_will(self, message):
        """bonjour: I know how to say bonjour! In French!"""
        self.reply(message, "bonjour!")


