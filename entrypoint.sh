#!/bin/sh
set -e

supervisord -c /crg/supervisord.conf

exec nginx -c /crg/nginx.conf -g "daemon off;"
