
import os
import litellm
from litellm import completion

os.environ['MISTRAL_API_KEY'] == os.environ.get('CODESTRAL_API_KEY')

messages = [
    {"role": "user", "content": "Write me a python program that prints all odd numbers from 1 to 50."}
]
# response = completion(
#     model="mistral/codestral-latest", 
#     messages=messages,
# )
# print(response)

# make me request using requests api
import requests
import json
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['CODESTRAL_API_KEY']}"
}

response = requests.post("https://codestral.mistral.ai/v1/chat/completions", 
              json={
                "model": "codestral-latest",
                "messages": messages,
                "stream": False
              },
            headers=headers
)
response = response.json()
print(response['choices'][0]['message']['content'])
