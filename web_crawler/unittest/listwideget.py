from PyQt5 import QtWidgets


class ListWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ListWidget, self).__init__()
        self.lable = QtWidgets.QLabel()
        self.lable.setFixedWidth(70)
        self.lable.setText('process')
        self.listWidget = QtWidgets.QListWidget()
        self.layout = QtWidgets.QVBoxLayout()
        item = QtWidgets.QListWidgetItem()
        item.setText('item')
        self.listWidget.addItem(item)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.lable)
        self.setLayout(self.layout)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lw = ListWidget()
    lw.resize(400, 200)
    lw.show()
    sys.exit(app.exec_())
