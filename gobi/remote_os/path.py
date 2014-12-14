from gobi.internal import is_cmd_succeeded, is_condition_true


def exists(path):
    return is_cmd_succeeded("ls %s" % path)


def isfile(path):
    return is_condition_true("-f %s" % path)


def isdir(path):
    return is_condition_true("-d %s" % path)


def islink(path):
    return is_condition_true("-h %s" % path)