#
# -- Create Subversion Rep:
# $ fab -a -f op -u jcruz -p mypwd svn svnsetup:userpwd="msilva=xpto|ckosta=kpto"
#
# -- Setup on test server
# fab -f op -u jcruz -p mypwd test setup:revision=2
#
# -- Deploy on test server
# fab -f op -u jcruz -p mypwd test deploy:revision=56
#
# -- Copy a single file to server
# fab -f op -u jcruz -p mypwd test copy:fname=/dir1/dir2/file.txt
#
# -- Setup on production server
# fab -f op -u jcruz -p mypwd test setup:revision=2
#
# -- Deploy on production server
# fab -f op -i /home/user/.pemdir/xpto.pem -u ubuntu prod deploy:revision=56
#
#

import sys

from cspfab import *

if __name__ == "__main__":
    helper()
    quit()

#
# local project-wise definitions
#
env.prj = "cnp_news"
env.svn_rep = "svn://cnpswvs02/%s/%s_trunk" %(env.prj, env.prj)

#
# local framework-wise definitons
#
home = os.getenv('HOME')
env.local_dir = "%s/tmp/deploys" %home

#
# remote framework-wise definitons
#
env.remote_www = "/var/www"
env.remote_data = "/var/data"
env.remote_uploads = "/var/data/%s_uploads" %env.prj

env.remote_svn="/home/svn"


def prod():
    env.remote_dir = "/home/ubuntu/temp"
    env.hosts = ['176.34.253.84']

def test():
    env.remote_dir = "/home/jcruz/temp"
    env.hosts = ['cnpswvs01']

def svn():
    env.hosts = ['cnpswvs02']
