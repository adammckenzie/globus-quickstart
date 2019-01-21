# 1. Install Python
(Might already be installed)

# 2. Install Globus command line:

```
pip install --upgrade --user globus-cli
```

# 3. Login

```
globus login
```

Will print out something like:

```
Please authenticate with Globus here:
------------------------------------
https://auth.globus.org/v2/oauth2/authorize?prompt=login&access_type=offline&state=_default&redirect_uri=https%3A%2F%2Fauth.globus.org%2Fv2%2Fweb%2Fauth-code&response_type=code&client_id=1234abc5-1a23-4321-a1bc-a12b3cde45fg&scope=openid+profile+email+urn%3Aglobus%3Aauth%3Ascope%3Aauth.globus.org%3Aview_identity_set+urn%3Aglobus%3Aauth%3Ascope%3Atransfer.api.globus.org%3Aall
------------------------------------

Enter the resulting Authorization Code here: O6pIVr6gsDRGaPxH37MAGqW0uxTsEd


You have successfully logged in to the Globus CLI!

You can check your primary identity with
  globus whoami

For information on which of your identities are in session use
  globus session show

Logout of the Globus CLI with
  globus logout
```

# 4. Find endpoint id (UUID)

```
$ globus endpoint search computecanada#cedar-dtn

ID                                   | Owner                      | Display Name
------------------------------------ | -------------------------- | -----------------------------------
c99fd40c-5545-11e7-beb6-22000b9a448b | computecanada@globusid.org | computecanada#cedar-dtn
```

```
$ globus endpoint search computecanada#graham-dtn
ID                                   | Owner                      | Display Name
------------------------------------ | -------------------------- | -------------------------
499930f1-5c43-11e7-bf29-22000b9a448b | computecanada@globusid.org | computecanada#graham-dtn
```

# 5. List files in a directory

```
$ globus ls c99fd40c-5545-11e7-beb6-22000b9a448b:~/
project/
projects/
scratch/
```

```
$ globus ls c99fd40c-5545-11e7-beb6-22000b9a448b:~/project/
akm220/
```


```
$ globus ls 499930f1-5c43-11e7-bf29-22000b9a448b:~/
nearline/
project/
projects/
scratch/
```


# 6. Initiate transfer

```
$ globus transfer --recursive 499930f1-5c43-11e7-bf29-22000b9a448b:~/Globus/source c99fd40c-5545-11e7-beb6-22000b9a448b:~/Globus/dest
Message: The transfer has been accepted and a task has been created and queued for execution
Task ID: 5524c210-1dc9-11e9-9fa0-0a06afd4a22e
```

```
globus transfer --help
```

```
globus transfer -s, --sync-level [exists|size|mtime|checksum]
```

# 7. Resources
[Globus Install CLI](https://docs.globus.org/cli/installation/)

[Globus CLI Examples](https://docs.globus.org/cli/examples/)

