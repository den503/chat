import datetime
import time
import threading

import requests
from PyQt5 import QtWidgets
import design


class MessengerApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def send(self):
        username = self.login.text()
        password = self.password.text()
        text = self.inputText.toPlainText()

        if not username or not password or not text:
            return

        try:
            requests.post(
                'http://127.0.0.1:5000/send',
                json={'username': username, 'password': password, 'text': text}
            )
        except:
            pass

        self.inputText.setPlainText('')
        self.inputText.repaint()

    def receive(self):
        last_received = 0
        while True:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': last_received}
            )

            if response.status_code == 200:
                messages = response.json()['messages']
                for message in messages:
                    username = message['username']
                    time_msg = datetime.datetime.fromtimestamp(message['time'])
                    time_str = time_msg.strftime('%Y-%m-%d %H:%M:%S')
                    text = message['text']

                    self.messeges.append(f'{username} {time_str}')
                    self.messeges.append(text)
                    self.messeges.append('')
                    # self.messeges.repaint()

                    last_received = message['time']

            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessengerApp()
    window.show()
    app.exec_()
