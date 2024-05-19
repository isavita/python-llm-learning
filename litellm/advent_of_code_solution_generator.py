from litellm import completion

examples = """


"""

task = """Could you create a basic Ruby API with three endpoints?
One for creating an item, another for viewing the item, and a third for deleting the item.
The item should have name, quantity, and price.
The API should utilize the Sinatra library and include simple tests using Minitest."""

messages = [{"role": "user",
"content": f"""Write me Zig program the solves the following challenge.
The program should read the input from a file called 'input.txt' and print the answer to the stdout.
```{task}```
"""}]

payload = {
    "model": "gpt-4o",
    "messages": messages,
    "stream": False,
}

response = completion(
    model="gpt-4o",
    messages=messages
)
print(response.choices[0].message)
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {os.environ.get("OPENAI_API_KEY")}" 
# }

# url = "https://api.openai.com/v1/chat/completions"
# resp = requests.post(url, json=payload, headers=headers, timeout=(3.05, 60))
# print(resp.json())
