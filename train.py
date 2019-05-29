import string
from keras.callbacks import EarlyStopping, TensorBoard
from keras.models import *
from keras.layers import *
from keras.applications import *
from helper import load_data


def train():
    epoch = 1000  # 训练轮次
    batch_size = 100  # 一次输入的大小
    test_ratio = 0.1  # 测试集比例
    size = (150, 50)  # 固定尺寸
    captcha_characters = string.digits + string.ascii_lowercase  # 验证码字符

    directory = '/Users/taoting/Desktop/zf'  # 图片路径
    model_name = 'zf_model.h5'

    x_data, y_data = load_data(directory, captcha_characters, size)
    captcha_len = len(y_data)

    base_model = ResNet50(input_shape=x_data.shape[1:], include_top=False)

    x = base_model.output

    x = GlobalAveragePooling2D()(x)

    x = Dropout(0.25)(x)
    x = [Dense(len(captcha_characters), activation="softmax", name="x{}".format(i))(x)
         for i in range(captcha_len)]

    model = Model(inputs=base_model.input, outputs=x)

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(x_data, y_data, batch_size=batch_size, epochs=epoch, shuffle=True,
              validation_split=test_ratio,
              callbacks=[
                  EarlyStopping(patience=5, restore_best_weights=True),
                  TensorBoard(histogram_freq=1, batch_size=batch_size)
              ])

    model.save(model_name)


if __name__ == '__main__':
    train()
