# Project Banuyls

```bash
git clone --recursive {url_of_projet}
```


```
docker-compose up -d
```

or

```
docker compose up -d
```

## Optinal

> for ssl auto config


- run this command to init cerbot config

```bash
docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org
```

- run this command to generate cerbot config
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d banuyls.dev-analysis.com
```

