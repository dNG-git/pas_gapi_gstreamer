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

class GstMetadataMixin(object):
#
	"""
GStreamer mixin for metadata to provide some helper methods.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: gstreamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	@staticmethod
	def _parse_tag(tag):
	#
		"""
Parses a value or list of values of a GStreamer tag.

:param tag: GStreamer tag

:return: (str) Parsed and concatenated string
:since:  v0.2.00
		"""

		_return = ""

		if (type(tag) is list):
		#
			tag_list = [ ]
			for tag_element in tag: tag_list.append(str(tag_element))

			_return = ", ".join(tag_list)
		#
		else: _return = str(tag)

		return (", ".join(tag) if (type(tag) is list) else str(tag))
	#
#

##j## EOF