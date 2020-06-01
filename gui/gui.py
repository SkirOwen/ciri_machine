from cirilib.imports import *
from contextlib import redirect_stdout
import io
import traceback
import ClusteringCOVID19
import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, pyqtSlot, QRunnable, pyqtBoundSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QGroupBox,
                             QVBoxLayout, QWidget, QSlider, QFileDialog, QMainWindow, QAction, qApp,
                             QHBoxLayout, QFrame, QSplitter, QCheckBox, QDateEdit, QComboBox, QPushButton,
                             QRadioButton, QSpinBox)
from PyQt5.QtGui import QIcon

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class ExtractingDataThread(QThread):
    def __init__(self, **kwargs):
        super().__init__()
        self.args = kwargs

    def run(self):
        lockdown_split(**self.args)


class Canvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, dpi=100, **kwargs):
        self.fig, self.axes = ClusteringCOVID19.clustering("2020-03-17", "lockdown", **kwargs)
        super(Canvas, self).__init__(self.fig)

        # ClusteringCOVID19.clustering("2020-03-17", "lockdown3")

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_plot(self, **kwargs):
        self.fig, self.axes = ClusteringCOVID19.clustering("2020-03-17", "lockdown", **kwargs)
        FigureCanvas.updateGeometry(self)


class RawDataCanvas(Canvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        ClusteringCOVID19.clustering("2020-03-17", "lockdown3")


class AppForm(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.f = io.StringIO()

        # variable to by passed down to lockdown_split
        self.date_lockdown = ""
        self.lockdown_by_ctr = True
        self.drop_lc = False
        self.selected_data = None
        self.country = "Italy"
        self.csv_exp = True
        self.file_nm = None
        self.data_from_beg = True

        # Variable for clsustering
        self.file_nm_to_plot = None

        # variable for PyQt
        self.fl = ["--"]
        self.groupBoxSet = QGroupBox("Settings")
        self.radio_button2 = QHBoxLayout()
        self.radio_button1 = QHBoxLayout()
        self.axis_x_set = QHBoxLayout()
        self.axis_y_set = QHBoxLayout()
        self.k_clus = QSpinBox()
        self.k_clus_label = QLabel("k value for clustering")
        self.gr_sc4 = QRadioButton("Log")
        self.gr_sc3 = QRadioButton("Semilogy")
        self.gr_sc2 = QRadioButton("Semilogx")
        self.gr_sc1 = QRadioButton("Linear")
        self.gr_sc1.setChecked(True)
        self.gr_sc_label = QLabel("Graph Type:")
        self.ctr_labels = QCheckBox("Country Labels")
        self.y_axis_label = QLabel("y axis:")
        self.x_axis_label = QLabel("x axis:")
        self.y_axis = QComboBox()
        self.x_axis = QComboBox()
        self.gene_dtb = QPushButton("&Generate")
        self.gene_dtb_plt = QPushButton("Generate and &Plot")
        self.btn_plt = QPushButton("Plot")
        self.nm_fl_to_plt = QComboBox()
        self.groupBoxGen = QGroupBox("Generation of Database")
        self.nm_fl = QLineEdit()
        self.data_spt_bf = QCheckBox("Data computed from the beginning")
        self.data_spt_bf.setChecked(True)
        self.export_csv = QCheckBox("Export to .csv")
        self.export_csv.setChecked(True)
        self.lc_date = QDateEdit()
        self.dr_no_lc = QCheckBox("Drop no LC")
        self.q_lcd_b_cnt = QCheckBox("Lockdown by country")
        self.q_lcd_b_cnt.setChecked(True)
        self.dr_no_lc.setEnabled(True)
        self.output_rd = QtWidgets.QTextBrowser()
        self.main_widget = QtWidgets.QWidget(self)
        self.initUI()



        # Extract state for widgets
        self.gr_sc1.toggled.connect(lambda: self.btnstate(self.gr_sc1))
        self.gr_sc2.toggled.connect(lambda: self.btnstate(self.gr_sc2))
        self.gr_sc3.toggled.connect(lambda: self.btnstate(self.gr_sc3))
        self.gr_sc4.toggled.connect(lambda: self.btnstate(self.gr_sc4))
        self.q_lcd_b_cnt.stateChanged.connect(lambda: self.btnstate(self.q_lcd_b_cnt))
        self.dr_no_lc.stateChanged.connect(lambda: self.btnstate(self.dr_no_lc))
        self.ctr_labels.stateChanged.connect(lambda: self.btnstate(self.ctr_labels))
        self.data_spt_bf.stateChanged.connect(lambda: self.btnstate(self.data_spt_bf))
        self.export_csv.stateChanged.connect(lambda: self.btnstate(self.export_csv))
        self.lc_date.dateChanged.connect(self.onDateChanged)
        self.k_clus.valueChanged.connect(self.valuechange)
        self.nm_fl.textChanged.connect(self.textchanged)
        self.gene_dtb.clicked.connect(lambda: self.whichbtn(self.gene_dtb))
        self.gene_dtb_plt.clicked.connect(lambda: self.whichbtn(self.gene_dtb_plt))
        self.btn_plt.clicked.connect(lambda: self.whichbtn(self.btn_plt))
        # self.nm_fl_to_plt.textChanged.connect(self.textchanged_to_plt)
        self.x_axis.activated[str].connect(lambda: self.onChanged(self.x_axis, "x"))
        self.y_axis.activated[str].connect(lambda: self.onChanged(self.y_axis, "y"))
        self.nm_fl_to_plt.activated[str].connect(lambda: self.onChanged(self.nm_fl_to_plt, "plot"))

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.statusBar().showMessage('Ready')

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        # fileMenu = menubar.addAction("&Tools")

        fileMenu.addAction(exitAct)

        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle("Clustering")

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # hbox = QHBoxLayout(self)

        # splitter1 = QSplitter(Qt.Vertical)
        # splitter1.addWidget(QFrame().addWidget(self.GroupSettings()))
        # splitter1.addWidget(QFrame(self.output_rd).setFrameShape(QFrame.StyledPanel))

        # splitter2 = QSplitter(Qt.Horizontal)
        # splitter2.addWidget(self.GroupSettings())
        # splitter2.addWidget(splitter1)
        #
        # splitter3 = QSplitter(Qt.Horizontal)
        # splitter3.addWidget(self.GroupGraph())
        # splitter3.addWidget(splitter2)

        # hbox.addWidget(splitter2)
        # self.setLayout(hbox)

        grid = QGridLayout(self.main_widget)
        grid.addWidget(self.GroupGraph(), 0, 0, 3, 1)
        grid.addWidget(self.GroupSettings(), 0, 1)
        grid.addWidget(self.GroupGeneration(), 1, 1)
        grid.addWidget(self.output_rd, 2, 1)
        grid.setSpacing(10)

    def GroupGraph(self):
        # graphics and toolbars
        # Cd = ProcessDataCanvas(self.main_widget, width=5, height=5, dpi=100)
        # toolbarCd = NavigationToolbar(Cd, self)
        # attribute for graph
        self.Rd = Canvas(self.main_widget, dpi=100)
        self.toolbarRd = NavigationToolbar(self.Rd, self)

        groupBoxGraph = QGroupBox('Graphics and toolbars')
        vbox = QVBoxLayout()
        vbox.addWidget(self.toolbarRd)
        vbox.addWidget(self.Rd)
        # vbox.addWidget(toolbarCd)
        # vbox.addWidget(Cd)
        # vbox.addStretch(1)
        groupBoxGraph.setLayout(vbox)

        return groupBoxGraph

    def GroupSettings(self):
        # labelInfosK = QtWidgets.QLabel()
        # labelInfosK.setText('change k coeff slider \n(note: coeff was calculated to be optimal)')
        #
        # labelInfosA = QtWidgets.QLabel()
        # labelInfosA.setText(
        #     'change number of points for moving average \n(note: number of points was calculated to be optimal)')
        #
        self.x_axis.addItems(["Cases", "Deaths", "Growth Factor", "New Cases", "New Deaths"])
        self.y_axis.addItems(["New Cases", "New Deaths", "Growth Factor", "Cases", "Deaths"])

        self.nm_fl_to_plt.addItems(self.get_current_files_available())

        self.k_clus.setValue(3)

        # Layout for radio
        self.radio_button1.addSpacing(20)
        self.radio_button1.addWidget(self.gr_sc1)
        self.radio_button1.addSpacing(20)
        self.radio_button1.addWidget(self.gr_sc2)
        self.radio_button2.addSpacing(20)
        self.radio_button2.addWidget(self.gr_sc3)
        self.radio_button2.addSpacing(20)
        self.radio_button2.addWidget(self.gr_sc4)

        # Layout for axis
        self.axis_x_set.addWidget(self.x_axis_label)
        self.axis_x_set.addWidget(self.x_axis)
        self.axis_y_set.addWidget(self.y_axis_label)
        self.axis_y_set.addWidget(self.y_axis)

        # Main layout
        vbox = QVBoxLayout(self.groupBoxSet)
        vbox.addWidget(self.nm_fl_to_plt)
        vbox.addWidget(self.btn_plt)
        vbox.addSpacing(20)
        vbox.addLayout(self.axis_x_set)
        vbox.addLayout(self.axis_y_set)

        vbox.addWidget(self.ctr_labels)

        vbox.addWidget(self.gr_sc_label)
        vbox.addLayout(self.radio_button1)
        vbox.addLayout(self.radio_button2)

        vbox.addWidget(self.k_clus_label)
        vbox.addWidget(self.k_clus)

        vbox.addStretch(1)
        self.groupBoxSet.setLayout(vbox)

        return self.groupBoxSet

    def GroupGeneration(self):
        self.lc_date.setMinimumDate(datetime.datetime(year=2020, month=1, day=21))
        self.lc_date.setDisplayFormat("yyyy-MM-dd")
        # self.lc_date.setCalendarPopup(True)

        self.nm_fl.sizePolicy()
        self.nm_fl.setMaximumWidth(300)
        self.nm_fl.setFixedWidth(300)
        self.nm_fl.setPlaceholderText("- Enter a file name -")

        # Main layout
        vbox = QVBoxLayout(self.groupBoxGen)
        vbox.addWidget(self.q_lcd_b_cnt)
        vbox.addWidget(self.dr_no_lc)
        vbox.addWidget(self.lc_date)

        vbox.addWidget(self.export_csv)
        vbox.addWidget(self.data_spt_bf)
        vbox.addWidget(self.nm_fl)
        vbox.addWidget(self.gene_dtb_plt)
        vbox.addWidget(self.gene_dtb)
        vbox.addStretch(1)
        self.groupBoxGen.setLayout(vbox)

        return self.groupBoxGen

    # add if statement b.text for each widgets
    # def clickBox(self, state):
    #     if state == QtCore.Qt.Checked:
    #         self.lockdown_by_country = True
    #         self.output_rd.append("Lockdown by country set to True")
    #     else:
    #         self.lockdown_by_country = False
    #         self.output_rd.append("Lockdown by country set to False")

    def fileQuit(self):
        self.close()

    # Generate list of files name availble for plot
    def get_current_files_available(self):
        fl = os.listdir(CSV_DIR)
        fl = fl[:-len(fl) // 2]
        for i in range(len(fl)):
            self.fl.append(fl[i][6:-4])
        return self.fl

    # Get ComboBox value
    def onChanged(self, b, v):
        if v == "x":
            self.output_rd.append("x sele" + b.currentText())
        if v == "y":
            self.output_rd.append("x sele" + b.currentText())
        if v == "plot":
            self.output_rd.append("x sele" + b.currentText())

    # Get the filename
    def textchanged(self, text):
        if text == "":
            text = None
        self.file_nm = text
        self.output_rd.append("contents of text box: " + str(text))

    # Get the filename to plot
    def textchanged_to_plt(self, text):
        self.file_nm_to_plot = text
        self.output_rd.append("contents of text box: " + text)

    # Check value for K-Clustering
    def valuechange(self):
        self.output_rd.append("current value:" + str(self.k_clus.value()))

    # Date changed checking
    def onDateChanged(self, qDate):
        self.date_lockdown = "{:04d}-{:02d}-{:02d}".format(qDate.year(), qDate.month(), qDate.day())
        self.output_rd.append(self.date_lockdown)

    # Check button state
    def btnstate(self, b):

        if b.text() == "Linear":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
            else:
                self.statusBar().showMessage(b.text() + " is deselected")

        if b.text() == "Log":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
            else:
                self.statusBar().showMessage(b.text() + " is deselected")

        if b.text() == "Semilogx":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
            else:
                self.statusBar().showMessage(b.text() + " is deselected")

        if b.text() == "Semilogy":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
            else:
                self.statusBar().showMessage(b.text() + " is deselected")

        if b.text() == "Lockdown by country":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
                self.lockdown_by_ctr = True
                self.dr_no_lc.setEnabled(True)

            else:
                self.statusBar().showMessage(b.text() + " is deselected")
                self.lockdown_by_ctr = False
                self.dr_no_lc.setEnabled(False)

        if b.text() == "Drop no LC":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
                self.drop_lc = True
            else:
                self.statusBar().showMessage(b.text() + " is deselected")
                self.drop_lc = False

        if b.text() == "Country Labels":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
                self.Rd = Canvas(self.main_widget, dpi=100, label_countries=True)
            else:
                self.statusBar().showMessage(b.text() + " is deselected")

        if b.text() == "Export to .csv":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
                self.csv_exp = True
            else:
                self.statusBar().showMessage(b.text() + " is deselected")
                self.csv_exp = False

        if b.text() == "Data computed from the beginning":
            if b.isChecked():
                self.statusBar().showMessage(b.text() + " is selected")
                self.data_from_beg = True
            else:
                self.statusBar().showMessage(b.text() + " is deselected")
                self.data_from_beg = False

    def thread_complete(self):
        self.output_rd.append("Done")
        self.get_thread_extraction.finished()

    # Check when "generate button is pressed
    def whichbtn(self, b):
        # lockdown_split()
        self.output_rd.append("clicked button is " + b.text())
        if b.text() == "&Generate":
            self.output_rd.append("Generating")
            self.get_thread_extraction = ExtractingDataThread(date_of_lockdown=self.date_lockdown,
                                                              lockdown_by_country=self.lockdown_by_ctr,
                                                              drop_no_lc=self.drop_lc,
                                                              selected_data=self.selected_data, country=self.country,
                                                              to_csv=self.csv_exp,
                                                              file_name=self.file_nm,
                                                              data_split_before=self.data_from_beg)
            self.get_thread_extraction.start()
            if self.csv_exp and (self.file_nm if self.file_nm is not None else "lockdown" not in self.fl):
                self.fl.append(self.file_nm if self.file_nm is not None else "lockdown")
                self.nm_fl_to_plt.clear()
                self.nm_fl_to_plt.addItems(self.fl)
            # self.get_thread_extraction.signals.result.connect(self.print_output)
            # self.get_thread_extraction.signals.finished.connect(self.thread_complete)

        if b.text() == "Generate and &Plot":
            pass
            if self.csv_exp and (self.file_nm if self.file_nm is not None else "lockdown" not in self.fl):
                self.fl.append(self.file_nm if self.file_nm is not None else "lockdown")
                self.nm_fl_to_plt.clear()
                self.nm_fl_to_plt.addItems(self.fl)
            # clustering(lockdown_date, csv_name=None, label_countries=False, x_ax="Cases", y_ax="New Cases", k=3,
            #        omitted_country="France", graph_type="log", backend="plt", doubling=2, **kwargs)
        if b.text() == "Plot":
            pass
            # ClusteringCOVID19.clustering(self.lockdown_date, csv_name=self.file_nm_to_plot)

    def print_output(self, s):
        print(s)


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print(CSV_DIR)
    main()
