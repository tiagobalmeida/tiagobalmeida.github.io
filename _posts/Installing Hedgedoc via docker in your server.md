# Installing Hedgedoc via docker in your server

Hedgedoc (formerly know as CodiMD) is a great way to keep your own notes.

## Create a hedgedoc user

`adduser hedgedoc`

## Install packages

Make sure you have docker and docker-compose installed before proceeding.

## Switch to the hedgedoc user

`sudo su hedgedoc`

## Clone hedgedoc

```
git clone https://github.com/hedgedoc/container.git hedgedoc-container
cd hedgedoc-container
```

## Change the default configuration

```
nano docker-compose.yml
```

Add the following to the `environment` section:

```
 environment:
      # DB_URL is formatted like: <databasetype>://<username>:<password>@<hostname>:<port>/<database>
      # Other examples are:
      # - mysql://hedgedoc:password@database:3306/hedgedoc
      # - sqlite:///data/sqlite.db (NOT RECOMMENDED)
      # - For details see the official sequelize docs: http://docs.sequelizejs.com/en/v3/
      - CMD_DOMAIN=192.168.1.x
      - CMD_URL_ADDPORT=true
      - CMD_DB_URL=...
      - CMD_EMAIL=true
      - CMD_IMAGE_UPLOAD_TYPE=filesystem
    volumes:
      - uploads:/he
```

## Enable docker service

```
systemctl enable docker
```

## Start hedgedoc

```
docker-compose up
```

If the above eventually succeeds you'll see `listening on port 3000`. 
In that case, run it in the background:

```
docker-compose up -d
```
