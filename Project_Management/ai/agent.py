from pathlib import Path

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq

from .tools.rag_tool import search_knowledge


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(
    BASE_DIR / ".env"
)


# ============================================================
# CONFIGURATION
# ============================================================

GROQ_MODEL = "openai/gpt-oss-120b"


# ============================================================
# PROJECT HUB AGENT
# ============================================================

class ProjectHubAgent:

    def __init__(
        self,
        db=None,
        project_id: int | None = None,
    ):

        # ----------------------------------------------------
        # PROJECT ID IS REQUIRED
        # ----------------------------------------------------

        if project_id is None:

            raise ValueError(
                "project_id is required to create the "
                "Project Hub AI Agent."
            )

        self.db = db
        self.project_id = project_id

        print(
            f"ProjectHubAgent initialized "
            f"for project_id={self.project_id}"
        )

        # ----------------------------------------------------
        # RAG TOOL
        # ----------------------------------------------------

        def search_project_hub(
            query: str,
        ) -> str:
            """
            Search Project Hub knowledge.

            Search is strictly restricted to the
            current project_id.

            Uses Agno Knowledge with:
                - Recursive Chunking
                - Ollama nomic-embed-text
                - PostgreSQL + pgvector
                - Hybrid Search
                - Project-level filtering
            """

            results = search_knowledge(
                query=query,
                project_id=self.project_id,
            )

            if not results:

                return (
                    "NO INFORMATION FOUND IN THE "
                    "CURRENT PROJECT KNOWLEDGE BASE."
                )

            return "\n\n".join(
                results
            )

        # ----------------------------------------------------
        # AGNO AGENT
        # ----------------------------------------------------

        self.agent = Agent(

            id="projecthub-agent",

            name="Project Hub AI Agent",

            model=Groq(
                id=GROQ_MODEL
            ),

            tools=[
                search_project_hub
            ],

            instructions=[

                # --------------------------------------------
                # ROLE
                # --------------------------------------------

                "You are the Project Hub AI Agent.",

                "You answer questions using information "
                "available in the knowledge base of the "
                "currently selected project.",

                # --------------------------------------------
                # PROJECT SCOPE
                # --------------------------------------------

                f"The current project ID is "
                f"{self.project_id}.",

                "You must only use information retrieved "
                "for the current project.",

                "Never use information from another project.",

                # --------------------------------------------
                # RAG RULE
                # --------------------------------------------

                "For every Project Hub related question, "
                "ALWAYS use the search_project_hub tool first.",

                "The current project's knowledge base is "
                "the primary source of truth.",

                "Do not answer Project Hub questions from "
                "your pretrained knowledge.",

                # --------------------------------------------
                # NO HALLUCINATION
                # --------------------------------------------

                "Only answer using information supported "
                "by the retrieved project knowledge.",

                "Never invent Project Hub information.",

                "Never guess missing information.",

                "Never assume information that is not present "
                "in the retrieved knowledge.",

                # --------------------------------------------
                # MISSING INFORMATION
                # --------------------------------------------

                "If the retrieved knowledge does not contain "
                "the answer, say exactly:",

                "Information not found in the current "
                "project knowledge base.",

                # --------------------------------------------
                # GENERAL QUESTIONS
                # --------------------------------------------

                "If a question is completely unrelated to "
                "Project Hub and cannot be answered using "
                "the available project knowledge, say:",

                "This information is outside the available "
                "project knowledge base.",

                # --------------------------------------------
                # ANSWER STYLE
                # --------------------------------------------

                "Answer clearly and simply.",

                "Do not mention internal tools unless "
                "the user asks.",

                "Do not expose database implementation "
                "details unless they are present in the "
                "retrieved project knowledge.",
            ],

            markdown=True,
        )

    # ========================================================
    # CHAT
    # ========================================================

    def chat(
        self,
        message: str,
    ) -> str:

        if not message or not message.strip():

            raise ValueError(
                "Message cannot be empty."
            )

        response = self.agent.run(
            message.strip()
        )

        # ----------------------------------------------------
        # AGNO RESPONSE
        # ----------------------------------------------------

        answer = getattr(
            response,
            "content",
            None
        )

        if not answer:

            raise RuntimeError(
                "Groq/Agno returned an empty response."
            )

        return str(answer).strip()