# 04. mario_replay.py
import retro
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import numpy as np
import sys
import random
import os
import time

relu = lambda X: np.maximum(0, X)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(486, 48))
        self.b1 = np.random.uniform(low=-1, high=1, size=(48,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(48, 4))
        self.b2 = np.random.uniform(low=-1, high=1, size=(4,))

        self.start = [2, 3, 8, 9, 10, 11,
                      12, 13, 14, 15, 16]
        self.cnt = 0

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

        self.x = 0
        self.y = 2
        # self.y = 11

        self.generation = 0
        self.chromosome_index = 0

    def predict(self, data):
        self.l1 = relu(np.matmul(data, self.w1) + self.b1)
        # print("a")
        # a = np.matmul(self.l1, self.w2) + self.b2
        # a = 1.0 / (1.0 + np.exp(max(-np.matmul(self.l1, self.w2) + self.b2, 0.0001)))
        # print(a)
        # print(sigmoid(a))
        output = sigmoid(np.matmul(self.l1, self.w2) + self.b2)
        result = (output > 0.5).astype(np.int)
        # print(result)
        return result

    def fitness(self):
        # return int(max(self.distance ** 2 - self.frames + max(self.move - 5, 0) * 5 + self.win1 * 1000, 1))
        print(self.distance, self.move, self.win1, self.win2, self.win3, self.win4, self.win5)
        # 2-0
        return int(max(self.distance * 1.2 + self.move * 2 + self.win1 * 5 + self.win2 * 5 + self.win3 * 10 + self.win4 * 20 + self.win5 * 30, 1))
        # 2-1
        # return int(max(self.distance ** 2 - self.frames + max(self.move - 5, 0) * 5 + self.win1 * 1000, 1))

    # 개체 통계값 초기화
    def clear(self):
        self.cnt += 1

        self.x = 0
        self.y = self.start[self.cnt]
        # self.y = 11
        self.generation = self.cnt
        # self.generation = 123
        print(f'파일: {self.generation}')

        if self.cnt == 10:
            time.sleep(10)
            exit(0)

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
        self.setFixedSize(454, 448)
        self.setWindowTitle('Ventilation-AI')

        # while True:
        #     tmp = np.random.randint(0, 18)
        #     if self.map[0][tmp] == 0:
        #         break

        # self.screen_label = QLabel(self)
        # self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        # self.info_label = QLabel(self)
        # self.info_label.setGeometry(self.screen_width + 320, self.screen_height - 70, 70, 70)
        # self.info_label.setText('?????세대\n?번 마리오\n???????')

        self.current_chromosome = Chromosome()
        self.current_chromosome.w1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w1.npy')
        self.current_chromosome.b1 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b1.npy')
        self.current_chromosome.w2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/w2.npy')
        self.current_chromosome.b2 = np.load(f'../replay/{self.current_chromosome.generation}/{self.current_chromosome.chromosome_index}/b2.npy')

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(1000 // 60)

        self.show()

    def step(self, press_buttons):
        # current_chromosome = self.ga.chromosomes[self.ga.current_chromosome_index]
        # U, D, L, R
        # map[세로][가로]
        if press_buttons[0] == 1:
            if press_buttons[1] == 1:
                if press_buttons[2] == 1:
                    # UDL
                    if press_buttons[3] == 1:
                        # UDLR
                        self.map[self.current_chromosome.x][self.current_chromosome.y] = 2
                    else:
                        if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x][self.current_chromosome.y - 1] != 1 and \
                                self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                            self.map[self.current_chromosome.x][self.current_chromosome.y - 1] = 2
                            # self.map[self.x][self.y] = 0
                            self.current_chromosome.y = self.current_chromosome.y - 1
                            self.current_chromosome.move += 1
                elif press_buttons[3] == 1:
                    # UDR
                    if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x][self.current_chromosome.y + 1] != 1 and \
                            self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                        self.map[self.current_chromosome.x][self.current_chromosome.y + 1] = 2
                        # self.map[self.x][self.y] = 0
                        self.current_chromosome.y = self.current_chromosome.y + 1
                        self.current_chromosome.move += 1
                else:
                    # UD
                    self.map[self.current_chromosome.x][self.current_chromosome.y] = 2
            elif press_buttons[2] == 1:
                if press_buttons[3] == 1:
                    # ULR
                    if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x - 1][self.current_chromosome.y] != 1 and self.current_chromosome.x > 0 and self.current_chromosome.y >= 0:
                        self.map[self.current_chromosome.x - 1][self.current_chromosome.y] = 2
                        # self.map[self.x][self.y] = 0
                        self.current_chromosome.x = self.current_chromosome.x - 1
                        self.current_chromosome.move += 1
                else:
                    # UL
                    if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x - 1][self.current_chromosome.y - 1] != 1 and self.current_chromosome.x > 0 and self.current_chromosome.y >= 0:
                        self.map[self.current_chromosome.x - 1][self.current_chromosome.y - 1] = 2
                        # self.map[self.x][self.y] = 0
                        self.current_chromosome.x = self.current_chromosome.x - 1
                        self.current_chromosome.y = self.current_chromosome.y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # UR
                if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x - 1][self.current_chromosome.y + 1] != 1 and self.current_chromosome.x > 0 and self.current_chromosome.y >= 0:
                    self.map[self.current_chromosome.x - 1][self.current_chromosome.y + 1] = 2
                    # self.map[self.x][self.y] = 0
                    self.current_chromosome.x = self.current_chromosome.x - 1
                    self.current_chromosome.y = self.current_chromosome.y + 1
                    self.current_chromosome.move += 1
            else:
                # U
                if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x - 1][self.current_chromosome.y] != 1 and self.current_chromosome.x > 0 and self.current_chromosome.y >= 0:
                    self.map[self.current_chromosome.x - 1][self.current_chromosome.y] = 2
                    # self.map[self.x][self.y] = 0
                    self.current_chromosome.x = self.current_chromosome.x - 1
                    self.current_chromosome.move += 1
        elif press_buttons[1] == 1:
            if press_buttons[2] == 1:
                if press_buttons[3] == 1:
                    # DLR
                    if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x + 1][self.current_chromosome.y] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                        self.map[self.current_chromosome.x + 1][self.current_chromosome.y] = 2
                        # self.map[self.x][self.y] = 0
                        self.current_chromosome.x = self.current_chromosome.x + 1
                        self.current_chromosome.move += 1
                else:
                    # DL
                    if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x + 1][self.current_chromosome.y - 1] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                        self.map[self.current_chromosome.x + 1][self.current_chromosome.y - 1] = 2
                        # self.map[self.x][self.y] = 0
                        self.current_chromosome.x = self.current_chromosome.x + 1
                        self.current_chromosome.y = self.current_chromosome.y - 1
                        self.current_chromosome.move += 1
            elif press_buttons[3] == 1:
                # DR
                if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x + 1][self.current_chromosome.y + 1] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                    self.map[self.current_chromosome.x + 1][self.current_chromosome.y + 1] = 2
                    # self.map[self.x][self.y] = 0
                    self.current_chromosome.x = self.current_chromosome.x + 1
                    self.current_chromosome.y = self.current_chromosome.y + 1
                    self.current_chromosome.move += 1
            else:
                # D
                if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x + 1][self.current_chromosome.y] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                    self.map[self.current_chromosome.x + 1][self.current_chromosome.y] = 2
                    # self.map[self.x][self.y] = 0
                    self.current_chromosome.x = self.current_chromosome.x + 1
                    self.current_chromosome.move += 1
        elif press_buttons[2] == 1:
            if press_buttons[3] == 1:
                # LR
                self.map[self.current_chromosome.x][self.current_chromosome.y] = 2
            else:
                # L
                if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x][self.current_chromosome.y - 1] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                    self.map[self.current_chromosome.x][self.current_chromosome.y - 1] = 2
                    # self.map[self.x][self.y] = 0
                    self.current_chromosome.y = self.current_chromosome.y - 1
                    self.current_chromosome.move += 1
        elif press_buttons[3] == 1:
            # R
            if self.current_chromosome.x + 1 != 27 and self.map[self.current_chromosome.x][self.current_chromosome.y + 1] != 1 and self.current_chromosome.x >= 0 and self.current_chromosome.y >= 0:
                self.map[self.current_chromosome.x][self.current_chromosome.y + 1] = 2
                # self.map[self.x][self.y] = 0
                self.current_chromosome.y = self.current_chromosome.y + 1
                self.current_chromosome.move += 1
        # print(self.x, self.y)

    # def update_screen(self):
        # screen = self.env.get_screen()
        # qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap(qimage)
        # pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        # self.screen_label.setPixmap(pixmap)

    def update_game(self):
        # self.update_screen()
        self.update()
        # self.info_label.setText(f'{self.generation}세대\n{self.chromosome_index}번 마리오\n{self.current_chromosome.fitness()}')

    def paintEvent(self, e):

        painter = QPainter()
        painter.begin(self)

        cnt = 0
        a = 0
        b = 0

        painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        # 브러쉬 설정 (채우기)
        painter.setBrush(QBrush(Qt.white))
        # 직사각형 (왼쪽 위, 오른쪽 아래)

        t = 0
        # 타일 그리기
        for i in range(486):
            # 18X26
            cnt += 1
            if self.map[t][i % 18] == 0:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.gray))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a, 0 + b, 16, 16)
            elif self.map[t][i % 18] == 2:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.yellow))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a, 0 + b, 16, 16)
            else:
                painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
                # 브러쉬 설정 (채우기)
                painter.setBrush(QBrush(Qt.blue))
                # painter.drawRect(480 + a, 0 + b, 10, 10)
                painter.drawRect(a, 0 + b, 16, 16)
            a += 16
            # print(cnt)
            if cnt % 18 == 0:
                a = 0
                b += 16
                t += 1

        # 원래 코드
        # painter.setPen(QPen(Qt.black))
        #
        # ram = self.env.get_ram()
        #
        # full_screen_tiles = ram[0x0500:0x069F+1]
        # full_screen_tile_count = full_screen_tiles.shape[0]
        #
        # full_screen_page1_tiles = full_screen_tiles[:full_screen_tile_count // 2].reshape((-1, 16))
        # full_screen_page2_tiles = full_screen_tiles[full_screen_tile_count // 2:].reshape((-1, 16))
        #
        # full_screen_tiles = np.concatenate((full_screen_page1_tiles, full_screen_page2_tiles), axis=1).astype(np.int)
        #
        # enemy_drawn = ram[0x000F:0x0014]
        # enemy_horizontal_position_in_level = ram[0x006E:0x0072+1]
        # enemy_x_position_on_screen = ram[0x0087:0x008B+1]
        # enemy_y_position_on_screen = ram[0x00CF:0x00D3+1]
        #
        # for i in range(5):
        #     if enemy_drawn[i] == 1:
        #         ex = (((enemy_horizontal_position_in_level[i] * 256) + enemy_x_position_on_screen[i]) % 512 + 8) // 16
        #         ey = (enemy_y_position_on_screen[i] - 8) // 16 - 1
        #         if 0 <= ex < full_screen_tiles.shape[1] and 0 <= ey < full_screen_tiles.shape[0]:
        #             full_screen_tiles[ey][ex] = -1
        #
        # current_screen_in_level = ram[0x071A]
        # screen_x_position_in_level = ram[0x071C]
        # screen_x_position_offset = (256 * current_screen_in_level + screen_x_position_in_level) % 512
        # sx = screen_x_position_offset // 16
        #
        # screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, sx:sx+16]
        #
        # for i in range(screen_tiles.shape[0]):
        #     for j in range(screen_tiles.shape[1]):
        #         if screen_tiles[i][j] > 0:
        #             screen_tiles[i][j] = 1
        #         if screen_tiles[i][j] == -1:
        #             screen_tiles[i][j] = 2
        #             painter.setBrush(QBrush(Qt.red))
        #         else:
        #             painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if screen_tiles[i][j] == 0 else 1, 120 / 240)))
        #         painter.drawRect(self.screen_width + self.screen_tiles_margin_x + 16 * j, self.screen_tiles_margin_y + 16 * i, 16, 16)
        #
        # player_x_position_current_screen_offset = ram[0x03AD]
        # player_y_position_current_screen_offset = ram[0x03B8]
        # px = (player_x_position_current_screen_offset + 8) // 16
        # py = (player_y_position_current_screen_offset + 8) // 16 - 1
        # painter.setBrush(QBrush(Qt.blue))
        # painter.drawRect(self.screen_width + self.screen_tiles_margin_x + 16 * px, self.screen_tiles_margin_y + 16 * py, 16, 16)
        #
        # painter.setPen(QPen(Qt.magenta, 2, Qt.SolidLine))
        # painter.setBrush(Qt.NoBrush)
        # ix = px
        # iy = 2
        # painter.drawRect(self.screen_width + self.screen_tiles_margin_x + 16 * ix, self.screen_tiles_margin_y + iy * 16, 16 * 8, 16 * 10)
        #
        # input_data = screen_tiles[iy:iy+10, ix:ix+8]
        input_data = self.map
        # if 2 <= py <= 11:
        #     input_data[py - 2][0] = 2

        input_data = input_data.flatten()
        self.current_chromosome.frames += 1
        # self.current_chromosome.distance = ram[0x006D] * 256 + ram[0x0086]
        self.current_chromosome.distance = self.current_chromosome.x
        for i in range(2):
            if self.map[26][i + 3] == 2:
                self.current_chromosome.win1 = 1
                break
        for i in range(6):
            for j in range(4):
                if self.map[i + 16][j + 6] == 2:
                    self.current_chromosome.win2 = 1
                    break
        for i in range(5):
            for j in range(5):
                if self.map[i + 16][j + 12] == 2:
                    self.current_chromosome.win3 = 1
                    break
        for i in range(5):
            for j in range(12):
                # map[세로][가로]
                if self.map[i + 18][j + 5] == 2:
                    self.current_chromosome.win4 = 1
                    break
        for i in range(5):
            if self.map[26][i + 9] == 2:
                self.current_chromosome.win5 = 1
                break
        if self.current_chromosome.max_distance < self.current_chromosome.distance:
            self.current_chromosome.max_distance = self.current_chromosome.distance
            self.current_chromosome.stop_frames = 0
        else:
            self.current_chromosome.stop_frames += 1
        if self.current_chromosome.stop_frames > 5 or self.current_chromosome.win1 == 1 or self.current_chromosome.win5 == 1:
            # if ram[0x001D] == 3:
            #     self.current_chromosome.win = 1

            print(f'적합도: {self.current_chromosome.fitness()}')

            self.current_chromosome.clear()
            self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')
            # self.env.reset()
            # self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')
            # while True:
            #     tmp = np.random.randint(0, 18)
            #     if self.map[0][tmp] == 0:
            #         break

        else:
            predict = self.current_chromosome.predict(input_data)
            # press_buttons = np.array([predict[5], 0, 0, 0, predict[0], predict[1], predict[2], predict[3], predict[4]])
            # self.env.step(press_buttons)
            press_buttons = np.array([predict[0], predict[1], predict[2], predict[3]])
            self.step(press_buttons)

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
        #     painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        #     for i in range(self.current_chromosome.l1.shape[0]):
        #         painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if self.current_chromosome.l1[i] == 0 else 1, 120 / 240)))
        #         painter.drawEllipse(self.screen_width + self.neural_network_l1_margin_x + i * 40, 240, 12 * 2, 12 * 2)
        #
        #     for i in range(predict.shape[0]):
        #         painter.setBrush(QBrush(QColor.fromHslF(0.8, 0 if predict[i] <= 0.5 else 1, 0.8)))
        #         painter.drawEllipse(self.screen_width + self.neural_network_predict_margin_x + i * 40, 440, 12 * 2, 12 * 2)
        #         text = ('U', 'D', 'L', 'R', 'A', 'B')[i]
        #         painter.drawText(self.screen_width + self.neural_network_predict_margin_x + i * 40 - 5, 470, text)
        #
        # painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventilation = Ventilation()
    exit(app.exec_())