# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;imaging

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasImagingVersion)#
#echo(__FILEPATH__)#
"""

from dNG.gapi.media.gstreamer import Gstreamer
from dNG.runtime.io_exception import IOException
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.value_exception import ValueException

from .abstract_image import AbstractImage
from .image_metadata import ImageMetadata

class GstImage(Gstreamer, AbstractImage):
#
	"""
GStreamer implementation of the image class.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: imaging
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(GstImage)

:since: v0.2.00
		"""

		AbstractImage.__init__(self)
		Gstreamer.__init__(self)
	#

	def copy(self, file_path_name):
	#
		"""
Creates a copy of the image converting it to match the file extension if
needed.

:param file_path_name: Image file path and name

:return: (bool) True on success
:since:  v0.2.00
		"""

		if (self.image is None): raise IOException("Invalid image state")

		raise NotImplementedException()
	#

	def get_metadata(self):
	#
		"""
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.2.00
		"""

		_return = Gstreamer.get_metadata(self)
		if (not isinstance(_return, ImageMetadata)): raise ValueException("Metadata do not correspond to an image")
		return _return
	#

	def save(self):
	#
		"""
Saves the image if changed.

:return: (bool) True on success
:since:  v0.2.00
		"""

		return False
	#

	def set_resize_mode(self, mode):
	#
		"""
Sets the resize mode.

:param mode: Resize mode

:since: v0.2.00
		"""

		self.resize_mode = mode
	#

	def set_size(self, width, height):
	#
		"""
Sets the image size (and resizes it).

:param width: Image width
:param height: Image height

:since: v0.2.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF