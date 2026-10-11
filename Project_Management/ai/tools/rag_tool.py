# ============================================================
# PROJECT HUB RAG TOOL - AGNO
# ============================================================

from ...rag.agno_knowledge import knowledge


def search_knowledge(
    query: str,
    project_id: int,
):
    """
    Search the Project Hub knowledge base.

    Retrieval is strictly restricted to the supplied project_id.

    Uses:
        - Agno Knowledge
        - RecursiveChunking
        - Ollama nomic-embed-text
        - PostgreSQL + pgvector
        - Hybrid Search
        - Project-level metadata filtering
        - Result-level project validation
    """

    # --------------------------------------------------------
    # Validate Query
    # --------------------------------------------------------

    if not query or not query.strip():
        return []

    # --------------------------------------------------------
    # Validate Project ID
    # --------------------------------------------------------

    if project_id is None:
        raise ValueError(
            "project_id is required for project-scoped RAG search."
        )

    try:
        project_id = int(project_id)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "project_id must be a valid integer."
        ) from exc

    # --------------------------------------------------------
    # Project Filter
    # --------------------------------------------------------

    filters = {
        "project_id": project_id
    }

    print(
        f"\n========== PROJECT-SCOPED RAG =========="
    )

    print(
        f"RAG QUERY: {query.strip()}"
    )

    print(
        f"RAG PROJECT ID: {project_id}"
    )

    print(
        f"RAG FILTER: {filters}"
    )

    # --------------------------------------------------------
    # Agno Knowledge Search
    # --------------------------------------------------------

    results = knowledge.search(
        query=query.strip(),
        max_results=5,
        filters=filters,
        search_type="hybrid",
    )

    print(
        f"RAG RAW RESULT COUNT: {len(results)}"
    )

    # --------------------------------------------------------
    # Strict Result Validation
    # --------------------------------------------------------

    valid_results = []

    for index, result in enumerate(results):

        # --------------------------------------------
        # Read metadata
        # --------------------------------------------

        metadata = getattr(
            result,
            "metadata",
            None
        )

        if metadata is None:

            metadata = getattr(
                result,
                "meta_data",
                None
            )

        if not isinstance(metadata, dict):

            print(
                f"RAG RESULT {index + 1}: "
                "REJECTED - no metadata"
            )

            continue

        # --------------------------------------------
        # Read result project ID
        # --------------------------------------------

        result_project_id = (
            metadata.get("project_id")
        )

        try:

            result_project_id = int(
                result_project_id
            )

        except (TypeError, ValueError):

            print(
                f"RAG RESULT {index + 1}: "
                "REJECTED - invalid project_id"
            )

            continue

        # --------------------------------------------
        # STRICT PROJECT CHECK
        # --------------------------------------------

        if result_project_id != project_id:

            print(
                f"RAG RESULT {index + 1}: "
                f"REJECTED - result project_id="
                f"{result_project_id}, "
                f"requested project_id="
                f"{project_id}"
            )

            continue

        # --------------------------------------------
        # Content validation
        # --------------------------------------------

        content = getattr(
            result,
            "content",
            None
        )

        if not content:

            print(
                f"RAG RESULT {index + 1}: "
                "REJECTED - empty content"
            )

            continue

        # --------------------------------------------
        # ACCEPT
        # --------------------------------------------

        print(
            f"RAG RESULT {index + 1}: "
            f"ACCEPTED - project_id="
            f"{result_project_id}"
        )

        valid_results.append(
            content
        )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print(
        f"RAG VALID RESULT COUNT: "
        f"{len(valid_results)}"
    )

    print(
        "========================================\n"
    )

    return valid_results