import streamlit.components.v1 as components


def add_chatbot():
    #     <iframe
#     allow="microphone;"
#     width="350"
#     height="430"
#     src="https://console.dialogflow.com/api-client/demo/embedded/961031b7-c48e-4973-93b3-ddf01b97a1fc">
# </iframe>

    components.html(
    """
    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
        chat-title="Web-Search"
        agent-id="961031b7-c48e-4973-93b3-ddf01b97a1fc"
        language-code="en"></df-messenger>
    """,
    width=800,
    height=300, # try various values to see what works best (maybe use st.slider)
)