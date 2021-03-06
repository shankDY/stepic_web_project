#!bin/bash
#

sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

# Updating components for course
sudo apt-get update
sudo apt-get install -y python3.5
sudo apt-get install -y python3.5-dev
sudo unlink /usr/bin/python3
sudo ln -s /usr/bin/python3.5 /usr/bin/python3
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade django==2.1
sudo pip3 install --upgrade gunicorn
sudo apt-get install libssl-dev
sudo apt-get install libmysqlclient-dev
sudo pip3 install mysqlclient

# db
sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE djtest;"
mysql -uroot -e "FLUSH PRIVILEGES;"

#create migration
cd ask
python3 manage.py makemigrations qa
python3 manage.py migrate