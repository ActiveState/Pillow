import pytest
import os

from PIL import Image

from .helper import PillowTestCase, hopper

TEST_FILE = "Tests/images/hopper.ppm"

ORIGINAL_LIMIT = Image.MAX_IMAGE_PIXELS


class TestDecompressionBomb(PillowTestCase):
    def tearDown(self):
        Image.MAX_IMAGE_PIXELS = ORIGINAL_LIMIT

    def test_no_warning_small_file(self):
        # Implicit assert: no warning.
        # A warning would cause a failure.
        Image.MAX_IMAGE_PIXELS = ORIGINAL_LIMIT
        Image.open(TEST_FILE)

    def test_no_warning_no_limit(self):
        # Arrange
        # Turn limit off
        Image.MAX_IMAGE_PIXELS = None
        self.assertIsNone(Image.MAX_IMAGE_PIXELS)

        # Act / Assert
        # Implicit assert: no warning.
        # A warning would cause a failure.
        Image.open(TEST_FILE)

    def test_warning(self):
        # Set limit to trigger warning on the test file
        Image.MAX_IMAGE_PIXELS = 128 * 128 - 1
        self.assertEqual(Image.MAX_IMAGE_PIXELS, 128 * 128 - 1)

        self.assert_warning(Image.DecompressionBombWarning,
                            Image.open, TEST_FILE)

    def test_exception(self):
        # Set limit to trigger exception on the test file
        Image.MAX_IMAGE_PIXELS = 64 * 128 - 1
        self.assertEqual(Image.MAX_IMAGE_PIXELS, 64 * 128 - 1)

        self.assertRaises(Image.DecompressionBombError,
                          lambda: Image.open(TEST_FILE))

    @pytest.mark.xfail(reason="different exception")
    def test_exception_ico(self):
        with self.assertRaises(Image.DecompressionBombError):
            Image.open("Tests/images/decompression_bomb.ico")

    def test_exception_gif(self):
        with self.assertRaises(Image.DecompressionBombError):
            Image.open("Tests/images/decompression_bomb.gif")

    def test_exception_gif_extents(self):
        with Image.open("Tests/images/decompression_bomb_extents.gif") as im:
            with pytest.raises(Image.DecompressionBombError):
                im.seek(1)

    def test_exception_bmp(self):
        with self.assertRaisesRegex(IOError, "Unsupported BMP Size"):
            with Image.open("Tests/images/bmp/b/reallybig.bmp"):
                pass


class TestDecompressionCrop(PillowTestCase):
    def setUp(self):
        self.src = hopper()
        Image.MAX_IMAGE_PIXELS = self.src.height * self.src.width * 4 - 1

    def tearDown(self):
        Image.MAX_IMAGE_PIXELS = ORIGINAL_LIMIT

    def testEnlargeCrop(self):
        # Crops can extend the extents, therefore we should have the
        # same decompression bomb warnings on them.
        box = (0, 0, self.src.width * 2, self.src.height * 2)
        self.assert_warning(Image.DecompressionBombWarning, self.src.crop, box)

    def test_crop_decompression_checks(self):

        im = Image.new("RGB", (100, 100))

        good_values = ((-9999, -9999, -9990, -9990), (-999, -999, -990, -990))

        warning_values = ((-160, -160, 99, 99), (160, 160, -99, -99))

        error_values = ((-99909, -99990, 99999, 99999),
                        (99909, 99990, -99999, -99999))

        for value in good_values:
            self.assertEqual(im.crop(value).size, (9, 9))

        for value in warning_values:
            self.assert_warning(Image.DecompressionBombWarning, im.crop, value)

        for value in error_values:
            with self.assertRaises(Image.DecompressionBombError):
                im.crop(value)
