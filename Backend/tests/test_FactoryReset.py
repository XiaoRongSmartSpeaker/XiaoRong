import FactoryReset
import configparser
import filecmp
import unittest

config = configparser.ConfigParser()

class TestFactoryReset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.factory_reset_object = FactoryReset.FactoryReset()

    def test_restore_config(self):
        # set up config.ini content
        config['TestSection'] = {}
        config['TestSection']['test_id'] = "2"
        config['TestSection']['test_context'] = "This message has been modified"
        with open('config.ini', 'w') as file:
            config.write(file)

        # test if _restore_config works
        self.factory_reset_object._restore_config()
        self.assertEqual(filecmp.cmp('default/default_config.ini', 'config.ini'), True)

if __name__ == "__main__":
    unittest.main()