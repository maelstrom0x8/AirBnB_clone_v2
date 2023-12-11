package { 'nginx':
  ensure   => 'installed',
  provider => 'apt'
}
-> file { '/data':
  ensure  => 'directory'
}
-> file { ['/data/web_static', '/data/web_static/releases', '/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory'
}
-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
  <head>
  </head>
  <body>
        Holberton School
  </body>
</html>
'
}
-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}
-> exec { 'chown -R ubuntu:ubuntu /data/':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
}
-> file { '/var/www':
  ensure => 'directory'
}
-> file { '/var/www/html':
  ensure => 'directory'
}
-> file { ['/var/www/html/index.html', '/var/www/html/404.html']:
  ensure  => 'file',
  content => ["Holberton School Nginx\n", "This is not a page\n"]
}
-> file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_conf
}
-> exec { 'nginx restart':
  command     => '/etc/init.d/nginx restart',
  refreshonly => true,
}
