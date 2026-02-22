"""Google OAuth utilities."""

import os
from google.auth.transport import requests
from google.oauth2 import id_token
from typing import Optional, Dict, Any


class GoogleOAuthManager:
    """Manages Google OAuth authentication."""

    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if not self.google_client_id:
            raise ValueError("GOOGLE_CLIENT_ID environment variable not set")

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Google ID token and return user info.

        Args:
            token: Google ID token from frontend

        Returns:
            Dictionary with user info (id, email, name, picture) or None if invalid
        """
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                self.google_client_id
            )

            # Verify that the token was issued for the correct app
            if idinfo['aud'] != self.google_client_id:
                return None

            return {
                'google_id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo.get('given_name', ''),
                'surname': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture'),
            }

        except ValueError:
            # Token is invalid
            return None
        except Exception as e:
            print(f"Error verifying Google token: {str(e)}")
            return None


# Initialize the Google OAuth manager
try:
    google_oauth = GoogleOAuthManager()
except ValueError as e:
    print(f"Warning: {str(e)}")
    google_oauth = None
