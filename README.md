# back-fish

## Docker

```docker
docker volume create fish-volume

docker build -t back-fish .
docker run -it --rm --volume fish_volume:/api/instance --publish 80:80 --name server-fish back-fish
```