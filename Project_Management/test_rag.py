from Project_Management.database import SessionLocal
from Project_Management.rag.ingestion import ingest_knowledge


db = SessionLocal()

try:

    result = ingest_knowledge(
        knowledge_id=6,
        db=db,
    )

    print(result)

finally:

    db.close()