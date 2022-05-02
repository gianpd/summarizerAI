# SummarizerWPA with Bart Large CNN 🏻 🤟🏼

**FastApi**

![Continuous Integration and Delivery](https://github.com/gianpDomiziani/summarizerWPA/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=master)

### Setup
1. docker-compose up -d --build
2. docker-compose logs web

### DB setup
Go inside the web-db running container and use the postgres CLI:
```
docker-compose exec web-db psql -U postgres

\c web_dev
\dt # shows tables
\q # exit
```

