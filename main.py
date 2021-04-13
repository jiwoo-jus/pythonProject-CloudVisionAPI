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
        self.resize(300, 300)
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)
        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        addbutton1 = QPushButton('Open File', self)
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(addbutton1, 2, 1)
        addbutton1.clicked.connect(self.add_open)
        addbutton2 = QPushButton('Save File', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        self.Lgrid.addWidget(addbutton2, 4, 1)
        addbutton2.clicked.connect(self.add_save)
        addbutton3 = QPushButton('Run', self)
        self.Lgrid.addWidget(self.label3, 5, 1)
        self.Lgrid.addWidget(addbutton3, 6, 1)
        addbutton3.clicked.connect(self.detect_text)
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
        # 텍스트 파일 내용 리스트 형태로 변수에 담기
        with codecs.open(self.label1.text(), 'r', 'utf-8') as f:
            b = f.readlines()

        # pdfotext했을 때 생긴 공백문장과 줄바꿈문자 삭제
        # i = 0
        # while (i < len(b)):
        #     if b[i] == "\r\n":  # 줄바꿈으로만 이루어진 문장 삭제
        #         b.pop(i)
        #         i -= 1
        #     elif b[i][-2:] == "\r\n":  # 줄바꿈 삭제
        #         b[i] = b[i][:-2]
        #     elif b[i] == "\n":  # 줄바꿈 삭제
        #         b[i] = b[i][:-1]
        #     i += 1

        # 문장 사이 개행 없애기
        for i in range(len(b) - 1):
            l1 = b[i].split()[-1] if (len(b[i]) >= 2) else ""
            l2 = b[i + 1].split()[0] if (len(b[i + 1]) >= 2) else ""
            str = l1 + l2  # i번째줄 문장의 끝 단어와 i+1번째줄 문장의 첫 단어를 일단 붙인다
            # print(spell_checker.check(str).errors, spell_checker.check(str).original, spell_checker.check(str).checked)
            if (spell_checker.check(str).errors > 0):  # 맞춤법검사해서 에러 있으면 i번째 문장 끝에 띄어쓰기(공백) 붙여서 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(b[i] + " ")
                # print("fiexd newline : ", b[i] + " ")
            else:  # 맞춤법검사해서 에러 없으면 i번째 문장 그대로 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(b[i])

        self.label3.setText('Successed')


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
