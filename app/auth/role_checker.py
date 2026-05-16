from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_role(required_role: str):

    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            user_role = payload.get("role")

            if user_role != required_role:
                raise HTTPException(
                    status_code=403,
                    detail="Access Denied"
                )

            return payload

        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

    return role_checker