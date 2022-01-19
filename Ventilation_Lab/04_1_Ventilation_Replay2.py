# replay 스크립트 기능 완성본
# UI 및 통신 적용 필요
# x -> 세로, y -> 가로

import retro
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import numpy as np
import sys
import random
import os
import time
import websocket

import Web_Crawler
import Web_Socket_Client

relu = lambda X: np.maximum(0, X)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

main_map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

# cnt = 0
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
    global generation
    global chromosome_index

    def __init__(self):
        # print(generation)
        # self.w1 = np.load(f'../replay/{generation}/{chromosome_index}/w1.npy')
        # self.b1 = np.load(f'../replay/{generation}/{chromosome_index}/b1.npy')
        # self.w2 = np.load(f'../replay/{generation}/{chromosome_index}/w2.npy')
        # self.b2 = np.load(f'../replay/{generation}/{chromosome_index}/b2.npy')

        # print(self.w1)

        # self.w1 = [np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
        #            np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
        #            np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)), np.random.uniform(low=-1, high=1, size=(486, 48)),
        #            np.random.uniform(low=-1, high=1, size=(486, 48))]
        # # self.w1 = np.random.uniform(low=-1, high=1, size=(486, 48))
        # self.b1 = [np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
        #            np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
        #            np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)), np.random.uniform(low=-1, high=1, size=(48,)),
        #            np.random.uniform(low=-1, high=1, size=(48,))]
        # # self.b1 = np.random.uniform(low=-1, high=1, size=(48,))
        #
        # self.w2 = [np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
        #            np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
        #            np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)), np.random.uniform(low=-1, high=1, size=(48, 4)),
        #            np.random.uniform(low=-1, high=1, size=(48, 4))]
        # # self.w2 = np.random.uniform(low=-1, high=1, size=(48, 4))
        # self.b2 = [np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
        #            np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
        #            np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)), np.random.uniform(low=-1, high=1, size=(4,)),
        #            np.random.uniform(low=-1, high=1, size=(4,))]
        # # self.b2 = np.random.uniform(low=-1, high=1, size=(4,))

        # self.start = [2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16]

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

        # self.x = 0
        # self.y = 2
        #
        # self.generation = 0
        # self.chromosome_index = 0

    def predict(self, data):
        global w1
        global b1
        global w2
        global b2

        global generation
        global socket_check

        # self.l1 = relu(np.matmul(data, self.w1) + self.b1)
        # print(data)
        self.l1 = relu(np.matmul(data, w1[generation]) + b1[generation])
        # a = np.matmul(self.l1, self.w2) + self.b2
        # a = 1.0 / (1.0 + np.exp(max(-np.matmul(self.l1, self.w2) + self.b2, 0.0001)))
        # print(a)
        # print(sigmoid(a))
        # output = sigmoid(np.matmul(self.l1, self.w2) + self.b2)
        output = sigmoid(np.matmul(self.l1, w2[generation]) + b2[generation])
        result = (output > 0.5).astype(np.int)
        # print(result)
        return result

    def fitness(self):
        return int(max(self.distance ** 2 - self.frames + max(self.move - 5, 0) * 5 + self.win1 * 1000, self.win5 * 1000, 1))

    # 개체 통계값 초기화
    def clear(self):
        # time.sleep(3)

        global x
        global y
        global generation
        global chromosome_index
        global time_check

        generation += 1
        time_check = 0

        if generation == 10:
            # Web_Socket_Client.sendstring(socket_check)
            Web_Socket_Client.ending()
            time.sleep(5)
            exit(0)

        self.current_chromosome = Chromosome()
        # self.current_chromosome.generation = cnt
        # generation = cnt

        # self.x = 0
        # self.y = self.start[cnt]
        x = 0
        y = start[generation]
        # y = self.start[cnt]

        # self.current_chromosome.w1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w1.npy')
        # self.current_chromosome.b1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b1.npy')
        # self.current_chromosome.w2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w2.npy')
        # self.current_chromosome.b2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b2.npy')

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

        # global w1
        # global b1
        # global w2
        # global b2

        self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

        # self.env = retro.make(game='SuperMarioBros-Nes', state=f'Level1-1')
        # screen = self.env.reset()

        # self.screen_width = screen.shape[0] * 2
        # self.screen_height = screen.shape[1] * 2
        #
        # self.screen_tiles_margin_x = 60
        # self.screen_tiles_margin_y = 10
        # self.neural_network_l1_margin_x = 20
        # self.neural_network_w2_margin_x = 10
        # self.neural_network_predict_margin_x = 70
        #
        # self.setFixedSize(self.screen_width + 400, self.screen_height)
        # self.setFixedSize(454, 448)
        self.setFixedSize(655, 448 + 16)
        self.setWindowTitle('Ventilation-AI')

        # while True:
        #     tmp = np.random.randint(0, 18)
        #     if self.map[0][tmp] ==
        #         break

        # self.screen_label = QLabel(self)
        # self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)
        # self.image_label = QLabel(self)
        # self.image_label.setPixmap(QPixmap("C:/Users/user/Desktop/철권.png"))
        # self.image_label.setGeometry(QRect(288 + 100, 200, 200, 200))

        self.lbl = QLabel(self)
        self.lbl.resize(400, 400)
        self.lbl.setGeometry(QRect(288 + 16 + 100, 208, 160, 160))
        pixmap = QPixmap("C:/Users/user/Documents/GitHub/Ventilation-AI/SCINOVATOR.png")
        self.lbl.setPixmap(QPixmap(pixmap))

        self.info_label = QLabel(self)
        # self.info_label.setGeometry(288 + 10 + 200, 432 + 10 - 70, 70, 70)
        self.info_label.setGeometry(288 + 220 + 32, 384, 70, 70)
        # self.info_label.setText('?????세대\n?번 \n???????')
        self.info_label.setText('?????번 유전자\n적합도: ???????')

        # self.current_chromosome.w1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w1.npy')
        # self.current_chromosome.b1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b1.npy')
        # self.current_chromosome.w2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w2.npy')
        # self.current_chromosome.b2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b2.npy')

        self.current_chromosome = Chromosome()

        for i in range(10):
            # print(1)
            # self.current_chromosome.w1[i] = np.load(f'../replay/{i}/{chromosome_index}/w1.npy')
            # self.current_chromosome.b1[i] = np.load(f'../replay/{i}/{chromosome_index}/b1.npy')
            # self.current_chromosome.w2[i] = np.load(f'../replay/{i}/{chromosome_index}/w2.npy')
            # self.current_chromosome.b2[i] = np.load(f'../replay/{i}/{chromosome_index}/b2.npy')
            w1[i] = np.load(f'../replay/{i}/{chromosome_index}/w1.npy')
            b1[i] = np.load(f'../replay/{i}/{chromosome_index}/b1.npy')
            w2[i] = np.load(f'../replay/{i}/{chromosome_index}/w2.npy')
            b2[i] = np.load(f'../replay/{i}/{chromosome_index}/b2.npy')

        print(x, y, generation)

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(1000 // 60)

        self.show()

    # def update_screen(self):
        # screen = self.env.get_screen()
        # qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap(qimage)
        # pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        # self.screen_label.setPixmap(pixmap)

    def step(self, press_buttons):
        global main_map

        global x
        global y

        # current_chromosome = self.ga.chromosomes[self.ga.current_chromosome_index]
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
                            # self.map[self.x][self.y] = 0
                            y = y - 1
                            self.current_chromosome.move += 1
                elif press_buttons[3] == 1:
                    # UDR
                    if x + 1 != 27 and self.map[x][y + 1] != 1 and \
                            x >= 0 and y >= 0:
                        self.map[x][y + 1] = 2
                        main_map[x][y + 1] = 2
                        # self.map[self.x][self.y] = 0
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
                        # self.map[self.x][self.y] = 0
                        x = x - 1
                        self.current_chromosome.move += 1
                else:
                    # UL
                    if x + 1 != 27 and self.map[x - 1][y - 1] != 1 and x > 0 and y >= 0:
                        self.map[x - 1][y - 1] = 2
                        main_map[x - 1][y - 1] = 2
                        # self.map[self.x][self.y] = 0
                        x = x - 1
                        y = y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # UR
                if x + 1 != 27 and self.map[x - 1][y + 1] != 1 and x > 0 and y >= 0:
                    self.map[x - 1][y + 1] = 2
                    main_map[x - 1][y + 1] = 2
                    # self.map[self.x][self.y] = 0
                    x = x - 1
                    y = y + 1
                    self.current_chromosome.move += 1
            else:
                # U
                if x + 1 != 27 and self.map[x - 1][y] != 1 and x > 0 and y >= 0:
                    self.map[x - 1][y] = 2
                    main_map[x - 1][y] = 2
                    # self.map[self.x][self.y] = 0
                    x = x - 1
                    self.current_chromosome.move += 1
        elif press_buttons[1] == 1:
            if press_buttons[2] == 1:
                if press_buttons[3] == 1:
                    # DLR
                    if x + 1 != 27 and self.map[x + 1][y] != 1 and x >= 0 and y >= 0:
                        self.map[x + 1][y] = 2
                        main_map[x + 1][y] = 2
                        # self.map[self.x][self.y] = 0
                        x = x + 1
                        self.current_chromosome.move += 1
                else:
                    # DL
                    if x + 1 != 27 and self.map[x + 1][y - 1] != 1 and x >= 0 and y >= 0:
                        self.map[x + 1][y - 1] = 2
                        main_map[x + 1][y - 1] = 2
                        # self.map[self.x][self.y] = 0
                        x = x + 1
                        y = y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # DR
                if x + 1 != 27 and self.map[x + 1][y + 1] != 1 and x >= 0 and y >= 0:
                    self.map[x + 1][y + 1] = 2
                    main_map[x + 1][y + 1] = 2
                    # self.map[self.x][self.y] = 0
                    x = x + 1
                    y = y + 1
                    self.current_chromosome.move += 1
            else:
                # D
                if x + 1 != 27 and self.map[x + 1][y] != 1 and x >= 0 and y >= 0:
                    self.map[x + 1][y] = 2
                    main_map[x + 1][y] = 2
                    # self.map[self.x][self.y] = 0
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
                    # self.map[self.x][self.y] = 0
                    y = y - 1
                    self.current_chromosome.move += 1
        elif press_buttons[3] == 1:
            # R
            if x + 1 != 27 and self.map[x][y + 1] != 1 and x >= 0 and y >= 0:
                self.map[x][y + 1] = 2
                main_map[x][y + 1] = 2
                # self.map[self.x][self.y] = 0
                y = y + 1
                self.current_chromosome.move += 1

    def update_game(self):
        global main_map

        global generation
        global chromosome_index

        # self.update_screen()
        self.update()
        # self.info_label.setText(f'{generation}세대\n{chromosome_index}번 \n{self.current_chromosome.fitness()}')
        # self.image_label.setPixmap(QPixmap("SCINOVATOR.png"))
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
            # if self.map[t][i % 18] == 0:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.gray))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a + 16, b + 16, 16, 16)
            elif main_map[t][i % 18] == 2:
            # elif self.map[t][i % 18] == 2:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.yellow))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a + 16, b + 16, 16, 16)
            else:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.blue))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a + 16, b + 16, 16, 16)
            a += 16
            # print(cnt)
            if cnt % 18 == 0:
                a = 0
                b += 16
                t += 1

        painter.setPen(QPen(Qt.magenta, 2, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        # painter.drawRect(2 * 16, 7 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(8 * 16, 3 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(14 * 16, 3 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(11 * 16, 6 * 16, 2 * 16, 2 * 16)
        # painter.drawRect(11 * 16, 11 * 16, 2 * 16, 2 * 16)
        # painter.drawRect(7 * 16, 15 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(7 * 16, 20 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(5 * 16, 22 * 16, 1 * 16, 2 * 16)
        # painter.drawRect(2 * 16, 26 * 16, 2 * 16, 1 * 16)
        # painter.drawRect(9 * 16, 26 * 16, 4 * 16, 1 * 16)

        painter.drawRect(3 * 16, 8 * 16, 2 * 16, 1 * 16)
        painter.drawRect(9 * 16, 4 * 16, 2 * 16, 1 * 16)
        painter.drawRect(15 * 16, 4 * 16, 2 * 16, 1 * 16)
        painter.drawRect(12 * 16, 7 * 16, 2 * 16, 2 * 16)
        painter.drawRect(12 * 16, 12 * 16, 2 * 16, 2 * 16)
        painter.drawRect(8 * 16, 16 * 16, 2 * 16, 1 * 16)
        painter.drawRect(8 * 16, 21 * 16, 2 * 16, 1 * 16)
        painter.drawRect(6 * 16, 23 * 16, 1 * 16, 2 * 16)
        painter.drawRect(3 * 16, 27 * 16, 2 * 16, 1 * 16)
        painter.drawRect(8 * 16, 27 * 16, 4 * 16, 1 * 16)

        input_data = self.map
        # if 2 <= py <= 11:
        #     input_data[py - 2][0] = 2

        input_data = input_data.flatten()
        self.current_chromosome.frames += 1
        # self.current_chromosome.distance = ram[0x006D] * 256 + ram[0x0086]
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

        # for i in range(6):
        #     for j in range(4):
        #         if self.map[i + 16][j + 6] == 2:
        #             self.current_chromosome.win2 = 1
        #             break
        # for i in range(5):
        #     for j in range(5):
        #         if self.map[i + 16][j + 12] == 2:
        #             self.current_chromosome.win3 = 1
        #             break
        # for i in range(5):
        #     for j in range(12):
        #         # map[세로][가로]
        #         if self.map[i + 18][j + 5] == 2:
        #             self.current_chromosome.win4 = 1
        #             break
        for i in range(5):
            if self.map[26][i + 9] == 2:
                self.current_chromosome.win5 = 1
                break

        if self.current_chromosome.max_distance < self.current_chromosome.distance:
            self.current_chromosome.max_distance = self.current_chromosome.distance
            self.current_chromosome.stop_frames = 0
        else:
            self.current_chromosome.stop_frames += 1

        # print(time_check)
        if time_check == 0 and (self.current_chromosome.stop_frames > 5 or self.current_chromosome.win1 == 1 or self.current_chromosome.win5 == 1):
            # if ram[0x001D] == 3:
            #     self.current_chromosome.win = 1

            # print(f'적합도: {self.current_chromosome.fitness()}')
            # print(y, self.current_chromosome.generation)
            # time.sleep(2)
            # time_check = 0
            time_check += 1

        elif time_check == 300:
            Web_Socket_Client.sendstring(socket_check)
            self.current_chromosome.clear()
            self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

            time_check = 0
            print(x, y, generation)

        elif time_check != 0:
            time_check += 1
            # print(time_check)

            predict = self.current_chromosome.predict(input_data)
            # press_buttons = np.array([predict[5], 0, 0, 0, predict[0], predict[1], predict[2], predict[3], predict[4]])
            # self.env.step(press_buttons)
            press_buttons = np.array([predict[0], predict[1], predict[2], predict[3]])
            # print(press_buttons)
            self.step(press_buttons)
            # print(press_buttons[0][generation])
            # self.step(press_buttons[0][generation])

            # print("load", self.current_chromosome.w1, self.current_chromosome.b1, self.current_chromosome.w2, self.current_chromosome.b2)

            # for i in range(predict.shape[0]):
            #     if predict[i] == 1:
            #         painter.setBrush(QBrush(Qt.magenta))
            #     else:
            #         painter.setBrush(QBrush(Qt.gray))
            #     painter.drawEllipse(300 + i * 40, 100, 10 * 2, 10 * 2)
            #     text = ('U', 'D', 'L', 'R')[i]
            #     painter.drawText(300 + i * 40, 140, text)

            # painter.end()

            #     for i in range(self.current_chromosome.w2.shape[0]):
            #         for j in range(self.current_chromosome.w2.shape[1]):
            #             if self.current_chromosome.w2[i][j] > 0:
            #                 painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
            #             else:
            #                 painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
            #             painter.drawLine(self.screen_width + self.neural_network_l1_margin_x + self.neural_network_w2_margin_x + i * 40, 252, self.screen_width + self.neural_network_predict_margin_x + self.neural_network_w2_margin_x + j * 40, 452)
            #
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            # for i in range(self.current_chromosome.l1.shape[0]):
            #     painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if self.current_chromosome.l1[i] == 0 else 1, 120 / 240)))
            #     painter.drawEllipse(288 + 10 + i * 40, 240, 12 * 2, 12 * 2)

            weather_text = ['온도', '습도', '풍향', '풍속']
            door_text = ['1번문', '2번문', '3번문', '4번문', '5번문', '6번문', '7번문', '8번문']

            for i in range(4):
                painter.drawText(288 + 70 + i * 75 - 5, 50, weather_text[i])
                painter.drawText(288 + 70 + i * 75 - 5, 70, weather[i])

            for i in range(8):
                painter.drawText(288 + 42.5 + i * 40 - 5, 130 + 16, door_text[i])

            # print(socket_check)
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
            # press_buttons = np.array([predict[5], 0, 0, 0, predict[0], predict[1], predict[2], predict[3], predict[4]])
            # self.env.step(press_buttons)
            press_buttons = np.array([predict[0], predict[1], predict[2], predict[3]])
            # print(press_buttons)
            self.step(press_buttons)
            # print(press_buttons[0][generation])
            # self.step(press_buttons[0][generation])

            # print("load", self.current_chromosome.w1, self.current_chromosome.b1, self.current_chromosome.w2, self.current_chromosome.b2)

            # for i in range(predict.shape[0]):
            #     if predict[i] == 1:
            #         painter.setBrush(QBrush(Qt.magenta))
            #     else:
            #         painter.setBrush(QBrush(Qt.gray))
            #     painter.drawEllipse(300 + i * 40, 100, 10 * 2, 10 * 2)
            #     text = ('U', 'D', 'L', 'R')[i]
            #     painter.drawText(300 + i * 40, 140, text)

        # painter.end()

        #     for i in range(self.current_chromosome.w2.shape[0]):
        #         for j in range(self.current_chromosome.w2.shape[1]):
        #             if self.current_chromosome.w2[i][j] > 0:
        #                 painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        #             else:
        #                 painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        #             painter.drawLine(self.screen_width + self.neural_network_l1_margin_x + self.neural_network_w2_margin_x + i * 40, 252, self.screen_width + self.neural_network_predict_margin_x + self.neural_network_w2_margin_x + j * 40, 452)
        #
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            # for i in range(self.current_chromosome.l1.shape[0]):
            #     painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if self.current_chromosome.l1[i] == 0 else 1, 120 / 240)))
            #     painter.drawEllipse(288 + 10 + i * 40, 240, 12 * 2, 12 * 2)

            weather_text = ['온도', '습도', '풍향', '풍속']
            door_text = ['1번문', '2번문', '3번문', '4번문', '5번문', '6번문', '7번문', '8번문']

            for i in range(4):
                painter.drawText(288 + 70 + i * 75 - 5, 50, weather_text[i])
                painter.drawText(288 + 70 + i * 75 - 5, 70, weather[i])

            for i in range(8):
                painter.drawText(288 + 42.5 + i * 40 - 5, 130 + 16, door_text[i])

            # print(socket_check)
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