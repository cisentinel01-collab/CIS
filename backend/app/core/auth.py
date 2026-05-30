import os
from keycloak import KeycloakOpenID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://keycloak:8080/")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "oneops")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "oneops-backend")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # In production, this would use public keys to verify JWT locally
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(roles: List[str]):
    async def role_checker(user: dict = Depends(get_current_user)):
        user_roles = user.get("resource_access", {}).get(KEYCLOAK_CLIENT_ID, {}).get("roles", [])
        if not any(role in user_roles for role in roles):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return role_checker
