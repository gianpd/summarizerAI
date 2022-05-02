# fastapi-tdd-docker

**FastApi project template.**

![Continuous Integration and Delivery](https://github.com/gianpDomiziani/fastapi-tdd-docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=master)

### Setup
1. docker-compose up -d --build
2. 

### DB setup
for checking the db tables have been created:
go inside the web-db running container and use the postgres CLI:
```
docker-compose exec web-db psql -U postgres
```
