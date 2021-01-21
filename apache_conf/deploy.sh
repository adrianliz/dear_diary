#!/bin/bash

echo -e "Stopping apache2 service...\n"
sudo service apache2 stop

if [ $? -eq 0 ]; then
	echo -e "\nService apache2 stopped\n"
else
	echo -e "\nCan't stop apache2 service\n"
	exit 1
fi

echo -e "\nRemoving last version of Dear Diary...\n"
cd /home/alumno/django
sudo rm -rf dear_diary/

if [ $? -eq 0 ]; then
	echo -e "\nLast version of Dear Diary removed\n"
else
	echo -e "\nCan't remove Dear Diary directory\n"
	exit 1
fi

echo -e "\nClonning git repo...\n"
git clone git@github.com:adrianliz/dear_diary.git
echo -e "\nDone\n"

cd dear_diary
cp /home/alumno/Escritorio/dear_diary_envs/.env ./dear_diary

echo -e "\nCopying static files...\n"
conda activate djangoEnv
python manage.py collectstatic

if [ $? -eq 0 ]; then
	echo -e "\nStatic files copied\n"
else
	echo -e "\nCan't copy static files\n"
	exit 1
fi

echo -e "\nMaking migrations...\n"
python manage.py migrate

if [ $? -eq 0 ]; then
	echo -e "\nMigrations done\n"
else
	echo -e "\nCan't do migrations\n"
	exit 1
fi

echo -e "\nRestarting apache2...\n"
sudo service apache2 restart

if [ $? -eq 0 ]; then
	echo -e "\nDear Diary deployed\n"
else
	echo -e "\nCan't restart apache2 service\n"
	exit 1
fi