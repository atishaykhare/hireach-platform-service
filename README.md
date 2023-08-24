# Hireach Platform Server

## Local Development

### First Build Only
1. `docker network create hireach`
2. `docker-compose up -d --build`

### Linters
Format the code
```shell
docker-compose exec app format
```


```
# Tests
All tests are integrational and require DB connection.

One of the choices I've made is to use default database (`postgres`), separated from app's `app` database.
- Using default database makes it easier to run tests in CI/CD environments, since there is no need to setup additional databases
- Tests are run with `force_rollback=True`, i.e. every transaction made is then reverted

### Run tests
```shell
docker-compose exec app pytest
```

# Run Code
```shell
docker-compose run -p 5000:8080 app
```

# Test API
*  http://localhost:5000/docs

# Health Check
*  http://localhost:5000/healthz
