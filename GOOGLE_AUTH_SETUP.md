# Google OAuth Login Setup Guide

This guide explains how to add Google login to your Digital Twin Health Backend.

## Features

✅ **Local Login**: Keep your existing email/password authentication  
✅ **Google Login**: New Google OAuth authentication  
✅ **Seamless Integration**: Both methods work together without conflicts  
✅ **Account Linking Detection**: Prevents accidental duplicate accounts

## What's Changed

### 1. Database Schema
- `User` model now has two optional authentication methods:
  - `hashed_password` (Optional) - For local login
  - `google_id` (Optional) - For Google login
  - `login_provider` - Tracks which method was used ("local" or "google")

### 2. New API Endpoints
- `POST /auth/register` - Local signup (unchanged)
- `POST /auth/login` - Local login (enhanced with Google check)
- `POST /auth/google-login` - **NEW: Google OAuth login**

### 3. New Dependencies
Added to `requirements.txt`:
- `google-auth==2.25.2`
- `google-auth-oauthlib==1.2.0`
- `PyJWT==2.8.1`
- `requests==2.31.0`

## Setup Steps

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API**:
   - Search "Google+ API" in the search bar
   - Click **Enable**

4. Create OAuth 2.0 Credentials:
   - Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
   - If prompted, configure OAuth consent screen first
   - Application type: **Web application**
   - Add Authorized redirect URIs:
     - `http://localhost:3000/auth/callback` (for development)
     - `http://localhost:5173/auth/callback` (if using Vite)
     - `https://yourdomain.com/auth/callback` (for production)

5. Copy your credentials:
   - **Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)
   - **Client Secret**

### Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update your `.env` file with Google credentials:
   ```env
   GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Update Database

Run alembic migrations to add new columns to the users table:
```bash
alembic upgrade head
```

Or if you're using SQLAlchemy auto-create (recommended for development):
The tables will be created automatically on app startup.

## API Usage

### Local Login (Existing)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Google Login (New)
```bash
curl -X POST "http://localhost:8000/auth/google-login" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "google_id_token_from_frontend"
  }'
```

## Frontend Implementation

### Using Google Sign-In Button

1. Install Google button library:
```bash
npm install @react-oauth/google
```

2. Add to your React component:
```jsx
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

export function LoginPage() {
  const handleGoogleSuccess = (credentialResponse) => {
    // Send the token to your backend
    fetch('http://localhost:8000/auth/google-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: credentialResponse.credential })
    })
    .then(res => res.json())
    .then(data => {
      console.log('Login successful:', data);
      // Store user data and redirect to dashboard
    });
  };

  return (
    <GoogleOAuthProvider clientId="YOUR_CLIENT_ID.apps.googleusercontent.com">
      <div>
        <h2>Login</h2>
        
        {/* Google Sign-In Button */}
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => console.log('Login failed')}
        />
        
        {/* Your existing password login form */}
        {/* ... */}
      </div>
    </GoogleOAuthProvider>
  );
}
```

### Using Google Sign-In SDK (Alternative)
```html
<script src="https://accounts.google.com/gsi/client" async defer></script>

<div id="g_id_onload"
     data-client_id="YOUR_CLIENT_ID.apps.googleusercontent.com"
     data-callback="handleCredentialResponse">
</div>
<div class="g_id_signin" data-type="standard"></div>

<script>
function handleCredentialResponse(response) {
  // response.credential is the ID token
  fetch('http://localhost:8000/auth/google-login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: response.credential })
  })
  .then(res => res.json())
  .then(data => console.log('Login successful:', data));
}
</script>
```

## Error Handling

### User exists with different auth method
```json
{
  "detail": "This email is already registered with password login. Please use your password to login or recover your account."
}
```

### Invalid token
```json
{
  "detail": "Invalid Google token"
}
```

### Google OAuth not configured
```json
{
  "detail": "Google OAuth not configured"
}
```

## Account Linking Rules

1. **New user with Google**: Creates account with `login_provider="google"`
2. **New user with local login**: Creates account with `login_provider="local"`
3. **Existing local user tries Google**: Gets error (prevents duplicate accounts)
4. **Existing Google user tries local**: Gets error (prevents mismatch)

## Security Best Practices

✅ **Token Verification**: Google tokens are verified on the backend  
✅ **No Secrets in Frontend**: Client ID only (Client Secret stays on backend)  
✅ **Email Validation**: Google OAuth handles email verification  
✅ **HTTPS**: Use HTTPS in production  
✅ **CORS**: Configure CORS properly for your frontend domain  

## Testing

Test local login still works:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "surname": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }'

curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

## Troubleshooting

### "GOOGLE_CLIENT_ID environment variable not set"
- Make sure you've added `GOOGLE_CLIENT_ID` to your `.env` file
- Restart your application after updating `.env`

### "Invalid Google token"
- Verify the token was generated for your `GOOGLE_CLIENT_ID`
- Check that the token is not expired (tokens expire after ~1 hour)
- Ensure `GOOGLE_CLIENT_ID` in `.env` matches the one in Google Cloud Console

### CORS errors in frontend
- Add your frontend URL to `ALLOWED_ORIGINS` in `.env`:
  ```env
  ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
  ```

## Database Migration (if using Alembic)

If you're using Alembic, create a migration:
```bash
alembic revision --autogenerate -m "Add Google OAuth support"
alembic upgrade head
```

The migration will add:
- `google_id` column (String, unique, nullable)
- `login_provider` column (String, default="local")
- `hashed_password` modified to allow NULL values

## Next Steps

1. ✅ Generate Google OAuth credentials
2. ✅ Update `.env` with credentials
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Update database schema (migration or auto-create)
5. ✅ Test endpoints with curl/Postman
6. ✅ Implement Google Sign-In button on frontend
7. ✅ Deploy with HTTPS and proper CORS configuration

## Support

For issues or questions:
- Check Google OAuth documentation: https://developers.google.com/identity/protocols/oauth2
- Review your Google Cloud Console credentials setup
- Check application logs for detailed error messages
