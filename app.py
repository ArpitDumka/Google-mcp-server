import streamlit as st
import logging
from docs_tool import append_to_doc
from gmail_tool import create_email_draft

# ---------------- LOGGING SETUP ---------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Google MCP Server",
    page_icon="🚀",
    layout="wide"
)

# ---------------- HEADER ---------------- #
st.title("Google MCP Server 🚀")
st.markdown("Interact with Google Docs and Gmail APIs")

# ---------------- TABS ---------------- #
tab1, tab2 = st.tabs(["📄 Google Docs", "📧 Gmail"])

# ---------------- GOOGLE DOCS TAB ---------------- #
with tab1:
    st.header("Append to Google Doc")
    
    doc_id = st.text_input("Google Doc ID", placeholder="Enter your Google Doc ID")
    content = st.text_area("Content to Append", placeholder="Enter content to append to the document", height=150)
    
    if st.button("Append to Doc", type="primary"):
        if doc_id and content:
            with st.spinner("Appending content..."):
                result = append_to_doc(doc_id, content)
                
                if result.get("status") == "success":
                    st.success(f"✅ {result.get('message')}")
                    st.json(result)
                else:
                    st.error(f"❌ {result.get('message')}")
                    if result.get("details"):
                        st.error(f"Details: {result.get('details')}")
        else:
            st.warning("⚠️ Please enter both Doc ID and content")

# ---------------- GMAIL TAB ---------------- #
with tab2:
    st.header("Create Gmail Draft")
    
    to = st.text_input("To", placeholder="recipient@example.com")
    subject = st.text_input("Subject", placeholder="Email subject")
    body = st.text_area("Body", placeholder="Email body content", height=150)
    
    if st.button("Create Draft", type="primary"):
        if to and subject and body:
            with st.spinner("Creating draft..."):
                result = create_email_draft(to, subject, body)
                
                if result.get("status") == "success":
                    st.success(f"✅ {result.get('message')}")
                    st.json(result)
                else:
                    st.error(f"❌ {result.get('message')}")
                    if result.get("details"):
                        st.error(f"Details: {result.get('details')}")
        else:
            st.warning("⚠️ Please fill in all fields")

# ---------------- SIDEBAR INFO ---------------- #
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    **Available Tools:**
    - 📄 Append to Google Doc
    - 📧 Create Gmail Draft
    
    **Environment Variables Required:**
    - `GOOGLE_CREDENTIALS_JSON`
    - `GOOGLE_TOKEN_JSON`
    
    **Note:** Make sure your Google Cloud project has:
    - Google Docs API enabled
    - Gmail API enabled
    - OAuth consent screen configured
    """)
