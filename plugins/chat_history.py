from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import json
import datetime


class HistoryPlugin(WillPlugin):

    @hear("~find (?P<input>.*)")
    def get_history(self, message, input):
        match = False
        room = self.get_room_from_message(message)
        history = room.history
        reply = "IOC Query History \n"
        try:
            for count in range(len(history)):
                temp_msg = history[count]["message"]

                if (input in temp_msg and "find" not in temp_msg):
                    match = True
                    if (history[count]["from"] != "xiao bot"):
                        reply += history[count]["from"].get("name") + ", " + history[count]["date"].strftime("%d/%m/%Y %H:%M:%S") + ", " + history[count]["message"] + "\n"
            if (not match):
                self.reply(message, "Cannot find the same IOC query in the past 100 messages")
            else:
                self.reply(message, reply)
        except:
            self.reply(message, "Error: please try again")