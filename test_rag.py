# test_rag.py
# Quick test to check if RAG pipeline is working

from rag.rag_pipeline import initialize_rag, retrieve_relevant_chunks

print("Initializing RAG pipeline...")
print("This will take a few minutes on first run...\n")

# Initialize RAG — loads documents and builds vector store
collection = initialize_rag()

print("\n RAG pipeline ready!")
print("-" * 50)

# Test a query
query = "What was Kalam's childhood like in Rameswaram?"
print(f"Test Query: {query}\n")

chunks, sources = retrieve_relevant_chunks(query, collection)

print("Retrieved Chunks:")
for i, (chunk, source) in enumerate(zip(chunks, sources)):
    print(f"\n--- Chunk {i+1} (from {source}) ---")
    print(chunk[:300])  # Print first 300 characters