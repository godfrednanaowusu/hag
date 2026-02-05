#!/bin/bash
#Get servers list
set -f
string=$STAGING_SERVER
array=(${string//,/ })
#Iterate servers for deploy and pull last commit
for i in "${!array[@]}";
do    
    echo "Staging Deployment Started on server ${array[i]}"   
    ssh -T git@gitlab.com
    ssh -o StrictHostKeyChecking=no ubuntu@${array[i]} "sudo mkdir -p /var/www/hag_stage && sudo chmod -R 777 /var/www/hag_stage && cd /var/www/hag_stage && git init && git remote set-url master git@gitlab.com:osanim/hag.git && git commit --allow-empty -m "Initialization" && git fetch git@gitlab.com:osanim/hag.git && git checkout && git stash && git pull git@gitlab.com:osanim/hag.git --allow-unrelated-histories && source /var/www/hag_stage/hagstageenv/bin/activate && pip install -r /var/www/hag_stage/requirements.txt && python manage.py makemigrations && python manage.py migrate && sudo systemctl restart nginx && sudo systemctl restart gunicorn && python manage.py runserver ec2-18-224-134-218.us-east-2.compute.amazonaws.com:9902"
    echo "Staging Deployment Completed"  
done

