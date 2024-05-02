import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os
import pickle
import time

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
            image1_data = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            # Cache image1 data to file
            with open(self.cache_file, 'wb') as f:
                pickle.dump(image1_data, f)
        return image1_data
    
    # def compare_images(self):
    #     # Load the two images
    #     read_image_start_time = time.time()
    #     image1 = cv2.imread(self.image1_path)
    #     image2 = cv2.imread(self.image2_path)
    #     print("Time to read image: %s" % (time.time() -  read_image_start_time))
        
    #     # Resize image2 to match the dimensions of image1
    #     image2_resized = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
       
    #     # Convert the images to grayscale
    #     convert_image_start_time = time.time()
    #     gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    #     gray_image2_resize = cv2.cvtColor(image2_resized, cv2.COLOR_BGR2GRAY)
    #     print("Time to convert images to grey scale: %s" % (time.time() - convert_image_start_time))
        
    #     # Calculate the Structural Similarity Index (SSI)
    #     calculate_ssi_start_time = time.time()
    #     ssi_score, _ = ssim(gray_image1, gray_image2_resize, full=True)
    #     print("Time to calculate SSI: %s" % (time.time() - calculate_ssi_start_time))
    #     return ssi_score

    def compare_images(self, image2_path):
        # Load and convert image2 to grayscale
        image2 = cv2.imread(image2_path)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Resize image1 to match dimensions of image2
        image1_resized = cv2.resize(self.image1_data, (image2.shape[1], image2.shape[0]))

        # Calculate the Structural Similarity Index (SSI)
        ssi_score, _ = ssim(image1_resized, gray_image2, full=True)
        return ssi_score
    
    # def visualize_comparison(self, ssi_score):
    #     # Create a bar chart to show the accuracy
    #     plt.figure(figsize=(6, 4))
    #     plt.bar(['Image Comparison'], [ssi_score], color=['green'])
    #     plt.ylabel('Structural Similarity Index')
    #     plt.ylim(0, 1)  # Set the y-axis limits to match the range of SSI values
    #     plt.title('Image Comparison Accuracy')

    #     # Create the result folder if it doesn't exist
    #     if not os.path.exists('result'):
    #         os.makedirs('result')

    #     # Save the chart as a JPG file in the result folder
    #     plt.savefig('result/comparison_chart.jpg')

    #     # Display the chart
    #     plt.show()

if __name__ == "__main__":
    start_time = time.time()
    # comparator = ImageComparator('xiaomi/image1.jpg', 'xiaomi/image2.jpg')
    # ssi_score = comparator.compare_images()
    # print(f"Structural Similarity Index: {ssi_score}")
    comparator = ImageComparator('xiaomi/image1.jpg')
    ssi_score = comparator.compare_images('xiaomi/image2_edit.jpg')
    print(f"Structural Similarity Index with image2: {ssi_score}")
    print("Whole process time = %s" % (time.time() - start_time))
    # comparator.visualize_comparison(ssi_score)
