# -*- coding: utf-8 -*-

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

import gi
gi.require_version("Gst", "1.0")

from gi.repository import Gst

from dNG.data.byte_buffer import ByteBuffer
from dNG.data.settings import Settings
from dNG.gapi.media.gstreamer import Gstreamer
from dNG.runtime.io_exception import IOException
from dNG.runtime.value_exception import ValueException

from .abstract_video import AbstractVideo
from .container_metadata import ContainerMetadata

class GstVideo(Gstreamer, AbstractVideo):
    """
GStreamer implementation of the video class.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    X_TYPE = "video"
    """
Multi-value type name
    """

    def __init__(self):
        """
Constructor __init__(GstVideo)

:since: v0.2.00
        """

        AbstractVideo.__init__(self)
        Gstreamer.__init__(self)

        self.playback_control_timeout = 5
        """
Playback control command timeout.
        """
        self.thumbnail_position_percentage = 0.05
        """
Position in percent where to generate a thumbnail from.
        """

        playback_control_timeout = float(Settings.get("pas_gst_playback_control_timeout", 0))
        if (playback_control_timeout > 0): self.playback_control_timeout = playback_control_timeout

        self.supported_features['thumbnail'] = True

        thumbnail_position_percentage = Settings.get("pas_gst_thumbnail_position_percentage", 0)

        if (thumbnail_position_percentage > 0
            and thumbnail_position_percentage <= 100
           ): self.thumbnail_position_percentage = (thumbnail_position_percentage / 100)
    #

    def get_metadata(self):
        """
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.2.00
        """

        _return = Gstreamer.get_metadata(self)
        if (not isinstance(_return, ContainerMetadata)): raise ValueException("Metadata do not correspond to video")
        return _return
    #

    def get_thumbnail(self, mimetype = "image/jpeg"):
        """
Returns a thumbnail of the given mimetype.

:return: (object) Buffer object
:since:  v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_thumbnail({1})- (#echo(__LINE__)#)", self, mimetype, context = "pas_gapi_gstreamer")
        _return = None

        if (self.source_url is None): raise IOException("URL not defined")

        with self:
            self.pipeline = Gst.ElementFactory.make("playbin")
            Gst.util_set_object_arg(self.pipeline, "flags", "deinterlace+video")

            self.pipeline.set_property("uri", self.source_url)

            # Ensure we have a raw copy in memory before calling "convert-sample"
            video_capsfilter = Gst.ElementFactory.make("capsfilter")
            video_capsfilter.set_property("caps", Gst.Caps.from_string("video/x-raw"))
            self.pipeline.set_property("video-filter", video_capsfilter)

            video_fakesink = Gst.ElementFactory.make("fakesink")
            self.pipeline.set_property("video-sink", video_fakesink)

            caps = Gst.Caps.from_string(mimetype)

            try:
                state_result = self._set_pipeline_state(Gst.State.PAUSED, self.playback_control_timeout)

                if (state_result == Gst.StateChangeReturn.NO_PREROLL):
                    state_result = self._set_pipeline_state(Gst.State.PLAYING, self.playback_control_timeout)
                    self.pipeline.set_state(Gst.State.PAUSED)
                #

                if (state_result == Gst.StateChangeReturn.FAILURE): raise IOException("Failed to set up playback")

                duration = self.pipeline.query_duration(Gst.Format.TIME)[1]

                if (duration > 0): seek_pos = duration * self.thumbnail_position_percentage
                else: seek_pos = 0

                if (not self.pipeline.seek_simple(Gst.Format.TIME,
                                                  (Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT),
                                                  seek_pos
                                                 )
                   ): raise IOException("Failed to seek to thumbnail position")

                self._set_pipeline_state(Gst.State.PLAYING, self.playback_control_timeout)
                sample = self.pipeline.emit("convert-sample", caps)
                self.pipeline.set_state(Gst.State.PAUSED)

                _buffer = (None if (sample is None) else sample.get_buffer())

                if (_buffer is not None):
                    _return = ByteBuffer()
                    _return.write(_buffer.extract_dup(0, _buffer.get_size()))
                elif (self.log_handler is not None): self.log_handler.warning("GStreamer has not successfully received a tumbnail buffer for '{0}'", self.source_url, context = "pas_gapi_gstreamer")
            finally:
                state_result = self._set_pipeline_state(Gst.State.NULL, self.playback_control_timeout)
                if (state_result == Gst.StateChangeReturn.FAILURE): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_thumbnail()- reporting: Failed to clean up", self, context = "pas_gapi_gstreamer")
            #
        #

        return _return
    #
#
