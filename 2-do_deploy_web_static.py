#!/usr/bin/python3
""" Fabfile to distribute an archive to a web server """

from fabric.api import *       # we need to import put, run, env
from datetime import datetime
from os.path import exists

env.hosts = ['100.26.49.247', '54.173.27.192']


def do_deploy(archive_path):
    """ distributes an archive to the web servers """

    if exists(archive_path) is False:
        return False  # Returns False if the file at archive_path doesnt exist
    filename = archive_path.split('/')[-1]
    # filename is <web_static_20230503193956.tgz>
    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")   # Upload archive to /tmp/ in web-server
        run("mkdir -p {}/".format(no_tgz))
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        # Delete the archive from the web server
        run("rm -rf /data/web_static/current")
        # Delete the symbolic link /data/web_static/current from the web server
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        # Create a new the symbolic link /data/web_static/current on the
        # web server, linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        return True
    except Exception:
        return False
