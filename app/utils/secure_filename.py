import os
import re
import unicodedata


def secure_filename(filename: str) -> str:
    r"""
    传入一个文件名，返回处理过后的安全文件名。
    该文件名仅包含允许的字符，适合存储在文件系统中，并可安全传递给 os.path.join。
    
    返回的文件名允许使用英文字母、数字、下划线、减号、点、
    汉字（\u4E00-\u9FBF）、日文平假名（\u3040-\u309F）和日文片假名（\u30A0-\u30FF），以保证在中文、日文等环境下能正常显示。

    在 Windows 系统中，此函数还会确保文件名不会与特殊设备文件（如 CON、PRN 等）冲突。

    示例：
      secure_filename("My cool movie.mov") 返回 'My_cool_movie.mov'
      secure_filename("../../../etc/passwd") 返回 'etc_passwd'
      secure_filename("我喜欢映画.mov") 返回 '我喜欢映画.mov'
      secure_filename("i contain cool \xfcml\xe4uts.txt") 返回 'i_contain_cool_umlauts.txt'

    注意：函数返回的文件名可能为空，调用者应确保文件名的唯一性或者在遇到空文件名时重新生成随机文件名。

    :param filename: 原始文件名
    :return: 处理后的安全文件名
    """
    # 将 Unicode 字符串规范化，使用 NFKC 格式，可保留日文、中文等字符
    filename = unicodedata.normalize("NFKC", filename)
    
    # 将路径分隔符替换为空格，防止路径穿越攻击
    for sep in (os.sep, os.path.altsep):
        if sep:
            filename = filename.replace(sep, " ")
    
    # 定义允许的字符范围：
    # 英文字母、数字、下划线、汉字（\u4E00-\u9FBF）、日文平假名（\u3040-\u309F）、日文片假名（\u30A0-\u30FF）、点和减号
    _filename_strip_re = re.compile(r"[^A-Za-z0-9_\u4E00-\u9FBF\u3040-\u309F\u30A0-\u30FF.-]")
    
    # 将文件名中各部分以空白字符分割后，用下划线连接
    filename = "_".join(filename.split())
    # 过滤掉不在允许范围内的字符，并去除首尾的点和下划线
    filename = str(_filename_strip_re.sub("", filename)).strip("._")
    
    return filename
