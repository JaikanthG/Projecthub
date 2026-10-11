from Project_Management.rag.agno_knowledge import knowledge

results = knowledge.search(
    "What embedding model does Project Hub use?",
    max_results=5,
)

print("COUNT:", len(results))

for result in results:
    print("---")
    print(result.content)