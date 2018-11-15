import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import base64
import os

class Show_Img:

    @classmethod
    def from_svg_string(self, svg_data):
        with open('./lambda-result.svg', "wb") as fh:
            fh.write(base64.decodebytes(svg_data.encode()))

        img = mpimg.imread('./lambda-result.svg')
        plt.imshow(img)
        plt.axis('off')
        plt.show()                                  # this will show the file in IntelliJ UI
        os.remove('./lambda-result.svg')

    @staticmethod
    def from_png_string(png_data):
        with open('./lambda-result.png', "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))

        img = mpimg.imread('./lambda-result.png')
        plt.imshow(img)
        plt.axis('off')
        plt.show()                      # this will show the file in IntelliJ UI
        os.remove('./lambda-result.png')

    @staticmethod
    def from_path(path):
        img = mpimg.imread(path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()                      # this will show the file in IntelliJ UI


