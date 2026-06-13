import streamlit as st
import requests

API = "http://localhost:8000/api"

st.set_page_config(
    page_title="ReleaseNote Chatbot",
    page_icon="📄",
    layout="centered"
)

st.title("📄 ReleaseNote Chatbot")
st.caption("Upload a document and ask questions about it using AI")

st.divider()

st.subheader("Step 1 — Upload your document")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "txt", "csv", "xlsx"]
)

if uploaded_file:
    if st.button("Upload Document"):
        with st.spinner("Uploading, reading and chunking document..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{API}/upload", files=files)

            if response.status_code == 200:
                data = response.json()
                st.session_state.filename = uploaded_file.name
                st.session_state.word_count = data.get("word_count")
                st.session_state.chunk_count = data.get("chunk_count")
                st.session_state.preview = data.get("preview")
                st.session_state.chunks = data.get("chunks")
                st.session_state.vectors_stored = data.get("vectors_stored")
            else:
                st.error(f"Upload failed: {response.json().get('detail')}")

if "filename" in st.session_state:
    st.success(f"Uploaded: {st.session_state.filename}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("File", st.session_state.filename)
    col2.metric("Words", st.session_state.word_count)
    col3.metric("Chunks", st.session_state.chunk_count)
    col4.metric("Vectors", st.session_state.get("vectors_stored", 0))

    with st.expander("Document preview"):
        st.write(st.session_state.preview + "...")

    with st.expander("View chunks"):
        for chunk in st.session_state.chunks:
            st.markdown(f"**Chunk {chunk['chunk_index'] + 1}** "
                       f"({chunk['word_count']} words)")
            st.write(chunk["text"])
            st.divider()

    st.divider()

    st.subheader("Step 2 — Ask a question")

    question = st.text_input(
        "Your question",
        placeholder="e.g. What is new in version 2.0?"
    )

    if st.button("Ask") and question:
        with st.spinner("Searching document..."):
            response = requests.post(f"{API}/ask", json={
                "question": question,
                "filename": st.session_state.filename
            })

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer")
                relevant_chunks = data.get("relevant_chunks", [])
                tool_used = data.get("tool_used", "")
                reasoning = data.get("reasoning", "")

                if tool_used == "search_document":
                    st.info(f"🔍 Agent used: **Document Search**")
                else:
                    st.info(f"💡 Agent used: **Direct Answer**")

                st.caption(f"Reasoning: {reasoning}")

                st.subheader("Answer")
                st.write(answer)

                with st.expander("View retrieved chunks"):
                    for i, chunk in enumerate(relevant_chunks):
                        st.markdown(f"**Chunk {chunk['chunk_index'] + 1}** "
                                   f"— similarity distance: "
                                   f"`{round(chunk['distance'], 4)}`")
                        st.write(chunk["text"])
                        st.divider()
            else:
                error_detail = response.json().get("detail", "Unknown error")
                st.error(f"Error: {error_detail}")
else:
    st.info("Upload a document above to get started")