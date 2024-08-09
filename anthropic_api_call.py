import anthropic
from key import get_api_key



def send_prompt(prompt):
    

    OPENAI_API_KEY = get_api_key()

    client = anthropic.Anthropic(api_key=OPENAI_API_KEY)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    #print(message)
    return message


if __name__ == "__main__":
    send_prompt(prompt="hello?")