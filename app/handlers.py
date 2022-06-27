# -*- coding: utf-8 -*-
"""

@author: sebis
"""

from app import controllers
from flask import render_template
from flask_dialogflow.conversation import V2beta1DialogflowConversation
import pandas as pd
import random

dtype = {
    'Record': str,
    'Nationality': str,
    'Player': str,
    'Year(s)': str,
    'Details': str,
    'Type': str
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
    # register the user's order, the user can limit the nationality, the player, the record type etc.
    # It's also possible that nothing is limited, so a random record will be given.
    nation = conv.parameters.get("geo-country")
    year = conv.parameters.get("number-sequence")
    # year_period = conv.parameters.get("any")
    name = conv.parameters.get("whole-name")
    type = conv.parameters.get("record-type")

    get_out = 0

    # read the excel file and get a data frame.
    data_frame = pd.read_excel(r'data/football_records_table.xlsx', dtype=dtype)
    shuffled_df = data_frame.sample(frac=1)  # shuffle the records to find different record on every user request

    # according to the request, find a corresponding record.

    # if nationality is given by user (the Country England may not be recognized, which is weird)
    if nation != '':
        for i in range(shuffled_df.shape[0]):
            if shuffled_df.iloc[i][2] == nation:
                context_set(conv, shuffled_df, i)
                break

    # if Player is given by user
    elif name != '':
        # print(name)
        for i in range(shuffled_df.shape[0]):
            if shuffled_df.iloc[i][1] == name:
                context_set(conv, shuffled_df, i)
                break

    # if Type is is given by user
    elif type != '':
        for i in range(shuffled_df.shape[0]):
            if shuffled_df.iloc[i][5] == type:
                context_set(conv, shuffled_df, i)
                break

    # if time is is given by user
    elif year != '':
        # we use sys.number-sequence entity, this entity can only provide pure number,
        # so when a time period for example 2002-2021 was given, year=20022021,
        # this string needs to be processed

        if len(year) > 4:
            # the sys.number entity can not recognize 'present',
            # so we stipulate that the user needs to enter 2022 instead of present
            # then we revert '2022' to 'present' in the code and compare with the excel data.
            year = year.replace('2022', 'present')
            str_list = list(year)
            str_list.insert(4, '–')
            year = ''.join(str_list)
            print(len(year))

        for i in range(shuffled_df.shape[0]):
            year_col = str(shuffled_df.iloc[i][3])
            if len(year_col) == 9 and len(year) == 4:
                year1 = year_col[0:4]
                year2 = year_col[5:9]
                for y in range(int(year1), int(year2) + 1):
                    if str(y) == year:
                        print("getout")
                        context_set(conv, shuffled_df, i)
                        get_out = 1
                        break
                if get_out == 1:
                    break

            elif str(shuffled_df.iloc[i][3]) == str(year):
                context_set(conv, shuffled_df, i)
                break
            if i == shuffled_df.shape[0] - 1:
                conv.ask("There is no such a record in my list")
                conv.google.ask("There is no such a record in my list")
                return conv

    # if nothing is fixed, give a random record
    else:
        index = random.randint(0, shuffled_df.shape[0])
        context_set(conv, shuffled_df, index)

    Record = conv.contexts.find_record_ctx.parameters["Record"]
    Player = conv.contexts.find_record_ctx.parameters["Player"]
    conv.ask(render_template("Record-response", Player=Player, Record=Record))
    conv.google.ask(render_template("Record-response", Player=Player, Record=Record))
    return conv


def Time_supplementary_intent(conv: V2beta1DialogflowConversation) -> V2beta1DialogflowConversation:
    Years = conv.contexts.find_record_ctx.parameters["Years"]
    conv.ask(Years)
    conv.google.ask(Years)
    return conv


def context_set(conv, df, i):
    conv.contexts.set("find_record_ctx", lifespan_count=3, Record=df.iloc[i][0],
                      Player=df.iloc[i][1], Nationality=df.iloc[i][2],
                      Years=df.iloc[i][3], Details=df.iloc[i][4],
                      Type=df.iloc[i][5])
