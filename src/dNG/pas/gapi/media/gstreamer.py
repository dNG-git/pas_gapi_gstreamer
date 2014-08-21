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

# pylint: disable=import-error

from gi.repository import Gst, GstPbutils
from threading import local
import sys

from dNG.pas.data.settings import Settings
from dNG.pas.data.media.abstract import Abstract
from dNG.pas.data.media.gst_audio_metadata import GstAudioMetadata
from dNG.pas.data.media.gst_container_metadata import GstContainerMetadata
from dNG.pas.data.media.gst_image_metadata import GstImageMetadata
from dNG.pas.gapi.glib import Glib
from dNG.pas.gapi.mainloop.gobject import Gobject as GobjectMainloop
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.io_exception import IOException

class Gstreamer(Abstract):
#
	"""
This class provides access to GStreamer.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=unused-argument

	X_TYPE = None
	"""
Multi-value type name
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Gstreamer)

:since: v0.1.00
		"""

		self._gobject_mainloop = GobjectMainloop.get_instance()
		"""
GObject mainloop
		"""
		self.local = local()
		"""
Local data handle
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.metadata = None
		"""
Cached metadata instance
		"""
		self.source_url = None
		"""
GStreamer source URI
		"""
		self.pipeline = None
		"""
GStreamer pipeline in use
		"""
		self.discovery_timeout = 3
		"""
Processing may take some time. Wait for this amount of seconds.
		"""

		Settings.read_file("{0}/settings/pas_gst.json".format(Settings.get("path_data")))
		Settings.read_file("{0}/settings/pas_gst_caps.json".format(Settings.get("path_data")))
		Settings.read_file("{0}/settings/pas_gst_mimetypes.json".format(Settings.get("path_data")))

		try: self.discovery_timeout = float(Settings.get("pas_gst_discovery_timeout", 3))
		except ValueError: self.discovery_timeout = 3
	#

	def __del__(self):
	#
		"""
Destructor __del__(Gstreamer)

:since: v0.1.00
		"""

		self.stop()
	#

	def _ensure_thread_local(self):
	#
		"""
For thread safety some variables are defined per thread. This method makes
sure that these variables are defined.

:since: v0.1.00
		"""

		# pylint: disable=broad-except,no-member

		if (not hasattr(self.local, "libversion")):
		#
			self.local.libversion = None

			with ExceptionLogTrap("pas_gapi_gstreamer"):
			#
				Gst.init(sys.argv)
				self.local.libversion = Gst.version_string()
				if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._ensure_thread_local()- reporting: {1} ready", self, self.local.libversion, context = "pas_gapi_gstreamer")
			#
		#
	#

	def get_metadata(self):
	#
		"""
Get the metadata for the given source file. IOError will occur if it times
out.

:return: (object) Metadata; None on error
:since:  v0.1.00
		"""

		# pylint: disable=no-member

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_metadata()- (#echo(__LINE__)#)", self, context = "pas_gapi_gstreamer")

		if (self.metadata == None):
		#
			if (self.source_url == None): raise IOException("URL not defined")

			self._ensure_thread_local()

			gst_discoverer = GstPbutils.Discoverer()
			gst_discoverer.set_property("timeout", (self.discovery_timeout * Gst.SECOND))
			gst_discoverer_info = gst_discoverer.discover_uri(self.source_url)

			if (gst_discoverer_info != None):
			#
				gst_result = gst_discoverer_info.get_result()

				if (gst_result == GstPbutils.DiscovererResult.OK or gst_result == GstPbutils.DiscovererResult.MISSING_PLUGINS):
				#
					if (gst_result == GstPbutils.DiscovererResult.MISSING_PLUGINS and self.log_handler != None):
					# 
						self.log_handler.warning("GStreamer is missing plugins for '{0}'", self.source_url, context = "pas_gapi_gstreamer")
					#

					self.local.metadata = { "container": None,
					                        "audio": [ ],
					                        "video": [ ],
					                        "text": [ ],
					                        "other": [ ],
					                        "seekable": gst_discoverer_info.get_seekable(),
					                        "tags": { }
					                      }

					self.local.metadata['length'] = (gst_discoverer_info.get_duration() / Gst.SECOND)
					self._parse_gst_stream_list(gst_discoverer_info.get_stream_info())

					if (self.local.metadata['container'] == None
					    and len(self.local.metadata['audio']) == 1
					    and len(self.local.metadata['video']) == 0
					   ): self.metadata = GstAudioMetadata(self.source_url, self.local.metadata)
					elif (self.local.metadata['container'] == None
					      and len(self.local.metadata['audio']) == 0
					      and len(self.local.metadata['video']) == 1
					      and self.local.metadata['video'][0]['codec'][:6] == "image/"
					     ): self.metadata = GstImageMetadata(self.source_url, self.local.metadata)
					else: self.metadata = GstContainerMetadata(self.source_url, self.local.metadata)
				#
				elif (gst_result == GstPbutils.DiscovererResult.TIMEOUT): raise IOException("Timeout occured before discovery completed")
			#
		#

		return self.metadata
	#

	def _parse_gst_caps(self, caps):
	#
		"""
Parses the GStreamer caps definition.

:param caps: GStreamer caps definition

:return: (dict) GStreamer codec data
:since:  v0.1.00
		"""

		_return = { "codec": "", "gstcaps": "" }

		if (type(caps) == Gst.Caps):
		#
			_return['gstcaps'] = caps.to_string()
			caps_count = caps.get_size()

			for i in range(0, caps_count):
			#
				structure = caps.get_structure(i)
				_return.update(self._parse_gst_structure(structure))

				if (_return['codec'] == ""): _return['codec'] = self._parse_gst_caps_codec(_return, structure.get_name())
			#
		#

		return _return
	#

	def _parse_gst_caps_codec(self, caps, codec):
	#
		"""
Parses the GStreamer caps codec for a matching mimetype identifier.

:param caps: GStreamer caps dict
:param codec: GStreamer codec name

:return: (str) GStreamer codec / Mimetype identifier
:since:  v0.1.00
		"""

		_return = codec

		if (type(caps) == dict and type(codec) == str):
		#
			gst_mimetypes = Settings.get("pas_gst_mimetypes", { })

			if (codec in gst_mimetypes):
			#
				if (type(gst_mimetypes[codec]) == str): _return = gst_mimetypes[codec]
				else:
				#
					codec = self._parse_gst_caps_dependencies(caps, gst_mimetypes[codec])
					if (codec != None): _return = codec
				#
			#
		#

		return _return
	#

	def _parse_gst_caps_dependencies(self, caps, mimetype_definition):
	#
		"""
Parses the GStreamer caps dict to identify a matching mimetype.

:param caps: GStreamer caps dict
:param mimetype_definition: GStreamer caps to mimetype definition

:return: (str) MimeType; None on error
:since:  v0.1.00
		"""

		_return = None

		if (type(mimetype_definition) == dict):
		#
			for dependency in mimetype_definition:
			#
				mimetype_definition_match = None

				if (dependency in caps): mimetype_definition_match = mimetype_definition[dependency]
				elif (dependency == "_x_type" and self.__class__.X_TYPE in mimetype_definition['_x_type']): mimetype_definition_match = mimetype_definition['_x_type'][self.__class__.X_TYPE]

				if (mimetype_definition_match != None):
				#
					"""
Dependencies are reflected as hierarchal dicts with dict values for
additional dependencies or str containing the codec.
					"""

					type_mimetype_definition_match = type(mimetype_definition_match)

					if (type_mimetype_definition_match == str): _return = mimetype_definition_match
					elif (type_mimetype_definition_match == dict):
					#
						for value in mimetype_definition_match:
						#
							if (str(caps[dependency]) == value):
							#
								_return = (mimetype_definition_match[value] if (type(mimetype_definition_match[value]) == str) else self._parse_gst_caps_dependencies(caps, mimetype_definition_match[value]))
								break
							#
						#
					#
				#

				if (_return != None): break
			#
		#

		return _return
	#

	def _parse_gst_stream_list(self, stream_info):
	#
		"""
Parses the GStreamer stream list for contained streams.

:param stream_info: GStreamer stream info

:since: v0.1.00
		"""

		while (stream_info != None):
		#
			self._parse_gst_stream_info(stream_info)
			stream_info = stream_info.get_next()
		#
	#

	def _parse_gst_stream_info(self, stream_info):
	#
		"""
Parses the GStreamer stream info.

:param stream_info: GStreamer stream info

:since: v0.1.00
		"""

		stream_data = { }
		stream_type = None

		if (type(stream_info) == GstPbutils.DiscovererAudioInfo):
		#
			stream_data['bitrate'] = stream_info.get_bitrate()

			bitrate_max = stream_info.get_max_bitrate()
			if (bitrate_max > 0): stream_data['bitrate_max'] = bitrate_max

			stream_data['channels'] = stream_info.get_channels()
			stream_data['bits_per_sample'] = stream_info.get_depth()
			stream_data['sample_rate'] = stream_info.get_sample_rate()

			stream_type = "audio"
		#
		elif (type(stream_info) == GstPbutils.DiscovererContainerInfo):
		#
			for sub_stream_info in Glib.parse_glist(stream_info.get_streams()): self._parse_gst_stream_info(sub_stream_info)
			if (self.local.metadata['container'] == None): stream_type = "container"
		#
		elif (type(stream_info) == GstPbutils.DiscovererSubtitleInfo):
		#
			stream_type = "text"
		#
		elif (type(stream_info) == GstPbutils.DiscovererVideoInfo):
		#
			stream_data['bitrate'] = stream_info.get_bitrate()

			bitrate_max = stream_info.get_max_bitrate()
			if (bitrate_max > 0): stream_data['bitrate_max'] = bitrate_max

			stream_data['depth'] = stream_info.get_depth()
			stream_data['framerate'] = (stream_info.get_framerate_num() / stream_info.get_framerate_denom())

			stream_type = "video"
		#
		else:
		#
			stream_type = "other"
		#

		if (stream_type != None):
		#
			stream_data.update(self._parse_gst_caps(stream_info.get_caps()))

			if ("parsed" not in stream_data or stream_data['parsed']):
			#
				if (stream_type == "container"): self.local.metadata[stream_type] = stream_data
				else: self.local.metadata[stream_type].append(stream_data)

				gst_tags = stream_info.get_tags()
				stream_data['tags'] = { }
				if (gst_tags != None): gst_tags.foreach(self._parse_gst_tag, { "stream": stream_data })
			#
		#
	#

	def _parse_gst_structure(self, structure):
	#
		"""
Parses a GStreamer structure recursively.

:param structure: GStreamer structure

:return: (dict) GStreamer structure content
:since:  v0.1.00
		"""

		# pylint: disable=broad-except,no-member

		_return = { }

		structure_count = structure.n_fields()

		for i in range(0, structure_count):
		#
			with ExceptionLogTrap("pas_gapi_gstreamer"):
			#
				key = structure.nth_field_name(i)
				field_type = structure.get_field_type(key)

				try: _return[key] = (self._parse_gst_structure(structure.get_value(key)) if (field_type == Gst.Structure) else structure.get_value(key))
				except Exception:
				#
					"""n// NOTE
Workaround for "unknown type GstFraction". We can't handle "GstValueArray" or
"GstBitmask" here. Last seen with GStreamer 1.2.1.
					NOTE_END //n"""

					if (field_type.name == "GstFraction"):
					#
						fraction_struct = structure.get_fraction(key)
						_return[key] = fraction_struct[1] / fraction_struct[2]
					#
					else: raise
				#
			#
		#

		return _return
	#

	def _parse_gst_tag(self, tag_list, tag, kwargs):
	#
		"""
Parses the GStreamer tag data.

:param tag_list: GStreamer tag list definition
:param tag: GStreamer tag to be parsed

:return: (bool) True if the foreach operation should continue.
:since:  v0.1.00
		"""

		if (type(tag_list) == Gst.TagList and type(tag) == str):
		#
			tags_count = tag_list.get_tag_size(tag)

			for i in range(0, tags_count):
			#
				value = tag_list.get_value_index(tag, i)

				Gstreamer._add_unique_tag(self.local.metadata['tags'], tag, value)
				if ("stream" in kwargs): Gstreamer._add_unique_tag(kwargs['stream']['tags'], tag, value)
			#
		#

		return True
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop an active GStreamer process.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		return last_return
	#

	def open_url(self, url):
	#
		"""
Initializes an media instance for the given URL.

:param url: URL

:return: (bool) True on success
:since:  v0.1.00
		"""

		self.metadata = None
		self.source_url = url

		return True
	#

	@staticmethod
	def _add_unique_tag(tag_dict, tag, value):
	#
		"""
Adds not already added tags to the given dictionary.

:param tag_dict: Tag dictionary
:param tag: GStreamer tag name
:param value: Tag value

:since: v0.1.00
		"""

		if (type(tag_dict) == dict):
		#
			if (tag not in tag_dict): tag_dict[tag] = value
			elif (type(tag_dict[tag]) == list):
			#
				if (value not in tag_dict[tag]): tag_dict[tag].append(value)
			#
			elif (tag_dict[tag] != value): tag_dict[tag] = [ tag_dict[tag], value ]
		#
	#
#

##j## EOF