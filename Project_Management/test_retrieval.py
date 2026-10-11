from Project_Management.database import SessionLocal
from Project_Management.rag.retrieval import retrieve_context


db = SessionLocal()

try:

    query = "What authentication does Project Hub use?"

    results = retrieve_context(
        query=query,
        db=db,
        project_id=2,
        top_k=5,
    )

    print("\n==============================")
    print("RAG RETRIEVAL TEST")
    print("==============================")

    print("\nQuery:")
    print(query)

    print("\nRetrieved Chunks:")

    if not results:

        print("NO RESULTS FOUND")

    else:

        for index, content in enumerate(
            results,
            start=1
        ):

            print(
                f"\n--- Chunk {index} ---"
            )

            print(content)

    print("\n==============================")

finally:

    db.close()