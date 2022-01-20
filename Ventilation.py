# 최종 완성본

from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import numpy as np
import sys
import time

import Web_Crawler
import Web_Socket_Client

# 활성화 함수
relu = lambda X: np.maximum(0, X)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

# 전역 변수
main_map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

x = 0
y = 2
generation = 0
chromosome_index = 0
start = [2, 3, 8, 9, 10, 11, 12, 13, 14, 15]
weather = Web_Crawler.start()
socket_check = ['0', '0', '0', '0', '0', '0', '0', '0']
time_check = 0

w1 = [np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48)),
           np.random.uniform(low=-1, high=1, size=(486, 48))]
b1 = [np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,)),
           np.random.uniform(low=-1, high=1, size=(48,))]

w2 = [np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4)),
           np.random.uniform(low=-1, high=1, size=(48, 4))]
b2 = [np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,)),
           np.random.uniform(low=-1, high=1, size=(4,))]

class Chromosome:
    def __init__(self):
        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.move = 0
        self.stop_frames = 0
        self.win1 = 0
        self.win2 = 0
        self.win3 = 0
        self.win4 = 0
        self.win5 = 0

    def predict(self, data):
        global w1
        global b1
        global w2
        global b2
        global generation
        global socket_check

        self.l1 = relu(np.matmul(data, w1[generation]) + b1[generation])
        output = sigmoid(np.matmul(self.l1, w2[generation]) + b2[generation])
        result = (output > 0.5).astype(np.int)

        return result

    def fitness(self):
        return int(max(self.distance ** 2 - self.frames + max(self.move - 5, 0) * 5 + self.win1 * 1000, self.win5 * 1000, 1))

    # 개체 통계값 초기화
    def clear(self):
        global x
        global y
        global generation
        global chromosome_index
        global time_check

        generation += 1
        time_check = 0

        if generation == 10:
            # Web_Socket_Client.ending()
            time.sleep(5)
            exit(0)

        self.current_chromosome = Chromosome()
        x = 0
        y = start[generation]

        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.move = 0
        self.stop_frames = 0

        self.win1 = 0
        self.win2 = 0
        self.win3 = 0
        self.win4 = 0
        self.win5 = 0


class Ventilation(QWidget):
    def __init__(self):
        super().__init__()

        sys.excepthook = except_hook

        global x
        global y
        global generation
        global chromosome_index
        global start

        self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

        self.setFixedSize(655, 448 + 16)
        self.setWindowTitle('Ventilation-AI')

        self.lbl = QLabel(self)
        self.lbl.resize(400, 400)
        self.lbl.setGeometry(QRect(288 + 16 + 100, 208, 160, 160))
        pixmap = QPixmap("C:/Users/user/Documents/GitHub/Ventilation-AI/SCINOVATOR.png")
        self.lbl.setPixmap(QPixmap(pixmap))

        self.info_label = QLabel(self)
        self.info_label.setGeometry(288 + 220 + 32, 384, 70, 70)
        self.info_label.setText('?????번 유전자\n적합도: ???????')

        self.current_chromosome = Chromosome()

        for i in range(10):
            w1[i] = np.load(f'replay/{i}/{chromosome_index}/w1.npy')
            b1[i] = np.load(f'replay/{i}/{chromosome_index}/b1.npy')
            w2[i] = np.load(f'replay/{i}/{chromosome_index}/w2.npy')
            b2[i] = np.load(f'replay/{i}/{chromosome_index}/b2.npy')

        print(x, y, generation)

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(1000 // 60)

        self.show()

    def step(self, press_buttons):
        global main_map

        global x
        global y

        # U, D, L, R
        # map[세로][가로]
        if press_buttons[0] == 1:
            if press_buttons[1] == 1:
                if press_buttons[2] == 1:
                    # UDL
                    if press_buttons[3] == 1:
                        # UDLR
                        self.map[x][y] = 2
                        main_map[x][y] = 2
                    else:
                        if x + 1 != 27 and self.map[x][y - 1] != 1 and \
                                x >= 0 and y >= 0:
                            self.map[x][y - 1] = 2
                            main_map[x][y - 1] = 2
                            y = y - 1
                            self.current_chromosome.move += 1
                elif press_buttons[3] == 1:
                    # UDR
                    if x + 1 != 27 and self.map[x][y + 1] != 1 and \
                            x >= 0 and y >= 0:
                        self.map[x][y + 1] = 2
                        main_map[x][y + 1] = 2
                        y = y + 1
                        self.current_chromosome.move += 1
                else:
                    # UD
                    self.map[x][y] = 2
                    main_map[x][y] = 2
            elif press_buttons[2] == 1:
                if press_buttons[3] == 1:
                    # ULR
                    if x + 1 != 27 and self.map[x - 1][y] != 1 and x > 0 and y >= 0:
                        self.map[x - 1][y] = 2
                        main_map[x - 1][y] = 2
                        x = x - 1
                        self.current_chromosome.move += 1
                else:
                    # UL
                    if x + 1 != 27 and self.map[x - 1][y - 1] != 1 and x > 0 and y >= 0:
                        self.map[x - 1][y - 1] = 2
                        main_map[x - 1][y - 1] = 2
                        x = x - 1
                        y = y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # UR
                if x + 1 != 27 and self.map[x - 1][y + 1] != 1 and x > 0 and y >= 0:
                    self.map[x - 1][y + 1] = 2
                    main_map[x - 1][y + 1] = 2
                    x = x - 1
                    y = y + 1
                    self.current_chromosome.move += 1
            else:
                # U
                if x + 1 != 27 and self.map[x - 1][y] != 1 and x > 0 and y >= 0:
                    self.map[x - 1][y] = 2
                    main_map[x - 1][y] = 2
                    x = x - 1
                    self.current_chromosome.move += 1
        elif press_buttons[1] == 1:
            if press_buttons[2] == 1:
                if press_buttons[3] == 1:
                    # DLR
                    if x + 1 != 27 and self.map[x + 1][y] != 1 and x >= 0 and y >= 0:
                        self.map[x + 1][y] = 2
                        main_map[x + 1][y] = 2
                        x = x + 1
                        self.current_chromosome.move += 1
                else:
                    # DL
                    if x + 1 != 27 and self.map[x + 1][y - 1] != 1 and x >= 0 and y >= 0:
                        self.map[x + 1][y - 1] = 2
                        main_map[x + 1][y - 1] = 2
                        x = x + 1
                        y = y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # DR
                if x + 1 != 27 and self.map[x + 1][y + 1] != 1 and x >= 0 and y >= 0:
                    self.map[x + 1][y + 1] = 2
                    main_map[x + 1][y + 1] = 2
                    x = x + 1
                    y = y + 1
                    self.current_chromosome.move += 1
            else:
                # D
                if x + 1 != 27 and self.map[x + 1][y] != 1 and x >= 0 and y >= 0:
                    self.map[x + 1][y] = 2
                    main_map[x + 1][y] = 2
                    x = x + 1
                    self.current_chromosome.move += 1
        elif press_buttons[2] == 1:
            if press_buttons[3] == 1:
                # LR
                self.map[x][y] = 2
                main_map[x][y] = 2
            else:
                # L
                if x + 1 != 27 and self.map[x][y - 1] != 1 and x >= 0 and y >= 0:
                    self.map[x][y - 1] = 2
                    main_map[x][y - 1] = 2
                    y = y - 1
                    self.current_chromosome.move += 1
        elif press_buttons[3] == 1:
            # R
            if x + 1 != 27 and self.map[x][y + 1] != 1 and x >= 0 and y >= 0:
                self.map[x][y + 1] = 2
                main_map[x][y + 1] = 2
                y = y + 1
                self.current_chromosome.move += 1

    def update_game(self):
        global main_map

        global generation
        global chromosome_index

        self.update()
        self.info_label.setText(f'{generation + 1}번 유전자\n적합도: {self.current_chromosome.fitness()}')

    def paintEvent(self, e):
        global x
        global y
        global generation
        global weather
        global socket_check
        global time_check

        painter = QPainter()
        painter.begin(self)

        cnt = 0
        a = 0
        b = 0

        painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        # 브러쉬 설정 (채우기)
        painter.setBrush(QBrush(Qt.white))
        # 직사각형 (왼쪽 위, 오른쪽 아래)

        painter.drawRect(288 + 32, 16, 320, 80)
        painter.drawRect(288 + 32, 112, 320, 80)
        painter.drawRect(288 + 32, 384, 320, 64)

        for i in range(18):
            if main_map[0][i] == 2:
                main_map[0][i] = 0

        t = 0
        # 타일 그리기
        for i in range(486):
            # 18X26
            cnt += 1
            if main_map[t][i % 18] == 0:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.gray))
                painter.drawRect(a + 16, b + 16, 16, 16)
            elif main_map[t][i % 18] == 2:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.yellow))
                painter.drawRect(a + 16, b + 16, 16, 16)
            else:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect(a + 16, b + 16, 16, 16)
            a += 16

            if cnt % 18 == 0:
                a = 0
                b += 16
                t += 1

        painter.setPen(QPen(Qt.magenta, 2, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        # 문 구간 Painter
        painter.drawRect(3 * 16, 8 * 16, 2 * 16, 1 * 16)
        painter.drawRect(9 * 16, 4 * 16, 2 * 16, 1 * 16)
        painter.drawRect(15 * 16, 4 * 16, 2 * 16, 1 * 16)
        painter.drawRect(12 * 16, 7 * 16, 2 * 16, 2 * 16)
        painter.drawRect(12 * 16, 12 * 16, 2 * 16, 2 * 16)
        painter.drawRect(8 * 16, 16 * 16, 2 * 16, 1 * 16)
        painter.drawRect(8 * 16, 21 * 16, 2 * 16, 1 * 16)
        painter.drawRect(6 * 16, 23 * 16, 1 * 16, 2 * 16)
        painter.drawRect(3 * 16, 27 * 16, 2 * 16, 1 * 16)
        painter.drawRect(10 * 16, 27 * 16, 4 * 16, 1 * 16)

        input_data = self.map.flatten()

        self.current_chromosome.frames += 1
        self.current_chromosome.distance = x

        # 문 배열
        for i in range(2):
            if main_map[8][i + 2] == 2:
                socket_check[0] = '1'

        for i in range(2):
            if main_map[3][i + 8] == 2:
                socket_check[1] = '1'

        for i in range(2):
            if main_map[3][i + 14] == 2:
                socket_check[2] = '1'

        for i in range(2):
            for j in range(2):
                if main_map[i + 6][j + 11] == 2:
                    socket_check[3] = '1'

        for i in range(2):
            if main_map[15][i + 7] == 2:
                socket_check[4] = '1'

        for i in range(2):
            if main_map[20][i + 7] == 2:
                socket_check[5] = '1'

        for i in range(2):
            for j in range(2):
                if main_map[i + 11][j + 11] == 2:
                    socket_check[6] = '1'

        for i in range(2):
            if main_map[i + 22][5] == 2:
                socket_check[7] = '1'

        # 점수 체계
        for i in range(2):
            if self.map[26][i + 3] == 2:
                self.current_chromosome.win1 = 1
                break

        for i in range(5):
            if self.map[26][i + 9] == 2:
                self.current_chromosome.win5 = 1
                break

        # 정지 조건 관련 변수
        if self.current_chromosome.max_distance < self.current_chromosome.distance:
            self.current_chromosome.max_distance = self.current_chromosome.distance
            self.current_chromosome.stop_frames = 0
        else:
            self.current_chromosome.stop_frames += 1

        if time_check == 0 and (self.current_chromosome.stop_frames > 5 or self.current_chromosome.win1 == 1 or self.current_chromosome.win5 == 1):
            time_check += 1

        elif time_check == 600:
            # print(socket_check)
            Web_Socket_Client.sendstring(socket_check)
            Web_Socket_Client.ending()
            self.current_chromosome.clear()
            self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

            time_check = 0
            print(x, y, generation)

        elif time_check != 0:
            time_check += 1

            predict = self.current_chromosome.predict(input_data)
            press_buttons = np.array([predict[0], predict[1], predict[2], predict[3]])

            self.step(press_buttons)

            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

            weather_text = ['온도', '습도', '풍향', '풍속', '미세먼지', '초미세먼지']
            door_text = ['1번문', '2번문', '3번문', '4번문', '5번문', '6번문', '7번문', '8번문']

            for i in range(6):
                if i == 4:
                    painter.drawText(288 + 40 + i * 55 - 20, 50, weather_text[i])
                    painter.drawText(288 + 40 + i * 55 - 10, 70, weather[i])
                elif i == 5:
                    painter.drawText(288 + 40 + i * 55 - 25, 50, weather_text[i])
                    painter.drawText(288 + 40 + i * 55 - 5, 70, weather[i])
                else:
                    painter.drawText(288 + 50 + i * 50 - 5, 50, weather_text[i])
                    painter.drawText(288 + 50 + i * 50 - 5, 70, weather[i])


            for i in range(8):
                painter.drawText(288 + 42.5 + i * 40 - 5, 130 + 16, door_text[i])

            for i in range(8):
                if socket_check[i] == '1':
                    painter.setPen(QPen(Qt.green, 2.0, Qt.SolidLine))
                    painter.drawText(288 + 45 + i * 40 - 5, 150 + 16, '열림')
                else:
                    painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine))
                    painter.drawText(288 + 45 + i * 40 - 5, 150 + 16, '닫침')

            painter.setPen(QPen(Qt.black, 2.0, Qt.SolidLine))
            for i in range(predict.shape[0]):
                painter.setBrush(QBrush(QColor.fromHslF(0.8, 0 if predict[i] <= 0.5 else 1, 0.8)))
                # 세로 가로
                painter.drawEllipse(288 + 72 + i * 40, 390 + 10, 16 * 2, 16 * 2)
                text = ('U', 'D', 'L', 'R')[i]
                painter.drawText(288 + 72 + i * 40 - 5, 420 + 16, text)

            painter.end()

        else:
            predict = self.current_chromosome.predict(input_data)
            press_buttons = np.array([predict[0], predict[1], predict[2], predict[3]])

            self.step(press_buttons)

            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

            weather_text = ['온도', '습도', '풍향', '풍속', '미세먼지', '초미세먼지']
            door_text = ['1번문', '2번문', '3번문', '4번문', '5번문', '6번문', '7번문', '8번문']

            for i in range(6):
                if i == 4:
                    painter.drawText(288 + 40 + i * 55 - 20, 50, weather_text[i])
                    painter.drawText(288 + 40 + i * 55 - 10, 70, weather[i])
                elif i == 5:
                    painter.drawText(288 + 40 + i * 55 - 25, 50, weather_text[i])
                    painter.drawText(288 + 40 + i * 55 - 5, 70, weather[i])
                else:
                    painter.drawText(288 + 50 + i * 50 - 5, 50, weather_text[i])
                    painter.drawText(288 + 50 + i * 50 - 5, 70, weather[i])

            for i in range(8):
                painter.drawText(288 + 42.5 + i * 40 - 5, 130 + 16, door_text[i])

            for i in range(8):
                if socket_check[i] == '1':
                    painter.setPen(QPen(Qt.green, 2.0, Qt.SolidLine))
                    painter.drawText(288 + 45 + i * 40 - 5, 150 + 16, '열림')
                else:
                    painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine))
                    painter.drawText(288 + 45 + i * 40 - 5, 150 + 16, '닫침')

            painter.setPen(QPen(Qt.black, 2.0, Qt.SolidLine))
            for i in range(predict.shape[0]):
                painter.setBrush(QBrush(QColor.fromHslF(0.8, 0 if predict[i] <= 0.5 else 1, 0.8)))
                #세로 가로
                painter.drawEllipse(288 + 72 + i * 40, 390 + 10, 16 * 2, 16 * 2)
                text = ('U', 'D', 'L', 'R')[i]
                painter.drawText(288 + 72 + i * 40 - 5, 420 + 16, text)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventilation = Ventilation()
    exit(app.exec_())