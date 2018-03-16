from PyQt5.QtWidgets import QApplication, QWidget
from tweet_window import *
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tw = TweetWindow()
    sys.exit(app.exec_())