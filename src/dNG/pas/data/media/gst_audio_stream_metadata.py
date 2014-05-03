# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.media.GstAudioStreamMetadata
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
from .audio_stream_metadata import AudioStreamMetadata
from .gst_metadata_mixin import GstMetadataMixin

class GstAudioStreamMetadata(AudioStreamMetadata, GstMetadataMixin):
#
	"""
This class provides access to GStreamer audio stream metadata.

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
Constructor __init__(GstAudioStreamMetadata)

:since: v0.1.00
		"""

		# pylint: disable=star-args

		mimetype_definition = MimeType.get_instance().get(mimetype = gst_stream_metadata['codec'])
		if (mimetype_definition == None): mimetype_definition = { "type": gst_stream_metadata['codec'], "class": gst_stream_metadata['codec'].split("/", 1)[0] }
		if (mimetype_definition['class'] != "audio"): raise ValueException("Metadata do not correspond to audio")

		kwargs = { }

		kwargs['codec'] = gst_stream_metadata['codec']
		if (gst_stream_metadata['bitrate'] > 0): kwargs['bitrate'] = gst_stream_metadata['bitrate']
		if (gst_stream_metadata['bits_per_sample'] > 0): kwargs['bps'] = gst_stream_metadata['bits_per_sample']
		if (gst_stream_metadata['channels'] > 0): kwargs['channels'] = gst_stream_metadata['channels']

		if ("profile" in gst_stream_metadata):
		#
			profile = Binary.str(gst_stream_metadata['profile']).lower()
			if ("level" in gst_stream_metadata): profile += "-{0}".format(gst_stream_metadata['level'].lower())
			kwargs['codec_profile'] = profile
		#
		elif ("format" in gst_stream_metadata): kwargs['codec_profile'] = gst_stream_metadata['format'].lower()

		if ("language-code" in gst_stream_metadata['tags']): kwargs['lang'] = GstMetadataMixin._parse_tag(gst_stream_metadata['tags']['language-code'])
		kwargs['mimeclass'] = mimetype_definition['class']
		kwargs['mimetype'] = mimetype_definition['type']
		if (gst_stream_metadata['sample_rate'] > 0): kwargs['sample_rate'] = gst_stream_metadata['sample_rate']

		AudioStreamMetadata.__init__(self, url, **kwargs)
	#
#

##j## EOF