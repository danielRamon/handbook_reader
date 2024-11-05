import streamlit as st
from chroma_utils import ask_chroma

st.title("Encuentra en el Manual")

question = st.text_input("Haz una pregunta para encontrar en el manual")

if question:
    results = ask_chroma(question, k=5)
    for i, result in enumerate(results):
        with st.container(border=True):
            st.markdown(
                f"## [{result.metadata['title']}]({result.metadata['url']}) ")
            if len(result.page_content) > 500:
                st.markdown(f"{result.page_content[:500]}...")
            else:
                st.markdown(result.page_content)
