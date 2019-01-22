# 1. Get Client credentials

## a) Go to: [https://developers.globus.org/](https://developers.globus.org/)

## b) Click on:

```
Register your app with Globus
```

You will need to log in using your Globus account if you aren't logged in already.

## c) Enter a Project name and Contact email as well as set yourself as a project admin.

## d) In your new project click on the "Add..." button. Choose "Add New App". 

* Put the App Name as "My API Access"
* Native App checked.
* Scopes put: “openid”, “profile”, “email”, “urn:globus:auth:scope:transfer.api.globus.org:all“
* Redirects: https://auth.globus.org/v2/web/auth-code
* Required Identity Provider: <Leave Unchecked>
* Privacy Policy: <Leave Blank>
* Terms & Conditions: <Leave Blank>

## e) Expand the application details with the "..." on the right hand side.

## f) Copy the "Client ID" as this will be what you need to use.

# 2. Get Globus tokens

To use the Globus API you are going to need to use OAuth2 as a way to authenticate. The easiest way to do this is to get a token that you can use to make calls against the API. The most convienent method is to use refresh tokens as they are long lasting and can be used to create Active Tokens when they expire.

## a) Install python and python packages. 

```
pip install --upgrade --user configparser globus-sdk
```

## b) Create the python file get-refresh-token.py

```
import ConfigParser
import globus_sdk

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
client_id = Config.get("auth", "client_id")

client = globus_sdk.NativeAppAuthClient(client_id)
client.oauth2_start_flow(refresh_tokens=True)

print('Please go to this URL and login: {0}'
              .format(client.oauth2_get_authorize_url()))

get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input('Please enter the code here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

# let's get stuff for the Globus Transfer service
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
# the refresh token and access token, often abbr. as RT and AT
transfer_rt = globus_transfer_data['refresh_token']
transfer_at = globus_transfer_data['access_token']
expires_at_s = globus_transfer_data['expires_at_seconds']

print("Refresh_token (keep this safe as it can give others access to your Globus account): '" + str(transfer_rt) + "'")
print("Active_token: '" + str(transfer_at) + "'")
print("Token_expires '" + str(expires_at_s) + "'")
```

## c) Create the config.ini file

```
[auth]
# The client id of the user you want to use to access tasks that you get from https://auth.globus.org/v2/web/developers
client_id=
# Run the script get-refresh-token.py to get the following three values.
# WARNING: A refresh token should be as secret, or moreso than a password.
# More info at: https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-4-use-your-tokens-talk-to-the-service
refresh_token=
active_token=
token_expires=
```

## d) Put the client_id from step 1.f. into the config.ini file.

## e) Run the get-refresh-token.py script

```
$ python get-refresh-token.py
Please go to this URL and login: https://auth.globus.org/v2/oauth2/authorize?code_challenge=Wyk_TYMcNCJA5aRT-1qcNA-mEs7LNqiFb0YNp2JWOdI&state=_default&redirect_uri=https%3A%2F%2Fauth.globus.org%2Fv2%2Fweb%2Fauth-code&response_type=code&client_id=a12bc3de-f456-7890-1ef2-g3h456i7j8kl&scope=openid+profile+email+urn%3Aglobus%3Aauth%3Ascope%3Atransfer.api.globus.org%3Aall&code_challenge_method=S256&access_type=offline
```

Copy the code you get from the website and paste it into the console.

It will print out the refresh token, access token and when the access token expires.

## f) Put all three of the values (refresh token, access token and token expires) into config.ini.

Copy them into config.ini without the single quotes around the values.

# 3. Use Globus Tokens

## a) Create show_endpoints.py

Copy the below into another python script

```
import ConfigParser
import globus_sdk

# 1. The Globus SDK needs to be installed first: https://globus-sdk-python.readthedocs.io/en/stable/installation/
# short answer: pip install globus-sdk configparser

def show_endpoints(tc):
    print("My Endpoints:")
    for ep in tc.endpoint_search(filter_scope="my-endpoints"):
        print("[{}] {}".format(ep["id"], ep["display_name"]))

def get_transfer_client(client_id, transfer_rt, transfer_at, expires_at_s):
    client = globus_sdk.NativeAppAuthClient(client_id)
    client.oauth2_start_flow(refresh_tokens=True)
    authorizer = globus_sdk.RefreshTokenAuthorizer(
        transfer_rt, client, access_token=transfer_at, expires_at=int(expires_at_s))
    tc = globus_sdk.TransferClient(authorizer=authorizer)
    return tc

def main():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    client_id = Config.get("auth", "client_id")
    refresh_token = Config.get("auth", "refresh_token")
    active_token = Config.get("auth", "active_token")
    token_expires = Config.get("auth", "token_expires")

    tc = get_transfer_client(client_id, refresh_token, active_token, token_expires)

    show_endpoints(tc)

if __name__ == "__main__":
        main()
```

## b) Run the show_endpoints script to use the tokens to access the API.

```
$ python show_endpoints.py
My Endpoints:
[2988f8f0-3d6c-11e6-80c1-22000b1701d1] adammckenzie#briaree
[75d1d79a-3d6c-11e6-80c1-22000b1701d1] adammckenzie#bugaboo
[d3900078-3d6c-11e6-80c1-22000b1701d1] adammckenzie#colosse
[2f691e66-3d6d-11e6-80c1-22000b1701d1] adammckenzie#grex
[157ee6d8-3d6e-11e6-80c2-22000b1701d1] adammckenzie#guillimin
[688330e6-3d6e-11e6-80c2-22000b1701d1] adammckenzie#hermes
[7b3af308-3d6f-11e6-80c2-22000b1701d1] adammckenzie#mammouth
[b57aa73e-3d6f-11e6-80c2-22000b1701d1] adammckenzie#nestor
[dfe1c1b0-3d6f-11e6-80c2-22000b1701d1] adammckenzie#orcinus
[6eb48c2e-3d70-11e6-80c2-22000b1701d1] adammckenzie#sharcnet-dtn1
[9a1c6954-3d70-11e6-80c2-22000b1701d1] adammckenzie#ulaval-dtn2
[7e5f1382-5f13-11e6-8310-22000b97daec] akm220#shed1
[0b6ec948-3d68-11e6-80c1-22000b1701d1] akm220#silo
[037897f8-43c3-11e6-80d1-22000b1701d1] akm220-testing-jasper
[461816b0-3e6c-11e8-ba17-0ac6873fc732] Allowed Path
[4f5da09c-e7b7-11e8-8c9c-0a1d4c5c824a] Asus Laptop
[836a5b22-a7be-11e6-9ad6-22000a1e3b52] BugabooTests
[bec17d0c-b449-11e7-b0a7-22000a92523b] Cedar Share
[e5f33328-c92e-11e5-9a42-22000b96db58] computecanada#adammckenzie
[88a2e748-5fda-11e6-8316-22000b97daec] Dot Files Share
[bb01bcea-c88b-11e6-9c56-22000a1e3b52] Fedora Laptop
[b787e344-9f01-11e7-ad22-22000a92523b] Graham FloodNet Test
[edc59e1a-d061-11e7-9618-22000a8cbd7d] Graham Project
[0c86aac2-d07d-11e7-961c-22000a8cbd7d] Graham Scratch
[058fefde-8691-11e7-a92c-22000a92523b] Graham Shared Endpoint
```

# 4. Additional Resources

[Python SDK for Transfer Functions](https://globus-sdk-python.readthedocs.io/en/stable/clients/transfer/)

For more details about auth see [Globus Docs about OAuth Tokens](https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-3-get-some-access-tokens)

For all of the API operations for transfer see [Transfer API Docs](https://docs.globus.org/api/transfer/)
