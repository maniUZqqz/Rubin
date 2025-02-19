from openai import OpenAI

# تنظیمات API
API_KEY = 'tpsg-efF5t0ayIW2rGcC92TBMp4PKKgUMo2R'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

# گرفتن اطلاعات به‌عنوان متن مبنا
context = input("متن مبنا را وارد کنید: ")

# آماده‌سازی پرامپت برای مدل
system_prompt = f"""
شما یک دستیار هوشمند هستید که فقط بر اساس متن زیر به سوالات پاسخ می‌دهید:
متن:
{context}

- اگر جواب در متن وجود نداشت، فقط بنویسید: "جواب پیدا نشد".
- خارج از متن نظری ندید.
- پاسخ‌ها کوتاه و دقیق باشند.
"""

conversation_history = [
    {"role": "system", "content": system_prompt}
]

# حلقه پرسش و پاسخ
while True:
    question = input("سوال خود را وارد کنید (خروج: exit): ")
    if question.lower() == 'exit':
        print("پایان جلسه.")
        break

    conversation_history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    # نمایش پاسخ
    answer = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": answer})
    print("پاسخ:", answer)
