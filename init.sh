mysql -uroot -proot -e "create database YulaGroupDB;"
mysql -uroot -proot -e "create user 'YulaGroup'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YulaGroup';"
mysql -uroot -proot -e "grant all on YulaGroupDB.* to 'YulaGroup'@'localhost';"
sudo ln -s ~/Yula-Group-Task/etc/nginx_server.conf /etc/nginx/sites-enabled/YulaGroup.conf