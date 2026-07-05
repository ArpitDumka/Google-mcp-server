# Deployment Plan: Google MCP Server on Streamlit Cloud

This document describes how to deploy the Streamlit Google Docs and Gmail server to [Streamlit Cloud](https://streamlit.io/cloud). It covers prerequisites, code readiness, Streamlit Cloud configuration, and post-deployment verification.

---

## Overview

| Configuration Item | Local Environment | Streamlit Cloud (Production) |
| :--- | :--- | :--- |
| **Server Command** | `streamlit run app.py` | Streamlit Cloud auto-runs `app.py` |
| **Authentication** | Desktop OAuth flow via browser | Token loaded from environment variable |
| **Credentials** | `credentials.json` on disk | `GOOGLE_CREDENTIALS_JSON` secret |
| **Token** | `token.json` on disk | `GOOGLE_TOKEN_JSON` secret |

---

## 1. Code Readiness Changes (Completed)

We have updated the codebase to support Streamlit Cloud deployment:
1. **Streamlit App ([app.py](file:///c:/Users/lavid/nexleap/Google_MCP/mcp-server/app.py))**: Created a Streamlit application with tabs for Google Docs and Gmail operations.
2. **Authentication ([auth.py](file:///c:/Users/lavid\nextleap\Google_MCP\mcp-server\auth.py))**: Updated to detect Streamlit Cloud environment variables (`STREAMLIT_SERVER_PORT` or `STREAMLIT_SERVER_HEADLESS`).
3. **Python Version ([runtime.txt](file:///c:/Users/lavid\nextleap\Google_MCP\mcp-server\runtime.txt))**: Set to Python 3.12 for better Pillow compatibility.

---

## 2. Google Cloud Preparation

Before deploying, ensure your Google Cloud console is configured:

1. **Enable APIs**: Ensure **Google Docs API** and **Gmail API** are enabled in the Google Cloud Console.
2. **Test Users**: If your OAuth Consent Screen is in "Testing" mode, ensure your email address is added under **APIs & Services > OAuth consent screen > Test users**.
3. **Local Authentication Run**: Make sure you have successfully completed the OAuth authentication locally once to generate the [token.json](file:///c:/Users/lavid\nextleap\Google_MCP\mcp-server\token.json) file.

---

## 3. Deployment Steps on Streamlit Cloud

1. **Push to GitHub**: Ensure your repository is on GitHub. Your local `credentials.json` and `token.json` should **NOT** be committed (they are in `.gitignore`).

2. **Create New App on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://share.streamlit.io)
   - Click **New app**
   - Connect your GitHub repository
   - Select the repository and branch (usually `main`)
   - Set the main file path to `app.py`
   - Click **Deploy**

3. **Configure Secrets**:
   - After deployment, go to your app settings
   - Navigate to **Secrets** (or **.streamlit/secrets.toml**)
   - Add the following secrets in TOML format:

```toml
GOOGLE_CREDENTIALS_JSON = '''
{
  "client_id": "your-client-id.apps.googleusercontent.com",
  "project_id": "your-project-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_secret": "your-client-secret",
  "redirect_uris": ["http://localhost"]
}
'''

GOOGLE_TOKEN_JSON = '''
{
  "token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "your-client-id.apps.googleusercontent.com",
  "client_secret": "your-client-secret",
  "scopes": ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/gmail.compose"],
  "expiry": "2024-01-01T00:00:00Z"
}
'''
```

---

## 4. How to Generate Secret Values

For `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON`, copy the JSON content from your local files and paste them into the TOML format above.

* **Windows PowerShell**:
  ```powershell
  # Copy credentials.json content
  Get-Content -Raw credentials.json | Out-String

  # Copy token.json content
  Get-Content -Raw token.json | Out-String
  ```

---

## 5. Python Version Configuration

Streamlit Cloud allows you to specify the Python version. To avoid Pillow compilation issues:

1. Create a `runtime.txt` file in your repository with:
   ```
   3.12
   ```

2. This forces Streamlit Cloud to use Python 3.12, which has better pre-built wheel support for Pillow.

3. If you need to change the Python version in Streamlit Cloud:
   - Go to your app settings
   - Look for "Python version" or "Runtime" settings
   - Select Python 3.12

---

## 6. Verification

Once deployed, Streamlit Cloud will provide you with a public URL (e.g., `https://your-app.streamlit.app`). You can verify it works by:

1. **Health Check**: Open the URL in a browser - you should see the Streamlit app with "Google MCP Server 🚀" title.
2. **Google Docs Test**: Enter a Google Doc ID and content, then click "Append to Doc".
3. **Gmail Test**: Enter recipient, subject, and body, then click "Create Draft".
