import streamlit as st

from api_client import search_projects


def show_search():

    st.title("Search")

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found."
        )

        return

    st.subheader("Search Project Hub")

    query = st.text_input(
        "Search",
        placeholder="Enter project name or keyword..."
    )

    if st.button("Search"):

        if not query.strip():

            st.warning(
                "Please enter a search term."
            )

            return

        response = search_projects(
            access_token,
            query.strip()
        )

        if response.status_code == 200:

            data = response.json()

            st.success(
                "Search completed successfully."
            )

            # Handle common response format:
            #
            # {
            #     "count": 2,
            #     "data": [...]
            # }

            if isinstance(data, dict):

                results = data.get(
                    "data",
                    data
                )

            else:

                results = data

            if isinstance(results, list):

                if results:

                    st.write(
                        f"Found {len(results)} result(s)."
                    )

                    st.dataframe(
                        results,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No results found."
                    )

            else:

                st.json(
                    results
                )

        else:

            try:

                error_data = response.json()

                st.error(
                    error_data.get(
                        "detail",
                        "Search failed."
                    )
                )

            except Exception:

                st.error(
                    f"Error: {response.status_code}"
                )