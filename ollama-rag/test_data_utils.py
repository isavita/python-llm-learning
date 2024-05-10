import pytest

from data_utils import split_text_simple, split_json_simple, ollama_chat, describe_chart_from_image


def test_simple_text_splitting():
    text = "This is a simple example text that we will split into chunks."  # 61
    expected_chunks = [
        "This is a simple example",
        "text that we will split",
        "into chunks.",
    ]  # [24 + 1(space) = 25, 23 + 1(space) = 24, 12]
    chunk_size = 25
    overlap = 0
    assert split_text_simple(text, chunk_size, overlap) == expected_chunks


def test_text_splitting_with_overlap():
    text = "This is a simple example text that we will split into chunks."
    chunk_size = 25
    overlap = 10
    expected_chunks = [
        "This is a simple example",  # 24 + 1(space) = 25
        "example text that we",  # 8(overlap) + 12 + 1(space) = 21
        "that we will split into",  # 8(overlap) + 15 + 1(space) = 24
        "into chunks.",  # 5(overlap) + 7 = 12
    ]
    assert split_text_simple(text, chunk_size, overlap) == expected_chunks


def test_basic_json_splitting():
    data = {
        "type": "Document",
        "content": [
            {
                "type": "paragraph",
                "text": "This is a long paragraph that needs splitting.",
            },
            {
                "type": "paragraph",
                "text": "Another section of text that also needs splitting.",
            },
        ],
        "metadata": {"author": "John Doe", "date": "2024-01-01"},
    }
    min_chunk_size = 10
    max_chunk_size = 100
    expected_chunks = [
        {"type": "Document"},
        {
            "content": [
                {
                    "type": "paragraph",
                    "text": "This is a long paragraph that needs splitting.",
                },
                {
                    "type": "paragraph",
                    "text": "Another section of text that also needs splitting.",
                },
            ]
        },
        {"metadata": {"author": "John Doe", "date": "2024-01-01"}},
    ]
    assert split_json_simple(data, min_chunk_size, max_chunk_size) == expected_chunks


@pytest.mark.skip(reason="It has state for some reason")
def test_nested_json_splitting():
    data = {
        "name": "John",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
        "contacts": [
            {"type": "email", "value": "john@example.com"},
            {"type": "phone", "value": "+1 (555) 123-4567"},
        ],
    }
    min_chunk_size = 20
    max_chunk_size = 50
    expected_chunks = [
        {"metadata": {"author": "John Doe", "date": "2024-01-01"}},
        {"name": "John", "address": {"street": "123 Main St"}},
        {"address": {"city": "Anytown", "state": "CA"}},
        {"address": {"zip": "12345"}},
        {
            "contacts": [
                {"type": "email", "value": "john@example.com"},
                {"type": "phone", "value": "+1 (555) 123-4567"},
            ]
        },
    ]
    actual_chunks = split_json_simple(data, min_chunk_size, max_chunk_size)
    print(actual_chunks)
    assert actual_chunks == expected_chunks


@pytest.mark.skip(reason="we don't care")
def test_ollama_chat():
    answer = ollama_chat("Is Manchester United better than Liverpool?")
    print(answer)
    assert "No, Liverpool is better" in answer

def test_describe_chart_from_image():
    image_path = './tesla_q1_image1.png'
    description = describe_chart_from_image(image_path)
    print(description)
    assert "Statement of Operations" in description
    assert "Q1-2023" in description