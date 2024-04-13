from PyQt6 import QtWidgets, QtCore
import sys, numpy as np, pandas as pd, datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # Create widgets
        self.input_files = QtWidgets.QListWidget()
        self.output_dir_button = QtWidgets.QPushButton("Select Output Directory")
        self.kel_input = QtWidgets.QLineEdit()
        self.tipe_input = QtWidgets.QRadioButton("7MBT")
        self.tipe_input2 = QtWidgets.QRadioButton("Ment")
        self.run_button = QtWidgets.QPushButton("Run")

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Drag and drop your files here:"))
        layout.addWidget(self.input_files)
        layout.addWidget(QtWidgets.QLabel("Select your output directory:"))
        layout.addWidget(self.output_dir_button)
        layout.addWidget(QtWidgets.QLabel("Enter Kelompok Mentoring:"))
        layout.addWidget(self.kel_input)
        layout.addWidget(QtWidgets.QLabel("Select Tipe Tugas:"))
        layout.addWidget(self.tipe_input)
        layout.addWidget(self.tipe_input2)
        layout.addWidget(self.run_button)

        # Set the layout
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Enable drag and drop for the QListWidget
        self.input_files.setAcceptDrops(True)
        self.input_files.setDragEnabled(True)

        # Connect the directory button to the function that opens the file dialog
        self.output_dir_button.clicked.connect(self.select_output_directory)

        # Connect the run button to the function that runs your script
        self.run_button.clicked.connect(self.run_script)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.input_files.addItem(url.toLocalFile())

    def select_output_directory(self):
        self.output_directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        self.output_dir_button.setText(self.output_directory)

    def run_script(self):
        # Get the values from the GUI

        output_directory = self.output_directory
        files = [self.input_files.item(i).text() for i in range(self.input_files.count())]
        kel = self.kel_input.text()
        tipe = "7MBT" if self.tipe_input.isChecked() else "Ment"

        # Load data
        db = []
        for filename in files:
            data = pd.read_excel(filename)
            db.append(data)

        data = pd.concat(db, ignore_index=True)

        new_col = ['ID', 'Start', 'End', 'Email', 'Name', 'Nama', 'NIM', 'KelompokMentoring', 'Kumpul', 'Tanggal7MBT', 'Upload7MBT', 'TopikMent', 'UploadMent']
        data.columns = new_col
        data.drop(['Email', 'Name'], axis=1, inplace=True)

        # Selector
        subset = data[data['KelompokMentoring'] == kel]
        if tipe == '7MBT':
            subset = subset[subset['UploadMent'].isnull()]
        else:
            subset = subset[subset['Upload7MBT'].isnull()]

        # Process
        subset['Late'] = subset['End'] - subset['Tanggal7MBT']
        subset['Status'] = 'On Time'
        subset.loc[(subset['Late'] > pd.Timedelta('1 days')) & (subset['Late'] <= pd.Timedelta('7 days')), 'Status'] = '0,5 - telat ' + subset['Late'].astype(str)
        subset.loc[(subset['Late'] > pd.Timedelta('7 days')), 'Status'] = '0 -tolak ' + subset['Late'].astype(str)
        subset.loc[subset['Late'].isnull(), 'Status'] = 'Cek Manual'

        if tipe == '7MBT':
            subset = subset[['ID', 'Nama', 'NIM', 'KelompokMentoring', 'Kumpul', 'Tanggal7MBT', 'Upload7MBT', 'Status']]
        else:
            subset = subset[['ID', 'Nama', 'NIM', 'KelompokMentoring', 'Kumpul', 'TopikMent', 'UploadMent', 'Status']]

        # Output
        now = datetime.datetime.now()
        timestr = now.strftime('%d%b%Y-%H%M')
        subset.to_excel(output_directory + kel + '-' + tipe + '-' + timestr + '.xlsx', index=False)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
