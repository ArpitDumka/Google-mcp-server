# Deployment Plan: Google MCP Server on Render

This document describes how to deploy the FastAPI Google Docs and Gmail server to [Render](https://render.com). It covers prerequisites, code readiness, Render configuration, and post-deployment verification.

---

## Overview

| Configuration Item | Local Environment | Render (Production) |
| :--- | :--- | :--- |
| **Server Command** | `uvicorn server:app --reload` | `uvicorn server:app --host 0.0.0.0 --port $PORT` |
| **Authentication** | Desktop OAuth flow via browser | Token loaded from environment variable |
| **Credentials** | `credentials.json` on disk | `GOOGLE_CREDENTIALS_JSON` environment variable |
| **Token** | `token.json` on disk | `GOOGLE_TOKEN_JSON` environment variable |
| **Approval Flow** | Interactive terminal prompt `Approve? (y/n)` | Auto-approved via `AUTO_APPROVE=true` |

---

## 1. Code Readiness Changes (Completed)

We have updated the codebase to support Render deployment:
1. **Credentials Caching ([auth.py](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/auth.py))**: Updated the authentication code to cache credentials in memory. This prevents the server from reloading, parsing, and sending a refresh token request to Google on every API call, reducing latency.
2. **FastAPI Server ([server.py](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/server.py))**: Created a FastAPI application with endpoints for Google Docs and Gmail operations.

---

## 2. Google Cloud Preparation

Before deploying, ensure your Google Cloud console is configured:

1. **Enable APIs**: Ensure **Google Docs API** and **Gmail API** are enabled in the Google Cloud Console.
2. **Test Users**: If your OAuth Consent Screen is in "Testing" mode, ensure your email address (`lavi.dumka@gmail.com`) is added under **APIs & Services > OAuth consent screen > Test users**.
3. **Local Authentication Run**: Make sure you have successfully completed the OAuth authentication locally once to generate the [token.json](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/token.json) file (already completed).

---

## 3. Deployment Steps on Render

You can deploy using Render Blueprints (easiest) or manually.

### Option A: Using Render Blueprints (Recommended)
1. Push your repository to **GitHub** or **GitLab**. Ensure your local `credentials.json` and `token.json` are **NOT** committed (they are in `.gitignore`).
2. Go to the [Render Dashboard](https://dashboard.render.com).
3. Click **New > Blueprint**.
4. Connect your GitHub/GitLab repository.
5. Render will automatically read the [render.yaml](file:///c:/Users/lavid/nextleap/Google_MCP/mcp-server/render.yaml) file.
6. Under the blueprint settings, you will be prompted to enter values for:
   * `GOOGLE_CREDENTIALS_JSON`
   * `GOOGLE_TOKEN_JSON`
7. Copy and paste the minified JSON contents of your files into these fields (see how to generate them below).
8. Click **Approve**.

### Option B: Manual Web Service Setup
If you prefer to configure the Web Service manually:
1. Go to the Render Dashboard and click **New > Web Service**.
2. Connect your repository.
3. Configure the following service settings:
   * **Runtime**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Go to the **Environment** tab of the service and add the following variables:

| Key | Value | Description |
| :--- | :--- | :--- |
| `AUTO_APPROVE` | `true` | Skips interactive terminal prompt for approvals |
| `GOOGLE_CREDENTIALS_JSON` | *<Paste contents of credentials.json>* | Minified content of OAuth credentials |
| `GOOGLE_TOKEN_JSON` | *<Paste contents of token.json>* | Minified content of authorized OAuth token |

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

---

## 5. Verification

Once deployed, Render will provide you with a public URL (e.g., `https://google-mcp-server.onrender.com`). You can verify it works by sending HTTP requests:

### 5.1 Health Check
Verify the server is running:
```bash
curl https://YOUR-APP.onrender.com/
# Response: {"message": "Google MCP Server is running 🚀"}
```

### 5.2 Append to Google Doc
Append content to a Google Doc (substitute with your actual Google Doc ID):
```bash
curl -X POST https://YOUR-APP.onrender.com/append_to_doc \
  -H "Content-Type: application/json" \
  -d '{"doc_id": "YOUR_GOOGLE_DOC_ID", "content": "Appended from Render!"}'
```

### 5.3 Create Gmail Draft
Create a Gmail email draft:
```bash
curl -X POST https://YOUR-APP.onrender.com/create_email_draft \
  -H "Content-Type: application/json" \
  -d '{"to": "lavi.dumka@gmail.com", "subject": "Render Deploy Test", "body": "Draft successfully created!"}'
```
