import cv2
import numpy as np
import matplotlib.pyplot as plt

# Convert data to binary format
def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b') for i in data]
    return p

# Convert image to grayscale
def convert_to_grayscale(image):
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    return gray_image

# Hide data in given image
def hidedata(img, data):
    data += "$$"  # Add end-of-message marker
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

    gray_img = convert_to_grayscale(img)

    for i in range(gray_img.shape[0]):
        for j in range(gray_img.shape[1]):
            pixel = gray_img[i, j]
            if d_index < len_data:
                pixel = (pixel & 254) | int(b_data[d_index])
                gray_img[i, j] = pixel
                d_index += 1
            if d_index >= len_data:
                break

    return gray_img

# Plot histogram of an image
def plot_histogram(image, title):
    plt.hist(image.ravel(), bins=256, range=[0, 256])
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()



# Encode the message into the stego image
def encode():
    img_name = input("\nEnter image name: ")
    image = cv2.imread(img_name)
    plot_histogram(image, "Before encoding the image")
    w, h, _ = image.shape
    data = input("Enter message: ")
    if len(data) == 0:
        raise ValueError("Empty data")
    enc_img = input("Enter encoded image name: ")
    encoded_data = hidedata(image, data)
    cv2.imwrite(enc_img, encoded_data)
    print("Data encoded successfully!")
    print("Encoded image saved as:", enc_img)
    plot_histogram(encoded_data, "Encoded Image")

# Find hidden data in the stego image
def find_data(img):
    bin_data = ""
    message_end = False
    decoded_data = ""

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel = img[i, j]
            lsb = pixel & 1
            bin_data += str(lsb)

            if bin_data.endswith("00100100"):  # "$$"
                message_end = True
                break

            if len(bin_data) == 8:
                byte = bin_data
                decoded_data += chr(int(byte, 2))
                bin_data = ""

        if message_end:
            break

    return decoded_data

# Decode the hidden message from the stego image
def decode():
    img_name = input("\nEnter Encoded image name: ")
    image = cv2.imread(img_name)
    gray_img = convert_to_grayscale(image)
    decoded_data = find_data(gray_img)
    print("\nDecoded message:", decoded_data)
    dec_img = input("Enter decoded image name: ")
    cv2.imwrite(dec_img, gray_img)
    print("Decoded image saved as:", dec_img)

# Main function for steganography
def steganography():
    while True:
        print('''\nImage steganography
        1. Encode
        2. Decode
        3. Exit''')
        u_in = int(input("\nEnter your choice: "))
        if u_in == 1:
            encode()
        elif u_in == 2:
            decode()
        elif u_in == 3:
            break
        else:
            print("Invalid choice!")

# Run the steganography function
steganography()
