from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI


input_text = "اطلاعات دانش آموز"
info = "اطلاعات بیشتر"

client = OpenAI(
    base_url="https://api.avalai.ir/v1",
    api_key="aa-bCMbGUMwByZarx3MXTKend7CBc39XhlofwT7RnBtvIrUSSxc"
)

# تولید امبدینگ با متیس
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=input_text,
)

embedding_vector = response.data[0].embedding
print(f"Embedding generated: {embedding_vector}")


# ===== تنظیمات Pinecone =====
PINECONE_API_KEY = "pcsk_3JQw7_Jui1bJfxhxoPamQ7JseTpXzTBKHWka761AXJUtzML9opT9uTtoBPcmPNAE1uN8Q"

INDEX_NAME = "rubin"  # نام اندکس Pinecone
VECTOR_DIMENSION = 1536  # تعداد ابعاد امبدینگ مدل

# ایجاد نمونه Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# بررسی اینکه آیا اندکس ایجاد شده یا خیر
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# دسترسی به اندکس
index = pc.Index(INDEX_NAME)
# ===== دریافت ورودی، تولید امبدینگ و ذخیره =====


# افزودن امبدینگ به Pinecone
vector_id = "X"  # آیدی منحصر به‌فرد برای بردار == یا نیم اسپیس
# ای دی یوزر
vectors = [
    {
        "id": vector_id,
        "values": embedding_vector,
        # اطلاعات اضافی که کنار دیتا اصلی ذخیره شه
        "metadata": {
            "text": input_text,
            "additional_info": info
        }
    }
]
index.upsert(vectors)

print(f"Vector with ID '{vector_id}' added to Pinecone.")


