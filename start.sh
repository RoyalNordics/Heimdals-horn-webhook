#!/bin/bash
exec uvicorn webhook.main:app --host 0.0.0.0 --port 10000