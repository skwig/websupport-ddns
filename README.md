# websupport-ddns

[![CI](https://github.com/skwig/websupport-ddns/actions/workflows/ci.yml/badge.svg)](https://github.com/skwig/websupport-ddns/actions/workflows/ci.yml)

DDNS updater for [websupport.sk](websupport.sk) domains.

## How does it work
Gets the current IPv4 public IP, compares it with the previous public IP and updates your configured websupport DNS A record, if the IP changes. 
Can be periodically executed via a cronjob. 

Uses the [websupport REST API](https://rest.websupport.sk/docs/index), which requires an API key with a secret. 
This API key & secret pair can be generated [here](https://www.websupport.sk/podpora/kb/api-keys/).

## Configuring & running

Usage with docker is recommended for ease of deployment. The image is available [here](https://example.com).

The docker image is configured with the following environment variables: 
* `WEBSUPPORT_API_KEY` - Generated with https://www.websupport.sk/podpora/kb/api-keys/
* `WEBSUPPORT_SECRET` - Generated with https://www.websupport.sk/podpora/kb/api-keys/
* `WEBSUPPORT_DOMAIN` - Your domain. Example: `mydomain.com` in `subdomain.mydomain.com`
* `WEBSUPPORT_RECORD_ID`- Your record id. Can be seen in the url when editing the subdomain. Example `45528277`
* `WEBSUPPORT_RECORD_NAME` - Your record name, used as the subdomain. Example: `subdomain` in `subdomain.mydomain.com`

### Example docker usage

### Example docker-compose usage with cron