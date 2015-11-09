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
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasGapiGStreamerVersion)#
#echo(__FILEPATH__)#
"""

from gi.repository import Gst

from dNG.pas.data.byte_buffer import ByteBuffer
from dNG.pas.data.settings import Settings
from dNG.pas.data.media.abstract import Abstract
from dNG.pas.data.media.container_metadata import ContainerMetadata
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .gstreamer import Gstreamer

class GstVideo(Gstreamer, Abstract):
#
	"""
GStreamer implementation of the video class.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	X_TYPE = "video"
	"""
Multi-value type name
	"""

	def __init__(self):
	#
		"""
Constructor __init__(GstVideo)

:since: v0.1.00
		"""

		Abstract.__init__(self)
		Gstreamer.__init__(self)

		self.thumbnail_position_percentage = 0.05
		"""
Position in percent where to generate a thumbnail from.
		"""

		self.supported_features['thumbnail'] = True

		thumbnail_position_percentage = Settings.get("pas_gst_thumbnail_position_percentage", 0)

		if (thumbnail_position_percentage > 0
		    and thumbnail_position_percentage <= 100
		   ): self.thumbnail_position_percentage = (thumbnail_position_percentage / 100)
	#

	def get_metadata(self):
	#
		"""
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.1.00
		"""

		_return = Gstreamer.get_metadata(self)
		if (not isinstance(_return, ContainerMetadata)): raise ValueException("Metadata do not correspond to video")
		return _return
	#

	def get_thumbnail(self, mimetype = "image/jpeg"):
	#
		"""
Returns a thumbnail of the given mimetype.

:return: (object) Buffer object
:since:  v0.1.03
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_thumbnail({1})- (#echo(__LINE__)#)", self, mimetype, context = "pas_gapi_gstreamer")
		_return = None

		if (self.source_url is None): raise IOException("URL not defined")

		self._ensure_thread_local()

		caps = Gst.Caps.from_string(mimetype)
		pipeline = Gst.ElementFactory.make("playbin")

		audio_fakesink = Gst.ElementFactory.make("fakesink")
		video_fakesink = Gst.ElementFactory.make("fakesink")

		pipeline.set_property("audio-sink", audio_fakesink)
		pipeline.set_property("video-sink", video_fakesink)

		pipeline.set_property("uri", self.source_url)

		try:
		#
			pipeline.set_state(Gst.State.PAUSED)
			state_result = pipeline.get_state(self.discovery_timeout * Gst.SECOND)[0]

			if (state_result == Gst.StateChangeReturn.NO_PREROLL):
			#
				pipeline.set_state(Gst.State.PLAYING)
				state_result = pipeline.get_state(self.discovery_timeout * Gst.SECOND)[0]
			#

			if (state_result != Gst.StateChangeReturn.SUCCESS): raise IOException("Failed to set up playback")

			duration = pipeline.query_duration(Gst.Format.TIME)[1]

			if (duration > 0): seek_pos = duration * self.thumbnail_position_percentage
			else: seek_pos = 0

			pipeline.seek_simple(Gst.Format.TIME, (Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT), seek_pos)

			if (pipeline.get_state(self.discovery_timeout * Gst.SECOND)[0] != Gst.StateChangeReturn.SUCCESS): raise IOException("Failed to seek to start")

			sample = pipeline.emit("convert-sample", caps)
			_buffer = (None if (sample is None) else sample.get_buffer())

			if (_buffer is not None):
			#
				_return = ByteBuffer()
				_return.write(_buffer.extract_dup(0, _buffer.get_size()))
			#
		#
		finally: pipeline.set_state(Gst.State.NULL)

		return _return
	#
#

##j## EOF