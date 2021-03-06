"""Controller for the MVC structure. All logic of the Gui occurs here."""
import sys
import logging
import glob
from PySide6 import QtWidgets, QtCore, QtGui
from Model.model import Model
from View.view import View
from pydicom import dcmread, errors
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np


class Controller:
    """Controller class"""
    def __init__(self, root_dir=None):
        """initialise Controller class"""
        # setup attributes and create model and view
        self.root_dir = root_dir
        self.model = Model(self.root_dir)
        self.view = View(self)
        logging.info("Controller object initialised")

    def show_window(self):
        """Show the main display window"""
        self.view.show_main()

    def directory_input(self):
        """This function runs the file input GUI and processes the data in the folder selected"""
        self.model.dcm_data = []
        self.model.dcm_misc = []
        self.model.images = []
        logging.info("Data structures reset")
        dlg = QtWidgets.QFileDialog(self.view.display_window)
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        folder_names = QtCore.QStringListModel
        if dlg.exec():
            folder_names = dlg.selectedFiles()

        if len(folder_names) < 1 or len(folder_names) > 1:
            logging.warning("File Selection Error. Maintaining Current View State")
        else:
            logging.debug("Valid folder selection")
            # clear dicom data
            self.model.dcm_data = []
            self.model.dcm_misc = []
            open_data = self.open_dicom(folder_names[0]) # calls the open dicom function
            self.model.dcm_data = open_data[0]
            self.model.dcm_misc = open_data[1]

            if len(self.model.dcm_data) > 0:
                self.model.images = self.dicom_to_image(self.model.dcm_data)
                self.view_image(self.model.images[0])  # call to view function
                logging.info("Image Array Length = %s", str(len(self.model.images)))
                logging.info("Dicom Array Length = %s", str(len(self.model.dcm_data)))
                self.view_toggle()  # call to view function
            else:
                logging.warning("No Dicom Files Found in Folder. Maintaining Current View State")

    def update_image(self, value, force_init=False):
        """Handles the logic when the slider moves."""
        index = int(value - 1)
        if force_init is True:
            index = 0
            logging.debug("force init value = true")
        if 0 <= index < len(self.model.images):
            image = self.model.images[index]
            logging.debug("Accessing image at index %i", index)
            self.view_image(image)
            text1 = "Scan Position:   " + \
                    str(self.model.dcm_data[index].get_item((0x0020, 0x1041)).value) + "\n"
            text2 = "Series Position: " + str(index + 1)
            self.view.display_window.text_label.setText(text1 + text2)
            self.view.display_window.dicom_info.setText(str(self.model.dcm_data[index]))
        else:
            logging.debug("slider moved with no image associated")

    def view_toggle(self):
        """Handles the logic when a folder is selected"""
        text1 = "Scan Position:   " + \
                str(self.model.dcm_data[0].get_item((0x0020, 0x1041)).value) + "\n"
        text2 = "Series Position:  0"

        self.view.display_window.text_label.setText(text1 + text2)
        self.view.display_window.slider.setMinimum(1)
        self.view.display_window.slider.setMaximum(len(self.model.dcm_data))
        self.view.display_window.slider.setValue(1)
        self.view.display_window.slider.setSingleStep(1)
        self.update_image(True)
        self.view.display_window.resize(QtCore.QSize(1500, 500))
        logging.info("Display window default loaded")

    def view_image(self, picture):
        """Changes the image when the slider is moved"""
        try:
            data = ImageQt(picture)
            pix = QtGui.QPixmap.fromImage(data)
            self.view.display_window.label.setPixmap(pix)
            logging.info("image loaded")
        except Exception as exception:
            self.view.alert(str(exception))
            logging.warning("image loaded from dicom, Failed conversion to qt pixel map")
            logging.debug("exception: %s", exception)

    def open_dicom(self, directory):
        """Takes a folder directory as an input, and saves all the dicom files to an array"""
        str_input = directory + "/*.dcm"
        dir_list = glob.glob(str_input)
        temp_dcm_array = []
        temp_misc_array = []
        for i in dir_list:
            try:
                dicom = dcmread(i, force=True)
            except errors.InvalidDicomError as exception:
                logging.warning("Invalid dicom file read")
                self.view.alert(exception)
                continue
            try:
                dicom_test = dicom.get_item((0x0020, 0x1041)).value
                logging.debug("dicom file appended: %s", dicom_test)
                temp_dcm_array.append(dicom)
            except AttributeError:
                logging.debug("misc array populated")
                temp_misc_array.append(dicom)
        temp_dcm_array = self.sort_dicom(temp_dcm_array)
        logging.info("Dicom Array Sorted")
        self.model.dcm_data = temp_dcm_array
        self.model.dcm_misc = temp_misc_array
        return [temp_dcm_array, temp_misc_array]

    @staticmethod
    def sort_dicom(array):
        """Sorts Dicom files by the scan position"""
        array.sort(key=lambda x: float(x.get_item((0x0020, 0x1041)).value),
                   reverse=True)
        return array

    def dicom_to_image(self, dicom):
        """Converts the python dicom objects to multiple images, and saves them in an array"""
        images = []
        for i in dicom:
            try:
                arr = i.pixel_array.astype(float)
                rescaled_im = (np.maximum(arr, 0) / arr.max()) * 255
                final_image = np.uint8(rescaled_im)
                patient_image = Image.fromarray(final_image)
                images.append(patient_image)
                if sys.getsizeof(images) >= 500000000:
                    logging.warning("Image processing aborted(files to large)")
                    break
            except AttributeError:
                logging.debug("Importing DICOM Files without pixel data; Attribute Error")
            except TypeError:
                logging.info("Importing DICOM Files without pixel data; Type Error")

        logging.debug("Size of Image Array = %s", str(sys.getsizeof(images)))
        self.model.images = images
        return images