from openai import OpenAI

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(
    api_key="sk-7e20906faf2a43f59eca57d7d8d91649",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Отвечай всегда на русском",
        },
        {"role": "user", "content": "Напиши код на python"},
    ],
    max_tokens=1024,
    temperature=0.7,
    stream=False,
)

print(response.choices[0].message.content)
