# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.media.GstVideoStreamMetadata
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

from dNG.pas.data.binary import Binary
from dNG.pas.data.mime_type import MimeType
from dNG.pas.runtime.value_exception import ValueException
from .video_stream_metadata import VideoStreamMetadata

class GstVideoStreamMetadata(VideoStreamMetadata):
#
	"""
This class provides access to GStreamer video stream metadata.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, url, gst_stream_metadata):
	#
		"""
Constructor __init__(GstVideoStreamMetadata)

:since: v0.1.00
		"""

		# pylint: disable=star-args

		mimetype_definition = MimeType.get_instance().get(mimetype = gst_stream_metadata['codec'])
		if (mimetype_definition == None): mimetype_definition = { "type": gst_stream_metadata['codec'], "class": gst_stream_metadata['codec'].split("/", 1)[0] }
		if (mimetype_definition['class'] != "video"): raise ValueException("Metadata do not correspond to video")

		kwargs = { }

		kwargs['codec'] = gst_stream_metadata['codec']
		if (gst_stream_metadata['bitrate'] > 0): kwargs['bitrate'] = gst_stream_metadata['bitrate']
		if (gst_stream_metadata['depth'] > 0): kwargs['bpp'] = gst_stream_metadata['depth']
		if (gst_stream_metadata['framerate'] > 0): kwargs['framerate'] = gst_stream_metadata['framerate']
		if ("height" in gst_stream_metadata): kwargs['height'] = gst_stream_metadata['height']
		kwargs['mimeclass'] = mimetype_definition['class']
		kwargs['mimetype'] = mimetype_definition['type']

		if ("profile" in gst_stream_metadata):
		#
			profile = Binary.str(gst_stream_metadata['profile']).lower()
			if ("level" in gst_stream_metadata): profile += "-{0}".format(gst_stream_metadata['level'].lower())
			kwargs['codec_profile'] = profile
		#

		if ("width" in gst_stream_metadata): kwargs['width'] = gst_stream_metadata['width']

		VideoStreamMetadata.__init__(self, url, **kwargs)
	#
#

##j## EOF