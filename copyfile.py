# 拷贝文件
def copy_file(sourceFile: '原文件', targetFile: '目标文件') -> int:
    if not sourceFile:
        return 0
    if sourceFile == targetFile:
        return 0
    if os.path.exists(targetFile):
        return 0
    with open(sourceFile, 'rb') as s:
        with open(targetFile, 'wb') as fd:
            record_size = 1024
            records = iter(partial(s.read, record_size), b'')
            for data in records:
                fd.write(data)
        fd.close()
    s.close()
    return 0
