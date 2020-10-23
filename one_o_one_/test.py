import unittest
from extraction import send_r,process_level_1, save_file, process_data
from loader import read_data,combien_dict, mapper_p, clean_data
import os
class TestAll(unittest.TestCase):
    
    def test_send(self):
        url = 'https://www.meilleursagents.com/'
        self.assertEqual(send_r(url).status_code, 200)


    def setUp(self):
        self.f = open('mock.sourcecode', 'r')
        self.data =self.f.read()


    def test_parser_l1(self):
        parsed_data = process_level_1(self.data.split("###########################//")[0])
        for dict_ in parsed_data:
            for k in dict_:
                self.assertIsNotNone(dict_[k])

    def test_parser_l2(self):
        parsed_data = process_data(eval(self.data.split("###########################//")[1]))
        
        for dict_ in parsed_data:
            for k in dict_:
                self.assertIsNotNone(dict_[k])

    def tearDown(self):
        self.f.close()

    
    def test_save_data(self):
        save_file('test one', 'test_res.txt')
        with open('test_res.txt', 'r') as f:
            self.assertIn('test one',f.read())
        
        os.remove("test_res.txt")





if __name__ == '__main__':
    unittest.main()

