import psutil
import re
import os
import shutil


def get_first_removable_device() -> (str or None):

    ''' 获取可移动磁盘盘符

        Description:
            获取可移动磁盘（U盘或SD卡等）的盘符。

        Return:
            - <str | None> 如检测到可移动磁盘，则返回盘符；若未检测到可移动磁盘则返回 None
    '''

    diskparts = psutil.disk_partitions()
    removable_disks = []
    for disk in diskparts:
        if re.match(r'^(.*)?removable(.*)?$', disk.opts):
            removable_disks.append(disk)
    return removable_disks[0].device if len(removable_disks) > 0 else None


def move_video(file_name: str, destination_path: str) -> bool:

    ''' 移动录制文件

        Description:
            从 OBS 录制保存路径移动文件至可移动磁盘。

        Parameters:
            - file_name: str OBS 录制文件绝对路径及文件名
            - destination_path: str 移动目标路径（可移动磁盘的根目录）

        Return:
            - <bool> 移动成功返回 True，失败返回 False
    '''

    if os.path.exists(file_name):
        new_path = shutil.move(file_name, destination_path)
        return os.path.exists(new_path)
    else:
        return False
