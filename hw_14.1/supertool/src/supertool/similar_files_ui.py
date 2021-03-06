"""
Application to search duplicates.
"""
import os
import sys

from supertool import similar_files_qt
from supertool import similar_files as sf
from PyQt5 import QtWidgets


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApplication, self).__init__()

        self.collection = ''

        self.ui = similar_files_qt.Ui_MainWindow()
        self.ui.setupUi(self)

        self.select_button = self.ui.select_fold_butt
        self.select_button.clicked.connect(self.get_folder_name)

        self.analyse_button = self.ui.analyse_butt
        self.analyse_button.clicked.connect(self.analyse)

        self.path_line = self.ui.fold_sel_line_editor


    def get_folder_name(self):
        """
        Starts folder selecting dialog.
        Writes selected into QLine widget.
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
        self.path_line.setText(directory)


    def analyse(self):
        """
        Analyse selected folder.
        Collect duplicates into groups.
        Show it with self.output function.
        """
        path = self.path_line.text()

        if path == '':
            return

        if not os.path.isdir(path):
            self.path_line.setText("The folder does not exist. Please select another.")
            return

        filelist = sf.get_filelist(path)

        similar_dict = sf.compare_md5_sums(filelist)
        print(similar_dict)

        self.output(similar_dict)


    def output(self, similar):
        """
        Put duplicates into treeWidget and show it.

        :param dict similar: dict with groups of similar files.
        """
        for num, group in enumerate(similar):

            # create treeWidget items
            item_0 = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            for i in similar[group]:
                QtWidgets.QTreeWidgetItem(item_0)

            # name items
            self.ui.treeWidget.topLevelItem(num).setText(0, 'Group {}'.format(num + 1))

            # name files
            for n, name in enumerate(similar[group]):
                self.ui.treeWidget.topLevelItem(num).child(n).setText(0, name)

        self.ui.treeWidget.expandAll()


def start():
    """The main function."""
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    start()
