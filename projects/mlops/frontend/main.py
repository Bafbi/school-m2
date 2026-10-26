import streamlit as st


def chatbot():
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("Chat")
    st.markdown("Welcome to the chatbot!")
    st.chat_message("assistant").write("Hello!, how can I help you?")

    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "I'm sorry, I don't understand."}
        )

        for message in st.session_state.chat_history:
            st.chat_message(message["role"]).markdown(message["content"])


def main():
    st.set_page_config(page_title="MLOps Frontend", page_icon=":robot:")
    chatbot()


if __name__ == "__main__":
    main()
