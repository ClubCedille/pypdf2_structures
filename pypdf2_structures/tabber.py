_TAB = "\t"


def _make_tabs(n):
	return _TAB * n


class Tabber:

	def __init__(self):
		# Keys (int): numbers of tabulations
		# Values (str): series of tabulations
		self._tabulations = dict()

	def get_tabs(self, num_of_tabs):
		tabs = self._tabulations.get(num_of_tabs)

		if tabs is None:
			tabs = _make_tabs(num_of_tabs)
			self._tabulations[num_of_tabs] = tabs

		return tabs
