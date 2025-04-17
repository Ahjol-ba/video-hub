import subprocess
import random
from . import get_video_duration

def thumbnail_generator(video_path, thumbn_path, custom_time=None):
    """
    通过 ffmpeg 从视频中生成截屏
    :param video_path: 视频文件存储路径
    :param video_path: 截屏图片存储路径
    :param custom_time: 自定义截取时间（秒），若未提供则随机取一个时间
    :return: 截屏成功返回 True, 若失败返回 False
    """
    
    duration = get_video_duration(video_path)
    if duration is None:
        return False
    
    # 如果未提供自定义时间，则随机选择一个截取时间
    if custom_time is None:
        if duration > 2:
            t = random.uniform(1, duration - 1)
        else:
            t = duration / 2
    else:
        t = max(0, min(custom_time, duration))
    
    # 使用 ffmpeg 命令截取单帧图片
    command = [
        'ffmpeg',
        '-ss', str(t),
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',  # 图片质量参数，可调整
        '-y',  # 若文件已存在则覆盖
        thumbn_path
    ]
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception as e:
        return False