import unittest
import time

from unittest import mock, TestCase
from unittest.mock import MagicMock

from catfeeder import CatFeeder


class TestCatFeeder(TestCase):
    def setUp(self):
        self.rpi_gpio_patcher = mock.patch('catfeeder.catfeeder.GPIO')
        self.mocked_rpi = self.rpi_gpio_patcher.start()
        self.mocked_rpi.GPIO = MagicMock()

        self.mocked_gpio_enabled_patcher = mock.patch('catfeeder.catfeeder.GPIO_ENABLED', True)
        self.mocked_gpio_enabled = self.mocked_gpio_enabled_patcher.start()

    def tearDown(self):
        self.rpi_gpio_patcher.stop()
        self.mocked_gpio_enabled_patcher.stop()

    def test_catfeeder_initialized(self):
        """
        Assert object created
        """
        test_feeder = CatFeeder()
        test_feeder._GPIO_ENABLED = True
        self.assertIsInstance(test_feeder, CatFeeder)

    def test_catfeeder_called(self):
        """
        Ensure PWM called to start feeding
        """
        test_feeder = CatFeeder()
        test_feeder.feed_cats()
        self.assertTrue(self.mocked_rpi.PWM.called)

    def test_catfeeder_parameters_used(self):
        """
        Ensure PWM called to start feeding
        """
        test_feeder = CatFeeder(run_time=1.5, gpio_pin=12, db='testing.db')
        test_feeder._GPIO_ENABLED = True
        pre_time = time.time()
        test_feeder.feed_cats()
        end_time = time.time()
        run_time = end_time - pre_time
        self.assertEqual("{:1.1f}".format(run_time), '1.5')
        self.mocked_rpi.PWM.assert_called_with(12, 50)

    def test_catfeeder_last_feeding_time(self):
        """
        Ensure PWM called to start feeding
        """
        self.mocked_rpi.GPIO = MagicMock()
        test_feeder = CatFeeder(db='testing.db')
        test_feeder.feed_cats()
        # self.mocked_rpi.PWM.assert_called() requires 3.6
        self.assertTrue(self.mocked_rpi.PWM.called)

    def test_catfeeder_get_last_feeding_time(self):
        """
        Ensure PWM called to start feeding
        """
        self.mocked_rpi = MagicMock()
        test_feeder = CatFeeder(db='testing.db')
        cur_time = int(time.time())
        test_feeder.feed_cats()
        # three second threshold
        feed_time = test_feeder.get_last_feeding()
        time_difference = feed_time - cur_time
        self.assertLess(abs(time_difference), 3)


if __name__ == '__main__':
    unittest.main()
