# [도전과제9]
# 07. get_current_screen_tile.py 에서 가져온 현재 타일 정보 그리기

import sys
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication,\
    QWidget, QLabel, QPushButton
import numpy as np

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 고정
        self.setFixedSize(820, 448)
        # 창 제목 설정
        self.setWindowTitle('Ventilation')

        self.press_buttons = [0, 0, 0, 0]
        #self.full_screen_tiles = np.array([0])
        #self.i = 0

        # 이미지
        # self.label_image = QLabel(self)
        self.map = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')
        # self.map2 = np.load('C:/Users/user/Documents/GitHub/Ventilation-AI/map/map1.npy')

        # for i in range(18):
        #     if self.map[0][i] == 0:
        #         self.x = 0
        #         self.y = i
        #
        #         # 타이머 생성
        #         self.qtimer = QTimer(self)
        #         # 타이머에 호출할 함수 연결
        #         self.qtimer.timeout.connect(self.game_timer)
        #         # 1초(1000밀리초)마다 연결된 함수를 실행
        #         self.qtimer.start(1000)
        #
        #         self.show()
        while True:
            tmp = np.random.randint(0, 18)
            if self.map[0][tmp] == 0:
                break

        self.x = 0
        self.y = tmp

        # 타이머 생성
        self.qtimer = QTimer(self)
        # 타이머에 호출할 함수 연결
        self.qtimer.timeout.connect(self.game_timer)
        # 1초(1000밀리초)마다 연결된 함수를 실행
        self.qtimer.start(1000)

        self.show()

    def paintEvent(self, event):
        # self.ram = self.env.get_ram()

        # 위쪽 타일 배열
        # full_screen_tiles = self.ram[0x0500:0x069F + 1]
        # full_screen_tile_count = full_screen_tiles.shape[0]

        # 정수여야 해서 / 2개
        # full_screen_page1_tile = full_screen_tiles[0:full_screen_tile_count // 2].reshape((13, 16))
        # full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        # full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

        # 아래쪽 타일 배열
        # 0x071A	Current screen (in level)
        # 현재 화면이 속한 페이지 번호
        # current_screen_page = self.ram[0x071A]
        # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
        # 페이지 속 현재 화면 위치
        # screen_position = self.ram[0x071C]
        # 화면 오프셋
        # screen_offset = (256 * current_screen_page + screen_position) % 512
        # 타일 화면 오프셋
        # screen_tile_offset = screen_offset // 16

        # 현재 화면 추출
        # screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:,
                       # screen_tile_offset:screen_tile_offset + 16]

        #print(screen_tiles)

        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        # 481부터 그리기
        # Gray 107 107 107
        # RGB 색상으로 펜 설정
        #print(self.full_screen_tiles.shape)
        # c = full_screen_tiles.shape[0]
        # for i in range(0, c):
        #print(full_screen_tiles.size)
        cnt = 0
        a = 0
        b = 0
        #print(full_screen_tiles)

        painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        # 브러쉬 설정 (채우기)
        painter.setBrush(QBrush(Qt.white))
        # 직사각형 (왼쪽 위, 오른쪽 아래)
        # 1200, 448

        t = 0

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
            #print(cnt)
            if cnt % 18 == 0:
                a = 0
                b += 16
                t += 1
        # t = 0
        # for i in range(208):
        #     # print(t, i)
        #     cnt += 1
        #     if screen_tiles[t][i % 16] == 0:
        #         painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        #         # 브러쉬 설정 (채우기)
        #         painter.setBrush(QBrush(Qt.gray))
        #         painter.drawRect(480 + a, 20 + b, 10, 10)
        #     else:
        #         painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        #         # 브러쉬 설정 (채우기)
        #         painter.setBrush(QBrush(Qt.blue))
        #         painter.drawRect(480 + a, 20 + b, 10, 10)
        #     a += 10
        #     # print(cnt)
        #     if cnt % 16 == 0:
        #         a = 0
        #         b += 10
        #         t += 1


    # def update_screen(self):
        # # 화면 가져오기
        # self.screen = self.env.get_screen()

        # screen_qimage = QImage(self.screen, self.screen.shape[1], self.screen.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap(screen_qimage)
        # pixmap = pixmap.scaled(480, 448, Qt.IgnoreAspectRatio)
        # #pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        # self.label_image.setPixmap(pixmap)

    def step(self):
        if self.press_buttons[0] == 1:
            if self.map[self.x - 1][self.y] == 0:
                self.map[self.x - 1][self.y] = 2
                self.map[self.x][self.y] = 0
                self.x = self.x - 1
        elif self.press_buttons[1] == 1:
            if self.map[self.x + 1][self.y] == 0:
                self.map[self.x + 1][self.y] = 2
                self.map[self.x][self.y] = 0
                self.x = self.x + 1
        elif self.press_buttons[2] == 1:
            if self.map[self.x][self.y - 1] == 0:
                self.map[self.x][self.y - 1] = 2
                self.map[self.x][self.y] = 0
                self.y = self.y - 1
        elif self.press_buttons[3] == 1:
            if self.map[self.x][self.y + 1] == 0:
                self.map[self.x][self.y + 1] = 2
                self.map[self.x][self.y] = 0
                self.y = self.y + 1

    def game_timer(self):
        # 키 배열: B, NULL, SELECT, START, U, D, L, R, A
        # b = 66, u = 16777235, d = 16777237, l = 16777234, r = 16777236, a = 65
        # self.env.step(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.step()
        # self.update_screen()
        self.update()
        #print(self.press_buttons)

        #print(self.screen)

    # 키를 누를 때
    # def keyPressEvent(self, event):
    #     key = event.key()
    #     print(str(key) + ' press')

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777235:
            self.press_buttons[0] = 1
        elif key == 16777237:
            self.press_buttons[1] = 1
        elif key == 16777234:
            self.press_buttons[2] = 1
        elif key == 16777236:
            self.press_buttons[3] = 1

    # 키를 뗄 때
    # def keyReleaseEvent(self, event):
    #     key = event.key()
    #     print(str(key) + ' release')

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == 16777235:
            self.press_buttons[0] = 0
        elif key == 16777237:
            self.press_buttons[1] = 0
        elif key == 16777234:
            self.press_buttons[2] = 0
        elif key == 16777236:
            self.press_buttons[3] = 0


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   sys.exit(app.exec_())