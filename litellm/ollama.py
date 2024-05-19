import litellm
from litellm import completion

litellm.set_verbose=False

sys_prompt = """
You are an AI coding engineer. 
Your role is to assist the user by autonomously implementing programs and completing coding tasks based on their specifications,
with minimal additional input required from the user.
Aim to thoroughly understand the user's requirements upfront, then take the initiative to write clean, well-structured code that fully meets the specified functionality.
Explain your code with comments.
Ask clarifying questions if needed, but try to fill in any gaps yourself to the extent possible. Your goal is to deliver working, high-quality software with little back-and-forth.
""".strip()

prompt = """
Write me a simple random password generation script in Python.
I want everytime when I run the script (e.g. python script.py) the script to output a random secure password.
""".strip()
prompt = "How to add 4 and 5 in python?"
messages = [
    {"role": "system", "content": sys_prompt},
    {"role": "user", "content": prompt},
]

response = completion(
    model="ollama/llama3",
    messages=messages,
    api_base="http://localhost:11434",
    stream=False
)
content = response["choices"][0]["message"]["content"]
print(content)
