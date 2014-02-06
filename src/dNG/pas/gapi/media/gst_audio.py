# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.gapi.media.GstAudio
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

from dNG.pas.data.media.abstract import Abstract
from dNG.pas.data.media.audio_metadata import AudioMetadata
from dNG.pas.runtime.value_exception import ValueException
from .gstreamer import Gstreamer

class GstAudio(Gstreamer, Abstract):
#
	"""
GStreamer implementation of the audio class.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas;gapi
:subpackage: gstreamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	X_TYPE = "audio"
	"""
Multi-value type name
	"""

	def __init__(self):
	#
		"""
Constructor __init__(GstAudio)

:since: v0.1.00
		"""

		Abstract.__init__(self)
		Gstreamer.__init__(self)
	#

	def get_metadata(self):
	#
		"""
Return the metadata for this URL.

:return: (object) Metadata object
:since:  v0.1.00
		"""

		_return = Gstreamer.get_metadata(self)
		if (not isinstance(_return, AudioMetadata)): raise ValueException("Metadata do not correspond to audio")
		return _return
	#
#

##j## EOF