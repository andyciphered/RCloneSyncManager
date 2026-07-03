import shutil


def check_rclone():

    return shutil.which("rclone") is not None