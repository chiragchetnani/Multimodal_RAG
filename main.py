from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QFileDialog, QListWidgetItem, QStackedWidget, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt
import os
import shutil
import sys

# Import the necessary functions from the provided backend script
from discriminator import categorize_files
from doc_extract import pdf, docx_, pptx, csv, txt
from image_extract import image_text
from video_extract import video_transcript
from answer import answer

class UserNameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Enter your name:')
        self.label.setStyleSheet("font-size: 20px; color: white;")
        layout.addWidget(self.label)

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("background-color: #222; color: white;")
        layout.addWidget(self.name_input)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet("background-color: #444; color: white;")
        self.submit_button.clicked.connect(self.submitName)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #111; padding: 20px;")

    def submitName(self):
        name = self.name_input.text()
        if name:
            self.parentWidget().user_name = name
            self.parentWidget().setCurrentIndex(1)
            self.parentWidget().chat_bot_ui.updateUserName(name)

class ChatBotUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # File upload section
        file_upload_layout = QVBoxLayout()
        
        file_upload_title = QLabel('File Upload')
        file_upload_title.setStyleSheet("font-size: 20px; color: white;")
        file_upload_layout.addWidget(file_upload_title)
        
        file_upload_subtitle = QLabel('You can add any type of readable file')
        file_upload_subtitle.setStyleSheet("color: gray;")
        file_upload_layout.addWidget(file_upload_subtitle)
        
        choose_files_btn = QPushButton('Choose Files')
        choose_files_btn.clicked.connect(self.openFileDialog)
        choose_files_btn.setStyleSheet("background-color: #333; color: white; border: 1px dashed gray;")
        file_upload_layout.addWidget(choose_files_btn)
        
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #222; color: white;")
        file_upload_layout.addWidget(self.file_list)

        self.user_name_btn = QPushButton("User's Name")
        self.user_name_btn.setStyleSheet("background-color: #444; color: white;")
        file_upload_layout.addWidget(self.user_name_btn)

        file_upload_container = QWidget()
        file_upload_container.setLayout(file_upload_layout)
        file_upload_container.setStyleSheet("background-color: #111; padding: 20px;")

        # Chatbot section
        chatbot_layout = QVBoxLayout()

        chatbot_title = QLabel('Chat-Bot')
        chatbot_title.setStyleSheet("font-size: 20px; color: white;")
        chatbot_layout.addWidget(chatbot_title)
        
        chatbot_subtitle = QLabel('Get your answers from any files')
        chatbot_subtitle.setStyleSheet("color: gray;")
        chatbot_layout.addWidget(chatbot_subtitle)

        self.card_content = QTextEdit()
        self.card_content.setReadOnly(True)
        self.card_content.setStyleSheet("background-color: #222; color: white;")
        chatbot_layout.addWidget(self.card_content)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message Chat-Bot")
        self.message_input.setStyleSheet("background-color: #222; color: white;")
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #444; color: white;")
        self.send_button.clicked.connect(self.processUserInput)

        message_layout = QHBoxLayout()
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)

        chatbot_layout.addLayout(message_layout)

        chatbot_container = QWidget()
        chatbot_container.setLayout(chatbot_layout)
        chatbot_container.setStyleSheet("background-color: #111; padding: 20px;")

        # Set widths for both sections
        main_layout.addWidget(file_upload_container, 30)
        main_layout.addWidget(chatbot_container, 70)

        self.setLayout(main_layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Files", "", "All Files (*);;Text Files (*.txt)", options=options)
        if files:
            self.ensureDirectoryExists('uploaded_files')
            for file in files:
                shutil.copy(file, 'uploaded_files')  # Copy files to the directory
                self.addFileToList(file)
            self.processFiles(files)

    def ensureDirectoryExists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def addFileToList(self, file):
        item = QListWidgetItem()
        widget = QWidget()
        layout = QGridLayout()
        
        file_label = QLabel(os.path.basename(file))
        file_label.setStyleSheet("color: white;")
        layout.addWidget(file_label, 0, 0)
        
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("background-color: #444; color: white;")
        delete_button.clicked.connect(lambda: self.deleteFile(item, file))
        layout.addWidget(delete_button, 0, 1)
        
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        
        self.file_list.addItem(item)
        self.file_list.setItemWidget(item, widget)

    def deleteFile(self, item, file):
        self.file_list.takeItem(self.file_list.row(item))
        os.remove(os.path.join('uploaded_files', os.path.basename(file)))  # Remove file from the directory

    def updateUserName(self, name):
        self.user_name_btn.setText(name)

    def processFiles(self, files):
        self.context_text = ''
        for file in files:
            file_path = os.path.join('uploaded_files', os.path.basename(file))
            file_ext = file_path.split('.')[-1].lower()
            if file_ext == 'pdf':
                self.context_text += pdf(file_path)
            elif file_ext in ['docx', 'doc']:
                self.context_text += docx_(file_path)
            elif file_ext == 'pptx':
                self.context_text += pptx(file_path)
            elif file_ext == 'csv':
                self.context_text += csv(file_path)
            elif file_ext == 'txt':
                self.context_text += txt(file_path)
            elif file_ext in ['jpg', 'png', 'jpeg']:
                self.context_text += image_text(file_path)
            elif file_ext == 'mp4':
                self.context_text += video_transcript(file_path)
            os.remove(file_path)  # Optionally delete the file after processing if not needed

        self.card_content.setText(self.context_text)

    def processUserInput(self):
        user_input = self.message_input.text()
        if user_input and self.context_text:
            response = answer(user_input, self.context_text)
            self.card_content.append(f'User: {user_input}')
            self.card_content.append(f'Bot: {response}')
            self.message_input.clear()

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.user_name = ""

        self.user_name_screen = UserNameScreen()
        self.chat_bot_ui = ChatBotUI(self)

        self.addWidget(self.user_name_screen)
        self.addWidget(self.chat_bot_ui)

        self.setCurrentIndex(0)

        self.setWindowTitle('Chat-Bot UI')
        self.setGeometry(300, 300, 1200, 800)
        self.show()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
