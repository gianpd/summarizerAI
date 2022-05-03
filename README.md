# SummarizerPWA with Bart Large CNN ⚡️🔥🚀

### Setup
1. docker-compose --env-file FILE_NAME.env up -d --build
2. docker-compose logs web -f

### DB setup
Go inside the web-db running container and use the postgres CLI:
```
docker-compose exec web-db psql -U postgres

\c web_dev
\dt # shows tables
\q # exit
```

