import sys
import os
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QLabel, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPalette, QColor

import cv2
from skimage.metrics import structural_similarity as ssim

class ImageLoaderThread(QThread):
    loaded = pyqtSignal(object)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        image = cv2.imread(self.image_path)
        self.loaded.emit(image)

class ImageComparatorWorker(QObject):
    progress_updated = pyqtSignal(str, int)
    comparison_done = pyqtSignal(float)
    thread_finished = pyqtSignal()

    def __init__(self, image1):
        super().__init__()
        self.image1 = image1
        self.image2_loader = None  # Store reference to ImageLoaderThread

    def run(self):
        # Stage 1: Converting Image to Grayscale
        self.progress_updated.emit("Converting Image to Grayscale", 50)
        gray_image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)

        # Load the second image
        self.progress_updated.emit("Loading Image", 75)
        self.image2_loader = ImageLoaderThread('xiaomi/image1.jpg')
        self.image2_loader.loaded.connect(self.process_image2)
        self.image2_loader.finished.connect(self.thread_finished)  # Connect to thread's finished signal
        self.image2_loader.start()

    def process_image2(self, image2):
        # Convert the second image to grayscale
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Stage 2: Comparing Images
        self.progress_updated.emit("Comparing Images", 100)
        ssi_score, _ = ssim(gray_image1, gray_image2, full=True)
        self.comparison_done.emit(ssi_score)

        # Clean up the thread
        self.image2_loader.quit()  # Stop the thread
        self.image2_loader.wait()  # Wait for the thread to finish
        self.image2_loader.deleteLater()  # Delete the thread object


class ImageComparatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etisal End User Test Tool")
        self.setGeometry(100, 100, 400, 300)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(240, 240, 240))
        self.setPalette(palette)

        self.image_path_label = QLabel('Select Image to Compare:')
        self.image_path_label.setAlignment(Qt.AlignCenter)
        self.image_path_label.setFont(QFont("Arial", 12))

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.stage_label = QLabel()
        self.stage_label.setAlignment(Qt.AlignCenter)
        self.stage_label.setFont(QFont("Arial", 10))

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 14))

        layout = QVBoxLayout()
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.stage_label)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_folder)
        self.timer.start(1000)

    def check_folder(self):
        folder_to_watch = './captured_photos/'
        files = os.listdir(folder_to_watch)
        if files:
            file_path = os.path.join(folder_to_watch, files[0])
            self.start_comparison(file_path)

    def start_comparison(self, image_path):
        self.image_path_label.setText('Comparing Images...')
        self.progress_bar.setValue(0)

        image1_loader = ImageLoaderThread(image_path)
        image1_loader.loaded.connect(self.start_worker)
        image1_loader.start()

    def start_worker(self, image1):
        self.worker = ImageComparatorWorker(image1)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.comparison_done.connect(self.show_result)
        self.worker.run()

    def update_progress(self, stage_name, progress):
        self.stage_label.setText(stage_name)
        self.progress_bar.setValue(progress)

    def show_result(self, ssi_score):
        self.image_path_label.setText('Structural Similarity Index:')

        if ssi_score >= 0.5:
            self.result_label.setText(f"SSI: {ssi_score:.4f} (Accepted)")
            self.result_label.setStyleSheet("color: green")
            accepted_image_path = self.worker.image_path
            os.remove(accepted_image_path)
        else:
            self.result_label.setText(f"SSI: {ssi_score:.4f} (Rejected)")
            self.result_label.setStyleSheet("color: red")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageComparatorApp()
    window.show()

    sys.exit(app.exec_())
