from ollama import chat
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
)


def split_text_simple(text, chunk_size, overlap=0):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_text(text)


def split_json_simple(json_data, min_chunk_size, max_chunk_size):
    splitter = RecursiveJsonSplitter(
        min_chunk_size=min_chunk_size, max_chunk_size=max_chunk_size
    )
    return splitter.split_json(json_data=json_data)

def ollama_chat(message):
    messages = [
        {'role': 'user', 'content': message}
    ]
    resp = chat('llama3', messages=messages, stream=False)

    return resp['message']['content']

def describe_chart_from_image(image_path):
    system_message = {
        'role': 'system',
        'content': (
            "You are an information extraction assistant that focuses on extracting key numbers, labels, and data points from charts and images. "
            "Your primary goal is to identify and list the important numerical values and their corresponding labels or categories. "
            "Provide the extracted information in a structured format, such as a list or a set of key-value pairs. "
            "Minimize any additional descriptions or summaries of the chart. "
            "If you are uncertain about a specific number or value, it's better to skip it rather than making assumptions or including potentially incorrect information."
        )
    }
    user_message = {
        'role': 'user',
        'content': (
            "Extract the following information from the chart in the image:\n"
            "1. Numeric values: List all the significant numbers and percentages mentioned in the chart.\n"
            "2. Labels and categories: Extract the labels, headings, or categories associated with the numeric values.\n"
            "3. Units of measurement: Identify the units of measurement used in the chart, if applicable.\n"
            "4. Time period or date range: Extract any specific time periods or date ranges mentioned in the chart.\n\n"
            "Present the extracted information in a structured format, such as a list or key-value pairs, without providing an overall description of the chart. "
            "If you are unsure about a particular value or if the information is unclear, skip it instead of including potentially inaccurate data."
        ),
        'images': [image_path]
    }

    response = chat(
        model="llava-llama3",
        messages=[system_message, user_message]
    )
    return response['message']['content']