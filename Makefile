#!/usr/bin/make
SHELL = /bin/bash

dbup:
	docker compose up

app_up:
	poetry run python ./botworld/botworld_api/src/app.py
