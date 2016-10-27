presidents = {'Martin Van Buren': [1837, 1841], 'Andrew Johnson': [1865, 1869], 'John Quincy Adams': [1825, 1829], 'Calvin Coolidge': [1923, 1929], 'George Walker Bush': [2001, 2009], 'James Monroe': [1817, 1825], 'George Herbert Walker Bush': [1989, 1993], 'Barack Hussein Obama': [2009, 2017], 'Zachary Taylor': [1849, 1850], 'Millard Fillmore': [1850, 1853], 'Theodore Roosevelt': [1901, 1909], 'George Washington': [1789, 1797], 'James Madison': [1809, 1817], 'Harry S. Truman': [1945, 1953], 'James Earl Carter Jr.': [1977, 1981], 'Benjamin Harrison': [1889, 1893], 'John Tyler': [1841, 1845], 'Thomas Jefferson': [1801, 1809], 'William Jefferson Clinton': [1993, 2001], 'Dwight David Eisenhower': [1953, 1961], 'James Buchanan': [1857, 1861], 'Gerald Rudolph Ford': [1974, 1977], 'Abraham Lincoln': [1861, 1865], 'Ronald Wilson Reagan': [1981, 1989], 'William Henry Harrison': [1841, 1841], 'Chester Alan Arthur': [1881, 1885], 'William Howard Taft': [1909, 1913], 'John Fitzgerald Kennedy': [1961, 1963], 'Richard Milhous Nixon': [1969, 1974], 'Franklin Delano Roosevelt': [1933, 1945], 'James Knox Polk': [1845, 1849], 'Grover Cleveland': [1893, 1897], 'John Adams': [1797, 1801], 'Franklin Pierce': [1853, 1857], 'Woodrow Wilson': [1913, 1921], 'Herbert Clark Hoover': [1929, 1933], 'Rutherford Birchard Hayes': [1877, 1881],'William McKinley': [1897, 1901], 'Lyndon Baines Johnson': [1963, 1969], 'Warren Gamaliel Harding': [1921, 1923], 'James Abram Garfield': [1881, 1881], 'Andrew Jackson': [1829, 1837], 'Ulysses S. Grant': [1869, 1877]}

def find_by_year(date):
    result = []
    for prez, dates in presidents.iteritems():
             if dates[0] <= date <= dates[1]:
                     result.append(prez)
    return result

def findprez(date):
     print date
     result = find_by_year(date)
     if len(result) > 1:
             output =  "The presidents in " + str(date) + " were "
             printthem = result[0]
             for line in result[1:]:
                     printthem = printthem + ", and " + line
             output = output + printthem + "."
     else:
             output =  "The President in " + str(date) + " was " + result[0] + "."
     print output
     return output

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.62f50ee0-7045-423a-9130-b20f8ddd0b9c"):
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

    if intent_name == "PresYear":
        return get_president_by_year(intent)
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
    card_title = "FindPrez - Thanks"
    speech_output = "Thank you for using the Find President skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "FindPrez"
    speech_output = "Welcome to the Find President skill. " \
                    "You can ask me to find out who was President " \
                    "in a certain year."
    reprompt_text = "Please ask me a year, " \
                    "for example who was president in 1927."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_president_by_year(intent):
    session_attributes = {}
    card_title = "Finding President"
    speech_output = "I'm not sure what year you want me to look for. " \
                    "Please try again."
    reprompt_text = "I'm not sure what year you wanted. " \
                    "Try asking about 1943 or 1894 for example."
    should_end_session = False

    if "year" in intent["slots"]:
        try:
            year = intent["slots"]["year"]["value"]
            if year == "?":
                speech_output = "I did not understand the year you gave. " \
                                "Please ask for a year between 1789 and 2016."
                reprompt_text = "Please ask for a year between 1789 and 2016."
            else:
                if 1789 <= int(year) <= 2016:
                    speech_output = findprez(int(year))
                    reprompt_text = ""
                    should_end_session = True
                else:
                    speech_output = "That is not a valid year for American Presidents" \
                                "Please ask for a year between 1789 and 2016."
                    reprompt_text = "Please ask for a year between 1789 and 2016."
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
