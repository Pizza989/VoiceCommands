# VoiceCommands

>This is Work in Progress and will be updated whenever I feel like it.

Voice Commands uses the TTS and stt python modules and therefore supports the same models as those.
* Free speech to text models can be found [here](https://coqui.ai/models).
* Regarding text to speech, after installing all dependecies just execute ```tts --list_models``` to see a list of ids that can be used in voice commands config
## Features

### Implemented

-   Realtime Voice recognition
-   An event based command system supporting infinitely long dialogs

### Planed

-   Event system to implement python callbacks for commands
-   Recognising numbers as input (the stt model gives me the written versions)
-   Multi language support
-   Logging
-   Release as package for obs

## Configuration

All configuration is done in the .voice_commands directory

### 1. Commands

Events are implemented in commands.json which is a json obeject containing a list of events under "events" and the correlating commands in the json object "commands":

```python
class Event(TypedDict):
    id: str
    keywords: list[list[str, float]]
```

The keywords of an event are a list of (str, int) pairs that are the word and it's [score](##Scoring).\
The id is used to determine which event and command correlate.

```python
class Command(TypedDict):
    name: str
    text: str
```

The name is just used for the assistant to say.
The text will be said by the assistant if it's not an empty string

### 2. Config

#### 2.1 Models

```json
"tts": {            (contains data about the text-to-speech model)
    "model_id":     (id of the model according to tts module)
    "sample_rate":  (sample rate of the model)
},
"stt": {            (contains data about the speech-to-text model)
    "path":     (path of the model relative to core.py)
    "sample_rate":  (sample rate of the model)
    "scorer_path":       (optional scorer for the recognition)
}
```

#### 2.2 Recognition

```json
"talking_threshold": (filters all audio below|has no unit)
"accuracy": (the higher the shorter the programm waits for the next word)
```

#### 2.3 Scoring

```json
"required_comparison_ratio": (how much the transcript has to match a keyword|from 0 to 1)
```

## Scoring

An events score is the sum of all keywords that match any word from the transcript, if this score is above 1 the event is considered true (Therefore the events keywords should be defined accordingly). The event with the highest score out of the true ones is used exclusively
