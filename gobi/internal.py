from fabric.api import run

_SUCCESS = "GOBI-SUCCESS"
_FAILURE = "GOBI-FAILURE"


def _is_return_success(cmd_output):
    """
    After running a command, analyze it's output and look for the success/failure signs
    """
    success_count = cmd_output.count(_SUCCESS)
    failure_count = cmd_output.count(_FAILURE)

    if success_count and failure_count:
        raise Exception("Command both succeeded and failed?!")

    if success_count > 1:
        raise Exception("How many times can you succeed?")
    if failure_count > 1:
        raise Exception("How many times can you fail?")

    if cmd_output.count(_SUCCESS) == 1:
        return True
    if cmd_output.count(_FAILURE) == 1:
        return False

    raise Exception("If one neither succeeded nor failed, did he even do something?")


def is_cmd_succeeded(bash_cmd):
    """
    Run the command given, check it's return value and return whether it succeeded
    """
    cmd_output = run("%s && echo %s || echo %s" % (bash_cmd, _SUCCESS, _FAILURE))
    return _is_return_success(cmd_output)


def is_condition_true(bash_condition):
    """
    Run the conditional argument given on the remote shell, and return whether it's true
    """
    cmd_output = run("if [ %s ] ; then echo %s ; else echo %s ; fi"
                     % (bash_condition, _SUCCESS, _FAILURE))
    return _is_return_success(cmd_output)