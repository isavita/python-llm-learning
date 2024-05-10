import litellm
litellm.set_verbose=True
import requests
from litellm import completion as litellm_completion
import os

text = """Could you create a basic Ruby API with three endpoints?
One for creating an item, another for viewing the item, and a third for deleting the item.
The item should have name, quantity, and price.
The API should utilize the Sinatra library and include simple tests using Minitest."""

messages = [{"role": "user",
"content": f"""Could you improve this text for me?
I want to be without grammar and spelling mistakes and be clearer
```{text}```
"""}]

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages,
    "stream": False,
}
# openai call
# response = litellm_completion(model="gpt-3.5-turbo", messages=messages)
# print(response.choices[0].message)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ.get("OPENAI_API_KEY")}" 
}

url = "https://api.openai.com/v1/chat/completions"
resp = requests.post(url, json=payload, headers=headers, timeout=(3.05, 60))
print(resp.json())
