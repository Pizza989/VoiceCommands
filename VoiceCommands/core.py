import json
import numpy as np
import sounddevice as sd

from stt import Model
from TTS.api import TTS

import scoring


with open(".voice_commands/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open(".voice_commands/commands.json", "r", encoding="utf-8") as file:
    commands = json.load(file)


class Listener(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, config["models"]["stt"]["rel_path"], **kwargs)
        _ = config["models"]["stt"]["scorer"]
        self.enableExternalScorer(_) if _ else None
        self.__is_talking = False
        self.__silence_duration = 0
        self.__buffer = []

    # Optimise memory usage:
    #   Saving 64-bit int in buffer using only 16-bit int for recognition
    def recognition(self):
        with sd.InputStream(
            dtype="int16", samplerate=config["models"]["stt"]["sample_rate"]
        ) as stream:
            while True:
                if stream.read_available:
                    indata = stream.read(stream.read_available)[0]
                    if (
                        indata.max()
                        > config["recognition"]["talking_threshold"]
                    ):
                        self.__is_talking = True
                        self.__silence_duration = 0
                    elif (
                        self.__silence_duration
                        > 1 / config["recognition"]["accuracy"]
                        and self.__is_talking
                    ):
                        self.__is_talking = False
                        self.__silence_duration = 0
                        yield self.stt(np.array(self.__buffer, dtype="int16"))
                        self.__buffer.clear()

                    else:
                        self.__silence_duration += indata.shape[0] * (
                            1 / 16000
                        )  # Amount of frames read times the duration of one

                    if self.__is_talking:
                        self.__buffer.extend(indata[:, 0])

    def calibration(self):
        for tscript, buffer in self.recognition():
            print(tscript)
            sd.play(np.array(buffer, dtype="int16"), samplerate=16000)

    def listen(self, events=None):
        if not events:
            events = commands["events"]

        for tscript in self.recognition():
            yield scoring.evaluate(tscript, events)


class Speaker(TTS):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, config["models"]["tts"]["rel_path"], True, **kwargs
        )

    def say(self, txt: str):
        sd.play(
            self.tts(txt), samplerate=config["models"]["tts"]["sample_rate"]
        )


if __name__ == "__main__":
    li = Listener()
    li.calibration()
