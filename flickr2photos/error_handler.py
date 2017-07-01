import time


def handle(cmd, retries=0, max_retries=0, **kwargs):
    try:
        return cmd(**kwargs)
    except Exception as e:
        print(e)
        if retries > 5:
            time.sleep(5)
        if retries > 50:
            print(cmd, kwargs)
            time.sleep(120)

        if max_retries > 0 and retries > max_retries:
            raise
        else:
            print("Retrying (%s)..." % retries)
            return handle(cmd, retries=retries+1, **kwargs)


def try_again(string):
    response = input("An error occurred. Do you want to try again? (y/n)")
    if response in ['y', 'n']:
        return True if response == 'y' else False
    else:
        return get_input(string)
