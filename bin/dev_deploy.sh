#!/bin/bash

CONTAINER="mediark"
USER="mediark"
PROJECT_PATH=/mnt/Workspace/dev/github.com/knowark/mediark
POSTGRES_CONF_DIR="/etc/postgresql/10/main"
POSTGRES_CONF=$POSTGRES_CONF_DIR/postgresql.conf
POSTGRES_PG_HBA=$POSTGRES_CONF_DIR/pg_hba.conf

echo "Deploying development LXD container..."

lxc launch ubuntu:bionic $CONTAINER
lxc config device add $CONTAINER workspace disk \
source=$HOME/Workspace path=/mnt/Workspace

echo "Creating home directory..."

lxc exec $CONTAINER -- adduser $USER --home /opt/$USER \
--disabled-password --gecos ""

echo "Install Postgresql database and system dependencies..."

sleep 5  # Wait for container network connectivity.
lxc exec $CONTAINER -- apt update -y
lxc exec $CONTAINER -- apt install postgresql postgresql-server-dev-all -y
lxc exec $CONTAINER -- apt install libpq-dev -y
lxc exec $CONTAINER -- apt install build-essential python3.6-dev -y
lxc exec $CONTAINER -- apt install python3-wheel -y
lxc exec $CONTAINER -- apt autoremove -y

echo "Create database with its user..."

lxc exec $CONTAINER -- su - postgres -c \
"psql -c \"CREATE USER mediark WITH SUPERUSER PASSWORD 'mediark'\""

lxc exec $CONTAINER -- su - postgres -c \
"psql -c \"CREATE DATABASE mediark WITH OWNER mediark\""

echo "Install virtualenv..."

lxc exec $CONTAINER -- apt install python3-venv -y
lxc exec $CONTAINER -- su - $USER -c "python3 -m pip install -U pip wheel"
lxc exec $CONTAINER -- su - $USER -c "python3 -m venv /opt/mediark/env"

echo "Link project to home..."

lxc exec $CONTAINER -- ln -s $PROJECT_PATH /opt/$USER/mediark

echo "Install virtualenv dependencies..."

lxc exec $CONTAINER -- su - $USER -c "/opt/mediark/env/bin/python -m pip \
install -U pip wheel"
lxc exec $CONTAINER -- su - $USER -c "/opt/mediark/env/bin/python -m pip \
install -r /opt/mediark/mediark/requirements.txt"

echo "Open PostgreSQL port..."

lxc exec $CONTAINER -- sh -c "cp $POSTGRES_CONF $POSTGRES_CONF.bkp"
lxc exec $CONTAINER -- sh -c "cp $POSTGRES_PG_HBA $POSTGRES_PG_HBA.bkp"

OLD="#listen_addresses = 'localhost"
NEW="listen_addresses = '*"

lxc exec $CONTAINER -- sed -i "s/${OLD}/${NEW}/g" $POSTGRES_CONF

OLD="host    all             all             127.0.0.1\/32            md5"
NEW="host    all             all             0.0.0.0\/0               md5"

lxc exec $CONTAINER -- sed -i "s/${OLD}/${NEW}/g" $POSTGRES_PG_HBA

OLD="host    all             all             ::1\/128                 md5"
NEW="host    all             all             ::\/0                    md5"

lxc exec $CONTAINER -- sed -i "s/${OLD}/${NEW}/g" $POSTGRES_PG_HBA

echo "Restarting PostgreSQL..."

lxc exec $CONTAINER -- service postgresql restart
