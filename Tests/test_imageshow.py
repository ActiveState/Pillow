from PIL import Image, ImageShow
from tempfile import mkdtemp
from os import rmdir
from os.path import join
from shutil import rmtree

from .helper import PillowTestCase, hopper, on_ci, unittest


class TestImageShow(PillowTestCase):
    def test_sanity(self):
        dir(Image)
        dir(ImageShow)

    def test_register(self):
        # Test registering a viewer that is not a class
        ImageShow.register("not a class")

        # Restore original state
        ImageShow._viewers.pop()

    def test_viewer_show(self):
        class TestViewer(ImageShow.Viewer):
            methodCalled = False

            def show_image(self, image, **options):
                self.methodCalled = True
                return True

        viewer = TestViewer()
        ImageShow.register(viewer, -1)

        for mode in ("1", "I;16", "LA", "RGB", "RGBA"):
            im = hopper(mode)
            self.assertTrue(ImageShow.show(im))
            self.assertTrue(viewer.methodCalled)

        # Restore original state
        ImageShow._viewers.pop(0)

    @unittest.skipUnless(on_ci(), "Only run on CIs")
    def test_show(self):
        for mode in ("1", "I;16", "LA", "RGB", "RGBA"):
            im = hopper(mode)
            self.assertTrue(ImageShow.show(im))

    def test_viewer(self):
        viewer = ImageShow.Viewer()

        self.assertIsNone(viewer.get_format(None))

        self.assertRaises(NotImplementedError, viewer.get_command, None)

    def test_viewers(self):
        for viewer in ImageShow._viewers:
            viewer.get_command("test.jpg")

    def test_file_deprecated(self):
        tmp_path = mkdtemp()
        f = join(tmp_path, "temp.jpg")
        for viewer in ImageShow._viewers:
            hopper().save(f)
            viewer.show_file(file=f)
            # viewer.show_file()


try:
    import IPython

    HAS_IPYTHON = True
except (OSError, ImportError):
    HAS_IPYTHON = False

@unittest.skipIf(not HAS_IPYTHON, "IPython not installed")
def test_ipythonviewer():
    for viewer in ImageShow._viewers:
        if isinstance(viewer, ImageShow.IPythonViewer):
            test_viewer = viewer
            break
    else:
        assert False

    im = hopper()
    assert test_viewer.show(im) == 1
