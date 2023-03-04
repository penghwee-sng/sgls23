#!/bin/bash

while true; do
  mysql -u root log_test --execute="SELECT * FROM logs" | tr '\t' ',' > /var/log/mysql-exported-new
  comm -1 -3 /var/log/mysql-exported /var/log/mysql-exported-new >> /var/log/mysql-exported
  sleep 5;
done
