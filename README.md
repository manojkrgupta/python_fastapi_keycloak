### Install dependencies
```
python3 -m pip install -r requirements.txt
```

### Start environment
```text
]$ cd etc/
]$ mkdir postgres_data
]$ mkdir keycloak_data
]$ sudo docker login
]$ sudo docker compose -f docker-compose.yml up
```

### Create keycloak realm, client, user, client scope if not already created.
* Create Realm  : yahoo_realm
* Create Client : yahoo_client
  * Client Type=OpenID Connect
  * Client Authentication Enabled, 
  * OAuth2.0 Enabled
  * Root Login : http://127.0.0.1:8096/ 
  * Valid Redirect URIs: http://127.0.0.1:8096/docs/oauth2-redirect
* Create User : yahoo_user
  * Credentials -> Set Password
* Create Client scope : 'yahoo_client_scope' 
  * Within the settings of the 'yahoo_client_scope' goto Mappers tab
    * Click "Configure a new mapper"
    * Choose "Audience", Give a name = yahoo_audience
      * Name: yahoo-audience
      * Choose Mapper type: Audience
      * Included Client Audience: yahoo_client
      * Add to access token: on
  * Within the Scopes tab in yahoo_client settings -- Click on "Add client scope" -> choose "yahoo_client_scope" to assigned default client scopes

### Configurge Application to connect to keycloak
* Configuration File - bin/config.py
* Sample Configuration :
```text
keycloak_conf = keycloak_configuration(
    url="http://127.0.0.1:8095/",
    realm="yahoo_realm",
    client_id="yahoo_client",
    client_secret="<<Get this from Keycloak -> yahoo_realm -> Clients -> yahoo_client -> Credentials -> Client Secret>>",
    auth_url="http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/auth",
    token_url="http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/token",
    cert_url = "http://127.0.0.1:8095/realms/yahoo_realm/protocol/openid-connect/certs",
)
```

### Start Application (Webserver, FastAPI, Uvicorn)
```text
]$ cd bin
]$ uvicorn main:app --reload --log-level debug --port 8096 --host 127.0.0.1
```

### URLs
* Keycloak            : http://127.0.0.1:8095/   (admin/admin)
* Application Home    : http://127.0.0.1:8096/
* Application Swagger : http://127.0.0.1:8096/docs
* Public Area         : http://127.0.0.1:8096/
* Private Area        : http://127.0.0.1:8096/safe_house

### Simple Test
* Go to Swagger URL http://127.0.0.1:8096/docs
* Click on Authorize Lock Image (top right)
* ![](images/authorization_0.png)
* This will redirect you to keycloak page
* * ![](images/authorization_1.png)
* Enter Client ID : yahoo_client
* Enter Client Secret : `<<Get this from Keycloak -> yahoo_realm -> Clients -> yahoo_client -> Credentials -> Client Secret>>`
* Upon authentication of client (Once the platform/app is authenticated), keycloak redirects to ask for User ID and Password
* ![](images/authorization_2.png)
* Once success, you will see a page like
* ![](images/authorization_3.png)


### Tests using command line
* Accessing Public Area
```text
]$  curl -X 'GET'   'http://127.0.0.1:8096/'  
{"message":"Hello World"}
]$ 
```
* Accessing Private Area -- without authentication
```text
]$  curl -X 'GET' 'http://127.0.0.1:8096/safe_house'
{"detail":"Not authenticated"}
]$ 
```
* Accessing Private Area -- without authentication
```text
]$  curl -X 'GET' 'http://127.0.0.1:8096/safe_house'
{"detail":"Not authenticated"}
]$ 
```
* Accessing Private Area -- After authentication, and copying the Tokens from Swagger
```text
]$ curl -X 'GET' \
'http://127.0.0.1:8096/safe_house' \
-H 'accept: application/json' \
-H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyQUlfTHFGSHNybW9hZDR6dlgtVkpOUFVlQ2x3ZlpIV0ZvNVh1cmVIUk9VIn0.eyJleHAiOjE3MjQ2NTU1NjIsImlhdCI6MTcyNDY1NTI2MiwiYXV0aF90aW1lIjoxNzI0NjU1MjYyLCJqdGkiOiI5MDdmNDY4NS1lZDY2LTQ2NjktYjgxZS0yZDlkNzZjN2M3ZDQiLCJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwOTUvcmVhbG1zL3lhaG9vX3JlYWxtIiwiYXVkIjpbInlhaG9vX2NsaWVudCIsImFjY291bnQiXSwic3ViIjoiZjM5OTg4YWQtZWUzMC00YzhiLWEwMjYtMWRlNWRlZTIxZjNhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoieWFob29fY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6ImNkYmVjMDM2LTFlNDMtNDAyMi1iZTRjLWE0YTUwN2Y0ZjZiMyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovLzEyNy4wLjAuMTo4MDk2Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy15YWhvb19yZWFsbSJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCB5YWhvb19jbGllbnRfc2NvcGUiLCJzaWQiOiJjZGJlYzAzNi0xZTQzLTQwMjItYmU0Yy1hNGE1MDdmNGY2YjMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InlhaG9vX3VzZXIifQ.CiQUtsVPnArieH0MbYh18MkEqRBl42zpqlTThr2c74KZTLu2EFqzzR-DfKpSZ6tu3yvaH-g6R5pnBQkxUJ9C1gjGlnFYJCLWi64zhrl2HjwigDjiRM9xnSF1_Gt0UiZ5QV2mEc5rwoUveog170o4MEogDsAs49onSEPBHyQzUhTfVDs_ge8_INRfiFmDCsMtRLXy0tF-tl331aLkcui-blz5JlPBXIsl0yAyNWYDG-ZHYy0ahZNfZrPSjZhQChWo3YI_l7ZbfO3CE16HnxX4LZ1cp7clm7_73BlH5CKVLt5CkiIX3kLvF8utO3--slvpXD68hpDe8DvuHCBz1dTmTQ'
{"message":"Hello yahoo_user!!"}
```
* Accessing Private Area -- with incorrect keys
```text
]$ curl -X 'GET'   'http://127.0.0.1:8096/safe_house'   -H 'accept: application/json'   -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyQUlfTHFGSHNybW9hZDR6dlgtVkpOUFVlQ2x3ZlpIV0ZvNVh1cmVIUk9VIn0.eyJleHAiOjE3MjQ2NTU1NjIsImlhdCI6MTcyNDY1NTI2MiwiYXV0aF90aW1lIjoxNzI0NjU1MjYyLCJqdGkiOiI5MDdmNDY4NS1lZDY2LTQ2NjktYjgxZS0yZDlkNzZjN2M3ZDQiLCJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwOTUvcmVhbG1zL3lhaG9vX3JlYWxtIiwiYXVkIjpbInlhaG9vX2NsaWVudCIsImFjY291bnQiXSwic3ViIjoiZjM5OTg4YWQtZWUzMC00YzhiLWEwMjYtMWRlNWRlZTIxZjNhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoieWFob29fY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6ImNkYmVjMDM2LTFlNDMtNDAyMi1iZTRjLWE0YTUwN2Y0ZjZiMyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovLzEyNy4wLjAuMTo4MDk2Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy15YWhvb19yZWFsbSJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCB5YWhvb19jbGllbnRfc2NvcGUiLCJzaWQiOiJjZGJlYzAzNi0xZTQzLTQwMjItYmU0Yy1hNGE1MDdmNGY2YjMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InlhaG9vX3VzZXIifQ.CiQUtsVPnArieH0MbYh18MkEqRBl42zpqlTThr2c74KZTLu2EFqzzR-DfKpSZ6tu3yvaH-g6R5pnBQkxUJ9C1gjGlnFYJCLWi64zhrl2HjwigDjiRM9xnSF1_Gt0UiZ5QV2mEc5rwoUveog170o4MEogDsAs49onSEPBHyQzUhTfVDs_ge8_INRfiFmDCsMtRLXy0tF-tl331aLkcui-blz5JlPBXIsl0yAyNWYDG-ZHYy0ahZNfZrPSjZhQChWo3YI_l7ZbfO3CE16HnxX4LZ1cp7clm7_73BlH5CKVLt5CkiIX3kaaaaaLvF8utO3--slvpXD68hpDe8DvuHCBz1dTmTQ'
{"detail":"failed to authenticate : Signature verification failed"}
]$
```