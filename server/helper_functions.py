import os,shutil

def empty_the_folder(folder_path):
    folder = folder_path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            return 0
    return 1