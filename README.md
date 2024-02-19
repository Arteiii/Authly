# Authly

[![CodeFactor](https://www.codefactor.io/repository/github/wavy42/authly/badge)](https://www.codefactor.io/repository/github/wavy42/authly)

[![LICENSE](LICENSE)](<https://img.shields.io/github/license/Arteiii/Authly>)

Authly is a user management application built on [FastAPI](https://fastapi.tiangolo.com/) in Python, designed to provide user authentication and access control for various applications.

## Commercial Use

For any commercial use of this software, proper attribution to the original developer Arteii is required, and a link to the original repository on GitHub must be provided.

<!-- ## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Testing](#testing)
- [Credits](#credits)
- [License](#license)

## Installation

To set up Authly, please follow the instructions in the [Installation Guide](https://github.com/wavy42/authly/wiki/Installation-Guide) in our GitHub wiki.

For more detailed instructions and options, please refer to the same guide.

## Usage

Get started with Authly by following our setup guide, which can be found in the [Usage section of our GitHub wiki](https://github.com/wavy42/authly/wiki/Usage-Guide).
The wiki provides comprehensive information on all available options and configurations.

## Features

Authly offers a range of features, including but not limited to:

- User authentication and authorization
- Access control for different applications
- User subscription management

We are continuously developing and adding new features to enhance your user management experience. Stay tuned for more updates! -->

<!-- ## Contributing

We welcome contributions from the open-source community to make Authly even better. If you'd like to contribute, please check the [Contribution Guidelines](https://github.com/wavy42/authly/wiki/Contribution-Guidelines) in our GitHub wiki for details on how to get started. -->

<!-- ## Testing

We highly recommend writing tests for your application to ensure its reliability and functionality. You can find examples and instructions on how to run tests in the [Testing section of our GitHub wiki](https://github.com/wavy42/authly/wiki/Testing-Guide). -->

## Authly Backend

## Python Environment Setup

This project uses [Poetry](https://python-poetry.org/) for managing the Python environment

### Development Environment

To run the application in development mode, use the following command:

```shell
poetry run python main.py dev
```

### Release Environment

For the release environment, execute the following command:

```shell
poetry run python main.py deploy
```

### Docker Release

To run the application in a Dockerized environment, including the setup of MongoDB and Redis, use the following command:

```shell
docker-compose up --build -d
```

The -d option runs the containers in the background

### Note

Make sure to have Docker installed before running the Docker release command.
You can install Docker from <https://www.docker.com/get-started>.

Feel free to adjust the configurations in the docker-compose.yml file to match your requirements.

### Important

Ensure that the necessary environment variables are properly configured, especially when deploying in production.
Refer to the project documentation for details on configuring environment variables

## Mongo Schema

create db if selfhosted
in the db collections:

- Admin collection
- Users collection
- Applications collection

user/ applications in a collection also get there own object ids (`new ObjectId()`)

### Bubble Collection

currently:

```json
{
  "_id": {
    "$oid": "exmaple oid of bubble collection"
  },
  "name": "string",
  "settings": {
    "allow_new_user_registration": true,
    "test_settings": "HelloWorld",
    "bliblablu": true
  },
  "application_document_id": "example oid 1",
  "key_document_id": "example oid 2",
  "user_document_id": "example oid 3"
}
```

### Admin collection

currently:

directly ref to the document

```json
{
  "_id": ObjectId("admin_id"),
  "username": "admin_username",
  "email": "admin_email",
  "password": "hashed_password",
  "roles": ["admin"],
  "bubbles": [ObjectId("objectidforbubblea"), ObjectId("objectidforbubbleb")]
}
```

### Users collection

```json
{
  "bubbleA": {
    "_id": "ObjectId(objectidforbubblea)",
    "name": "bubbleA",
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
  "bubbleB": {
    "_id": "ObjectId(objectidforbubbleb)",
    "name": "bubbleB",
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
  "bubbleA": {
    "_id": "ObjectId(objectidforbubblea)",
    "name": "bubbleA",
    "applications": [
      {
        "_id": "ObjectId(app_id_1)",
        "name": "App 1",
        "version": "1.0",
        "default_access": "users of bubblea"
      },
      {
        "_id": "ObjectId(app_id_2)",
        "name": "App 2",
        "version": "2.0"
      }
    ]
  },
  "bubbleB": {
    "_id": "ObjectId(objectidforbubbleb)",
    "name": "bubbleB",
    "applications": []
  }
}
```

## Credits

Authly is developed by wavy42 & Arteii.

We appreciate the contributions of all our collaborators and supporters.

the frontend beta is available here:  
[AuthlyFrontend](https://github.com/Arteiii/AuthlyFrontend)

## License

Authly is licensed under the Affero General Public License v3.0 (AGPLv3). See the [LICENSE](LICENSE) file for details.
