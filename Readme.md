# Readme

## Build the container

```
docker build -t tara-docker:latest .
```

## Create and start a container (first time)

```
docker run -it --name mytara-docker -v "$(pwd)":/workspace tara-docker:latest bash
```

## Reuse the container

```
docker start -ai mytara-docker
```