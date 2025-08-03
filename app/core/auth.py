import jwt 
from jwt import PyJWKClient
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

def validate_clerk_token(token: str, audience: str = None):
    try:
        jwks_client = PyJWKClient(settings.CLERK_JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=audience,
            issuer=settings.CLERK_ISSUER,
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
        )

def get_payload(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return validate_clerk_token(credentials.credentials)
