.. py:module:: PIL.ImageFont
.. py:currentmodule:: PIL.ImageFont

:py:mod:`ImageFont` Module
==========================

The :py:mod:`ImageFont` module defines a class with the same name. Instances of
this class store bitmap fonts, and are used with the
:py:meth:`PIL.ImageDraw.Draw.text` method.

PIL uses its own font file format to store bitmap fonts. You can use the
:command:`pilfont` utility to convert BDF and PCF font descriptors (X window
font formats) to this format.

Starting with version 1.1.4, PIL can be configured to support TrueType and
OpenType fonts (as well as other font formats supported by the FreeType
library). For earlier versions, TrueType support is only available as part of
the imToolkit package

.. warning::
    To protect against potential DOS attacks when using arbitrary strings as
    text input, Pillow will raise a ``ValueError`` if the number of characters
    is over a certain limit, :py:data:`MAX_STRING_LENGTH`.

    This threshold can be changed by setting
    :py:data:`MAX_STRING_LENGTH`. It can be disabled by setting
    ``ImageFont.MAX_STRING_LENGTH = None``.


Example
-------

.. code-block:: python

    from PIL import ImageFont, ImageDraw

    draw = ImageDraw.Draw(image)

    # use a bitmap font
    font = ImageFont.load("arial.pil")

    draw.text((10, 10), "hello", font=font)

    # use a truetype font
    font = ImageFont.truetype("arial.ttf", 15)

    draw.text((10, 25), "world", font=font)

Functions
---------

.. autofunction:: PIL.ImageFont.load
.. autofunction:: PIL.ImageFont.load_path
.. autofunction:: PIL.ImageFont.truetype
.. autofunction:: PIL.ImageFont.load_default

Methods
-------

.. autoclass:: PIL.ImageFont.ImageFont
    :members:

.. autoclass:: PIL.ImageFont.FreeTypeFont
    :members:

.. autoclass:: PIL.ImageFont.TransposedFont
    :members:


Constants
---------

.. data:: MAX_STRING_LENGTH

    Set to 1,000,000, to protect against potential DOS attacks. Pillow will
    raise a ``ValueError`` if the number of characters is over this limit. The
    check can be disabled by setting ``ImageFont.MAX_STRING_LENGTH = None``.
