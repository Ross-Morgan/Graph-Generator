# Module imports
from PyQt6 import QtCore, QtGui, QtWidgets
import sys

# File imports
# from svg import SVGWriter

Any = object()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            window_size: tuple[int, int],
            window_title: str,
            window_icon: QtGui.QIcon,
            parent: QtWidgets.QWidget = None,
            **kwargs):

        super(MainWindow, self).__init__(parent)

        self.ui: dict[str, Any] = {}
        self.shortcuts: dict[str, QtGui.QShortcut] = {}

        self.setFixedSize(*window_size)
        self.setWindowTitle(window_title)
        self.setWindowIcon(window_icon)

        self.setup_ui()
        self.setup_shortcuts()

    @classmethod
    def child_window(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def setup_ui(self) -> None:
        box_names = ["days", "months", "years"]

        self.ui["form_layout"] = QtWidgets.QFormLayout(self)
        self.ui["form_layout"].setGeometry(QtCore.QRect(10, 10, 500, 175))
        self.ui["form_layout_rows"] = []

        for i in range(len(box_names)):
            spin_box = QtWidgets.QSpinBox(self)
            spin_box.resize(150, 50)

            # self.ui["form_layout_rows"].append()
            self.ui["form_layout"].addRow(box_names[i], spin_box)

        # self.setLayout(self.ui["form_layout"])

    def setup_shortcuts(self) -> None:
        QSct = QtGui.QShortcut
        QKSq = QtGui.QKeySequence

        self.shortcuts["exit"] = QSct(QKSq("ctrl+w"), self)
        self.shortcuts["exit"].activated.connect(self.close)
        # self.shortcuts
        # self.shortcuts


def main():
    app = QtWidgets.QApplication(sys.argv)

    WIDTH, HEIGHT = 640, 480
    TITLE = "Graph Generator"
    ICON = QtGui.QIcon("Assets/graph.png")

    window = MainWindow((WIDTH, HEIGHT), TITLE, ICON)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
