# Dentist's Den API

Beta Configuration (Requires `pipenv`)

```sh
pipenv shell
python app.py
```

Two-layer API

* **Interface Layer**: `__init__` files represent Controllers and host the endpoints
* **Domain Layer + Data Access Layer**: May be separated later (If application requires reuse)

## Useful Queries

### User table

```sql
SELECT * FROM USER
```