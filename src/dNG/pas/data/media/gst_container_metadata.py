# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.media.GstContainerMetadata
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
from .container_metadata import ContainerMetadata
from .gst_audio_stream_metadata import GstAudioStreamMetadata
from .gst_other_stream_metadata import GstOtherStreamMetadata
from .gst_text_stream_metadata import GstTextStreamMetadata
from .gst_video_stream_metadata import GstVideoStreamMetadata

class GstContainerMetadata(ContainerMetadata):
#
	"""
This class provides access to GStreamer container metadata.

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
Constructor __init__(GstContainerMetadata)

:since: v0.1.00
		"""

		# pylint: disable=star-args

		mimetype_definition = MimeType.get_instance().get(mimetype = gst_metadata['container']['codec'])
		if (mimetype_definition == None): mimetype_definition = { "type": gst_metadata['container']['codec'], "class": gst_metadata['container']['codec'].split("/", 1)[0] }

		kwargs = { }

		if ("encoder" in gst_metadata['tags']): kwargs['encoder'] = gst_metadata['tags']['encoder']
		kwargs['length'] = gst_metadata['length']
		kwargs['mimeclass'] = mimetype_definition['class']
		kwargs['mimetype'] = mimetype_definition['type']

		ContainerMetadata.__init__(self, url, **kwargs)

		for stream in gst_metadata['audio']: self.audio_streams.append(GstAudioStreamMetadata(url, stream))
		for stream in gst_metadata['video']: self.video_streams.append(GstVideoStreamMetadata(url, stream))
		for stream in gst_metadata['text']: self.text_streams.append(GstTextStreamMetadata(url, stream))
		for stream in gst_metadata['other']: self.other_streams.append(GstOtherStreamMetadata(url, stream))
	#
#

##j## EOF