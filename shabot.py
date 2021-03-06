

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
import time

#import Threading
chatterbot = ChatBot(
    'shabot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=['chatterbot.logic.MathematicalEvaluation',

                    'chatterbot.logic.BestMatch'],
    #input_adapter='chatterbot.input.TerminalAdapter',
    #output_adapter='chatterbot.output.TerminalAdapter',
    database='./database.sqlite3'
    )

chatterbot.set_trainer(ChatterBotCorpusTrainer)
#CONVERSATION_ID = chatterbot.storage.create_conversation()
def talking_mode(input_statements,CONVERSATION_ID):
        #input_statement = input_statements.decode()
        input_statement = input_statement
        input_statement = chatterbot.input.process_input_statement(input_statement)
        print (input_statement)
        statement, response = chatterbot.generate_response(input_statement, CONVERSATION_ID)
                
        output_statement=chatterbot.output.process_response(response)
        return output_statement
               


#####################################################################################################################

#main function to run the server 

#import socket
def main():
    host=''
    port=5530
    s=socket.socket()
    s.bind((host,port))
    s.listen(500)
    c,addr=s.accept()
    #print("connection from: " +str(data))
    while True:
        data=c.recv(1024)
        if not data:
            break
        print ("connected from user: " + str(data))
        convo_id = chatterbot.storage.create_conversation()
        message = data.decode("utf-8")
        message="%r"%message
        message = talking_mode(message,convo_id)
        message=str(message)
        message= message.encode()
        c.send(message)

main()


