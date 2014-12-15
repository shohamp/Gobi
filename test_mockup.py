from fabric.api import put

from gobi import remote_os
from gobi import gobi_test
from gobi.net.ifconfig import get_interfaces, get_ip


@gobi_test
def test_my_first():
    remote_os.path.isdir("~")
    interfaces = get_interfaces()
    print get_ip(interfaces[0])


@gobi_test
def test_with_file_upload():
    put("/home/shoham/Vagrantfile", "/tmp")
    assert False, "shohamp"
