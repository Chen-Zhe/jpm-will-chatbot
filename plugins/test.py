from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class TestMePlugin(WillPlugin):

    @respond_to("^testme")
    def testme(self, message):
        self.reply(message, message)


