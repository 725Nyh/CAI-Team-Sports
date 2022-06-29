# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import agent
from app import handlers
from flask_dialogflow.conversation import V2beta1DialogflowConversation

# define main handlers
@agent.handle(intent="test-intent")
def test_intent_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.test_intent(conv)

@agent.handle(intent="Function-introduction")
def Function_introduction_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.Function_introduction_intent(conv)

@agent.handle(intent="Find-record")
def Find_record_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.Find_record_intent(conv)

@agent.handle(intent="Detail-supplementary")
def Detail_supplementary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.Detail_supplementary_intent(conv)

@agent.handle(intent="Time-supplementary")
def Time_supplementary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.Time_supplementary_intent(conv)

@agent.handle(intent="Type-supplementary")
def Type_supplementary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.Type_supplementary_intent(conv)

@agent.handle(intent="country_supplementary")
def country_supplementary_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.country_supplementary_intent(conv)

@agent.handle(intent="record_count")
def record_count_handler(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    return handlers.record_count_intent(conv)

