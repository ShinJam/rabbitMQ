# rabbitMQ
Practice Chat application with rabbitMQ

## Prerequisites

- Django
- Vue
- pyenv
- uWSGI

## Libraries

*Python:*

- show list

*JavaScript:*

- show list
    - Vue.js
    - vue-cli
    - vue-router

## Virtual Environment

```bash
$ pyenv virtualenv 3.7.5 rabbit-env
$ pyenv local rabbit-env
```

## Installation

*uWSGI:*

OS X El Capitan부터 OpenSSL이 애플의 SDK에서 제외됐기 때문에 homebrew를 통해 설치하고 설정 해주어야 한다. 

```bash
$ brew update && brew upgrade && brew cleanup
$ brew install openssl

$ CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" UWSGI_PROFILE_OVERRIDE=ssl=true pip install uwsgi -Iv --no-cache-dir
```

*Python:*

```bash
# make rabbit-backend directory
$ mkdir rabbit-backend

# Start a Project called rabbitMQ
$ django-admin startproject config ./rabbit-backend

# Install DRF
$ pip install djangorestframework
```

*Vue.js:*

`vue-cli`를 사용해 빠르게 Vue 앱을 만든다.

```bash
# Install 'vue-cli' from npm
$ npm install -g vue-cli

# Scaffold a new project based on the webpack
$ vue init webpack rabbitMQ-frontend
```

## Running the Code

*Python:*

```bash
# Install requirements from pip
$ pip install -r requirements.txt

# Run server(localhost:8000)
$ python manage.py runserver
```

*Vue.js:*

```bash
# Change directory to frontend project
$ cd rabbitMQ-frontend

# Install packages from npm
$ npm install

# Run webpack dev server(locaohost:8080)
$ npm run dev
```

*RabbitMQ:*

```bash
# Run docker RabbitMQ Image
$ docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

*WebSocket Server:*

```bash
# Run uWSGI(localhost:8081) with websocket and gevent
$ uwsgi --http :8081 --gevent 100 --module websocket --gevent-monkey-patch --master
```