#!/bin/bash
#Get servers list
set -f
string=$PRODUCTION_SERVER
array=(${string//,/ })
#Iterate servers for deploy and pull last commit
for i in "${!array[@]}";
do    
    echo "Production Deployment Started on server ${array[i]}"   
    ssh -T git@gitlab.com
    ssh -o StrictHostKeyChecking=no ubuntu@${array[i]} "sudo mkdir -p /var/www/hag && sudo chmod -R 777 /var/www/hag && cd /var/www/hag && git init && git remote set-url origin git@gitlab.com:osanim/hag.git && git commit --allow-empty -m "Initialization" && git fetch git@gitlab.com:osanim/hag.git && git checkout && git stash && git pull git@gitlab.com:osanim/hag.git --allow-unrelated-histories && source /var/www/hag/hagenv/bin/activate && pip install -r /var/www/hag/requirements.txt && python manage.py migrate && sudo systemctl restart nginx && sudo systemctl restart gunicorn"
    echo "Production Deployment Completed"  
done

