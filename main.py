import codecs
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from hanspell import spell_checker

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\WorkSpace\pycharm\jw-img2txt-8f65dde3d9fb.json"

class QtGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.setWindowTitle("Appia Qt GUI")
        self.resize(300, 400)
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)
        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        self.label4 = QLabel('', self)
        addbutton1 = QPushButton('Open File', self)
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(addbutton1, 2, 1)
        addbutton1.clicked.connect(self.add_open)
        addbutton2 = QPushButton('Save File', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        self.Lgrid.addWidget(addbutton2, 4, 1)
        addbutton2.clicked.connect(self.add_save)
        addbutton3 = QPushButton('원본 형태', self)
        self.Lgrid.addWidget(self.label3, 5, 1)
        self.Lgrid.addWidget(addbutton3, 6, 1)
        addbutton3.clicked.connect(self.detect_text)
        addbutton4 = QPushButton('줄바꿈 제거 형태', self)
        self.Lgrid.addWidget(self.label4, 7, 1)
        self.Lgrid.addWidget(addbutton4, 8, 1)
        addbutton4.clicked.connect(self.removeNewLine)
        self.show()

    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\parkj\Downloads')

        self.label1.setText(FileOpen[0])

    def add_save(self):
        savepath = self.label1.text()
        savepath = savepath.split('/')
        filename = savepath.pop()
        filename = filename.capitalize()  # str.capitalize()는 str의 첫 글자만을 대문자로, 나머지는 전부 소문자로 바꾼 str을 return해 줍니다.
        savepath = ('\\').join(savepath) + '\\New' + filename

        FileSave = QFileDialog.getSaveFileName(self, 'Save file', savepath)

        self.label2.setText(FileSave[0])

    def detect_text(self):
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        path = self.label1.text()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        text = texts[0]

        with open(self.label2.text(), 'w', encoding='utf-8') as f:
            f.write(format(text.description))

        # print('\n"{}"'.format(text.description))
        self.label3.setText('Successed')

    def removeNewLine(self):
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        path = self.label1.text()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        text = format(texts[0].description).split("\n")

        for i in range(len(text) - 1):
            l1 = text[i].split()[-1] if (len(text[i]) >= 2) else ""
            l2 = text[i + 1].split()[0] if (len(text[i + 1]) >= 2) else ""
            str = l1 + l2  # i번째줄 문장의 끝 단어와 i+1번째줄 문장의 첫 단어를 일단 붙인다
            # print(spell_checker.check(str).errors, spell_checker.check(str).original, spell_checker.check(str).checked)
            if (spell_checker.check(str).errors > 0):  # 맞춤법검사해서 에러 있으면 i번째 문장 끝에 띄어쓰기(공백) 붙여서 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(text[i] + " ")
                # print("fiexd newline : ", b[i] + " ")
            else:  # 맞춤법검사해서 에러 없으면 i번째 문장 그대로 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(text[i])

        self.label4.setText('Successed')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()

    app.exec_()



























# import os
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\WorkSpace\pycharm\jw-img2txt-8f65dde3d9fb.json"
#
# def detect_text(path):
#     """Detects text in the file."""
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()
#
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#
#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')
#
#     text = texts[0]
#     print('\n"{}"'.format(text.description))
#
#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources\\book2.jpg')
#
# detect_text(file_name)
#
#
