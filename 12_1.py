import math
import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
                             QApplication,
                             QLineEdit,
                             QPushButton,
                             QMainWindow,
                             QLabel,
                             QButtonGroup,
                             QRadioButton,
                             QTextEdit,
                             QCheckBox)

SCREEN_SIZE = [1200, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_file = None
        self.coord_to_finde = None
        self.mark = False
        self.address = None
        self.not_clicked = True
        self.clicked_coord = None
        self.initUI()

    def getImage(self):
        d = {
            'схема': 'map',
            'спутник': 'sat',
            'гибрид': 'sat,skl'
        }
        coords = self.coord.text()
        z = self.zoom.text()
        map_type = d[self.button_group.checkedButton().text()]
        map_params = {
            'll': coords,
            'z': z,
            'l': map_type
            }
        if self.mark:
            if self.not_clicked:
                map_params['pt'] = '{0},pm2dgl'.format(self.coord_to_finde)
            else:
                map_params['pt'] = '{0},pm2dgl'.format(self.clicked_coord)
        map_api_server = 'http://static-maps.yandex.ru/1.x/'
        self.response = requests.get(map_api_server, params=map_params)
        if not self.response:
            print('Ошибка выполнения запроса:')
            print(self.response.url)
            print('Http статус:', self.response.status_code,
                  '(', self.response.reason, ')')
            raise ValueError
        else:
            self.map_file = 'map.png'
            with open(self.map_file, 'wb') as file:
                file.write(self.response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

        self.label = QLabel(self)
        self.label.setText(
            'Введите координаты\n(например:\n37.530887,55.7031188)')
        self.label.move(650, 0)
        self.label.resize(180, 60)

        self.coord = QLineEdit(self)
        self.coord.setText('2.294462,48.858602')
        self.coord.move(650, 60)
        self.coord.resize(200, 30)

        self.label1 = QLabel(self)
        self.label1.setText(
            'Введите масштаб\nцелое от 1 до 21')
        self.label1.move(650, 100)
        self.label1.resize(180, 40)

        self.zoom = QLineEdit(self)
        self.zoom.setText('17')
        self.zoom.move(650, 140)
        self.zoom.resize(200, 30)

        self.choice_1 = QRadioButton(self)
        self.choice_1.setText('схема')
        self.choice_1.setChecked(True)
        self.choice_1.move(650, 170)

        self.choice_2 = QRadioButton(self)
        self.choice_2.setText('спутник')
        self.choice_2.move(650, 190)

        self.choice_3 = QRadioButton(self)
        self.choice_3.setText('гибрид')
        self.choice_3.move(650, 210)

        self.run_button = QPushButton(self)
        self.run_button.move(650, 240)
        self.run_button.resize(180, 30)
        self.run_button.setText('Выполнить')
        self.run_button.clicked.connect(self.run)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.choice_1)
        self.button_group.addButton(self.choice_2)
        self.button_group.addButton(self.choice_3)

        self.label2 = QLabel(self)
        self.label2.setText(
            'Введите поисковый\nзапрос (например: Спб+\nЗвездная+2)')
        self.label2.move(650, 280)
        self.label2.resize(180, 50)

        self.req = QLineEdit(self)
        self.req.setText('Звездная+4')
        self.req.move(650, 330)
        self.req.resize(400, 30)

        self.find_button = QPushButton(self)
        self.find_button.move(650, 370)
        self.find_button.resize(180, 30)
        self.find_button.setText('Найти')
        self.find_button.clicked.connect(self.find)

        self.reset_button = QPushButton(self)
        self.reset_button.move(650, 410)
        self.reset_button.resize(180, 30)
        self.reset_button.setText('Сброс')
        self.reset_button.clicked.connect(self.reset)

        self.label3 = QLabel(self)
        self.label3.setText(
            'Адрес объекта')
        self.label3.move(950, 5)
        self.label3.resize(180, 20)

        self.show_address = QTextEdit(self)
        self.show_address.setReadOnly(True)
        self.show_address.move(950, 30)
        self.show_address.resize(200, 60)

        self.show_index = QCheckBox(self)
        self.show_index.setText('Индекс')
        self.show_index.move(950, 100)

        self.label4 = QLabel(self)
        self.label4.setText(
            'Введите организацию\nдля поиска кликните\nправой кнопкой мыши\n' +
            'в районе поиска')
        self.label4.move(950, 150)
        self.label4.resize(180, 65)

        self.org = QLineEdit(self)
        self.org.setText('аптека')
        self.org.move(950, 225)
        self.org.resize(200, 30)

    def reset(self):
        self.coord_to_finde = None
        self.mark = False
        self.address = None
        self.show_address.clear()
        self.req.clear()
        self.run()

    def find(self):
        geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
        toponym_to_find = self.req.text()
        geocoder_params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode': toponym_to_find,
            'format': 'json'
            }

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            print('Ошибка выполнения запроса:')
            print(self.response.url)
            print('Http статус:', self.response.status_code,
                  '(', self.response.reason, ')')
            raise ValueError
        else:
            json_response = response.json()
            toponym = json_response['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']
            toponym_index = toponym["metaDataProperty"][
                "GeocoderMetaData"]["Address"].get(
                    'postal_code', 'без индекса')
            if self.show_index.isChecked():
                self.address = toponym_index + ", " + toponym[
                    "metaDataProperty"]["GeocoderMetaData"]["text"]
            else:
                self.address = toponym["metaDataProperty"][
                    "GeocoderMetaData"]["text"]
            toponym_coordinates = toponym['Point']['pos']
            toponym_longitude, toponym_latitde = toponym_coordinates.split(' ')
            self.coord_to_finde = ','.join(
                [toponym_longitude, toponym_latitde])
            if self.not_clicked:
                self.coord.setText(self.coord_to_finde)
            self.show_address.setText(self.address)
            self.mark = True
            self.run()
            self.not_clicked = True

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos() in self.image.rect():
                self.image.setFocus()
                position = event.pos()
                x, y = position.x(), position.y()
                dx, dy = x - 300, 225 - y
                lon_center, lat_center = self.get_coords()
                zoom = int(self.zoom.text())
                lon = lon_center + (360 / 2 ** (8 + zoom)) * dx
                lat = lat_center + (180 / 2 ** (8 + zoom)) * dy
                self.clicked_coord = self.set_coords((lon, lat))
                self.req.setText(self.set_coords((round(lon, 6), round(lat, 6)
                                                  )))
                self.not_clicked = False
                self.find()
        if event.button() == Qt.MouseButton.RightButton:
            if event.pos() in self.image.rect():
                self.image.setFocus()
                position = event.pos()
                x, y = position.x(), position.y()
                dx, dy = x - 300, 225 - y
                lon_center, lat_center = self.get_coords()
                zoom = int(self.zoom.text())
                lon = lon_center + (360 / 2 ** (8 + zoom)) * dx
                lat = lat_center + (180 / 2 ** (8 + zoom)) * dy
                self.clicked_coord = self.set_coords((lon, lat))
                search_api_server = 'https://search-maps.yandex.ru/v1/'
                api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
                dist = 50 * 2
                long_dist = dist / ((40075696 / 360)
                                    * math.cos(math.radians(lat)))
                lat_dist = dist / (40008550 / 360)
                spn = ','.join([str(round(long_dist, 6)),
                                str(round(lat_dist, 6))])
                search_params = {
                    'apikey': api_key,
                    'text': self.org.text(),
                    'lang': 'ru_RU',
                    'll': self.clicked_coord,
                    'spn': spn,
                    'rspn': 1,
                    'type': 'biz'
                }

                response = requests.get(search_api_server,
                                        params=search_params)
                if not response:
                    self.reset()
                else:
                    json_response = response.json()
                    if json_response['features']:
                        organization = json_response['features'][0]
                        org_name = organization['properties'][
                            'CompanyMetaData']['name']
                        org_address = organization['properties'][
                            'CompanyMetaData']['address']
                        self.req.setText(', '.join([org_name, org_address]))
                        self.show_address.setText(org_address)
                    else:
                        self.reset()

    def run(self):
        try:
            self.image.setFocus()
            if not self.coord.text():
                self.statusBar().showMessage('Введите координаты!')
            elif not self.zoom.text():
                self.zoom.setText('17')
                self.statusBar().showMessage('Уровень масштабирования' +
                                             'по умолчанию равен 17!')
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
            elif int(self.zoom.text()) < 1 or int(self.zoom.text()) > 21:
                self.statusBar().showMessage('Соблюдайте пределы ' +
                                             'масштабирования!')
            else:
                self.statusBar().showMessage('')
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
        except Exception as err:
            self.statusBar().showMessage(err.__class__.__name__)

    def get_coords(self):
        coords = self.coord.text().split(',')
        coords = list(map(lambda i: float(i), coords))
        return coords

    def set_coords(self, coords):
        coords = list(map(lambda i: str(i), coords))
        x = ','.join(coords)
        return x

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            try:
                k = int(self.zoom.text())
                k += 1
                self.zoom.setText(str(k))
                self.run()
            except Exception as err:
                self.statusBar().showMessage(err.__class__.__name__)
        if event.key() == Qt.Key_PageDown:
            try:
                k = int(self.zoom.text())
                k -= 1
                self.zoom.setText(str(k))
                self.run()
            except Exception as err:
                self.statusBar().showMessage(err.__class__.__name__)
        if event.key() == Qt.Key_Left:
            coords = self.get_coords()
            zoom = int(self.zoom.text())
            lon = round(coords[0] - ((360 / 2 ** (8 + zoom)) * 600), 6)
            if lon > -180:
                coords[0] = lon
            self.coord.setText(self.set_coords(coords))
            self.run()
        if event.key() == Qt.Key_Right:
            coords = self.get_coords()
            zoom = int(self.zoom.text())
            lon = round(coords[0] + ((360 / 2 ** (8 + zoom)) * 600), 6)
            if lon < 180:
                coords[0] = lon
            self.coord.setText(self.set_coords(coords))
            self.run()
        if event.key() == Qt.Key_Up:
            coords = self.get_coords()
            zoom = int(self.zoom.text())
            lat = round(coords[1] + ((180 / 2 ** (8 + zoom)) * 450), 6)
            if lat < 90:
                coords[1] = lat
            self.coord.setText(self.set_coords(coords))
            self.run()
        if event.key() == Qt.Key_Down:
            coords = self.get_coords()
            zoom = int(self.zoom.text())
            lat = round(coords[1] - ((180 / 2 ** (8 + zoom)) * 450), 6)
            if lat > -90:
                coords[1] = lat
            self.coord.setText(self.set_coords(coords))
            self.run()

    def closeEvent(self, event):
        if self.map_file:
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
