import os
import random
import string
from io import BytesIO

import numpy as np

from helper import after_predict, before_predict
from keras.models import load_model


def predict():
    captcha_characters = string.digits + string.ascii_lowercase  # 验证码字符
    directory = r'C:\Users\taoti\Desktop\zf\zf'  # 图片路径
    model_filename = 'zf_model.h5'
    size = (150, 50)

    model = load_model(model_filename)
    file_list = os.listdir(directory)

    t = 0
    acc_sum = 0
    for _ in range(1000):
        file_name = random.choice(file_list)
        label = file_name.split('_')[0].lower()
        with open(os.path.join(directory, file_name), 'rb') as f:
            data = f.read()
        data = before_predict(BytesIO(data), size)
        data = np.array([data])
        data = model.predict(data)
        data = after_predict(data, captcha_characters)
        t += 1
        if label == data:
            acc_sum += 1
        print('{}: real:{} pred:{} acc:{:.6f}'.format(t, label, data, acc_sum / t))


if __name__ == '__main__':
    predict()
