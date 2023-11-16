# Authly Backend

with fastapi

Python Enviroment:
<https://python-poetry.org/>

## Mongo Schema

create db if selfhosted
in the db collections:

- Admin collection
- Users collection
- Applications collection

user/ applications in a collection also get there own object ids (`new ObjectId()`)

### Admin collection

currently:

```json
{
  "_id": "ObjectId(admin_id)",
  "username": "admin_username",
  "email": "admin_email",
  "password": "hashed_password",
  "roles": ["admin"],
  "containers": [
    { "ContainerA": "ObjectId(objectidforcontainera)" },
    { "ContainerB": "ObjectId(objectidforcontainera)" }
  ]
}
```

### Users collection

```json
{
  "ContainerA": {
    "_id": "ObjectId(objectidforcontainera)",
    "name": "ContainerA",
    "user": [
      {
        "_id": "ObjectId(user_id_1)",
        "username": "user1",
        "email": "user1@example.com",
        "roles": ["user"],
        "resources": []
      }
    ]
  },
  "ContainerB": {
    "_id": "ObjectId(objectidforcontainerb)",
    "name": "ContainerB",
    "user": [
      {
        "_id": "ObjectId(user_id_1)",
        "username": "user1",
        "email": "user1@example.com",
        "roles": ["user"],
        "resources": []
      }
    ]
  }
}
```

### Applications collection

```json
{
  "ContainerA": {
    "_id": "ObjectId(objectidforcontainera)",
    "name": "ContainerA",
    "applications": [
      {
        "_id": "ObjectId(app_id_1)",
        "name": "App 1",
        "version": "1.0",
        "default_access": "users of containera"
      },
      {
        "_id": "ObjectId(app_id_2)",
        "name": "App 2",
        "version": "2.0"
      }
    ]
  },
  "ContainerB": {
    "_id": "ObjectId(objectidforcontainerb)",
    "name": "ContainerB",
    "applications": []
  }
}
```
