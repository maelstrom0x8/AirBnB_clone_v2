#!/usr/bin/python3

"""
1-pack_web_static.py

This module provides functionality to create a compressed archive of the
web_static folder using Fabric.

Usage:
    $ fab -f 1-pack_web_static.cpy do_pack

Dependencies:
    - Fabric
    - Python 3
    - tar command-line tool
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a compressed archive of the web_static folder and saves
    it in the versions directory.
    The archive filename includes a timestamp to make it unique.

    Returns:
        str: The path to the created archive, or None if the
        archive creation fails.
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    tarball_dir = "versions/web_static_{}.tgz".format(date)
    tarball = local("tar -cvzf {} web_static".format(tarball_dir))

    return tarball_dir if tarball.succeeded else None
