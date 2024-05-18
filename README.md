# Diplom

How to run:
Docker
```shell
docker build -t lab_check_score .
docker run -v "//var/run/docker.sock:/var/run/docker.sock" --privileged --name lab_check_score lab_check_score
docker cp lab_check_score:/app/full_file.xlsx .
```
