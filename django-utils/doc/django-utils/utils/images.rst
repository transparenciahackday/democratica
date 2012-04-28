Images
======

.. py:module:: djutils.utils.images

Uses the Python Imaging Library to provide methods for working with images.

.. note:: requires PIL

.. py:function:: resize(source_file, target_filename, new_width, new_height=None)

    Resize or scale an image.  Returns the width and height after resizing.
    
    :param source_file: the path to the source image
    :param target_filename: the path to store the resized image (can be same as source_file)
    :param new_width: width to resize image to
    :param new_height: height to resize image to, if not provided, will be calculated
        in proportion to new_width

.. py:function:: crop(source_file, target_filename, x, y, w, h)

    Extract part of an existing Image file and save in a new file.
