from litellm import completion
import os

text = """Could you create a basic Ruby API with three endpoints?
One for creating an item, another for viewing the item, and a third for deleting the item.
The API should utilize the Sinatra library and include simple tests using Minitest."""
messages = [{"role": "user",
"content": f"""Could you improve this text for me?
I want to be without grammar and spelling mistakes and be clearer
```{text}```
"""}]

# openai call
response = completion(model="gpt-3.5-turbo", messages=messages)
print(response.choices[0].message)
