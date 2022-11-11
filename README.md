
run thgis command to init cerbot config

```
docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org
```

run this command to generate cerbot config
```
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d banuyls.dev-analysis.com
```

