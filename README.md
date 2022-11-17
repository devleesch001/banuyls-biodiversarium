# back-fish

## Docker

```docker
docker volume create database-fish

docker build -t back-fish .
docker run -it --rm --volume database-fish:/api/instance --publish 80:80 --name server-fish back-fish
```