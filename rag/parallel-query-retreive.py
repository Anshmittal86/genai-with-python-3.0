from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from concurrent.futures import ThreadPoolExecutor #Multithreading
from itertools import chain #Flatten
import ast #Parsing
from openai import OpenAI

load_dotenv()

client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_existing_collection(
  url="http://localhost:6333",
  collection_name="GenAI",
  embedding=embedding_model
)

user_query = input("👨: ")

query_brekdown_prompt = """
You are a helpful AI Assistant. 
Your task is to take the user query and
break down the user query into different sub-quries.

Rule:
maximum Sub Query Length :- 3

Example: 
Query: How to become GenAI Developer?
Output: [
    'How to become GenAI Developer?',
    'What is GenAI?',
    'What is Developer?',
]
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": query_brekdown_prompt},
        { "role": "user", "content": user_query }
    ]
)

sub_queries = ast.literal_eval(response.choices[0].message.content.strip())
print("Sub Queries:", sub_queries)

def retrieve_chunks(query):
    return vector_store.similarity_search(query=query)

with ThreadPoolExecutor() as executor:
    all_chunks = list(executor.map(retrieve_chunks, sub_queries))
    
flattened_chunks = list(chain.from_iterable(all_chunks))

unique_chunks = list({doc.page_content: doc for doc in flattened_chunks}.values())


system_prompt = f"""
You are a helpful assistant who answer user's query by using the following pieces of context with the page no so that user can refer.
If you don't know the answer, just say that I don't know with the reason why you are not able to give the answer only give the 2 to 3 line max reason instead of just saying I don't know, don't try to make up an answer.

context: 
{[doc.page_content for doc in unique_chunks]}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": system_prompt},
        { "role": "user", "content": user_query }
    ]
)

pdf_response = response.choices[0].message.content
print(f"🤖: {pdf_response}")