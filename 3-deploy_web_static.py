#!/usr/bin/python3

"""
3-deploy_web_static.py

This module provides functionality to create and distribute a compressed
archive of the web_static folder to a remote server using Fabric.

Usage:
    $ fab -f 3-deploy_web_static.py deploy

Dependencies:
    - Fabric
    - Python 3
    - tar command-line tool
    - sudo privileges on the remote server

Note:
    - Ensure that the Fabric environment variable 'env.hosts' is set
    appropriately before running the script.
    - The 'do_pack' and 'do_deploy' functions from the
    '2-do_deploy_web_static.py' module must be defined and executed
    successfully before using 'deploy'.
"""

import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["100.25.160.191", "52.91.178.10"]

def do_pack():
    """
    Creates a compressed archive of the web_static folder and saves
    it in the versions directory.
    The archive filename includes a timestamp to make it unique.

    Returns:
        str: The path to the created archive, or None if the archive
        creation fails.
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    tarball_dir = "versions/web_static_{}.tgz".format(date)
    tarball = local("tar -cvzf {} web_static".format(tarball_dir))

    return tarball_dir if tarball.succeeded else None


def do_deploy(archive_path):
    """
    Deploys a compressed archive of the web_static folder to a remote server.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """
    Wrapper function to execute the 'do_pack' and 'do_deploy' functions.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
