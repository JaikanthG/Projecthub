from Project_Management.database import SessionLocal
from Project_Management.rag.ingestion import ingest_all_documents


db = SessionLocal()

try:

    print("\n==============================")
    print("PROJECT HUB DOCUMENT INGESTION")
    print("==============================\n")

    results = ingest_all_documents(
        db=db,
        project_id=9,
    )

    for result in results:

        print(result)

finally:

    db.close()