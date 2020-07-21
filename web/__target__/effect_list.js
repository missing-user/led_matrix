// Transcrypt'ed from Python, 2020-07-21 08:34:44
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'effect_list';
export var Effect_List =  __class__ ('Effect_List', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, list) {
		if (typeof list == 'undefined' || (list != null && list.hasOwnProperty ("__kwargtrans__"))) {;
			var list = null;
		};
		self.list = (list === null ? [] : list);
	});},
	get add () {return __get__ (this, function (self) {
		var elems = tuple ([].slice.apply (arguments).slice (1));
		self.list.extend (elems);
	});},
	get py_clear () {return __get__ (this, function (self) {
		self.list.py_clear ();
	});},
	get get_active () {return __get__ (this, function (self, time) {
		return (function () {
			var __accu0__ = [];
			for (var e of self.list) {
				if ((e.start_time <= time && time < e.start_time + e.elength)) {
					__accu0__.append (e);
				}
			}
			return __accu0__;
		}) ();
	});},
	get repr () {return __get__ (this, function (self) {
		return '{}{}'.format (self.list);
	});},
	get __getitem__ () {return __get__ (this, function (self, time) {
		return self.get_active (time);
	});},
	get get_current () {return __get__ (this, function (self, time) {
		return (function () {
			var __accu0__ = [];
			for (var func of self.get_active (time)) {
				__accu0__.append (func (time - func.start_time));
			}
			return __accu0__;
		}) ();
	});}
});
export var timed = function (func, start_time, override_length) {
	if (typeof override_length == 'undefined' || (override_length != null && override_length.hasOwnProperty ("__kwargtrans__"))) {;
		var override_length = null;
	};
	var wrapper = function (time) {
		return func (time);
	};
	wrapper.start_time = start_time;
	wrapper.elength = (func.elength ? func.elength.elength : 1);
	if (override_length) {
		wrapper.elength = override_length;
	}
	return wrapper;
};

//# sourceMappingURL=effect_list.map