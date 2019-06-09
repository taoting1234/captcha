import os

import numpy as np

from keras.utils import to_categorical
from PIL import Image


def load_data(directory, characters, size):
    file_list = os.listdir(directory)

    x_data = []
    y_data = []

    for file_name in file_list:
        label = file_name.split('_')[0].lower()
        img = Image.open(os.path.join(directory, file_name))
        img = img.convert('RGB')
        img = img.resize(size)
        x_data.append(np.array(img))
        y_data.append([to_categorical(characters.find(label[i]), len(characters)) for i in range(len(label))])

    x_data = np.array(x_data) / 255
    y_data = np.array(y_data)
    y_data = np.swapaxes(y_data, 0, 1)
    y_data = y_data.tolist()
    y_data = [np.array(i) for i in y_data]

    return x_data, y_data


def before_predict(img_byte, size):
    img = Image.open(img_byte)
    img = img.convert('RGB')
    img = img.resize(size)
    data = np.array(np.array(img)) / 255
    return data


def after_predict(pred, characters):
    res = np.array(pred).reshape((-1, len(characters)))
    res = ''.join([characters[x] for x in np.argmax(res, axis=1)])
    return res
