from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_file = Path(__file__).parent / "nodejs.pdf"

# Load the pdf file and break into pages
loader = PyPDFLoader(pdf_file)
docs = loader.load()

# Breaking pages into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents=docs)

# Vector Embeddings and store in vector database
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_documents(
  documents=[],
  url="http://localhost:6333",
  collection_name="GenAI",
  embedding=embedding_model
)


vector_store.add_documents(chunks)

print("Indexing is done...")