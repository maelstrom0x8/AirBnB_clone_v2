#!/usr/bin/python3

"""
100-clean_web_static.py

This script provides functionality to clean up outdated archives and releases
of the web_static folder on both the local and remote servers.

Usage:
    $ fab -f 100-clean_web_static.py do_clean:number=<number>

Arguments:
    number (int, optional): The number of versions to keep (default is 1).

Dependencies:
    - Fabric
    - Python 3

Note:
    - Ensure that the Fabric environment variable 'env.hosts' is set
    appropriately before running the script.
"""

import os
from fabric.api import *

env.hosts = ["100.25.160.191", "52.91.178.10"]


def do_clean(number=0):
    """
    Cleans up outdated archives and releases of the web_static folder on
    both the local and remote servers.

    Args:
        number (int, optional): The number of versions to keep (default is 1).

    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    for _ in range(number):
        archives.pop()

    with lcd("versions"):
        for a in archives:
            local("rm ./{}".format(a))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        for _ in range(number):
            archives.pop()
        for a in archives:
            run("rm -rf ./{}".format(a))
