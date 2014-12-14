from fabric.api import put

from gobi import test
from gobi import remote_os
from gobi.net.ifconfig import get_interfaces, get_ip


@test
def test_my_first():
    remote_os.path.isdir("~")
    interfaces = get_interfaces()
    print get_ip(interfaces[0])


@test
def test_with_file_upload():
    put("/home/shoham/Vagrantfile", "/tmp")
