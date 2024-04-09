# import tkinter as tk
# time


# root = tk.Tk()
# root.attributes('-zoomed', True)

# frame1 = tk.Label(root)
# frame1.pack(fill="both", expand=True)
# frame1.pack_propagate(False)
# frame1.config(text="thing1")

# frame2 = tk.Label(root)
# frame2.pack(fill="both", expand=True)
# frame2.pack_propagate(False)
# frame2.config(text="thing2")

# frame3 = tk.Label(root)
# frame3.pack(fill="both", expand=True)
# frame3.pack_propagate(False)
# frame3.config(text="thing3")

# root.mainloop()

# frame3.config(text="thingmultiple")

# def textchange():
#     if

from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Hello, World!", parent=self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Example')
        self.setGeometry()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.label.setText("butthead")
    sys.exit(app.exec_())