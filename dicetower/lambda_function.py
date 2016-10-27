import random



def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.dbc9d0ff-fda9-4e82-a0eb-1adcc87fe783"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "DiceRoll":
        return get_diceroll(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "DiceTower - Thanks"
    speech_output = "Thank you for using the Dice Tower skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "DiceTower"
    speech_output = "Welcome to the Dice Tower skill. " \
                    "You can ask me to roll dice for you by " \
                    "telling me how many rolls of what kind of die."
    reprompt_text = "Please ask me for a dice roll, " \
                    "for example 2 d 6."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_diceroll(intent):
    random.seed()
    session_attributes = {}
    card_title = "Rolling Dice"
    speech_output = "I'm not sure what dice you wanted rolled. " \
                    "Please try again."
    reprompt_text = "I'm not sure what dice roll you wanted. " \
                    "Try asking about 2 d 6 or 1 d 4 for example."
    should_end_session = False

    if "Num" in intent["slots"] and "Die" in intent["slots"]:
        try:
            print "Num: " + str(intent["slots"]["Num"]["value"])
            print "Die: " + str(intent["slots"]["Die"]["value"])
            if intent["slots"]["Num"]["value"] != "?" or intent["slots"]["Die"]["value"] != "?" :
                num = int(intent["slots"]["Num"]["value"])
                die = int(intent["slots"]["Die"]["value"])
                try:
                    value = rolldice(num,die)
                    speech_output = "The Dice Roll resulted in " + str(value) + "."
                    reprompt_text = ""
                    should_end_session = True
                except:
                    pass
        except:
            pass

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


def rolldice(num,die):
        b,e = pickdie(die)
        total = 0
        for i in range(num):
                total = total + random.randint(b,e)
        return total

def pickdie(die):
        if (die in [4,6,8,10,12,20]):
            b,e = 1,die
        else:
                print "Unrecognized die size"
                raise ValueError('Unrecognized die size')

        return b,e
