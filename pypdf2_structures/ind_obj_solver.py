from PyPDF2.generic import IndirectObject


def _make_ind_obj_id(ind_obj):
	"""
	Creates a tuple that represents a PyPDF2 IndirectObject ID. The first
	element is attribute idnum; the second is attribute generation.

	Args:
		ind_obj (PyPDF2.generic.IndirectObject): an indirect object

	Returns:
		tuple:
			[0]: ind_obj.idnum (int)
			[1]: ind_obj.generation (int)
	"""
	return (ind_obj.idnum, ind_obj.generation)


class _IndObjRecord:

	def __init__(self, ind_obj, solved_obj_used):
		self._ind_obj = ind_obj
		self._solved_obj_used = solved_obj_used
		self._solved_obj = ind_obj.getObject()
		self._solved_type = type(self._solved_obj)

	@property
	def ind_obj(self):
		return self._ind_obj

	@property
	def solved_obj(self):
		return self._solved_obj

	@property
	def solved_obj_used(self):
		return self._solved_obj_used

	@solved_obj_used.setter
	def solved_obj_used(self, used):
		self._solved_obj_used = used

	@property
	def solved_type(self):
		return self._solved_type


class IndObjSolver:

	def __init__(self):
		# Keys: ID tuples
		# Values: _IndObjRecord instances
		self._ind_obj_records = dict()

	def get_resolved_type(self, ind_obj):
		ind_obj_id = _make_ind_obj_id(ind_obj)
		record = self._ind_obj_records.get(ind_obj_id)

		if record is None:
			record = _IndObjRecord(ind_obj, False)
			self._ind_obj_records[ind_obj_id] = record

		return record.solved_type

	@staticmethod
	def is_ind_obj(obj):
		"""
		Determines whether the given object is a PyPDF2 IndirectObject.

		Args:
			obj: any object

		Returns:
			bool: True if obj in an IndirectObject, False otherwise
		"""
		return isinstance(obj, IndirectObject)

	def solve_ind_obj(self, ind_obj):
		ind_obj_id = _make_ind_obj_id(ind_obj)
		record = self._ind_obj_records.get(ind_obj_id)
		was_solved = True

		if record is None:
			record = _IndObjRecord(ind_obj, True)
			self._ind_obj_records[ind_obj_id] = record

		elif not record.solved_obj_used:
			was_solved = False
			record.solved_obj_used = True

		return record.solved_obj, was_solved
