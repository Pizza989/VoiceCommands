import json


with open(".voice_commands/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open(".voice_commands/commands.json", "r", encoding="utf-8") as file:
    commands = json.load(file)


def compare_str(a: str, b: str) -> float:
    return sum([b.count(char) for char in a]) / len(b)


def get_score(transcript: str, event: dict):
    score = 0
    for word in transcript.split():
        for keyword in event["keywords"]:
            if (
                compare_str(word, keyword[0])
                >= config["scoring"]["required_comparison_ratio"]
            ):
                score += keyword[1]

    return score


def evaluate(transcript: str, events: list):
    evaluation = [(event, get_score(transcript, event)) for event in events]
    event_eval = max(evaluation, key=lambda x: x[1])
    if event_eval[1] >= 1:
        return event_eval[0]
    else:
        return {
            "id": "unrecognised",
            "keywords": [],
        }  # kinda ugly but the best i could think of
