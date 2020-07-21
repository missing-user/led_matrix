// Transcrypt'ed from Python, 2020-07-21 07:46:57
var easing = {};
var gif = {};
var math = {};
var random = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_gif__ from './gif.js';
__nest__ (gif, '', __module_gif__);
import * as __module_easing__ from './easing.js';
__nest__ (easing, '', __module_easing__);
import * as env from './environment.js';
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
import * as __module_math__ from './math.js';
__nest__ (math, '', __module_math__);
var __name__ = 'animations';
export var row = env.rows;
export var col = env.cols;
export var listOfGifs = gif.gifs;
export var overlay_border = function (leds, overlay, width) {
	if (typeof overlay == 'undefined' || (overlay != null && overlay.hasOwnProperty ("__kwargtrans__"))) {;
		var overlay = (function () {
			var __accu0__ = [];
			for (var i = 0; i < row * col; i++) {
				__accu0__.append (0);
			}
			return __accu0__;
		}) ();
	};
	if (typeof width == 'undefined' || (width != null && width.hasOwnProperty ("__kwargtrans__"))) {;
		var width = 1;
	};
	for (var y = 0; y < col; y++) {
		for (var x = 0; x < width; x++) {
			leds [from_xy (x, y)] = overlay [from_xy (x, y)];
		}
	}
	for (var y = 0; y < width; y++) {
		for (var x = 0; x < row; x++) {
			leds [from_xy (x, y)] = overlay [from_xy (x, y)];
		}
	}
	for (var y = col - width; y < col; y++) {
		for (var x = 0; x < row; x++) {
			leds [from_xy (x, y)] = overlay [from_xy (x, y)];
		}
	}
	for (var y = 0; y < col; y++) {
		for (var x = row - width; x < row; x++) {
			leds [from_xy (x, y)] = overlay [from_xy (x, y)];
		}
	}
	return leds;
};
export var clamp = function (value, min, max) {
	if (typeof min == 'undefined' || (min != null && min.hasOwnProperty ("__kwargtrans__"))) {;
		var min = 0;
	};
	if (typeof max == 'undefined' || (max != null && max.hasOwnProperty ("__kwargtrans__"))) {;
		var max = 1;
	};
	if (value <= min) {
		return min;
	}
	else if (value >= max) {
		return max;
	}
	return value;
};
export var from_xy = function (x, y) {
	return y * row + x;
};
export var xy = function (index) {
	return [__mod__ (index, row), Math.floor (index / row)];
};
export var multiply = function (leds, mult) {
	if (isinstance (mult, list)) {
		return (function () {
			var __accu0__ = [];
			for (var i = 0; i < len (leds); i++) {
				__accu0__.append (leds [i] * mult [i]);
			}
			return __accu0__;
		}) ();
	}
	return (function () {
		var __accu0__ = [];
		for (var i = 0; i < len (leds); i++) {
			__accu0__.append (leds [i] * (__mod__ (mult, 1)));
		}
		return __accu0__;
	}) ();
};
export var flipBottomHalf = function (leds) {
	for (var x = 0; x < row; x++) {
		for (var y = 0; y < Math.floor (col / 2); y++) {
			leds [from_xy ((row - 1) - x, (col - 1) - y)] = leds [from_xy (x, y)];
		}
	}
	return leds;
};
export var ease_image = function (leds, ease) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.linear;
	};
	return (function () {
		var __accu0__ = [];
		for (var i of leds) {
			__accu0__.append (ease (i));
		}
		return __accu0__;
	}) ();
};
export var flipLeftHalf = function (leds) {
	for (var y = 0; y < col; y++) {
		for (var x = Math.floor (row / 2); x < row; x++) {
			leds [from_xy ((row - 1) - x, (col - 1) - y)] = leds [from_xy (x, y)];
		}
	}
	return leds;
};
export var mask_rect = function (input_leds, fromx, tox, fromy, toy) {
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var fromx = clamp (fromx, 0, row);
	var tox = clamp (tox, 0, row);
	var fromy = clamp (fromy, 0, col);
	var toy = clamp (toy, 0, col);
	for (var y = fromy; y < toy; y++) {
		for (var x = fromx; x < tox; x++) {
			leds [from_xy (x, y)] = input_leds [from_xy (x, y)];
		}
	}
	return leds;
};
export var flipEverySecondRow = function (input_leds) {
	var leds = input_leds;
	for (var y of range (0, col, 2)) {
		for (var x = 0; x < row; x++) {
			leds [from_xy ((row - 1) - x, y)] = input_leds [from_xy (x, y)];
		}
	}
	return leds;
};
export var rotate90 = function (input_leds, count) {
	if (typeof count == 'undefined' || (count != null && count.hasOwnProperty ("__kwargtrans__"))) {;
		var count = 1;
	};
	var count = __mod__ (count + 4, 4);
	var rotated_leds = input_leds;
	if (count == 1) {
		for (var i = 0; i < len (input_leds); i++) {
			rotated_leds [from_xy (xy (i) [1], (row - 1) - xy (i) [0])] = input_leds [i];
		}
	}
	else if (count == 2) {
		var rotated_leds = list (py_reversed (input_leds));
	}
	else if (count == 3) {
		for (var i = 0; i < len (input_leds); i++) {
			rotated_leds [i] = input_leds [from_xy (xy (i) [1], (row - 1) - xy (i) [0])];
		}
	}
	else if (count == 0) {
		return input_leds;
	}
	return rotated_leds;
};
export var add = function (matrices) {
	if (len (matrices) == 0) {
		return (function () {
			var __accu0__ = [];
			for (var i = 0; i < row * col; i++) {
				__accu0__.append (0);
			}
			return __accu0__;
		}) ();
	}
	return (function () {
		var __accu0__ = [];
		for (var vals of zip (...matrices)) {
			__accu0__.append ((any (vals) ? sum (vals) : 0));
		}
		return __accu0__;
	}) ();
};
export var add_clamped = function (matrices) {
	if (len (matrices) == 0) {
		return (function () {
			var __accu0__ = [];
			for (var i = 0; i < row * col; i++) {
				__accu0__.append (0);
			}
			return __accu0__;
		}) ();
	}
	return (function () {
		var __accu0__ = [];
		for (var vals of zip (...matrices)) {
			__accu0__.append ((any (vals) ? clamp (sum (vals)) : 0));
		}
		return __accu0__;
	}) ();
};
export var mirrorX = function (input_leds) {
	for (var y = 0; y < col; y++) {
		for (var x = 0; x < Math.floor (row / 2); x++) {
			input_leds [from_xy ((row - 1) - x, y)] = input_leds [from_xy (x, y)];
		}
	}
	return input_leds;
};
export var mirrorY = function (input_leds) {
	for (var x = 0; x < row; x++) {
		for (var y = 0; y < Math.floor (col / 2); y++) {
			input_leds [from_xy (x, (col - 1) - y)] = input_leds [from_xy (x, y)];
		}
	}
	return input_leds;
};
export var arrow = function (time_percent, iterations, ease) {
	if (typeof iterations == 'undefined' || (iterations != null && iterations.hasOwnProperty ("__kwargtrans__"))) {;
		var iterations = 1;
	};
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.gaussianFit;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var i = 0; i < Math.floor (len (leds) / 2); i++) {
		var param_res = ((time_percent * (iterations + 1.5) - 1.5) + xy (i) [0] / row) + xy (i) [1] / col;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	for (var i = Math.floor (len (leds) / 2); i < len (leds); i++) {
		var param_res = ((time_percent * (iterations + 1.5) + xy (i) [0] / row) - 1.5) + ((col - 1) - xy (i) [1]) / col;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	return leds;
};
export var doubleArrow = function (time_percent, iterations, ease) {
	if (typeof iterations == 'undefined' || (iterations != null && iterations.hasOwnProperty ("__kwargtrans__"))) {;
		var iterations = 1;
	};
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.spikeSquare;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var i = 0; i < Math.floor (len (leds) / 4); i++) {
		var param_res = ((time_percent * (iterations + 1.5) - 1.5) + xy (i) [0] / row) + xy (i) [1] / col;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	for (var i = Math.floor (len (leds) / 4); i < len (leds); i++) {
		var param_res = ((time_percent * (iterations + 1.5) + xy (i) [0] / row) - 2) + ((col - 1) - xy (i) [1]) / col;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	return flipBottomHalf (leds);
};
export var diagonal_wave = function (time_percent, ease, iterations) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.gaussianFit;
	};
	if (typeof iterations == 'undefined' || (iterations != null && iterations.hasOwnProperty ("__kwargtrans__"))) {;
		var iterations = 1;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var i = 0; i < len (leds); i++) {
		var param_res = ((time_percent * (iterations + 2) - 2) + xy (i) [0] / row) + xy (i) [1] / col;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	return leds;
};
export var wave = function (time_percent, iterations, ease) {
	if (typeof iterations == 'undefined' || (iterations != null && iterations.hasOwnProperty ("__kwargtrans__"))) {;
		var iterations = 1;
	};
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.gaussianFit;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var i = 0; i < len (leds); i++) {
		var param_res = (time_percent * (iterations + 1) - 1) + xy (i) [0] / row;
		if (param_res >= iterations || param_res < 0) {
			leds [i] = ease (clamp (param_res));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res, 1)));
		}
	}
	return leds;
};
export var square_inwards_sharp = function (time_percent, ease) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.square;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	var param_res = (time_percent * row) / 2;
	for (var i = 0; i < len (leds); i++) {
		var dist_from_center = max (abs ((col - 1) / 2 - xy (i) [1]), abs ((row - 1) / 2 - xy (i) [0]));
		leds [i] = ease (clamp ((param_res - dist_from_center) + 0.5));
	}
	return leds;
};
export var square_inwards = function (time_percent, ease, origin) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.spikeInCubic;
	};
	if (typeof origin == 'undefined' || (origin != null && origin.hasOwnProperty ("__kwargtrans__"))) {;
		var origin = tuple ([(row - 1) / 2, (col - 1) / 2]);
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	var max_dist_origin = max (origin [1], origin [0], col - origin [1], row - origin [0]);
	var matrix_percent = row / max_dist_origin;
	for (var i = 0; i < len (leds); i++) {
		var dist_from_origin = max (abs (origin [1] - xy (i) [1]), abs (origin [0] - xy (i) [0]));
		leds [i] = ease (clamp ((time_percent * 2) * matrix_percent - dist_from_origin / max_dist_origin));
	}
	return leds;
};
export var curtain = function (time_percent, ease) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.spikeInCubic;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var i = 0; i < len (leds); i++) {
		var dist_from_center = abs ((row - 1) / 2 - xy (i) [0]);
		leds [i] = ease (clamp (time_percent * 1.2 - dist_from_center / row));
	}
	return leds;
};
export var fill = function (time_percent, ease, width, height) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.triangle;
	};
	if (typeof width == 'undefined' || (width != null && width.hasOwnProperty ("__kwargtrans__"))) {;
		var width = row;
	};
	if (typeof height == 'undefined' || (height != null && height.hasOwnProperty ("__kwargtrans__"))) {;
		var height = col;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var x = 0; x < width; x++) {
		for (var y = 0; y < height; y++) {
			leds [from_xy (x, y)] = ease (time_percent);
		}
	}
	return leds;
};
export var cross = function (time_percent, ease) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.linearCutoff;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	var ratio_x = Math.floor (row / 3);
	var ratio_y = Math.floor (col / 3);
	for (var y = 0; y < Math.floor (col / 2); y++) {
		for (var x = ratio_x; x < row - ratio_x; x++) {
			leds [from_xy (x, y)] = ease (1 - clamp ((time_percent * 2 - 1) + y / col));
		}
	}
	var leds = add ([leds, rotate90 (leds, 1)]);
	for (var y = ratio_y; y < col - ratio_y; y++) {
		for (var x = ratio_x; x < row - ratio_x; x++) {
			leds [from_xy (x, y)] = leds [from_xy (x, y)] * 0.5;
		}
	}
	return mirrorX (mirrorY (leds));
};
export var splitLines = function (time_percent) {
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	if (time_percent < 0.5) {
		var ease = function (t) {
			return (t <= 1 / 16 && t > 0 ? 1 : 0);
		};
		for (var y = 0; y < Math.floor (col / 2); y++) {
			for (var x = 0; x < row; x++) {
				leds [from_xy (x, y)] = ease (time_percent - y / col);
			}
		}
		mirrorY (leds);
		return leds;
	}
	else {
		var ease = function (t) {
			return (t <= 1 / 8 && t > 0 ? 1 : 0);
		};
		for (var y = 0; y < col; y++) {
			for (var x = 0; x < row; x++) {
				leds [from_xy (x, y)] = ease ((time_percent - y / col) + 1 / 16);
			}
		}
		return flipLeftHalf (leds);
	}
};
export var circle_inwards = function (time_percent, ease, iterations, origin) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.spikeInCubic;
	};
	if (typeof iterations == 'undefined' || (iterations != null && iterations.hasOwnProperty ("__kwargtrans__"))) {;
		var iterations = 1;
	};
	if (typeof origin == 'undefined' || (origin != null && origin.hasOwnProperty ("__kwargtrans__"))) {;
		var origin = tuple ([(row - 1) / 2, (col - 1) / 2]);
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	var param_res = time_percent * (0.4143 + iterations);
	for (var i = 0; i < len (leds); i++) {
		var dy = origin [0] - xy (i) [1];
		var dx = origin [1] - xy (i) [0];
		var dist_from_center = Math.pow (Math.pow (dy, 2) + Math.pow (dx, 2), 0.5);
		if (param_res - dist_from_center / row > iterations || param_res - dist_from_center / row < 0) {
			leds [i] = ease (clamp (param_res - dist_from_center / row));
		}
		else {
			leds [i] = ease (clamp (__mod__ (param_res - dist_from_center / row, 1)));
		}
	}
	return leds;
};
export var strobe = function (time_percent, ease, time_factor) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.triangle;
	};
	if (typeof time_factor == 'undefined' || (time_factor != null && time_factor.hasOwnProperty ("__kwargtrans__"))) {;
		var time_factor = 2;
	};
	var time_percent = __mod__ (time_percent, 1);
	return ([clamp (ease (time_percent * time_factor))] * row) * col;
};
export var zipper = function (time_percent, simultaneus) {
	if (typeof simultaneus == 'undefined' || (simultaneus != null && simultaneus.hasOwnProperty ("__kwargtrans__"))) {;
		var simultaneus = 4;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var time_percent = __mod__ (time_percent, 1);
	for (var y = 0; y < col; y++) {
		var param_res = time_percent * (col / simultaneus + 1) - y / simultaneus;
		for (var x = 0; x < Math.floor (row / 2); x++) {
			if (clamp (param_res) == param_res) {
				leds [from_xy (x, y)] = easing.square ((param_res * (row - 1)) / 2 - x);
			}
		}
		if (param_res < 0) {
			leds [from_xy (0, y)] = 1;
		}
		if (param_res > 1) {
			leds [from_xy (Math.floor (row / 2) - 1, y)] = 1;
		}
	}
	mirrorX (leds);
	return leds;
};
export var gif = function (time_percent, gifName, colorMask) {
	if (typeof gifName == 'undefined' || (gifName != null && gifName.hasOwnProperty ("__kwargtrans__"))) {;
		var gifName = 'compress';
	};
	if (typeof colorMask == 'undefined' || (colorMask != null && colorMask.hasOwnProperty ("__kwargtrans__"))) {;
		var colorMask = 0;
	};
	var pos = int ((__mod__ (time_percent, 1)) * len (listOfGifs [gifName]));
	return (function () {
		var __accu0__ = [];
		for (var i of list (listOfGifs [gifName] [pos])) {
			__accu0__.append (i [colorMask]);
		}
		return __accu0__;
	}) ();
};
export var dissolve_random = function (time_percent, ease) {
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.linear;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < col * row; i++) {
			__accu0__.append ((random.random () + 1) - __mod__ (time_percent * 2, 2));
		}
		return __accu0__;
	}) ();
	return (function () {
		var __accu0__ = [];
		for (var led of leds) {
			__accu0__.append (ease (clamp (led)));
		}
		return __accu0__;
	}) ();
};
export var draw_line = function (x0, y0, x1, y1) {
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var dx = x1 - x0;
	var dy = y1 - y0;
	var xsign = (dx > 0 ? 1 : -(1));
	var ysign = (dy > 0 ? 1 : -(1));
	var dx = abs (dx);
	var dy = abs (dy);
	if (dx > dy) {
		var __left0__ = tuple ([xsign, 0, 0, ysign]);
		var xx = __left0__ [0];
		var xy = __left0__ [1];
		var yx = __left0__ [2];
		var yy = __left0__ [3];
	}
	else {
		var __left0__ = tuple ([dy, dx]);
		var dx = __left0__ [0];
		var dy = __left0__ [1];
		var __left0__ = tuple ([0, ysign, xsign, 0]);
		var xx = __left0__ [0];
		var xy = __left0__ [1];
		var yx = __left0__ [2];
		var yy = __left0__ [3];
	}
	var D = 2 * dy - dx;
	var y = 0;
	for (var x = 0; x < dx + 1; x++) {
		var lx = (x0 + x * xx) + y * yx;
		var ly = (y0 + x * xy) + y * yy;
		if (ly == clamp (ly, 0, col - 1) && lx == clamp (lx, 0, row - 1)) {
			leds [from_xy (lx, ly)] = 1;
		}
		if (D >= 0) {
			y += 1;
			D -= 2 * dx;
		}
		D += 2 * dy;
	}
	return leds;
};
export var clock = function (time_percent) {
	var time_percent = __mod__ (time_percent, 1);
	var l1 = draw_line (Math.floor (row / 2), Math.floor (col / 2), Math.floor (row / 2) + int (row * math.sin (time_percent * math.pi)), Math.floor (col / 2) + int (-(col) * math.cos (time_percent * math.pi)));
	var l2 = draw_line (Math.floor (row / 2), Math.floor (col / 2), Math.floor (row / 2) + int (-(row) * math.sin (time_percent * math.pi)), Math.floor (col / 2) + int (col * math.cos (time_percent * math.pi)));
	return add_clamped ([l1, l2]);
};
export var fill_triangle = function (time_percent, corner) {
	if (typeof corner == 'undefined' || (corner != null && corner.hasOwnProperty ("__kwargtrans__"))) {;
		var corner = 0;
	};
	var time_percent = __mod__ (time_percent, 1);
	if (corner == 0) {
		var l1 = draw_line (0, 0, int ((2 * row) * math.sin ((time_percent * math.pi) / 2)), int ((2 * col) * math.cos ((time_percent * math.pi) / 2)));
		var l1 = fill_empty (l1, 1);
	}
	else if (corner == 1) {
		var l1 = draw_line (row, 0, (row - 1) - int ((2 * row) * math.sin ((time_percent * math.pi) / 2)), int ((2 * col) * math.cos ((time_percent * math.pi) / 2)));
		var l1 = fill_empty (l1);
	}
	return l1;
};
export var fill_empty = function (input_leds, corner) {
	if (typeof corner == 'undefined' || (corner != null && corner.hasOwnProperty ("__kwargtrans__"))) {;
		var corner = 0;
	};
	if (__mod__ (corner, 4) == 0) {
		for (var x = 0; x < row; x++) {
			for (var y = 0; y < col; y++) {
				if (input_leds [from_xy (x, y)] == 1) {
					break;
				}
				input_leds [from_xy (x, y)] = 1;
			}
		}
	}
	else if (__mod__ (corner, 4) == 1) {
		for (var y = 0; y < col; y++) {
			for (var x = 0; x < row; x++) {
				if (input_leds [from_xy (x, y)] == 1) {
					break;
				}
				input_leds [from_xy (x, y)] = 1;
			}
		}
	}
	else if (__mod__ (corner, 4) == 2) {
		for (var y = 0; y < col; y++) {
			for (var x of py_reversed (list (range (row)))) {
				if (input_leds [from_xy (x, y)] == 1) {
					break;
				}
				input_leds [from_xy (x, y)] = 1;
			}
		}
	}
	else if (__mod__ (corner, 4) == 3) {
		for (var y = 0; y < col; y++) {
			for (var x of py_reversed (list (range (row)))) {
				if (input_leds [from_xy (x, y)] == 1) {
					break;
				}
				input_leds [from_xy (x, y)] = 1;
			}
		}
	}
	return input_leds;
};
export var snowflake = function (time_percent, x, y, fade) {
	if (typeof fade == 'undefined' || (fade != null && fade.hasOwnProperty ("__kwargtrans__"))) {;
		var fade = 8;
	};
	var leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) ();
	var y = (int ((time_percent * 2) * col) - y) - fade;
	for (var i = 1; i < fade + 1; i++) {
		var yi = y + i;
		if (yi >= 0 && yi < col) {
			leds [from_xy (x, yi)] = 1 - 1 / i;
		}
	}
	return leds;
};
export var dissolve = function (time_percent, random_leds, number_of_steps, ease) {
	if (typeof number_of_steps == 'undefined' || (number_of_steps != null && number_of_steps.hasOwnProperty ("__kwargtrans__"))) {;
		var number_of_steps = 1;
	};
	if (typeof ease == 'undefined' || (ease != null && ease.hasOwnProperty ("__kwargtrans__"))) {;
		var ease = easing.linear;
	};
	var time_percent = __mod__ (time_percent, 1);
	return (function () {
		var __accu0__ = [];
		for (var led of random_leds) {
			__accu0__.append (ease (clamp ((1 + led * number_of_steps) - time_percent * (1 + number_of_steps))));
		}
		return __accu0__;
	}) ();
};

//# sourceMappingURL=animations.map