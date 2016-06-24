from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings



class BaseSixFourPlugin(WillPlugin):

    # Function names should be lowercase, with words separated by underscores as necessary to improve readability.
    @hear("^~b64 (?P<text>.*)")
    def base_six_four(self, message, text):
        text_arr = text.split()
        # self.reply(message, "text arr: %s" % str(text_arr))
        if len(text_arr) < 2:
            self.reply(message, "Invalid! usage: ~b64 <encode/decode> <text>")
        else:
            if text_arr[0] == "encode":
                # TODO: check if its valid string
                make_string = text_arr[1:]
                base_six_four = ""
                for word in make_string:
                    base_six_four = base_six_four + word + " "
                ret_text = base_six_four.strip().encode('base64').strip()
                self.reply(message, "Your base64 encoded string:\n" + ret_text)
            elif text_arr[0] == "decode":
                self.reply(message, "Your base64 decoded string:\n" + text_arr[1].decode('base64'))
            else:
                self.reply(message, "Invalid! usage: base64 <encode/decode> <text>")


