#!/usr/bin/python3
""" Compress before sending """


from fabric.api import *
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory web_static"""

    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None
