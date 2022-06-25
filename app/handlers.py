# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation
import pandas as pd
import random

dtype={
      'Record':str,
      'Nationality':str,
      'Player':str,
      'Year(s)':str,
      'Details':str,
      'Type':str
      }

# define sub handlers
def test_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("test_response"))
    conv.google.ask(render_template("test_response"))
    return conv

def welcome_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("welcome"))
    conv.google.ask(render_template("welcome"))
    return conv

def Function_introduction_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    conv.ask(render_template("Functions"))
    conv.google.ask(render_template("Functions"))
    return conv

def Find_record_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    
    #register the user's order, the user can limit the nationality, the player, the record type etc.
    #It's also possible that nothing is limited, so a random record will be given.
    nation = conv.parameters.get("geo-country")
    year = conv.parameters.get("time")
    year_period = conv.parameters.get("time-period")
    name = conv.parameters.get("whole-name")
    type = conv.parameters.get("record-type")

    print(nation)
    #read the excel file and get a data frame.

    data_frame = pd.read_excel(r'C:\Users\Dominik Nie\Desktop\football_records_table.xlsx',dtype=dtype)
    print(data_frame.values)

    #according to the request, find a corresponding record.

    #if nationality is fixed.(the Country England may not be recognized, which is wierd)
    if nation != '':
        for i in range(data_frame.shape[0]):
            if data_frame.iloc[i][2]==nation:
                conv.contexts.set("find_record_ctx",lifespan_count=3,Record=data_frame.iloc[i][0],Player=data_frame.iloc[i][1],Nationality=data_frame.iloc[i][2],Years=data_frame.iloc[i][3],Details=data_frame.iloc[i][4],Type=data_frame.iloc[i][5])
                break
    
    #if Player is fixed
    elif name != '':
        #print(name)
        for i in range(data_frame.shape[0]):
            if data_frame.iloc[i][1]==name:
                conv.contexts.set("find_record_ctx",lifespan_count=3,Record=data_frame.iloc[i][0],Player=data_frame.iloc[i][1],Nationality=data_frame.iloc[i][2],Years=data_frame.iloc[i][3],Details=data_frame.iloc[i][4],Type=data_frame.iloc[i][5])
                break

    #if Type is fixed           
    elif type != '':
        for i in range(data_frame.shape[0]):
            if data_frame.iloc[i][5]==type:
                conv.contexts.set("find_record_ctx",lifespan_count=3,Record=data_frame.iloc[i][0],Player=data_frame.iloc[i][1],Nationality=data_frame.iloc[i][2],Years=data_frame.iloc[i][3],Details=data_frame.iloc[i][4],Type=data_frame.iloc[i][5])
                break

    #if time is fixed, not done yet


    #if nothing is fixed, give a random record
    else :
        index=random.randint(0,data_frame.shape[0])
        conv.contexts.set("find_record_ctx",lifespan_count=3,Record=data_frame.iloc[index][0],Player=data_frame.iloc[index][1],Nationality=data_frame.iloc[index][2],Years=data_frame.iloc[index][3],Details=data_frame.iloc[index][4],Type=data_frame.iloc[index][5])
    
    
    Record= conv.contexts.find_record_ctx.parameters["Record"]
    Player= conv.contexts.find_record_ctx.parameters["Player"]
    conv.ask(render_template("Record-response",Player=Player,Record=Record))
    conv.google.ask(render_template("Record-response",Player=Player,Record=Record))
    return conv

def Time_supplementary_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    Years=conv.contexts.find_record_ctx.parameters["Years"]
    if len(Years)<=4:
        conv.ask(Years)
        conv.google.ask(Years)
    else:
        conv.ask(Years)
        conv.google.ask(Years)
    return conv