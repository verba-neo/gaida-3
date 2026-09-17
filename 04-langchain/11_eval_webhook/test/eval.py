# test/eval.py
from langsmith import Client, wrappers
from openai import OpenAI
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add project root directory (11_eval_webhook) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# 내가 만든 agent/graph
from src.app import agent


def target(inputs: dict) -> dict:
    # 제작한 agent 실행 후 답변 저장
    response = agent.invoke({
        'messages': [
            {'role': 'user', 'content': inputs['question']}
        ]
    })
    return {"answer": response['messages'][-1].content}


def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        model="openai:o3-mini",
        feedback_key="correctness",
    )
    return evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )


def main():
    client = Client()
    experiment_results = client.evaluate(
        target,
        data="Sample dataset",
        evaluators=[
            correctness_evaluator,
            # can add multiple evaluators here
        ],
        experiment_prefix="first-eval-in-langsmith",
        max_concurrency=2,
    )
    print(experiment_results)

if __name__ == "__main__":
    main()