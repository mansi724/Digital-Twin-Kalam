import os
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader


# Load all documents from data/ folder


def load_documents(data_folder="data"):
    """
    Reads all PDF and TXT files from the data folder.
    Returns a list of dicts with filename and text content.
    """
    documents = []

    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)

        # Handle PDF files
        if filename.endswith(".pdf"):
            print(f"Loading PDF: {filename}")
            text = extract_text_from_pdf(filepath)
            documents.append({
                "filename": filename,
                "text": text
            })

        # Handle TXT files
        elif filename.endswith(".txt"):
            print(f"Loading TXT: {filename}")
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            documents.append({
                "filename": filename,
                "text": text
            })

    print(f"\nTotal documents loaded: {len(documents)}")
    return documents




def extract_text_from_pdf(filepath):
    """
    Extracts all text from a PDF file page by page.
    """
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text



def split_into_chunks(text, chunk_size=500, overlap=50):
    """
    Splits a long text into smaller overlapping chunks.
    chunk_size = number of words per chunk
    overlap = number of words shared between chunks
    """
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap

    return chunks




def build_vector_store(documents, db_path="chroma_db"):
    """
    Takes all documents, splits into chunks,
    and stores them in ChromaDB with embeddings.
    """
    # Use sentence transformers for embeddings (free, local)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Create ChromaDB client
    client = chromadb.PersistentClient(path=db_path)

    # Create or get collection
    collection = client.get_or_create_collection(
        name="kalam_knowledge",
        embedding_function=embedding_fn
    )

    # Check if already populated
    if collection.count() > 0:
        print(f"Vector store already exists with {collection.count()} chunks.")
        print("Skipping rebuild. Delete 'chroma_db/' folder to rebuild.")
        return collection

    # Process each document
    all_chunks = []
    all_ids = []
    all_metadata = []

    chunk_id = 0
    for doc in documents:
        chunks = split_into_chunks(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            all_ids.append(f"chunk_{chunk_id}")
            all_metadata.append({"source": doc["filename"]})
            chunk_id += 1

    print(f"\nTotal chunks created: {len(all_chunks)}")
    print("Building vector store... this may take a few minutes...")

    # Add to ChromaDB in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        collection.add(
            documents=all_chunks[i:i+batch_size],
            ids=all_ids[i:i+batch_size],
            metadatas=all_metadata[i:i+batch_size]
        )
        print(f"Added {min(i+batch_size, len(all_chunks))}/{len(all_chunks)} chunks")

    print("\nVector store built successfully!")
    return collection



#Retrieve relevant chunks


def retrieve_relevant_chunks(query, collection, top_k=5):
    """
    Given a user query, finds the most relevant
    chunks from the vector store.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    return chunks, sources



# Initialize RAG 


def initialize_rag(data_folder="data", db_path="chroma_db"):
    """
    Loads documents and builds vector store.
    Returns the collection ready for querying.
    """
    documents = load_documents(data_folder)
    collection = build_vector_store(documents, db_path)
    return collection