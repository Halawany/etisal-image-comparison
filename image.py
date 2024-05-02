"""
    Etisal Image comparison tool
    This is project is to compare 2 photos first one from the Xiaomi smart TV and the second is pre-saved image.
    if the 2 images are Identical or semi identical PASS -- on Rejected score less than or equal to 0.5 
    on scale from -1 to 1 if image score is above 0.5 => accepted else => there's a problem
"""
import matplotlib
matplotlib.use('TkAgg')  # Use the TkAgg backend
import time
import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os

# Load the two images
image1 = cv2.imread('xiaomi/image1.jpg')
image2 = cv2.imread('xiaomi/image2.jpg')

# Resize image2 to match the dimensions of image1
image2_resized = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

# Convert the images to grayscale
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2_resized = cv2.cvtColor(image2_resized, cv2.COLOR_BGR2GRAY)

# Calculate the Structural Similarity Index (SSI)
start_time = time.time()
ssi_score, _ = ssim(gray_image1, gray_image2_resized, full=True)
print("Process time: %s" % (time.time() - start_time))
# The SSI score ranges from -1 to 1, with 1 indicating identical images
print(f"Structural Similarity Index: {ssi_score}")

# Create a bar chart to show the accuracy
plt.figure(figsize=(6, 4))
plt.bar(['Image Comparison'], [ssi_score], color=['green'])
plt.ylabel('Structural Similarity Index')
plt.ylim(0, 1)  # Set the y-axis limits to match the range of SSI values
plt.title('Image Comparison Accuracy')

# Create the result folder if it doesn't exist
if not os.path.exists('result'):
    os.makedirs('result')

# Save the chart as a JPG file in the result folder
plt.savefig('result/comparison_chart.jpg')

# Display the chart
plt.show()

