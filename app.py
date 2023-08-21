import requests
import os
import openai
import json
import datetime
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')
URL = os.getenv('SHETTY_URL')
now = datetime.datetime.now()
time_string = now.strftime("%I:%M:%S %p")
date_string = now.strftime("%m/%d/%Y")

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [{'role':'system', 'content':'You are an expert web developer and tester with high skills for great code.'},{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


#post row
url = URL
print("What was your exercise today ?")
text = input()
json_string = [
    {
        "workout":{ 
        "date": date_string,
        "time": time_string,
        "exercise": "",
        "duration":"",
        "calories":""
        }
    }
]
json_string = json.dumps(json_string)
prompt = f'''You will receive a tex of an exercise or exercises i realize|
and i want you to give me this info in this json format|
{json_string}|
Calculate the calories that the exercise burn|
Obviously having as many objects as exercises done in the text and filling the empty string with info|
Only return me the json object, don't say anything more
Here is the text: {text}
'''
openAiResponse = get_completion(prompt)
exercises = json.loads(openAiResponse)
for exercise in exercises:
    response = requests.post(url=url,json=exercise)
    if(response.status_code==200):
        print(response.json())
    else:
        print(response.text)