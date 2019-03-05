import time
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .feeder_objects import FeedTimes, Base

GPIO_ENABLED = False

try:
    import RPi.GPIO as GPIO
    GPIO_ENABLED = True
except RuntimeError:
    # can only be run on RPi
    import RPi as GPIO



class CatFeeder:
    def __init__(self, run_time=1.65, gpio_pin=18, db='feeder.db'):
        self._GPIO_ENABLED = GPIO_ENABLED
        self.run_time = run_time
        self.gpio_pin = gpio_pin
        engine = create_engine('sqlite:///{}'.format(db))
        Base.metadata.create_all(engine)
        self.dbsession = sessionmaker(bind=engine)
        self.session = self.dbsession()

    def _init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.p = GPIO.PWM(self.gpio_pin, 50)

    def feed_cats(self, user=None):
        success = False
        try:
            if self._GPIO_ENABLED:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gpio_pin, GPIO.OUT)
                p=GPIO.PWM(self.gpio_pin, 50)
                p.start(11)
                time.sleep(self.run_time)
                p.stop()
                success = True
        except Exception as e:
            sys.stderr.write("Error in feeding\n {}".format(e))
        finally:
            feeding = FeedTimes(feed_time=int(time.time()),
                                feed_length=self.run_time,
                                user=user,
                                success=success)
            self.session.add(feeding)
            self.session.commit()
            if self._GPIO_ENABLED:
                GPIO.cleanup()

    def get_last_feeding(self):
        last_feeding = self.session.query(FeedTimes). \
            order_by(FeedTimes.feed_time.desc()).limit(1).one()
        return last_feeding.feed_time
