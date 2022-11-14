
```bash
git clone --recursive 
```

run thgis command to init cerbot config

```bash
docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org
```

run this command to generate cerbot config
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d banuyls.dev-analysis.com
```

