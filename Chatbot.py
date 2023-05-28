# -*- coding: utf-8 -*-
"""
Created on Mon May  1 12:31:22 2023

@author: sibin
"""

import numpy as np
import tensorflow as tf
import re
import time

#Step-1 Data preprocessing

#Importing datasets.(step 5)
lines= open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conversations= open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

#creating a dictionary to store id and lines.(step 6)
id2line={}
for line in lines:
    _line=line.split(' +++$+++ ')
    if len(_line)==5:
        id2line[_line[0]]=_line[4]
        
#creating a list for conversations ids.(step 7)
conversations_ids=[]
for conversation in conversations:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations_ids.append(_conversation.split(','))
    
#Separating the question and answer from the dataset.(step 8)
questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
        
#1st cleaning part for the texts, improving the grammer and removing unnecessary symbols from the text(step 9)
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)  # Replace non-alphanumeric characters with a space
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading/trailing spaces
    return text

    
#cleaning the questions one by one from the above list.
#The cleaning process is done with the help of the 'clean_text' function. (step 10)
clean_questions= []
for question in questions:
    clean_questions.append(clean_text(question))

#By using the same method we are cleaning the answers. (step 10)    
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    
    
#counting the occarence of the word in the clean_questions and clean_answers. (step 11)    
word2count = {}
#For clean_questions
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word]=1
        else:
            word2count[word] +=1
#For clean_answers
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] +=1
        
#creating 2 dictionaries to convert/map question word and answer word into a unqiue integer. (step 12)    
#converting question words into a unique int
threshold = 20
questionsword2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        questionsword2int[word] = word_number
        word_number += 1
#converting answer words into a unique int    
answersword2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        answersword2int[word] = word_number
        word_number += 1    
    
    
    
    
    