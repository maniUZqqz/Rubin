


# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_6wK7rt_9hcNfdA2HPVRMFwCr5EuNwmf6CLDAXJwW4JSM126j4tYJof9yUxpA5bVBQyAxDe")

# Define a sample dataset where each item has a unique ID, text, and category
data = [
    {
        "id": "rec1",
        "text": "Apples are a great source of dietary fiber, which supports digestion and helps maintain a healthy gut.",
        "category": "digestive system"
    },
    {
        "id": "rec2",
        "text": "Apples originated in Central Asia and have been cultivated for thousands of years, with over 7,500 varieties available today.",
        "category": "cultivation"
    },
    {
        "id": "rec3",
        "text": "Rich in vitamin C and other antioxidants, apples contribute to immune health and may reduce the risk of chronic diseases.",
        "category": "immune system"
    },
    {
        "id": "rec4",
        "text": "The high fiber content in apples can also help regulate blood sugar levels, making them a favorable snack for people with diabetes.",
        "category": "endocrine system"
    }
]

# # Convert the text into numerical vectors that Pinecone can index
# embeddings = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[d["text"] for d in data],
#     parameters={
#         "input_type": "passage",
#         "truncate": "END"
#     }
# )
embeddings = data




print(embeddings)
