# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;gapi;gstreamer

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
#echo(pasGapiGStreamerVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.logging.log_line import LogLine
from dNG.data.mime_type import MimeType

from .stream_metadata import StreamMetadata

class GstTextStreamMetadata(StreamMetadata):
#
	"""
This class provides access to GStreamer audio stream metadata.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, url, gst_stream_metadata):
	#
		"""
Constructor __init__(GstTextStreamMetadata)

:since: v0.2.00
		"""

		# pylint: disable=star-args

		mimetype_definition = MimeType.get_instance().get(mimetype = gst_stream_metadata['codec'])
		if (mimetype_definition is None): mimetype_definition = { "type": gst_stream_metadata['codec'], "class": gst_stream_metadata['codec'].split("/", 1)[0] }
		if (mimetype_definition['class'] != "text"): LogLine.debug("Metadata '{0}' do not correspond to text streams".format(mimetype_definition['type']), context = "pas_media")

		kwargs = { }

		kwargs['codec'] = gst_stream_metadata['codec']
		kwargs['mimeclass'] = mimetype_definition['class']
		kwargs['mimetype'] = mimetype_definition['type']

		StreamMetadata.__init__(self, url, **kwargs)
	#
#

##j## EOF