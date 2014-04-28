#!/bin/bash
set -x
source /var/bot/init.sh
/var/bot/botenv/bin/python /var/bot/bot.py
CODE=$?
if [ $CODE -ne '0' ]; then
  echo 'RESULT=failed'
else
  echo 'RESULT=success'
fi
echo "CODE=$CODE"
exit $CODE
