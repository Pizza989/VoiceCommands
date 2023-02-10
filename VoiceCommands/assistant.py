import json

import core


with open(".voice_commands/commands.json", "r", encoding="utf-8") as file:
    commands = json.load(file)


class Assistant:
    def __init__(self) -> None:
        self.listener = core.Listener()
        self.speaker = core.Speaker()

    # TODO: Implement confirm behaviour
    def execute_cmd(self, cmd: dict):
        if "text" in cmd:
            self.speaker.say(cmd["text"])

    # TODO: Handle connection of python function to event
    def execute_event(self, event: dict):
        if event["id"] in commands["commands"]:
            self.execute_cmd(commands["commands"][event["id"]])
        if "options" in event:
            print([each["id"] for each in event["options"]])
            for ev in self.listener.listen(event["options"]):
                self.execute_event(ev)
                if not ev["id"] == "unrecognised":
                    break

    def run(self):
        for event in self.listener.listen():
            self.execute_event(event)


a = Assistant()
a.run()
