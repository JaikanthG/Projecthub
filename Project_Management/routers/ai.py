from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..ai.agent import ProjectHubAgent
from ..utils.permissions import require_project_member


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/ai",
    tags=["AI Agent"],
)


# ============================================================
# REQUEST
# ============================================================

class AIChatRequest(BaseModel):

    message: str

    project_id: int


# ============================================================
# RESPONSE
# ============================================================

class AIChatResponse(BaseModel):

    response: str


# ============================================================
# CHAT
# ============================================================

@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat(
    request: AIChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    print("\n========================================")
    print("AI CHAT REQUEST")
    print("========================================")

    print(
        f"User: {current_user}"
    )

    print(
        f"Message: {request.message}"
    )

    print(
        f"Project ID: {request.project_id}"
    )

    # --------------------------------------------------------
    # Validate message
    # --------------------------------------------------------

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    # --------------------------------------------------------
    # Project Access Check
    # --------------------------------------------------------

    project_id = request.project_id

    print(
        f"Checking project access for project_id={project_id}"
    )

    # Admin → allowed
    # Employee + Member → allowed
    # Employee + Contributor → allowed
    # Employee without membership → 403
    require_project_member(
        project_id=project_id,
        current_user=current_user,
        db=db,
    )

    print(
        f"Project access verified for project_id={project_id}"
    )

    # --------------------------------------------------------
    # Create Agent
    # --------------------------------------------------------

    try:

        print(
            "Creating ProjectHubAgent..."
        )

        agent = ProjectHubAgent(
            db=db,
            project_id=project_id,
        )

        print(
            "ProjectHubAgent created."
        )

    except Exception as e:

        print(
            f"Agent creation failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create AI Agent: {str(e)}",
        )

    # --------------------------------------------------------
    # Run Agent
    # --------------------------------------------------------

    try:

        print(
            f"Running AI for project_id={project_id}"
        )

        answer = agent.chat(
            request.message
        )

        print(
            "AI response received."
        )

        print(
            f"Response: {answer}"
        )

    except Exception as e:

        print(
            f"AI Agent execution failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"AI Agent failed: {str(e)}",
        )

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

    if not answer:

        raise HTTPException(
            status_code=500,
            detail="AI Agent returned an empty response.",
        )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    print(
        "Returning response to Streamlit."
    )

    print(
        "========================================\n"
    )

    return AIChatResponse(
        response=answer
    )