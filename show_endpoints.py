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
