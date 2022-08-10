# websupport-ddns

[![CI](https://github.com/skwig/websupport-ddns/actions/workflows/ci.yml/badge.svg)](https://github.com/skwig/websupport-ddns/actions/workflows/ci.yml)

DDNS updater for [websupport.sk](websupport.sk) domains.

## How does it work
Gets the current IPv4 public IP, compares it with the previous public IP and updates your configured websupport DNS A record if needed. 
Can be periodically executed via a cronjob. 

Uses the [websupport REST API](https://rest.websupport.sk/docs/index), which requires an API key with a secret. 
This API key & secret pair can be generated [here](https://www.websupport.sk/podpora/kb/api-keys/).

## Running it

The script is published in a docker image available [in the packages tab](https://github.com/skwig/websupport-ddns/pkgs/container/websupport-ddns).
Using the docker image is recommended for ease of deployment.

You can configure the script & the docker image with the following environment variables: 
* `WEBSUPPORT_API_KEY` - Generated with https://www.websupport.sk/podpora/kb/api-keys/
* `WEBSUPPORT_SECRET` - Generated with https://www.websupport.sk/podpora/kb/api-keys/
* `WEBSUPPORT_DOMAIN` - Your domain. Example: `mydomain.com` in `subdomain.mydomain.com`.
* `WEBSUPPORT_RECORD_ID`- Your record id. Can be seen in the url when editing the subdomain in the websupport administration. Example `123456789`.
* `WEBSUPPORT_RECORD_NAME` - Your record name, used as the subdomain. Example: `subdomain` in `subdomain.mydomain.com`.

### Example docker usage
TODO

### Example docker-compose with cron

Your docker-compose.yml file should look like this
<h5 a><strong><code>docker-compose.yml</code></strong></h5>
```yml
version: '3.4'
services:
  websupport-ddns-cronjob:
    image: "ghcr.io/skwig/websupport-ddns:main"
    restart: always
    environment:
      - "WEBSUPPORT_API_KEY=<api-key>"
      - "WEBSUPPORT_SECRET=<secret>"
      - "WEBSUPPORT_DOMAIN=mydomain.com"
      - "WEBSUPPORT_RECORD_ID=123456789"
      - "WEBSUPPORT_RECORD_NAME=subdomain"
    volumes:
      - "/tmp/volumes/websupport-ddns:/app/files"
    command: [ "/bin/bash", "-c", "echo '*/10 * * * * root cd /app && /usr/local/bin/python main.py > /proc/1/fd/1 2>/proc/1/fd/2' > /etc/crontab && printenv > /etc/environment && cron -f" ]
```

This will run websupport-ddns as a cronjob every 10th minute (xx:0, xx:10, xx:20 etc.). It will also automatically start when the docker service starts. 