import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import base64
import os
from   pbx_gs_python_utils.utils.Dev import Dev


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

    @staticmethod
    def save_png_file(png_data):
        try:
            png_file = '/tmp/lambda_png_file.png'
            if png_data:
                with open(png_file, "wb") as fh:
                    fh.write(base64.decodebytes(png_data.encode()))
                Dev.pprint("Png data with size {0} saved to {1}".format(len(png_data),png_file))
        except Exception as error:
            Dev.print("[_save_png_file][Error] {0}".format(error))
            Dev.print(png_data)


