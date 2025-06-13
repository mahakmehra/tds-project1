from rag.retriever import Retriever

def test_retriever():
    print("Testing retriever...")
    retriever = Retriever()
    results = retriever.retrieve("VS Code setup")
    print(f"Retrieved {len(results)} results")
    for i, r in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Score: {r['score']}")
        print(f"Content: {r['content'][:200]}...")
        print(f"Metadata: {r['metadata']}")

if __name__ == "__main__":
    test_retriever()