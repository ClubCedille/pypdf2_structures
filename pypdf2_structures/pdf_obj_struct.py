"""
This module allows to write a PyPDF2 object structure in a file stream. An
object structure consists of containers (dictionaries, lists, sets and tuples)
embedded in one another and other objects. This module also works on structures
that do not contain PyPDF2 objects.
"""


from PyPDF2.generic import\
	BooleanObject,\
	DictionaryObject

from .ind_obj_solver import IndObjSolver


_DLST = (dict, list, set, tuple)
_LT = (list, tuple)

_PAGE_KEYS = ("/Annots", "/Contents", "/CropBox", "/MediaBox",
	"/Parent", "/Resources", "/Rotate", "/Tabs", "/Type")

_STREAM_WRITING_MODES = ("a", "a+", "r+", "w", "w+")

_CLOSING_BRACKET_COLON_SPACE = "]: "
_COLON_SPACE = ": "
_NEW_LINE = "\n"
_OPENING_BRACKET = "["
_PAGE_REF = "\tReference to a page\n"
_SPACE = " "
_TAB = "\t"
_UNEXPLORED_OBJS = "\t[...]\n"


def _get_obj_type(obj, ind_obj_solver):
	if IndObjSolver.is_ind_obj(obj):
		return ind_obj_solver.get_resolved_type(obj)

	else:
		return type(obj)


def _index_between_brackets(index):
	return _OPENING_BRACKET + str(index) + _CLOSING_BRACKET_COLON_SPACE


def _make_tabs(n):
	return _TAB * n


def _next_rec_allowed(item, rec_depth, depth_limit):
	return depth_limit<=0\
		or rec_depth<=depth_limit\
		or not obj_is_a_dlst(item)


def _obj_and_type_to_str(obj):
	if isinstance(obj, BooleanObject):
		return str(obj.value) + _SPACE + str(type(obj))

	else:
		return str(obj) + _SPACE + str(type(obj))


def obj_is_a_dlst(obj):
	"""
	Indicates whether the given object is a dictionary, a list, a set or a
	tuple.

	Args:
		obj: any object

	Returns:
		bool: True if the object's type is dict, list, set or tuple, False
			otherwise
	"""
	return isinstance(obj, _DLST)


def _obj_is_a_page(obj):
	"""
	Indicates whether the given object is a dictionary that represents a page
	of a PDF file.

	Args:
		obj: any object

	Returns:
		bool: True if the object represents a PDF page, False otherwise.
	"""
	if isinstance(obj, DictionaryObject):
		return tuple(obj.keys()) == _PAGE_KEYS

	else:
		return False


def write_pdf_obj_struct(struct, w_stream, depth_limit=0):
	"""
	Writes a PDF object structure in a file stream. The indentation indicates
	which objects are contained in others. The stream's mode must be "a",
	"a+", "r+", "w" or "w+". If argument struct is not a dictionary, a list,
	a set or a tuple, this function will only write one line representing that
	object.

	Args:
		struct: any object. Can be a container or not.
		w_stream (TextIOWrapper): the file stream that will contain the
			structure's representation
		depth_limit (int): a limit to the recursion depth. If it is set to 0
			or less, no limit is enforced. Defaults to 0.

	Raises:
		RecursionError: if this function exceeds the maximum recursion depth
		ValueError: if the stream's mode is incorrect
	"""
	if w_stream.mode not in _STREAM_WRITING_MODES:
		raise ValueError("The stream's mode must be "
			+ "\"a\", \"a+\", \"r+\", \"w\" or \"w+\".")

	if obj_is_a_dlst(struct):
		w_stream.write(str(type(struct)) + _NEW_LINE)
		rec_depth = 1

	else:
		rec_depth = 0

	_write_pdf_obj_struct_rec(
		struct, w_stream, rec_depth, depth_limit, IndObjSolver())


def _write_pdf_obj_struct_rec(obj_to_write, w_stream, rec_depth,
		depth_limit, ind_obj_solver):
	tabs = _make_tabs(rec_depth)
	rec_depth += 1

	if IndObjSolver.is_ind_obj(obj_to_write):
		w_stream.write(tabs + repr(obj_to_write) + _NEW_LINE)

		obj_to_write, ind_obj_resolved =\
			ind_obj_solver.solve_ind_obj(obj_to_write)

		if ind_obj_resolved and obj_is_a_dlst(obj_to_write):
			return

	if isinstance(obj_to_write, _LT):
		length = len(obj_to_write)

		for i in range(length):
			item = obj_to_write[i]
			line = tabs + _index_between_brackets(i)

			item_type = _get_obj_type(item, ind_obj_solver)

			line += str(item_type)
			w_stream.write(line + _NEW_LINE)

			if _obj_is_a_page(item):
				line = tabs + _PAGE_REF
				w_stream.write(line)

			elif _next_rec_allowed(item, rec_depth, depth_limit):
				_write_pdf_obj_struct_rec(item, w_stream, rec_depth,
					depth_limit, ind_obj_solver)

			else:
				w_stream.write(tabs + _UNEXPLORED_OBJS)

	elif isinstance(obj_to_write, dict):
		for key, value in obj_to_write.items():
			line = tabs + str(key) + _COLON_SPACE

			value_type = _get_obj_type(value, ind_obj_solver)

			line += str(value_type)
			w_stream.write(line + _NEW_LINE)

			if _obj_is_a_page(value):
				line = tabs + _PAGE_REF
				w_stream.write(line)

			elif _next_rec_allowed(value, rec_depth, depth_limit):
				_write_pdf_obj_struct_rec(value, w_stream, rec_depth,
					depth_limit, ind_obj_solver)

			else:
				w_stream.write(tabs + _UNEXPLORED_OBJS)

	elif isinstance(obj_to_write, set):
		for item in obj_to_write:
			line = tabs

			item_type = _get_obj_type(item, ind_obj_solver)

			line += str(item_type)
			w_stream.write(line + _NEW_LINE)

			if _obj_is_a_page(item):
				line = tabs + _PAGE_REF
				w_stream.write(line)

			elif _next_rec_allowed(item, rec_depth, depth_limit):
				_write_pdf_obj_struct_rec(item, w_stream, rec_depth,
					depth_limit, ind_obj_solver)

			else:
				w_stream.write(tabs + _UNEXPLORED_OBJS)

	else:
		line = tabs + str(obj_to_write)
		w_stream.write(line + _NEW_LINE)
