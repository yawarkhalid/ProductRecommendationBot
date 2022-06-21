#!/usr/bin/env python
# coding: utf-8

# In[8]:

import streamlit as st
from streamlit_chat import message
import pandas as pd
import numpy as np
import os
from src.information_retrieval_model import Product_Information_Retrieval_Model
import pandas as pd 
import emoji

import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from chatterbot.trainers import read_file

header = st.container()
chatbot = st.container()


with header:
    st.title('Hi! Im YK the fashion recommedation chatbot!')
    
    
    
with chatbot:
    
    bot = ChatBot("Example Bot", read_only=False)
    trainer = ListTrainer(bot)
    
    
    bot.storage.drop()
    
    
    trainer.train([
    'Hi',
    'Hello',
    'Sorry, we dont have this product',
    'Yes, enter detailed description',
    'Tell me more about it.',
    'Sorry, we dont stock that item, add more description.',
    'Im sorry, we dont have recommedations for that, you can try our webstore or add more description',
    'Please enter more description',
    'I hope ive helped.',
    'Yes',
    'No',
    'You can exit any time',
    'No Problem! Have a Good Day!'
    ])
    
    
    model = Product_Information_Retrieval_Model()
    df = pd.read_excel("data/fashion_final.xlsx")

    #name=st.text_input("Enter Your Name: ")

    st.write("\nHi there! I'm a chatbot programmed to help you find your perfect fashion product! To get started, just respond with a description of what you are looking for. Be as detailed as you want!\n")

    while True:
        request_body= st.text_input('How may I help?')

        if request_body=='Bye' or request_body =='bye':
            st.write('Bot: Thanks and enjoy your new purchase! If you want new recommendations, just reset me.')
            break

        else:
            recs = model.query_similar_products(request_body, 3)

            #format recommendation 1
            product_name = recs.index.tolist()[0]
            product_score1  = round(recs.iloc[0].ensemble_similarity,4)

            if product_score1 <=0.4:
                response=bot.get_response(request_body)
                st.write('Bot:',response)

            else:

                shopping_link = "https://www.google.com/search?q=" + product_name.replace(" ", "+")
                sms_message = emoji.emojize("Great! Here are your top recommendations :cherry_blossom:\n\n1) {} (match score={}). Shop for it here {}.\n ".format(product_name, product_score1, shopping_link))  


                #format recommendation 2
                product_name = recs.index.tolist()[1]
                product_score2  = round(recs.iloc[1].ensemble_similarity,4)
                shopping_link = "https://www.google.com/search?q=" + product_name.replace(" ", "+")
                sms_message = sms_message + emoji.emojize("\n2) You can also try :mushroom: {} (match score={}). Shop it here {}.\n".format(product_name, product_score2, shopping_link))


                #format recommendation 3
                product_name = recs.index.tolist()[2]
                product_score3  = round(recs.iloc[2].ensemble_similarity,4)
                shopping_link = "https://www.google.com/search?q=" + product_name.replace(" ", "+")
                sms_message = sms_message + emoji.emojize("\n3) Or try :bouquet: {} (match score={}. Shop it here {}. Enjoy!\n".format(product_name, product_score3 , shopping_link))
                sms_message = sms_message + emoji.emojize(":red_heart:")


                sms_message = sms_message + "\n\nThanks and enjoy your new purchase! If you want new recommendations, just type another product description.\nYou can type 'Bye' anytime to quit."

                response = sms_message
                st.write('\nBot:',response)