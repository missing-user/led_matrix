// Transcrypt'ed from Python, 2020-07-21 08:34:51
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'easing';
export var inverse = function (t) {
	return 1 - t;
};
export var linear = function (t) {
	return t;
};
export var linearCutoff = function (t) {
	if (t >= 1) {
		return 0;
	}
	return t;
};
export var square = function (t) {
	if (t >= 1 || t <= 0) {
		return 0;
	}
	return 1;
};
export var easeInQuad = function (t) {
	return t * t;
};
export var easeOutQuad = function (t) {
	return t * (2 - t);
};
export var easeInOutQuad = function (t) {
	if (t < 0.5) {
		return (2 * t) * t;
	}
	else {
		return -(1) + (4 - 2 * t) * t;
	}
};
export var easeInCubic = function (t) {
	return (t * t) * t;
};
export var easeOutCubic = function (t) {
	return (-(t) * t) * t + 1;
};
export var easeInOutCubic = function (t) {
	if (t < 0.5) {
		return ((4 * t) * t) * t;
	}
	else {
		return ((t - 1) * (2 * t - 2)) * (2 * t - 2) + 1;
	}
};
export var gaussianFit = function (t) {
	return (16 * Math.pow (t, 2) - 32 * Math.pow (t, 3)) + 16 * Math.pow (t, 4);
};
export var triangle = function (t) {
	if (t < 0.5) {
		return t * 2;
	}
	else {
		return 2 - t * 2;
	}
};
export var spikeInQuad = function (t) {
	return easeInQuad (triangle (t));
};
export var spikeOutQuad = function (t) {
	return easeOutQuad (triangle (t));
};
export var spikeInOutQuad = function (t) {
	return easeInOutQuad (triangle (t));
};
export var spikeInCubic = function (t) {
	return easeInCubic (triangle (t));
};
export var spikeInOutCubic = function (t) {
	return easeInOutCubic (triangle (t));
};
export var spikeSquare = function (t) {
	if (t > 0 && t < 1 / 4) {
		return 1;
	}
	return 0;
};
if (__name__ == '__main__') {
	var eases = [gaussianFit, easeInOutCubic, easeInOutCubic, inverse, linear, linearCutoff, square, easeInQuad, easeOutQuad, easeInOutQuad, spikeSquare];
	var sym_functions = [spikeInOutCubic, spikeInCubic, spikeInOutQuad, spikeOutQuad, spikeInQuad, triangle];
	var num_iterations = 151;
	var success = true;
	print ('testing easing functions');
	for (var ease of eases) {
		print ('testing', ease.__name__);
		for (var i = 0; i < num_iterations; i++) {
			var res = ease (i / num_iterations);
			if (res < 0 || res > 1) {
				print (ease.__name__, 'failed at', i / num_iterations, 'with result', res);
				var success = false;
			}
		}
	}
	print ('testing symetric easing functions');
	for (var ease of sym_functions) {
		print ('testing', ease.__name__);
		for (var i = 0; i < num_iterations; i++) {
			var res1 = ease (i / num_iterations);
			var res2 = ease (1 - i / num_iterations);
			if (res1 < 0 || res1 > 1) {
				print (ease.__name__, 'failed at', i / num_iterations, 'with result', res1);
				var success = false;
			}
			if (!(abs (res1 - res2) < 1e-08)) {
				print (ease.__name__, 'not symetrical at', i / num_iterations, 'error', abs (res1 - res2));
				var success = false;
			}
		}
	}
	print ();
	print ((success ? 'all easing functions PASSED' : 'some tests have FAILED!'));
}

//# sourceMappingURL=easing.map