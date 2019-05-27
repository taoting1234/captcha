import os
import random
import string
import numpy as np
from keras.models import load_model
from PIL import Image
from keras.utils import to_categorical


def predict():
    model = load_model('model.h5')
    captcha_characters = string.digits + string.ascii_lowercase  # 验证码字符

    directory = '/Users/taoting/Desktop/zf'  # 图片路径
    file_list = os.listdir(directory)
    file_name = random.choice(file_list)
    label = file_name.split('_')[0].lower()
    img = Image.open(os.path.join(directory, file_name))
    img_arr = np.array(img)
    img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1], -1))
    x_data = img_arr
    y_data = np.array([to_categorical(captcha_characters.find(label[i]), len(captcha_characters)) for i in range(4)])

    pred = model.predict(x_data.reshape((1, x_data.shape[0], x_data.shape[1], x_data.shape[2])))
    pred = np.array(pred).reshape((4, 36))
    pred = ''.join([captcha_characters[x] for x in np.argmax(pred, axis=1)])
    real = ''.join([captcha_characters[x] for x in np.argmax(y_data, axis=1)])
    print(pred)
    print(real)


if __name__ == '__main__':
    predict()
