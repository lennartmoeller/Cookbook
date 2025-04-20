import os

from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

def main() -> None:
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[ChatCompletionUserMessageParam(content="Tell a joke", role="user")],
    )
    print(response.choices[0].message.content.strip())

if __name__ == "__main__":
    main()
