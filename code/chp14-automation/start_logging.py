import logging
from datetime import datetime


def start_logger():
    logging.basicConfig(filename='/var/log/my_script/daily_report_%s.log' %
                        datetime.strftime(datetime.now(), '%m%d%Y_%H%M%S'),
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m-%d %H:%M:%S')


def main():
    start_logger()
    logging.debug("SCRIPT: I'm starting to do things!")

    try:
        20 / 0
    except Exception:
        logging.exception('SCRIPT: We had a problem!')
        logging.error('SCRIPT: Issue with division in the main() function')

    logging.debug('SCRIPT: About to wrap things up!')

if __name__ == '__main__':
    main()
