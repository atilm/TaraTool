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

## Create a html file from the Markdown Report

`pandoc --css=tara_report.css -s -f markdown+smart --toc --metadata pagetitle="Tara" --to=html5 tara_report.md -o tara_report.html`