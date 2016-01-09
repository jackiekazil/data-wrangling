import os

def get_latest(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]
