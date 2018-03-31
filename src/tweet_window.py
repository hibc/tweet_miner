from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDir
from tweet_mine import *

import tweet_mine as tw
import sys
import os
import subprocess, shlex
# import json

current_os = sys.platform
mine_status = True
verified_user = None
num_of_tweets = 0

class TweetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.twitter_config_box = self.twitter_config_group_box()
        self.file_config_box = self.file_info_layout()
        self.search_box = self.search_layout()

        self.main_layout(twitter_config_box=self.twitter_config_box,
        file_config_box=self.file_config_box,
        search_box=self.search_box)
        self.mine_process = None

    def twitter_config_group_box(self):
        
        tw_group_box = QGroupBox("Twitter Token Config")

        tw_consumer_key = QLabel('Twitter Consumer Key:')
        tw_consumer_secret = QLabel('Twitter Consumer Secret:')
        tw_access_token = QLabel('Twitter Access Token:')
        tw_access_secret = QLabel('Twitter Access Secret:')

        self.tw_consumer_key_edit = QLineEdit()
        self.tw_consumer_secret_edit = QLineEdit()
        self.tw_access_token_edit = QLineEdit()
        self.tw_access_secret_edit = QLineEdit()

        tw_layout = QGridLayout()
        tw_layout.setSpacing(5)

        tw_layout.addWidget(tw_consumer_key, 1, 0)
        tw_layout.addWidget(self.tw_consumer_key_edit, 1, 1, 1, 4)
        tw_layout.addWidget(tw_consumer_secret, 2, 0)
        tw_layout.addWidget(self.tw_consumer_secret_edit, 2, 1, 1, 4)

        tw_layout.addWidget(tw_access_token, 3, 0)
        tw_layout.addWidget(self.tw_access_token_edit, 3, 1, 1, 4)
        tw_layout.addWidget(tw_access_secret, 4, 0)
        tw_layout.addWidget(self.tw_access_secret_edit, 4, 1, 1, 4)
        tw_group_box.setLayout(tw_layout)

        return tw_group_box


    def file_info_layout(self):
        file_group_box = QGroupBox("File Settings config")

        file_name_text = QLabel('Enter a file name:')
        self.file_line_edit = QLineEdit()
        self.file_line_edit.setPlaceholderText(" ex. file1")
        file_location_text = QLabel('Save file to:')
        self.file_location_line_edit = QLineEdit()
        self.file_location_line_edit.setPlaceholderText(" ex. /Users/user/Desktop/")
        file_browse_btn = QPushButton('Browse', self)
        file_browse_btn.clicked.connect(self.file_browse_dialog)
        
        file_layout = QGridLayout()
        file_layout.setSpacing(5)
        file_layout.addWidget(file_name_text, 0, 0)
        file_layout.addWidget(self.file_line_edit, 0, 1, 1 , 3)
        file_layout.addWidget(file_location_text, 1, 0)
        file_layout.addWidget(self.file_location_line_edit, 1, 1)
        file_layout.addWidget(file_browse_btn, 1, 2)
        file_group_box.setLayout(file_layout)
        
        return file_group_box
    
    def file_browse_dialog(self):
        default_directory = ""
        
        if current_os == 'darwin':
            default_directory = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        elif current_os == 'win32':
            default_directory = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        
#         print('default directory is ' + default_directory)
        directory_path = QFileDialog.getExistingDirectory(self, "Browse File", default_directory, QFileDialog.ShowDirsOnly)
#         print("file_directry: " + QDir.toNativeSeparators(directory_path))
        self.file_location_line_edit.setText(QDir.toNativeSeparators(directory_path))

    def search_layout(self):
        search_main_box = QGroupBox("Search config and box")
        
        search_main_layout = QHBoxLayout()
        search_config_group = QGroupBox("Search Config (Optional)")
        search_config_layout = QGridLayout()
        search_config_location_label = QLabel("Location:")
        self.search_config_location_input = QLineEdit()
        search_config_language_label = QLabel("Language:")
        self.search_config_language_input = QLineEdit()
        search_config_follow_id_label = QLabel("Twitter ID to follow:")
        self.search_config_follow_id_input = QLineEdit()
        
        search_config_layout.addWidget(search_config_location_label, 0, 0)
        search_config_layout.addWidget(self.search_config_location_input, 0, 1)
        search_config_layout.addWidget(search_config_language_label, 1, 0)
        search_config_layout.addWidget(self.search_config_language_input, 1, 1)
        search_config_layout.addWidget(search_config_follow_id_label, 2, 0)
        search_config_layout.addWidget(self.search_config_follow_id_input, 2, 1)          
        search_config_group.setLayout(search_config_layout)

        search_box_group = QGroupBox("Search Box")
        search_box_layout = QGridLayout()    
        self.search_box_txt_edit = QTextEdit()
        self.search_box_txt_edit.setPlaceholderText("Enter your search terms separated by a comma. ex. Korea_Town, KBBQ, Good_Doctor")
        search_box_layout.addWidget(self.search_box_txt_edit)
        search_box_group.setLayout(search_box_layout)
        search_main_layout.addWidget(search_config_group)
        search_main_layout.addWidget(search_box_group)

        search_main_box.setLayout(search_main_layout)

        return search_main_box
        
    def on_click_mine_start_btn(self):
        if ( len(self.tw_consumer_key_edit.text()) == 0 or len(self.tw_consumer_secret_edit.text())==0 \
            or len(self.tw_access_secret_edit.text()) == 0 or len(self.tw_access_token_edit.text())==0):
            self.show_required_dialog()
            return
        
        twitter_info_all = {
            "TwitterConfig": {            
                "consumer_key": self.tw_consumer_key_edit.text(),
                "consumer_secret": self.tw_consumer_secret_edit.text(),
                "access_token": self.tw_access_token_edit.text(),
                "access_secret": self.tw_access_secret_edit.text() 
            },
            "FileConfig": {            
                'name': self.file_line_edit.text(),
                'location': self.file_location_line_edit.text(),
                'full_path': QDir.toNativeSeparators(self.file_location_line_edit.text() + '/' + self.file_line_edit.text())
            }, 
            "SearchConfig":{
                'location': self.search_config_location_input.text(),
                'language': self.search_config_language_input.text(),
                'follow_id': self.search_config_follow_id_input.text(),
                'keyword': self.search_box_txt_edit.toPlainText()
            }
        }

        cmd = "python tweet_mine.py --consumer_key \'" + twitter_info_all["TwitterConfig"]['consumer_key'] +\
        "\' --consumer_secret \'" + twitter_info_all["TwitterConfig"]['consumer_secret'] +\
        "\' --access_token \'" + twitter_info_all["TwitterConfig"]['access_token'] +\
        "\' --access_secret \'" + twitter_info_all["TwitterConfig"]['access_secret'] +\
        "\' --track \'" + twitter_info_all["SearchConfig"]["keyword"] +\
        "\' --file_path \'" + twitter_info_all["FileConfig"]["full_path"]+\
        "\' --locations \'" + twitter_info_all["SearchConfig"]["location"]+\
        "\' --follow \'" + twitter_info_all["SearchConfig"]["follow_id"]+\
        "\' --languages \'" + twitter_info_all["SearchConfig"]["language"] + "\'"
        
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        self.mine_process = process
        
        self.show_mine_start_stop_message_dialog(start=True)

    def show_required_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Twitter Tweet Miner")
        msg_box.setText("Configurations cannot be blank!!")
        
        try:
            msg_box.exec_()
        except Exception as e:
            print(str(e))
    
    def show_user_unverified_dialog(self):
        print("Unverified User")
        if self.mine_process is not None:
            self.mine_process.kill()
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Twitter Tweet Miner")
        msg_box.setText("Please check your Twitter token configuration again !!")
        
        try:
            msg_box.exec_()
        except Exception as e:
            print(str(e))
  
    def on_click_mine_stop_btn(self):
        mine_status = False

        if self.mine_process is not None:
            self.mine_process.kill()

        self.show_mine_start_stop_message_dialog(start=False)

    def show_mine_start_stop_message_dialog(self, start=False):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Twitter Tweet Miner")
        if start is False:
            msg_box.setText("Mining has stopped !!")
        else:
            msg_box.setText("Mining has started !!")
        
        try:
            msg_box.exec_()
        except Exception as e:
            print(str(e))

    
    def main_layout(self, twitter_config_box=None, file_config_box=None, search_box=None):
        # self.setGeometry(100, 500, 150, 500)
        self.setWindowTitle('Twitter Tweet Miner')

        css_file = "./data/css/widgetStyleSheet.txt"
        with open(css_file, 'r') as css:
            self.setStyleSheet(css.read())
        
        main = QVBoxLayout()
        
        main_top_box = QGroupBox()
        main_top = QHBoxLayout()
        main_top.addWidget(twitter_config_box)
        main_top.addWidget(file_config_box)
        main_top_box.setLayout(main_top)
        
        main.addWidget(main_top_box)
        main.addWidget(search_box)


        mine_btn_group = QGroupBox('Mine Button Group')
        mine_btn_layout = QGridLayout()
        mine_start_btn = QPushButton('START MINING')
        mine_start_btn.clicked.connect(self.on_click_mine_start_btn)
        mine_stop_btn = QPushButton('STOP MINING')
        mine_stop_btn.clicked.connect(self.on_click_mine_stop_btn)
        mine_btn_layout.addWidget(mine_start_btn, 0, 0)
        mine_btn_layout.addWidget(mine_stop_btn, 0, 1)
        
        mine_btn_group.setLayout(mine_btn_layout)

        main.addWidget(mine_btn_group)

        self.setLayout(main)
        self.show()

        
