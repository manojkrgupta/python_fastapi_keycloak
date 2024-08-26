from models import keycloak_configuration

keycloak_conf = keycloak_configuration(
    url="http://127.0.0.1:8095/",
    realm="yahoo_realm",
    client_id="yahoo_client",
    client_secret="v6fVMx1CrMGJ2xr9xojwULuo8Ps9xKy7",
    auth_url="http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/auth",
    token_url="http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/token",
    cert_url = "http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/certs",
)