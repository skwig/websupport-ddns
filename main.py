import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone

import requests
from requests.auth import HTTPBasicAuth


def get_public_ip() -> str:
    public_ip_response_raw = requests.get('https://api.ipify.org?format=json')
    public_ip_response = json.loads(public_ip_response_raw.content)

    return public_ip_response["ip"]


def get_last_public_ip(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_last_public_ip(public_ip: str, path: str):
    public_ip_as_json = json.dumps(
        {
            "public_ip": public_ip,
            "saved_on": datetime.fromtimestamp(int(time.time()), timezone.utc).isoformat()
        }
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as outfile:
        outfile.write(public_ip_as_json)


def update_record_a(api_key: str, secret: str, domain: str, record_id: int, name: str, ip: str):
    method = "PUT"
    path = "/v1/user/%s/zone/%s/record/%s" % ("self", domain, record_id)
    timestamp = int(time.time())

    canonical_request = "%s %s %s" % (method, path, timestamp)
    signature = hmac.new(bytes(secret, 'UTF-8'), bytes(canonical_request, 'UTF-8'), hashlib.sha1).hexdigest()

    url = "%s%s" % ("https://rest.websupport.sk", path)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Date": datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
    }

    body = {
        "name": name,
        "content": ip,
        "ttl": 600
    }

    print("Setting domain's '%s' record_id '%s' to '%s' and '%s'" % (domain, record_id, name, ip))
    response = requests.put(url, json=body, headers=headers, auth=HTTPBasicAuth(api_key, signature), timeout=5)
    if not response.ok:
        raise Exception("Not OK. %s" % response)


param_api_key = os.environ["WEBSUPPORT_API_KEY"]
param_secret = os.environ["WEBSUPPORT_SECRET"]
param_domain = os.environ["WEBSUPPORT_DOMAIN"]
param_dns_record_id = int(os.environ["WEBSUPPORT_RECORD_ID"])
param_dns_record_name = os.environ["WEBSUPPORT_RECORD_NAME"]

last_saved_public_ip = get_last_public_ip("files/public_ip.json")

last_public_ip = last_saved_public_ip["public_ip"] if last_saved_public_ip is not None else ""
public_ip = get_public_ip()

if last_public_ip == public_ip:
    print("Public IP is unchanged: '%s'. Exiting..." % public_ip)
    exit(0)

print("New public IP: '%s', changed from '%s'" % (public_ip, last_public_ip))

update_record_a(param_api_key, param_secret, param_domain, param_dns_record_id, param_dns_record_name, public_ip)

save_last_public_ip(public_ip, "files/public_ip.json")