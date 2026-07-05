# Deployment Plan: Google MCP Server on Streamlit Cloud

This document describes how to deploy the Streamlit Google Docs and Gmail server to [Streamlit Cloud](https://streamlit.io/cloud). It covers prerequisites, code readiness, Streamlit configuration, and post-deployment verification.

---

## Overview

| Configuration Item | Local Environment | Streamlit Cloud (Production) |
| :--- | :--- | :--- |
| **Server Command** | `streamlit run app.py` | `streamlit run app.py` |
| **Authentication** | Desktop OAuth flow via browser | Token loaded from environment variable |
| **Credentials** | `credentials.json` on disk | `GOOGLE_CREDENTIALS_JSON` environment variable |
| **Token** | `token.json` on disk | `GOOGLE_TOKEN_JSON` environment variable |
| **Approval Flow** | Interactive terminal prompt `Approve? (y/n)` | Removed (Streamlit UI provides approval) |

---

## 1. Code Readiness Changes (Completed)

We have updated the codebase to support Streamlit deployment:
1. **Streamlit App ([app.py](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/app.py))**: Created a Streamlit web interface with tabs for Google Docs and Gmail operations, replacing the FastAPI server.
2. **Requirements Updated ([requirements.txt](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/requirements.txt))**: Added `streamlit==1.39.0` to dependencies.
3. **Credentials Caching ([auth.py](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/auth.py))**: Authentication code caches credentials in memory to reduce latency.

---

## 2. Google Cloud Preparation

Before deploying, ensure your Google Cloud console is configured:

1. **Enable APIs**: Ensure **Google Docs API** and **Gmail API** are enabled in the Google Cloud Console.
2. **Test Users**: If your OAuth Consent Screen is in "Testing" mode, ensure your email address (`lavi.dumka@gmail.com`) is added under **APIs & Services > OAuth consent screen > Test users**.
3. **Local Authentication Run**: Make sure you have successfully completed the OAuth authentication locally once to generate the [token.json](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/token.json) file (already completed).

---

## 3. Deployment Steps on Streamlit Cloud

### Option A: Using Streamlit Cloud (Recommended)

1. **Push to GitHub**: Ensure your repository is pushed to GitHub. Your local `credentials.json` and `token.json` should **NOT** be committed (they are in `.gitignore`).

2. **Create Streamlit Cloud Account**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign up/login with your GitHub account

3. **Deploy Your App**:
   - Click **"New app"** in the Streamlit Cloud dashboard
   - Select your GitHub repository: `ArpitDumka/Google-mcp-server`
   - Select the branch: `main`
   - Main file path: `app.py`
   - Click **"Deploy"**

4. **Configure Environment Variables**:
   - After deployment, go to your app settings
   - Navigate to **"Secrets"** or **"Environment Variables"**
   - Add the following secrets:

| Key | Value | Description |
| :--- | :--- | :--- |
| `GOOGLE_CREDENTIALS_JSON` | *<Paste contents of credentials.json>* | Minified content of OAuth credentials |
| `GOOGLE_TOKEN_JSON` | *<Paste contents of token.json>* | Minified content of authorized OAuth token |

5. **Restart Your App**: After adding the environment variables, restart your Streamlit app from the dashboard.

---

## 4. How to Generate Environment Variable Values

For `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON`, paste the **minified single-line** JSON content:

* **Windows PowerShell**:
  ```powershell
  # Copy credentials.json content
  Get-Content -Raw credentials.json | Out-String

  # Copy token.json content
  Get-Content -Raw token.json | Out-String
  ```

* **Mac/Linux Terminal**:
  ```bash
  # Copy credentials.json content
  cat credentials.json

  # Copy token.json content
  cat token.json
  ```

---

## 5. Local Testing

Before deploying to Streamlit Cloud, test the app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 6. Verification

Once deployed, Streamlit Cloud will provide you with a public URL (e.g., `https://your-app-name.streamlit.app`). You can verify it works by:

### 6.1 Health Check
Open the app in your browser and verify the page loads with the title "Google MCP Server 🚀"

### 6.2 Append to Google Doc
1. Click on the **"📄 Google Docs"** tab
2. Enter a valid Google Doc ID
3. Enter content to append
4. Click **"Append to Doc"**
5. Verify success message and check your Google Doc

### 6.3 Create Gmail Draft
1. Click on the **"📧 Gmail"** tab
2. Enter recipient email, subject, and body
3. Click **"Create Draft"**
4. Verify success message and check your Gmail drafts

---

## 7. Troubleshooting

### App fails to start
- Check that all dependencies are in `requirements.txt`
- Verify `app.py` is in the repository root
- Check Streamlit Cloud logs for error messages

### Authentication errors
- Ensure `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` are set correctly
- Verify the JSON content is properly formatted (no extra whitespace)
- Check that your Google Cloud project has the required APIs enabled

### Google API errors
- Verify your OAuth consent screen is configured
- Ensure your email is added as a test user if in testing mode
- Check that the token hasn't expired (tokens expire after 7 days in testing mode)

---

## 8. Streamlit Configuration (Optional)

You can customize your Streamlit app by creating a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
```

This file is optional and the app will work with default Streamlit settings.
