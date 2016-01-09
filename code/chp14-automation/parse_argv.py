from import_config import get_config
import sys


def main(env):
    config = get_config(env)
    print config


if __name__ == '__main__':
    if len(sys.argv) > 1:
        env = sys.argv(1)
    else:
        env = 'TEST'
    main(env)
