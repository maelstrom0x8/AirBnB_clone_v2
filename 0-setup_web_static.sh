#!/usr/bin/env bash
# Sets stage for web_static deployment

sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo echo "<html>
  <head>
  </head>
  <body>
	Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
sudo sed -i '53i \\tlocation \/hbnb_static {\n\t\t alias /data/web_static/current;\n\t}' /etc/nginx/sites-available/default
/etc/init.d/nginx restart
