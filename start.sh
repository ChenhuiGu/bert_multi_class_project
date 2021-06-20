#!/usr/bin/env bash
gunicorn -w 2 -b 0.0.0.0:80 -D --access-logfile ./log/server.log run_server:app