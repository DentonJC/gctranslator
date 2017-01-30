import os
import unittest
 
import PIL
from PIL import Image
 
from gctranslator import Dictionaries, ImageRecognition
 
def_input_address = 'tests/test.png'
def_examples_path = os.getcwd() + '/tests/examples/'
def_empty_threshold = 65
def_lines_threshold = 20

pil_img = PIL.Image.Image

input_values = {'input_address': def_input_address,
                'examples_path': def_examples_path,
                'empty_threshold': def_empty_threshold,
                'empty_lines_threshold': def_lines_threshold}
 
class TestDictionaries(unittest.TestCase):
    def test_Dictionaries_init(self):
        dictionaries = Dictionaries(def_examples_path)
        self.assertIsInstance(dictionaries.dictionaries, dict)
 
class TestImageRecognition(unittest.TestCase): 
    def test_ImageRecognition_init(self):
        image = ImageRecognition(**input_values)
        self.assertIsInstance(image.bin_img, pil_img)
 
class TestMain(unittest.TestCase):
    def test_main(self):
        dictionaries = Dictionaries(input_values['examples_path'])
        image = ImageRecognition(**input_values)
        self.assertEqual(image.get_result(dictionaries),'test')

class TestImageRecognitionFalse(unittest.TestCase): 
    def test_ImageRecognitionFalse_init(self):
        input_values = {'input_address': '/definitely_incorrect_address',
                        'examples_path': def_examples_path,
                        'empty_threshold': def_empty_threshold,
                        'empty_lines_threshold': def_lines_threshold}

        image = ImageRecognition(**input_values)
        self.assertNotIsInstance(image.bin_img, pil_img)


if __name__ == '__main__':
    unittest.main()
