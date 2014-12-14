from glob import glob
import subprocess

import vagrant
from fabric.api import execute, env, quiet
from fabric.state import connections

from logger import init_logger, debug, info


VM_NAME = "default"


def clear_fabric_cache():
    """
    Fabric caches it's connections, so it won't have to re-connect every time you use it.
    But, when working with VMs whose connections are getting reset, we can't use a cache.
    Use this function to reset fabric's cache
    """
    connection_keys = connections.keys()
    for host_string in connection_keys:
        connections[host_string].close()
        del connections[host_string]


def get_all_test_functions():
    """
    Get all the tests from the current directory
    Looking for python files starting with "test", and within, functions that start with "test"
    """
    test_files = glob("test*.py")
    test_modules = [__import__(module_name[:-3]) for module_name in test_files]

    test_tasks = []
    for test_module in test_modules:
        functions_in_module = dir(test_module)
        test_functions = [func for func in functions_in_module if func.startswith("test")]
        for test_function in test_functions:
            test_tasks.append(test_module.__dict__[test_function])

    return test_tasks


def vagrant_run_command(command):
    """
    Run the given command in a shell, after preceding it with "vagrant"
    """
    subprocess.call("vagrant " + command, shell=True, stdout=subprocess.PIPE)


def vagrant_take_snapshot():
    """
    Take a snapshot from the running machine, and name it "snapshot"
    """
    vagrant_run_command("snapshot take snapshot")


def vagrant_revert_to_snapshot():
    """
    In the running machine, revert to the last snapshot
    """
    vagrant_run_command("snapshot back")


def init_fabric(vclient):
    """
    init all the required environment for fabric
    """
    env.host_string = vclient.user_hostname_port(vm_name=VM_NAME)
    env.key_filename = vclient.keyfile(vm_name=VM_NAME)
    env.disable_known_hosts = True
    env.quiet = True
    env.warn_only = True


def main():
    """
    Gobi's main function.
    Finds the test functions, runs the machine, connects to them, and runs the tests
    """
    init_logger()
    info("Welcome to gobi. Sit back and relax :)")
    vclient = vagrant.Vagrant()

    test_funcs = get_all_test_functions()
    assert test_funcs > 0, "No tests found. What do you want me to run?"

    info("Found %d tests to run" % len(test_funcs))

    info("Setting up the environment...")
    vclient.up()
    info("Environment is up and ready")
    debug("Taking snapshot...")
    vagrant_take_snapshot()
    debug("Snapshot taken")

    init_fabric(vclient)

    counter = 1

    for task in test_funcs:
        # After the first test, clean - delete cache and revert to snapshot
        if counter != 1:
            clear_fabric_cache()
            debug("Reverting to snapshot...")
            vagrant_revert_to_snapshot()
            debug("Reverted!")

        info("Running test number %d - %s" % (counter, task.__name__))
        execute(task)

        counter += 1

    info("All tests finished")
    info("Destroying environment...")
    vclient.destroy()
    info("Environment has been destroyed...")

    info("Gobi, out")

if __name__ == "__main__":
    main()