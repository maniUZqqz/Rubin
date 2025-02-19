from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone



index_name="https://rubin-1hzcy7u.svc.aped-4627-b74a.pinecone.io"

QQz = "pcsk_6ib4Y8_SpqiiLctApfPHfHscdFJnDJRhChi6iojWCsZjgaxnq3TYZcUrapo7S3xDZvcNAt"


pc = Pinecone(api_key=QQz)

index = pc.Index(index_name)

client = OpenAI(
    base_url="https://api.avalai.ir/v1",
    api_key="aa-bCMbGUMwByZarx3MXTKend7CBc39XhlofwT7RnBtvIrUSSxc"
)

# Define a sample dataset where each item has a unique ID, text, and category
data = [
    {
        "id": "rec1",
        "text": "Apple.",
        "category": "digestive system" 
    },
]


response = client.embeddings.create(
    input=[d["text"] for d in data],
    model="text-embedding-3-small"
)





index = pc.Index

# Prepare the records for upsert
# Each contains an 'id', the vector 'values',
# and the original text and category as 'metadata'
records = []
for d, e in zip(data, response):

    records.append({
        "id": d["id"],
        "values": e,
        "metadata": {
            "source_text": d["text"],
            "category": d["category"]
        }
    })

# Upsert the records into the index
index.upsert(
    vectors=records,
    namespace="example-namespace"
)
