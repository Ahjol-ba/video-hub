import subprocess
def get_video_duration(video_path):
    """
    Get video's duration with ffprobe.

    :param video_path: 
    :return duration(float): If get duration successfully.
    :return None: If get duration failed.
    """
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries',
             'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        return None


def get_video_resolution(video_path: str):
    """
    Get video's width and height with ffprobe.

    :param video_path:
    :return Label of resolution: 
    """
    # 构造 ffprobe 命令，参数说明：
    # -v error          : 只显示错误信息
    # -select_streams v:0  : 仅选择第一个视频流
    # -show_entries stream=width,height : 仅显示宽度和高度的属性
    # -of csv=s=x:p=0     : 输出格式为 CSV，用 "x" 作为分隔符，无标题
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        video_path
    ]
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        # 期望输出格式形如 "1920x1080"
        if 'x' not in output:
            return None
        parts = output.split('x')
        if len(parts) != 2:
            return None
        width = int(parts[0])
        height = int(parts[1])
        min_edge = min(width,height)
        
        if min_edge > 2160:
            return '4k+'
        elif min_edge > 1080:
            return '1080p'
        elif min_edge > 720:
            return '1080p'
        elif min_edge > 480:
            return '1080p'
        else :
            return '360p'
    except Exception as e:
        return None
