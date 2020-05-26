from PIL import Image
import numpy as np


class ImageManager:
    @staticmethod
    def create_random_image(height: int, width: int) -> Image:
        array = ImageManager.create_random_array(height, width)
        return ImageManager.convert_to_image(array)

    @staticmethod
    def create_random_array(height: int, width: int):
        point_count: int = round((height + width) / 3)
        array = ImageManager.create_white_array(height, width)
        for i in range(point_count):
            x = np.random.randint(0, height)
            y = np.random.randint(0, width)
            array[x][y] = ImageManager.__get_black_point()
        return np.array(array, dtype=np.uint8)

    @staticmethod
    def create_white_image(height: int, width: int) -> Image:
        array = ImageManager.create_white_array(height, width)
        return ImageManager.convert_to_image(array)

    @staticmethod
    def create_white_array(height: int, width: int):
        return np.full((height, width, 3), 255, dtype=np.uint8)

    @staticmethod
    def convert_to_array(img: Image):
        return np.asarray(img)

    @staticmethod
    def convert_to_image(array) -> Image:
        return Image.fromarray(array)

    @staticmethod
    def __get_black_point():
        return [0, 0, 0]


if __name__ == '__main__':
    ImageManager.create_random_image(400, 300, 200).save("random.png")
