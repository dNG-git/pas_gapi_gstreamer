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

from dNG.data.logging.log_line import LogLine
from dNG.data.mime_type import MimeType

from .audio_metadata import AudioMetadata
from .gst_metadata_mixin import GstMetadataMixin

class GstAudioMetadata(AudioMetadata, GstMetadataMixin):
    """
This class provides access to GStreamer audio metadata.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self, url, gst_metadata):
        """
Constructor __init__(GstAudioMetadata)

:since: v0.2.00
        """

        # pylint: disable=star-args

        mimetype_definition = MimeType.get_instance().get(mimetype = gst_metadata['audio'][0]['codec'])
        if (mimetype_definition is None): mimetype_definition = { "type": gst_metadata['audio'][0]['codec'], "class": gst_metadata['audio'][0]['codec'].split("/", 1)[0] }
        if (mimetype_definition['class'] != "audio"): LogLine.debug("Metadata '{0}' do not correspond to audio".format(mimetype_definition['type']), context = "pas_media")

        kwargs = { }

        if ("album" in gst_metadata['tags']): kwargs['album'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['album'])
        if ("album-artist" in gst_metadata['tags']): kwargs['album_artist'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['album-artist'])
        if ("artist" in gst_metadata['tags']): kwargs['artist'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['artist'])
        if (gst_metadata['audio'][0]['bitrate'] > 0): kwargs['bitrate'] = gst_metadata['audio'][0]['bitrate']
        if (gst_metadata['audio'][0]['bits_per_sample'] > 0): kwargs['bps'] = gst_metadata['audio'][0]['bits_per_sample']
        if (gst_metadata['audio'][0]['channels'] > 0): kwargs['channels'] = gst_metadata['audio'][0]['channels']
        kwargs['codec'] = gst_metadata['audio'][0]['codec']

        if ("comment" in gst_metadata['tags']): kwargs['comment'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['comment'])
        elif ("extended-comment" in gst_metadata['tags']): kwargs['comment'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['extended-comment'])

        if ("genre" in gst_metadata['tags']): kwargs['genre'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['genre'])
        kwargs['length'] = gst_metadata['length']
        kwargs['mimeclass'] = mimetype_definition['class']
        kwargs['mimetype'] = mimetype_definition['type']
        if (gst_metadata['audio'][0]['sample_rate'] > 0): kwargs['sample_rate'] = gst_metadata['audio'][0]['sample_rate']
        if ("title" in gst_metadata['tags']): kwargs['title'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['title'])
        if ("track-number" in gst_metadata['tags']): kwargs['track'] = GstMetadataMixin._parse_tag(gst_metadata['tags']['track-number'])

        AudioMetadata.__init__(self, url, **kwargs)
    #
#
