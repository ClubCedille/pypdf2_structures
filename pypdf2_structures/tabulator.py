_TAB = "\t"


def _make_tabs(num_of_tabs):
	"""
	Creates a string consisting of the specified number of tabulations.

	Args:
		num_of_tabs (int): the wanted number of tabulations

	Returns:
		str: a string made of the specified number of tabulations or an empty
			string if num_of_tabs is 0 or less
	"""
	return _TAB * num_of_tabs


class Tabulator:
	"""
	This class creates strings consisting of a specified number of
	tabulations. It stores them so that tabulation series are reused when a
	number is requested again.
	"""

	def __init__(self):
		"""
		The constructor of Tabulator creates an empty record of tabulation
		series.
		"""
		# Keys (int): numbers of tabulations
		# Values (str): series of tabulations
		self._tabulations = dict()

	def get_tabs(self, num_of_tabs):
		"""
		Provides a string consisting of the specified number of tabulations.

		Args:
			num_of_tabs (int): the wanted number of tabulations

		Returns:
			str: a string made of the specified number of tabulations or an empty
				string if num_of_tabs is 0 or less
		"""
		tabs = self._tabulations.get(num_of_tabs)

		if tabs is None:
			tabs = _make_tabs(num_of_tabs)
			self._tabulations[num_of_tabs] = tabs

		return tabs
