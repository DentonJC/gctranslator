import os

import numpy as np
from PIL import Image, ImageDraw

np.seterr(divide='ignore', invalid='ignore')

def_input_address = 'test.png'
def_examples_path = os.getcwd() + '/examples/'
def_empty_threshold = 65
def_lines_threshold = 20


def ui(def_input_address, def_examples_path, 
       def_empty_threshold, def_lines_threshold):  # inputs check
    """
    User interface receives the defaults. The user can define values
    or they will be returned by default.

    """

    input_address = input('Enter the image address (default is ' +
                          def_input_address + ') :')
    if input_address == '':
        input_address = def_input_address

    examples_path = input('Enter the path to folder with samples ' +
                          '(default is ' + def_examples_path + '):')
    if examples_path == '':
        examples_path = def_examples_path

    empty_threshold = input('Enter the distance between letters ' +
                            '(default is ' + str(def_empty_threshold) +
                            ') [px]:')
    if empty_threshold == '':
        empty_threshold = def_empty_threshold

    empty_lines_threshold = input('Enter the distance between lines ' +
                                  '(default is ' +
                                  str(def_lines_threshold) + ') [px]:')
    if empty_lines_threshold == '':
        empty_lines_threshold = def_lines_threshold

    return {'input_address': input_address, 'examples_path': examples_path,
            'empty_threshold': empty_threshold, 
            'empty_lines_threshold': empty_lines_threshold}


class Dictionaries:
    def __init__(self, path_to_dictionaries):
        if (not os.path.exists(path_to_dictionaries) or 
            not os.listdir(path_to_dictionaries)):
            raise ValueError('Error. Dictionaries not found.')

        self.dictionaries = {}

        for dictionary in next(os.walk(path_to_dictionaries))[1]:
            self.dictionaries.update({dictionary: 
                                     self.upload_dictionary(path_to_dictionaries +
                                     dictionary)})

    def upload_dictionary(self, path_to_dictionary):
        dictionary = {}
        if not os.path.exists(path_to_dictionary):
            print('Error. Dictionary not found.')
            return False
        for file in os.listdir(path_to_dictionary):
            try:
                img = ImageRecognition.binarization(path_to_dictionary + '/' + file)
                dictionary.update({file.split('.')[0]: ImageRecognition.naive_cut(img)})
            except Exception as e:
                print(e)
        return dictionary

    @staticmethod
    def ncc(input_image, dictionary_image, width=10):
        """
        Function treat pixels of two images as vectors, normalizes them,
        then takes their dot product.

        """

        wpercent = (width / float(input_image.size[0]))
        height = int((float(input_image.size[1]) * float(wpercent)))
        input_image = input_image.resize((width, height), Image.ANTIALIAS)
        example = dictionary_image.resize((input_image.size[0],
                                           input_image.size[1]),
                                          Image.ANTIALIAS)

        images = [input_image, example]
        vectors = []
        norms = []
        for img in images:
            vector = []
            for pixel in img.getdata():
                vector.append(np.mean(pixel))
            vectors.append(vector)
            norms.append(np.linalg.norm(vector, 2))
        a, b = vectors
        a_norm, b_norm = norms
        res = np.dot(a / a_norm, b / b_norm)
        return res

    def get_symbol(self, input_image):
        result = {'dictionary': None, 'symbol': None, 'weight': 0}
        for name, dictionary in self.dictionaries.items():
            for letter, img in dictionary.items():
                w = Dictionaries.ncc(input_image, img)
                if w > result['weight']:
                    result['dictionary'] = name
                    result['symbol'] = letter
                    result['weight'] = w
        return result


class ImageRecognition:
    def __init__(self, **kwargs):
        for name in ('input_address', 'empty_threshold', 'empty_lines_threshold'):
            value = kwargs.get(name, None)
            if not value:
                raise ValueError('Missing value: {}'.format(name))
        if not isinstance(kwargs.get('empty_threshold'), int):
            raise ValueError('Value empty_threshold must be integer!')
        if not isinstance(kwargs.get('empty_lines_threshold'), int):
            raise ValueError('Value empty_lines_threshold must be integer!')

        self.input_address = kwargs.get('input_address')
        self.empty_threshold = kwargs.get('empty_threshold')
        self.empty_lines_threshold = kwargs.get('empty_lines_threshold')

        self.bin_img = ImageRecognition.binarization(self.input_address)
        self.found_lines = []
        self.found_symbols = []
        self.spaces = []

        self.separation()
        self.delete_trash()
        self.found_symbols = list(map(lambda x: ImageRecognition.naive_cut(x), 
                                      self.found_symbols))

    @staticmethod
    def binarization(img_path, bin_ratio=600):
        """
        The function takes an image and saves a copy in which all pixels
        are only black or white in /binary.

        """

        if not os.path.isfile(img_path):
            print('Error. Input image is not found.')
            return False
        
        # convert to 'RGBA' for .gif opening fix
        input_image = Image.open(img_path).convert('RGBA')
        draw = ImageDraw.Draw(input_image)

        for i in range(input_image.size[0]):
            for j in range(input_image.size[1]):
                r, g, b, a = input_image.getpixel((i, j))
                if a == 0:
                    r, g, b = 0, 0, 0
                if r + g + b > bin_ratio:
                    r, g, b = 255, 255, 255
                else:
                    r, g, b = 0, 0, 0
                draw.point((i, j), (r, g, b))
        del draw
        img = input_image.convert('L')
        #print('Image binarization "{}" successful.'.format(img_path))
        return img

    def separation(self, string_mode=True, threshold=3):
        """
        The function takes the image, cuts it into rows by a horizontal lines
        if the line and previous [empty_lines_threshold] lines contained
        less than [threshold] black pixels in each.
        The resulting images are saved in /found/lines.
        Function cuts the images from /found/lines on the characters by a vertical
        lines if the previous line and [empty_threshold] lines contained less
        than [threshold] black pixels in each.
        The resulting images are saved in /found.

        """

        if not self.bin_img:
            print('Binarization image does not exist. Use binarization() method before.')
            return False

        y0 = 0
        symbolsx = []
        symbolsy = []

        black = 0
        symbol = False
        empty = 0

        if string_mode:
            for y in range(self.bin_img.size[1]):
                for x in range(self.bin_img.size[0]):
                    pix = self.bin_img.getpixel((x, y))
                    if pix < 255:
                        black += 1
                if symbol and black < threshold:
                    empty += 1
                if not symbol and black > threshold:
                    y0 = y
                    symbol = True
                if (symbol and black <= threshold and 
                    empty >= self.empty_lines_threshold):
                    y1 = y
                    symbol = False
                    symbolsy.append((y0, y1))
                    empty = 0
                black = 0

            if not symbolsx:
                symbolsx = [(0, self.bin_img.size[0])]
            if not symbolsy:
                symbolsy = [(0, self.bin_img.size[1])]

            count = 0

            for y in symbolsy:
                for x in symbolsx:
                    if count < 1000:
                        self.found_lines.append(self.bin_img.crop((x[0], y[0], 
                                                                   x[1], y[1])))
                    count += 1

        scount = 0

        try:
            for img in self.found_lines:

                x0 = 0
                symbolsx = []
                symbolsy = []

                black = 0
                symbol = False
                empty = 0

                for x in range(img.size[0]):
                    for y in range(img.size[1]):
                        pix = img.getpixel((x, y))
                        if pix < 255:
                            black += 1
                    if symbol == True and black < threshold:
                        empty += 1
                    if symbol == False and black > threshold:
                        x0 = x
                        symbol = True
                    if (symbol == True and black <= threshold and
                                empty >= int(self.empty_threshold)):
                        x1 = x
                        symbol = False
                        scount += 1
                        symbolsx.append((x0, x1))
                        empty = 0
                    black = 0
                if not symbolsx:
                    symbolsx = [(0, img.size[0])]
                if not symbolsy:
                    symbolsy = [(0, img.size[1])]

                for y in symbolsy:
                    for x in symbolsx:
                        if count < 1000:
                            self.found_symbols.append(img.crop((x[0], y[0], 
                                                                x[1], y[1])))
                        count += 1
                self.spaces.append(scount)
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def naive_cut(img):
        """
        The function cuts the image on all sides by removing rows and columns in which
        no black pixels.

        """
        arr = np.array(img)

        for c in range(4):
            black = 0
            find = False
            img = Image.fromarray(arr)
            for x in range(len(arr[:, 1])):
                if find:
                    break
                for y in range(len(arr[1, :])):
                    if arr[x, y] == 0:
                        black += 1
                if black >= 1:
                    arr = np.delete(arr, np.s_[0:x], axis=0)
                    find = True
                    break
            arr = np.rot90(arr)

        return Image.fromarray(arr)

    def delete_trash(self, delete_threshold=100):
        """
        The function deletes the images from /found if the number
        of black pixels in it less than [delete_threshold].

        """

        for img in self.found_symbols:
            black = 0
            for x in range(img.size[0]):
                for y in range(img.size[1]):
                    pix = img.getpixel((x, y))
                    if pix != 255:
                        black += 1
            if black < delete_threshold:
                self.found_symbols.remove(img)
        return True

    def get_result(self, dictionaries):
        if not isinstance(dictionaries, Dictionaries):
            raise ValueError('Value dictionaries must be Dictionaries instance!')

        result = ''
        for symbol in self.found_symbols:
            s = dictionaries.get_symbol(symbol)
            result += s['symbol']
            print(s)
        result = ''.join([s if i not in self.spaces 
                         else ' '+s for i, s in enumerate(result)])
        return result

    def clean(self):
        self.bin_img = None
        self.found_symbols = []
        self.found_lines = []
        self.spaces = []


if __name__ == '__main__':
    input_values = ui(def_input_address, def_examples_path, 
                      def_empty_threshold, def_lines_threshold)
    dictionaries = Dictionaries(input_values['examples_path'])
    image = ImageRecognition(**input_values)
    print(image.get_result(dictionaries))
