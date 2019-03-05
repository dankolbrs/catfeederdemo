import argparse
import sys
import time

from catfeeder import CatFeeder


def get_args():
    parser = argparse.ArgumentParser(description='Feed the cats')
    parser.add_argument('--runtime', type=float, default=1.65, help='Run time in seconds')
    parser.add_argument('--gpiopin', type=int, default=18, help='GPIO pin')
    parser.add_argument('--db', type=str, default='feeder.db', help='Database name')
    parser.add_argument('--user', type=str, default='script', help='User feeding cats')
    return parser.parse_args()


def main():
    args = get_args()
    feeder = CatFeeder(run_time=args.runtime,
                       gpio_pin=args.gpiopin,
                       db=args.db)

    # One hour ago in seconds
    ONE_HOUR = 60 * 60
    last_threshold = int(time.time()) - ONE_HOUR
    if feeder.get_last_feeding() > last_threshold:
        sys.stderr.write("Error: Fed within the last hour")
        exit(1)
    else:
        feeder.feed_cats(args.user)
        sys.stdout.write("Cats fed {}".format(time.strftime('%d %b %Y %I:%M:%S %P',
                                                            time.localtime())))

if __name__ == '__main__':
    main()
