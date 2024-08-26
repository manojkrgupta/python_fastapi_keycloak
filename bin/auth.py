import jwt
from config import keycloak_conf
from jwt import PyJWKClient
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Security, HTTPException, status,Depends
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=keycloak_conf.auth_url,
    tokenUrl=keycloak_conf.token_url,
)

# Token from keycloak
async def authenticate(token: str = Security(oauth2_scheme)) -> dict:
    try:
        jwks_client = PyJWKClient(keycloak_conf.cert_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=keycloak_conf.client_id, # make sure this is correct else error --> Audience doesn't match (Fix Create Client Scope, Add Audience)
            options={"verify_exp": True},
        )
    except Exception as e:
        logger.info(f"error -- {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="failed to authenticate : " + str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )