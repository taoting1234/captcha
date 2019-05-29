import os
import random
import string
import numpy as np
from io import BytesIO
from keras.models import load_model

from helper import before_predict, after_predict


def predict():
    captcha_characters = string.digits + string.ascii_lowercase  # 验证码字符
    captcha_len = 4
    directory = '/Users/taoting/Desktop/zf'  # 图片路径
    model_filename = 'zf_model.h5'
    size = (150, 50)

    model = load_model(model_filename)
    file_list = os.listdir(directory)
    for _ in range(10):
        file_name = random.choice(file_list)
        label = file_name.split('_')[0].lower()
        with open(os.path.join(directory, file_name), 'rb') as f:
            data = f.read()
        data = before_predict(BytesIO(data), size)
        data = np.array([data])
        data = model.predict(data)
        data = after_predict(data, captcha_characters, captcha_len)
        print('real:{} pred:{}'.format(label, data))


if __name__ == '__main__':
    predict()
