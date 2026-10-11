from Project_Management.database import SessionLocal
from Project_Management.ai.agent import ProjectHubAgent


db = SessionLocal()

try:

    agent = ProjectHubAgent(
        db=db,
        project_id=2,
    )

    print("Starting agent test...")

    response = agent.chat(
        "Explain the complete RAG pipeline used by Project Hub."
    )

    print("\n==============================")
    print("AGENT RESPONSE")
    print("==============================")
    print(response)
    print("==============================")

finally:

    db.close()