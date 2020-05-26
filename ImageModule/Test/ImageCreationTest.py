from ImageModule.ImageManager import ImageManager


class ImageCreationTest:
    @staticmethod
    def create_image():
        ImageManager.create_random_image(100, 100).save("random.png")


if __name__ == '__main__':
    ImageCreationTest.create_image()
