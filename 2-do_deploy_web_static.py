#!/usr/bin/python3
"""
2-do_deploy_web_static.py

This module provides functionality to deploy a compressed archive of
the web_static folder to a remote server using Fabric.

Usage:
    $ fab -f 2-do_deploy_web_static.py do_deploy:archive_path

Dependencies:
    - Fabric
    - Python 3
    - tar command-line tool
    - sudo privileges on the remote server

Note:
    - Ensure that the Fabric environment variables 'env.hosts' and
    'env.user' are set appropriately before running the script.
    - The 'do_pack' function from the '1-pack_web_static.py' module must
    be executed before using 'do_deploy'.
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.25.160.191", "52.91.178.10"]
env.user = "ubuntu"


def do_pack():
    """
    Creates a compressed archive of the web_static folder and saves it
    in the versions directory.
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
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
