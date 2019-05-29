import os
import numpy as np
from PIL import Image
from keras.utils import to_categorical


def load_data(directory, characters, size):
    file_list = os.listdir(directory)

    x_data = []
    y_data = []

    for file_name in file_list:
        label = file_name.split('_')[0].lower()
        img = Image.open(os.path.join(directory, file_name))
        img = img.convert('RGB')
        img = img.resize(size)
        img_arr = np.array(img)
        img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1], -1))
        x_data.append(img_arr)
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
    img_arr = np.array(img)
    img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1], -1))
    data = np.array(img_arr) / 255
    return data


def after_predict(pred, characters, captcha_len):
    res = np.array(pred).reshape((captcha_len, len(characters)))
    res = ''.join([characters[x] for x in np.argmax(res, axis=1)])
    return res
