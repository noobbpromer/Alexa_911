# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import json
import random
import os
# import ask_sdk_core.utils as ask_utils

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.skill_builder import SkillBuilder
# from ask_sdk_core.dispatch_components import AbstractRequestHandler
# from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

question_data = json.loads(open('question_data.json').read())
accident_data = json.loads(open('car_accident.json').read())

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["quiz_started"] = False
        
        speak_output = "912, what is yoyr emergency？"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class YesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        quiz_started = session_attributes["quiz_started"]
        # say_yes=0
        if not quiz_started:
            current_question_index = 0
            question = question_data[current_question_index]["q"]
            speak_output = ("here is the first question: <break time='0.5s'/> {}").format(question)
            reprompt = "what is the answer?"

            session_attributes["current_question_index"] = current_question_index
            session_attributes["question"] = question
            session_attributes["quiz_started"] = True
            quiz_started=True
        # elif quiz_started :
        #     speech_output = 'you already start the survey, please finish it.'
        #     reprompt = 'you already start the survey, please finish it.'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )
    
class NoIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ok, let me know when you free."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

class AnswerIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        answer = slots["answer"].value
        year=slots["year"].value
        # mouth=slots["mouth"].value
        # day=slots["day"].value
        # number=slots["number"].value
        current_question_index = session_attributes["current_question_index"] + 1
        if current_question_index < 5:
            
            
            question = question_data[current_question_index]["q"]
            next_question_speech = (" {}").format(question)
            session_attributes["current_question_index"] = current_question_index
            session_attributes["question"] = question
            # speech_output += next_question_speech
            speak_output = "this is the answer intent"

        else:
            next_question_speech = ("thank you for taking the survey!")
            
            return(
            
                handler_input.response_builder
                    .speak(next_question_speech)
                    .set_should_end_session(True)
                    .response
            )
        
        
        return (
            handler_input.response_builder
                .speak(next_question_speech)
                .ask(speak_output)
                .response
        )   

class AccidentIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AccidentIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        # quiz_started = session_attributes["quiz_started"]
        slots = handler_input.request_envelope.request.intent.slots
        location = slots["location"].value
        prepositions=slots["prepositions"].value
        if location ==None:
            current_question_index = 0
            question = accident_data[current_question_index]["q"]
            speak_output = ("<break time='0.5s'/> {}").format(question)
        # else if location == "here":
        #     speak_output="can you give me your exact address？"
        else:
            current_question_index = 1
            question = accident_data[current_question_index]["q"]
            speak_output = ("{prepositions}{location}? {}").format(question,prepositions=prepositions,location=location)
            
        session_attributes["current_question_index"] = current_question_index
        session_attributes["question"] = question
        
        # session_attributes["quiz_started"] = True
        # quiz_started=True

        
            

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
    
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.




sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(AccidentIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()