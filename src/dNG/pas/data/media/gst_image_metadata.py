# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.media.GstImageMetadata
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;gapi;gstreamer

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
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasGapiGStreamerVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from dNG.pas.data.mime_type import MimeType
from dNG.pas.runtime.value_exception import ValueException
from .image_metadata import ImageMetadata

class GstImageMetadata(ImageMetadata):
#
	"""
This class provides access to GStreamer image metadata.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, url, gst_metadata):
	#
		"""
Constructor __init__(GstImageMetadata)

:since: v0.1.00
		"""

		mimetype_definition = MimeType.get_instance().get(mimetype = gst_metadata['video'][0]['codec'])
		if (mimetype_definition == None): mimetype_definition = { "type": gst_metadata['video'][0]['codec'], "class": gst_metadata['video'][0]['codec'].split("/", 1)[0] }
		if (mimetype_definition['class'] != "image"): raise ValueException("Metadata do not correspond to an image")

		kwargs = { }

		if ("height" in gst_metadata['video'][0]): kwargs['height'] = gst_metadata['video'][0]['height']
		kwargs['mimeclass'] = mimetype_definition['class']
		kwargs['mimetype'] = mimetype_definition['type']
		if ("width" in gst_metadata['video'][0]): kwargs['width'] = gst_metadata['video'][0]['width']

		ImageMetadata.__init__(self, url, **kwargs)
	#
#

##j## EOF