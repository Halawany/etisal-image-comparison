import cv2
from skimage.metrics import structural_similarity as ssim
from colorama import Fore, Style
from tqdm import tqdm
import os
import pickle
import time
from connection import TestToolDB

class ImageComparator:
    def __init__(self, image1_path, cache_file='image1_cache.pkl'):
        self.image1_path = image1_path
        self.cache_file = cache_file
        self.image1_data = self.load_or_generate_image1_data()

    def load_or_generate_image1_data(self):
        if os.path.exists(self.cache_file):
            # Load cached image1 data from file
            with open(self.cache_file, 'rb') as f:
                image1_data = pickle.load(f)
        else:
            # Load image1 and convert to grayscale
            image1 = cv2.imread(self.image1_path)
            self.image1 = image1  # Store the loaded image
            image1_data = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            # Cache image1 data to file
            with open(self.cache_file, 'wb') as f:
                pickle.dump(image1_data, f)
        return image1_data
    
    def compare_images(self, image2_path):
        # Load and convert image2 to grayscale
        self.image2 = cv2.imread(image2_path)
        gray_image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        # Resize image1 to match dimensions of image2
        image1_resized = cv2.resize(self.image1_data, (self.image2.shape[1], self.image2.shape[0]))

        # Initialize progress bar
        progress_bar = tqdm(total=3, desc="Image Comparison Progress", unit="stage")

        # Stage 1: Resize images
        progress_bar.update(1)
        # Calculate the Structural Similarity Index (SSI)
        progress_bar.update(1)
        self.ssi_score, _ = ssim(image1_resized, gray_image2, full=True)
        progress_bar.update(1)
        progress_bar.close()

        return self.ssi_score

    def get_image_info(self, image):
        height, width, channels = image.shape
        return height, width, channels

    def print_result(self):
        print(Fore.CYAN + Style.BRIGHT + "Image Comparison Result:" + Style.RESET_ALL)
        print()

        print("Structural Similarity Index:", end=" ")
        if self.ssi_score >= 0.5:
            print(Fore.GREEN + Style.BRIGHT + f"{self.ssi_score:.4f}" + Style.RESET_ALL)
            print(Fore.GREEN + Style.BRIGHT + "Result: PASS" + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + f"{self.ssi_score:.4f}" + Style.RESET_ALL)
            print(Fore.RED + Style.BRIGHT + "Result: FAIL" + Style.RESET_ALL)

        print(Fore.YELLOW + Style.BRIGHT + "\nImage 1 Data Information:" + Style.RESET_ALL)
        print("Image 1 Data Shape:", self.image1_data.shape)

        print(Fore.YELLOW + Style.BRIGHT + "\nImage 2 Information:" + Style.RESET_ALL)
        print("Image 2 Shape:", self.image2.shape)



if __name__ == "__main__":
    start_time = time.time()
    comparator = ImageComparator('image1.jpg')
    ssi_score = comparator.compare_images('image2.jpg')
    
    # Ensure that self.image1 is assigned before calling print_result
    comparator.load_or_generate_image1_data()

    # Print comparison result
    comparator.print_result()
    db = TestToolDB(dbname='image_comparison', user='postgres', password='eslam010', host='localhost', port=5432)
    db.connect()
    db.insert_data(sn='123456', pre_saved_image='image1.jpg', image='image2.jpg', result=ssi_score)
    db.disconnect()
    print(f"Structural Similarity Index with image2: {ssi_score}")
    print("Whole process time = %s" % (time.time() - start_time))
