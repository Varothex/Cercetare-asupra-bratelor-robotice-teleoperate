import subprocess
import sys
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import InferenceClient
from transformers import pipeline
import torch


def call_publish_joint_commands(joint_values):
    # Construct the command to call the shell script
    command = './publish_joint_commands.sh ' + ' '.join([str(val) for val in joint_values])
    
    #print(command)
    os.system(command)

    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}", file=sys.stderr)
        
tokenizer = AutoTokenizer.from_pretrained("/home/vivio/chatbot/ChatbotTokenizer")
model = AutoModelForSequenceClassification.from_pretrained("/home/vivio/chatbot/ChatbotModel")
classifier = pipeline("text-classification", model = model, tokenizer=tokenizer, top_k=2)

# Example joint values; replace these with your desired values
joint_values = [0.0, 0.0, 0.0, 0.0]

while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        #print("Chatbot: Goodbye!")
        break
        
    first_dic = classifier(user_input)[0][0]
    label1 = first_dic['label']
    score1 = first_dic['score']
    
    second_dic = classifier(user_input)[0][1]
    label2 = second_dic['label']
    score2 = second_dic['score']
    
    print(label1, label2)
    print(score1, score2)

    # first command
    if score1 >= 0.02:
        if label1 == '0':
            waist = 0.0
            shoulder = 0.0
            elbow = 0.0
            wrist = 0.0
            print("Returning home...")
        elif label1 == '1':
            waist = 1.5
            print("Moving left...")
        elif label1 == '2':
            waist = -1.5
            print("Moving right...")
        elif label1 == '3':
            shoulder = 0.5
        elif label1 == '4':
            shoulder = -0.5
        elif label1 == '5':
            elbow = -0.5
        elif label1 == '6':
            elbow = 0.5
        elif label1 == '7':
            wrist = -0.5
        elif label1 == '8':
            wrist = 0.5
        elif label1 == '9':
            waist = 0.0
            shoulder = 0.0
            elbow = 1.0
            wrist = 0.0
            print("Up!")
        elif label1 == '10':
            waist = 0.0
            shoulder = -1.9
            elbow = -1.6
            wrist = -0.5
        elif label1 == '11':
            waist = 0.0
            shoulder = -1.9
            elbow = -1.6
            wrist = -0.5
            print("Going to sleep.")
        elif label1 == '12':
            joint_values = [0.0, 0.0, 0.0, 0.0]
         
    #second command
    if score2 >= 0.02:
        if label2 == '0':
            print("Can't do that!")
        elif label2 == '1':
            waist = 1.5
            print("Moving left...")
        elif label2 == '2':
            waist = -1.5
            print("Moving right...")
        elif label2 == '3':
            shoulder = 0.5
        elif label2 == '4':
            shoulder = -0.5
        elif label2 == '5':
            elbow = -0.5
        elif label2 == '6':
            elbow = 0.5
        elif label2 == '7':
            wrist = -0.5
        elif label2 == '8':
            wrist = 0.5
	        
    
    call_publish_joint_commands([waist, shoulder, elbow, wrist])
