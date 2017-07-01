import os

from tasks.save_photos import process_photo


def start():
    for dirname, subdirs, filenames in os.walk('json_files'):
        print('Queueing: %s' % dirname)
        for filename in filenames:
            process_photo.delay('%s/%s' % (dirname, filename))


if __name__ == "__main__":
    start()
