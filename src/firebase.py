import firebase_admin
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from src.models.AuthUser import AuthUser

cred = credentials.Certificate("sercrets/fastapi-tutorial-f4878-firebase-adminsdk-lkjko-c8eaa0d030.json")
firebase_admin.initialize_app(cred)


def get_user(res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> AuthUser:
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    res.headers["WWW-Authenticate"] = 'Bearer realm="auth_required"'
    print(type(decoded_token))
    return decoded_token
