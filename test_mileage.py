import mileage  # fine pep8, i won't put my simple imports on one line! (yes i could turn them off, but it does help)
import sqlite3
import logging
from unittest import TestCase, main
from unittest.mock import patch
logging.basicConfig(level=logging.DEBUG, filename='mileage.log', filemode='w')
logger = logging.getLogger("jack_kerouac")


class TestMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()

    def test_valid_numbers(self):
        # check to verify number strings can have actual numeric values
        # value ranges not checked as that's business logic

        # should all be false:
        self.assertFalse(mileage.validate_number("pizza"))
        self.assertFalse(mileage.validate_number("three"))
        self.assertFalse(mileage.validate_number("1..0"))
        self.assertFalse(mileage.validate_number("1.2.3.5.8.13"))

        # should all be true
        self.assertFalse(mileage.validate_number("1,000.00"))
        self.assertFalse(mileage.validate_number("1,000.01"))
        self.assertTrue(mileage.validate_number("1.0"))
        self.assertTrue(mileage.validate_number("0.1"))
        self.assertTrue(mileage.validate_number("0"))
        self.assertTrue(mileage.validate_number("1"))
        self.assertTrue(mileage.validate_number("-1.5"))
        self.assertTrue(mileage.validate_number("0112358.13"))

    def test_add_new_vehicle(self):
        mileage.add_miles('Blue Car', 100)
        expected = {'Blue Car'.upper(): 100}
        self.compare_db_to_expected(expected)

        mileage.add_miles('Green Car', 50)
        expected['Green Car'.upper()] = 50
        self.compare_db_to_expected(expected)

    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = {'Red Car'.upper(): 100}
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['Red Car'.upper()] = 100 + 50
        self.compare_db_to_expected(expected)

    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.addMiles(None, 100)

    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(Exception):
            mileage.addMiles('Car', -100)
        with self.assertRaises(Exception):
            mileage.addMiles('Car', 'abc')
        with self.assertRaises(Exception):
            mileage.addMiles('Car', '12.def')

    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()


class TestMileageSearch(TestCase):
    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()
        mileage.add_miles('purple car', 50)
        mileage.add_miles('green car', 25)

    def test_search_parms(self):
        logger.debug("test_search_parms")
        entries = str(mileage.search_entries('PURPLE CAR'))
        self.assertIn("PURPLE CAR", entries)
        # assert only one entry as this is a targeted query
        self.assertEqual(len(mileage.search_entries('purple car'.upper())), 1)
        # assert the value entered was stored to the vehicle
        self.assertIn("PURPLE CAR: 50", entries)
        logger.info(mileage.search_entries('PURPLE CAR'))
        expected_data = {
            "PURPLE CAR": 50,
            "GREEN CAR": 25
        }
        self.compare_db_to_expected(expected_data)

        # now searching with bad parameters
        self.assertEqual(mileage.search_entries('pizza'), [])
        self.assertEqual(mileage.search_entries('BLUE CAR'), [])
        self.assertEqual(mileage.search_entries(0), [])
        self.assertEqual(mileage.search_entries("\n"), [])

    def test_search_no_parms(self):
        logger.debug("test_search_no_parms")
        entries = str(mileage.search_entries())
        logger.info(entries)
        expected_data = {
            "PURPLE CAR": 50,
            "GREEN CAR": 25
        }
        self.compare_db_to_expected(expected_data)

    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])
        conn.close()


if __name__ == '__main__':
    main()
