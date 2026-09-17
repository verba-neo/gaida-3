# dataset.py
'''
.env 에 LANGSMITH_API_KEY 세팅 되어있어야함

uv add langsmith openevals openai
'''

# dataset.py
from pathlib import Path
from langsmith import Client
from dotenv import load_dotenv

# 수동 .env 로딩 (프로젝트 루트의 .env 로드)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def main():
    client = Client()

    # Programmatically create a dataset in LangSmith
    dataset = client.create_dataset(
        dataset_name="Sample dataset",
        description="A sample dataset in LangSmith."
    )

    # Create examples
    examples = [
        {
            "inputs": {"question": "Which country is Mount Kilimanjaro located in?"},
            "outputs": {"answer": "Mount Kilimanjaro is located in Tanzania."},
        },
        {
            "inputs": {"question": "What is Earth's lowest point?"},
            "outputs": {"answer": "Earth's lowest point is The Dead Sea."},
        },
    ]

    # Add examples to the dataset
    client.create_examples(dataset_id=dataset.id, examples=examples)
    print("✅Created dataset:", dataset.name)

if __name__ == "__main__":
    main()