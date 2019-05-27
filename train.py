import string
from keras.callbacks import EarlyStopping
from keras.models import *
from keras.layers import *
from helper import load_data


def train():
    epoch = 100  # 训练轮次
    batch_size = 100  # 一次输入的大小
    test_ratio = 0.1  # 测试集比例
    captcha_len = 4  # 验证码长度
    captcha_characters = string.digits + string.ascii_lowercase  # 验证码字符

    directory = '/Users/taoting/Desktop/zf'  # 图片路径
    x_data, y_data = load_data(directory, captcha_characters)

    inputs = Input(shape=x_data.shape[1:])

    x = inputs
    for i in range(4):
        x = Convolution2D(32 * 2 ** i, (3, 3), padding="same", activation='relu')(x)
        x = Convolution2D(32 * 2 ** i, (3, 3), padding="same", activation='relu')(x)
        x = MaxPooling2D((2, 2))(x)

    x = Flatten()(x)
    x = Dense(len(captcha_characters))(x)
    x = Dropout(0.25)(x)
    x1 = Dense(len(captcha_characters), activation="softmax", name="x1")(x)
    x2 = Dense(len(captcha_characters), activation="softmax", name="x2")(x)
    x3 = Dense(len(captcha_characters), activation="softmax", name="x3")(x)
    x4 = Dense(len(captcha_characters), activation="softmax", name="x4")(x)

    model = Model(inputs=inputs, outputs=[x1, x2, x3, x4])

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

    model.fit(x_data, y_data, batch_size=batch_size, epochs=epoch, shuffle=True,
              validation_split=test_ratio, callbacks=[EarlyStopping(patience=10)])

    model.save('model.h5')


if __name__ == '__main__':
    train()
