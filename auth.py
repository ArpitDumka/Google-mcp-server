import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.compose"
]

_cached_creds = None


def get_creds():
    global _cached_creds

    # If credentials are already cached and still valid, return them directly
    if _cached_creds and _cached_creds.valid:
        return _cached_creds

    is_deployed = bool(
        os.environ.get("RENDER")
        or os.environ.get("RAILWAY_ENVIRONMENT")
        or os.environ.get("IS_DEPLOYED")
    )

    # If cached credentials exist but are expired, refresh them directly
    if _cached_creds and _cached_creds.expired and _cached_creds.refresh_token:
        try:
            _cached_creds.refresh(Request())
            if not is_deployed:
                with open("token.json", "w") as token:
                    token.write(_cached_creds.to_json())
            return _cached_creds
        except Exception:
            # If refresh fails, fall back to reloading/re-authenticating
            _cached_creds = None

    creds = None
    
    # 1. Load from Environment Variable (for Render)
    env_token = os.environ.get("GOOGLE_TOKEN_JSON")
    if env_token:
        creds = Credentials.from_authorized_user_info(json.loads(env_token), SCOPES)
    # 2. Fallback to local file
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 3. Refresh or Fail (No interactive login in cloud)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if is_deployed:
                raise Exception("Missing GOOGLE_TOKEN_JSON env var or token is totally invalid.")

            # Local flow
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the refreshed token locally only when not running in a deployed env
        if not is_deployed:
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                
    _cached_creds = creds
    return _cached_creds