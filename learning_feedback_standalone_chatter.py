#!/usr/bin/python3

from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot import conversation
import logging
import os
import sys
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import statement
import socket
#import Threading

prev_statement=''
#----------------------------------------------------------------
#main function to run the server for chatterbot
#----------------------------------------------------------------
def Main():
    host='127.0.0.1'
    port=5008
    s=socket.socket()
    s.bind((host,port))
    s.listen(1)
    c, addr=s.accept()
    print("connected from " + str(addr))
    while True:
        CONVERSATION_ID = chatterbot.storage.create_conversation()
        datas=c.recv(1024)
        datas=(datas.decode())
        print (datas)
        #print (datas + "lauda")
        data = chatterbot.input.process_input_statement()
        print(data)
        print ("from connected user :" + str(addr) + "recieved message" + str(data))
        statement, response = chatterbot.generate_response(data, CONVERSATION_ID)
        #print (CONVERSATION_ID)
        output_statement=chatterbot.output.process_response(response)
        c.send(output_statement.encode())
        
        
    c.close
###################################################################
#####################################################################
chatterbot = ChatBot(
    'shabot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=['chatterbot.logic.MathematicalEvaluation',

                    'chatterbot.logic.BestMatch'],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    database='./database.sqlite3'
    )

chatterbot.set_trainer(ChatterBotCorpusTrainer)

CONVERSATION_ID = chatterbot.storage.create_conversation()

#chatterbot.train('chatterbot.corpus.english')
def get_feedback():
        from chatterbot.utils import input_function
        text = input_function()

        if 'yes' in text.lower():
                return False
        elif 'no' in text.lower():
                return True
        else:
                print('Please type either "Yes" or "No"')
                return get_feedback()
print ('Type something to begin...')
a="""If you want to enter feedback interactive training mode please enter 1 \n
    If you want to enter talk to the bot ,please press 2"""
print (a)


def interactive_training_mode():
    print ('Type anything to begin with ')

    while True:
        try:

        # We pass None to this method because the parameter
        # is not used by the TerminalAdapte



                input_statement = chatterbot.input.process_input_statement()
              
               
                
                
                statement, response = chatterbot.generate_response(input_statement, CONVERSATION_ID)
                print (CONVERSATION_ID)
                chatterbot.output.process_response(response)
                print('\n Is "{}" a coherent response to "{}"? \n'.format(response, input_statement))
                if get_feedback():
                     print("please input the correct one")
                     response1 = chatterbot.input.process_input_statement()
                     chatterbot.learn_response(response1, input_statement)
                     chatterbot.storage.add_to_conversation(CONVERSATION_ID, statement, response1)
                     print("Responses added to bot!")

    # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break



def talking_mode():
    #print ('Type something to begin...')

    # The following loop will execute each time the user enters input

    while True:
            try:
                #input_statement = input_statements 
                

                input_statement = chatterbot.input.process_input_statement()
                global prev_statement
                #print (prev_statement)
                #print (input_statement)
                
                if input_statement == 'incorrect':
                    print("can you give me the correct answer?")
                    response1 = chatterbot.input.process_input_statement()
                    #print (response1)
                    chatterbot.learn_response(response1,prev_statement)
                    chatterbot.storage.add_to_conversation(CONVERSATION_ID, statement, response1)
                    print("Learnt that , Hope to help others on this question in future")
 
                else:
                #print (input_statement)
                        statement, response = chatterbot.generate_response(input_statement, CONVERSATION_ID)
                #print (CONVERSATION_ID)
                        output_statement=chatterbot.output.process_response(response)
                        #global prev_statement
                        prev_statement=input_statement

                #return output_statement
                #print(output_statement)
               # bot_input = chatterbot.get_response(None)
            except (KeyboardInterrupt, EOFError,SystemExit):
                # Press ctrl-c or ctrl-d on the keyboard to exit
                #print (prev_statement)
                break


user_input=input()
if user_input == '1':
    interactive_training_mode()

elif user_input == '2':
    talking_mode()
    print(prev_statement)
elif user_input == '3':
    Main()    

