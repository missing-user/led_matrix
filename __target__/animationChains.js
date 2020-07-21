// Transcrypt'ed from Python, 2020-07-21 07:47:04
var easing = {};
var effect_list = {};
var random = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_effect_list__ from './effect_list.js';
__nest__ (effect_list, '', __module_effect_list__);
import {add, add_clamped, arrow, circle_inwards, clamp, clock, cross, curtain, diagonal_wave, dissolve, dissolve_random, doubleArrow, draw_line, ease_image, fill, fill_empty, fill_triangle, flipBottomHalf, flipEverySecondRow, flipLeftHalf, from_xy, gif, listOfGifs, mask_rect, mirrorX, mirrorY, multiply, overlay_border, rotate90, snowflake, splitLines, square_inwards, square_inwards_sharp, strobe, wave, xy, zipper} from './animations.js';
import * as __module_easing__ from './easing.js';
__nest__ (easing, '', __module_easing__);
import * as env from './environment.js';
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
var __name__ = 'animationChains';
export var row = env.rows;
export var col = env.cols;
export var makeRegistrar = function () {
	var registry = [];
	var registrar = function (func) {
		registry.append (func);
		return func;
	};
	registrar.all = registry;
	return registrar;
};
export var reg = makeRegistrar ();
export var simple_factory = function (func) {
	var factory = function () {
		return func;
	};
	return factory;
};
export var properties = function (elength, intensity) {
	if (typeof intensity == 'undefined' || (intensity != null && intensity.hasOwnProperty ("__kwargtrans__"))) {;
		var intensity = null;
	};
	var decorator = function (func) {
		func.elength = elength;
		if (intensity != null) {
			func.intensity = intensity;
		}
		return func;
	};
	return decorator;
};
export var snowflake_single_factory = reg (function (x, y) {
	if (typeof x == 'undefined' || (x != null && x.hasOwnProperty ("__kwargtrans__"))) {;
		var x = null;
	};
	if (typeof y == 'undefined' || (y != null && y.hasOwnProperty ("__kwargtrans__"))) {;
		var y = null;
	};
	if (!(x)) {
		var x = random.choice (range (row));
	}
	else {
		var x = clamp (x, 0, row - 1);
	}
	if (!(y)) {
		var y = random.choice (range (col));
	}
	else {
		var y = clamp (y, 0, col - 1);
	}
	var snowflake_single = properties (__kwargtrans__ ({elength: 2})) (function (time) {
		return snowflake (time, x, y);
	});
	return snowflake_single;
});
export var snowflake_multiple_factory = reg (function () {
	var count = random.choice (range (Math.floor (row / 4), row));
	var methods = (function () {
		var __accu0__ = [];
		for (var i = 0; i < count; i++) {
			__accu0__.append (snowflake_single_factory ());
		}
		return __accu0__;
	}) ();
	var snowflake_multiple = properties (__kwargtrans__ ({elength: 2})) (function (time) {
		var matrices = (function () {
			var __accu0__ = [];
			for (var method of methods) {
				__accu0__.append (method (time));
			}
			return __accu0__;
		}) ();
		return add_clamped (matrices);
	});
	return snowflake_multiple;
});
export var dithered_diamond = reg (simple_factory (properties (__kwargtrans__ ({elength: 12})) (function (time) {
	if (time < 4) {
		return gif (time / 4, 'dithered45degSquare');
	}
	else if (time < 6) {
		return multiply (splitLines (time / 2), time / 2);
	}
	else if (time < 9) {
		return gif (time / 3, 'buildArrows');
	}
	else if (time < 10) {
		var effectResult = doubleArrow (time / 2 + 1, 1, (function __lambda__ (t) {
			return (__mod__ (t * 6, 1) == __mod__ (t * 6, 2) ? 0 : 1);
		}));
		return rotate90 (effectResult, 1);
	}
	else if (time < 11) {
		return diagonal_wave (1 - time, easing.square);
	}
	return diagonal_wave (time, easing.square);
})));
export var dsc_list = effect_list.Effect_List ();
dsc_list.add (effect_list.timed (diagonal_wave, 0, 3), effect_list.timed ((function __lambda__ (t) {
	return diagonal_wave (t, easing.easeOutQuad);
}), 3, 1), effect_list.timed ((function __lambda__ (t) {
	return square_inwards (t, easing.easeOutCubic);
}), 4, 1), effect_list.timed (square_inwards, 5, 3), effect_list.timed ((function __lambda__ (t) {
	return square_inwards (easing.triangle (t / 2), easing.easeOutQuad);
}), 8, 2), effect_list.timed ((function __lambda__ (t) {
	return mirrorX (mirrorY (diagonal_wave (-(t))));
}), 10, 6));
export var diamond_square_compress = reg (simple_factory (properties (__kwargtrans__ ({elength: 16})) (function (time) {
	return dsc_list.get_current (time) [0];
})));
export var cross_routine = reg (simple_factory (properties (__kwargtrans__ ({elength: 16, intensity: true})) (function (time) {
	if (time < 4) {
		return cross (time, easing.square);
	}
	else if (time < 12) {
		var filledCorners = mirrorX (mirrorY (fill (clamp ((__mod__ (time, 1)) * 2 - 1), __kwargtrans__ ({width: 4, height: 4}))));
		return add_clamped ([cross (time), filledCorners]);
	}
	else if (time < 13) {
		return rotate90 (flipBottomHalf (wave (time)), 1);
	}
	else if (time < 14) {
		return flipBottomHalf (wave (time));
	}
	return strobe (time * 3);
})));
export var stonehenge_routine = reg (simple_factory (properties (__kwargtrans__ ({elength: 7})) (function (time) {
	if (time < 1) {
		return gif (time, 'compressingLines');
	}
	else if (time < 4) {
		return gif ((time - 1) / 3, 'rotatingLines');
	}
	else if (time < 5) {
		return gif (time, 'stonehengeToBorder');
	}
	return overlay_border ((function () {
		var __accu0__ = [];
		for (var i = 0; i < row * col; i++) {
			__accu0__.append (0);
		}
		return __accu0__;
	}) (), square_inwards (time, easing.inverse), 2);
})));
export var flipped_lines = reg (simple_factory (properties (__kwargtrans__ ({elength: 8, intensity: true})) (function (time) {
	if (time < 4) {
		return gif (time, 'symTriangle');
	}
	else if (__mod__ (time, 2) <= 1) {
		return rotate90 (flipEverySecondRow (wave (time, 1, easing.spikeInCubic)), 1);
	}
	else {
		return flipEverySecondRow (wave (time, 1, easing.spikeInCubic));
	}
})));
export var audc_list = effect_list.Effect_List ();
audc_list.add (effect_list.timed ((function __lambda__ (t) {
	return rotate90 (arrow (-(t)));
}), 0, 1), effect_list.timed ((function __lambda__ (t) {
	return rotate90 (arrow (t / 3, 4));
}), 1, 3), effect_list.timed ((function __lambda__ (t) {
	return curtain (-(t));
}), 4, 2), effect_list.timed ((function __lambda__ (t) {
	return rotate90 (wave (t / 2));
}), 6, 2));
export var arrow_up_down_curtain = reg (simple_factory (properties (__kwargtrans__ ({elength: 8})) (function (time) {
	return audc_list.get_current (time) [0];
})));
export var build_wipe_corners = reg (simple_factory (properties (__kwargtrans__ ({elength: 6})) (function (time) {
	var diamond = mirrorX (mirrorY (diagonal_wave (time)));
	if (time < 1) {
		return gif (time, 'buildTiles');
	}
	else if (time < 2) {
		return rotate90 (curtain (time, easing.spikeSquare), 1);
	}
	else if (time < 3) {
		return mask_rect (diamond, 0, Math.floor (row / 2), 0, Math.floor (col / 2));
	}
	else if (time < 4) {
		return mask_rect (diamond, Math.floor (row / 2), row, 0, Math.floor (col / 2));
	}
	else if (time < 5) {
		return mask_rect (diamond, Math.floor (row / 2), row, Math.floor (col / 2), col);
	}
	else if (time < 6) {
		return mask_rect (diamond, 0, Math.floor (row / 2), Math.floor (col / 2), col);
	}
})));
export var dot_and_square = reg (simple_factory (properties (__kwargtrans__ ({elength: 6})) (function (time) {
	if (__mod__ (time, 2) <= 1) {
		return gif (time, 'dot');
	}
	return square_inwards_sharp (time);
})));
export var cross_flipper = reg (simple_factory (properties (__kwargtrans__ ({elength: 4})) (function (time) {
	if (time >= 1 && time < 2) {
		return cross (-(time), easing.spikeInCubic);
	}
	return cross (time, easing.spikeInCubic);
})));
export var diagonal_masked_factory = reg (function () {
	var masks = random.choice (['triangleMasks', 'borderMasks', 'ditheredMasks']);
	var masked_factory_child = properties (__kwargtrans__ ({elength: 10})) (function (time) {
		var m = gif (0, masks);
		var inv_m = ease_image (m, easing.inverse);
		var diagonal_arrow = multiply (square_inwards (time, __kwargtrans__ ({origin: tuple ([0, 0])})), inv_m);
		if (time < 1) {
			return multiply (rotate90 (diagonal_wave (time, easing.linear)), m);
		}
		if (time < 5) {
			return add ([diagonal_arrow, m]);
		}
		if (time < 6) {
			return multiply (diagonal_wave (time, easing.inverse), m);
		}
		if (time < 9) {
			return rotate90 (diagonal_arrow, 3);
		}
		return rotate90 (multiply (diagonal_wave (time), m));
	});
	return masked_factory_child;
});
export var fancy_diagonal_masked_factory = reg (function () {
	var masks = random.choice (['triangleMasks', 'triangleMasks', 'borderMasks', 'ditheredMasks']);
	var rot = random.randint (0, 4);
	var fancy_masked_factory_child = properties (__kwargtrans__ ({elength: 10})) (function (time) {
		var m = gif (0, masks);
		var inv_m = ease_image (m, easing.inverse);
		var diagonal_arrow = function (t, e) {
			return multiply (square_inwards (t, __kwargtrans__ ({origin: tuple ([0, 0]), ease: e})), inv_m);
		};
		if (time < 1) {
			return diagonal_arrow (time, easing.easeInCubic);
		}
		else if (time < 3) {
			return add_clamped ([diagonal_wave (time), inv_m]);
		}
		else if (time < 4) {
			return multiply (rotate90 (diagonal_wave (time, easing.easeOutCubic)), inv_m);
		}
		else if (time < 5) {
			return rotate90 (diagonal_arrow (time, easing.easeInCubic), 3);
		}
		else if (time < 6) {
			return rotate90 (add_clamped ([inv_m, diagonal_wave (time, easing.easeInCubic)]));
		}
		else if (time < 10) {
			var static_mask = rotate90 (fill (0.5, easing.triangle, row, col - Math.floor ((col * (int (time - 6) + 1)) / 4)), 2);
			var moving_stripe = mask_rect (wave (time, 1, easing.inverse), 0, row, Math.floor ((col * int (time - 6)) / 4), Math.floor ((col * (int (time - 6) + 1)) / 4));
			return rotate90 (add_clamped ([static_mask, moving_stripe]), rot);
		}
		return diagonal_arrow (time, easing.spikeInCubic);
	});
	return fancy_masked_factory_child;
});
export var chain10 = reg (simple_factory (properties (__kwargtrans__ ({elength: 32, intensity: true})) (function (time) {
	if (time < 8) {
		return circle_inwards (time / 4, easing.spikeInOutCubic, 4);
	}
	else if (time < 12) {
		return rotate90 (curtain (easing.triangle (time / 2)), 1);
	}
	else if (time < 16) {
		return curtain (easing.triangle (time / 2));
	}
	else if (time < 20) {
		return strobe (time);
	}
	else if (time < 24) {
		return multiply (gif (time, 'compress'), time);
	}
	else if (time < 28) {
		return circle_inwards (easing.triangle (__mod__ (time / 2, 1)), easing.linear);
	}
	return circle_inwards (-(time));
})));
export var flashing_corners = reg (simple_factory (properties (__kwargtrans__ ({elength: 28, intensity: true})) (function (time) {
	if (time < 8) {
		return rotate90 (arrow (time, 2), int (time));
	}
	else if (time < 12) {
		return square_inwards_sharp (time);
	}
	else if (time < 16) {
		return rotate90 (fill (time * 2, __kwargtrans__ ({width: Math.floor (row / 2), height: Math.floor (col / 2)})), int (time));
	}
	else if (time < 20) {
		return gif (time, 'fourGradientsLinearSpin');
	}
	return rotate90 (gif (time, 'spiral16'), 2 * int (time));
})));
export var sample = function (listt, repeat) {
	var resultingList = [];
	for (var i = 0; i < repeat; i++) {
		listt [Math.floor (Math.random () * listt.length)];
	}
	return resultingList;
};
export var flashing_symbols = reg (simple_factory (properties (__kwargtrans__ ({elength: 12})) (function (time) {
	return multiply (gif (time / 4, 'staticFrames', int (__mod__ (time / 4, 3))), time);
})));
export var random_dissolve_factory = reg (function () {
	var random_leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < col * row; i++) {
			__accu0__.append (random.random ());
		}
		return __accu0__;
	}) ();
	var ordered_leds = sample (list (range (col * row)), row * col);
	var ordered_leds = (function () {
		var __accu0__ = [];
		for (var led of ordered_leds) {
			__accu0__.append (led / (row * col));
		}
		return __accu0__;
	}) ();
	var dissolve_chain = properties (__kwargtrans__ ({elength: 14})) (function (time) {
		if (time < 4) {
			return dissolve_random (-(time) / 4);
		}
		else if (time < 8) {
			return dissolve (time / 4, ordered_leds, row * col);
		}
		else if (time < 10) {
			return rotate90 (wave (1 - easing.triangle (__mod__ (time / 2, 1)), 1, easing.inverse));
		}
		return dissolve (-(easing.triangle (__mod__ (time / 2, 1))), random_leds);
	});
	return dissolve_chain;
});
export var calm_list = effect_list.Effect_List ();
calm_list.add (effect_list.timed ((function __lambda__ (t) {
	return dissolve_random (t / 6);
}), 0, 6), effect_list.timed ((function __lambda__ (t) {
	return circle_inwards (t / 3);
}), 6, 3), effect_list.timed ((function __lambda__ (t) {
	return square_inwards (t / 3);
}), 9, 3), effect_list.timed ((function __lambda__ (t) {
	return cross (t);
}), 12, 4), effect_list.timed ((function __lambda__ (t) {
	return diagonal_wave (t / 3);
}), 15, 3));
export var calming = reg (simple_factory (properties (__kwargtrans__ ({elength: 18})) (function (time) {
	return add_clamped (calm_list.get_current (time));
})));
export var sharp_list = effect_list.Effect_List ();
sharp_list.add (effect_list.timed ((function __lambda__ (t) {
	return square_inwards_sharp (-(t));
}), 0, 4), effect_list.timed ((function __lambda__ (t) {
	return circle_inwards (easing.easeInOutCubic (easing.triangle (t / 2)), easing.easeInOutQuad);
}), 4, 2), effect_list.timed ((function __lambda__ (t) {
	return multiply (square_inwards (t / 8), gif (t, 'fourGradientsLinearSpin'));
}), 6, 6));
export var sharp_pattern = reg (simple_factory (properties (__kwargtrans__ ({elength: 10})) (function (time) {
	return add_clamped (sharp_list.get_current (time));
})));
export var color_steps_factory = reg (function () {
	var random_leds = (function () {
		var __accu0__ = [];
		for (var i = 0; i < col * row; i++) {
			__accu0__.append (random.random ());
		}
		return __accu0__;
	}) ();
	var random_colors = [1 / 8, 3 / 8, 5 / 8, 7 / 8];
	random.shuffle (random_colors);
	var color_steps = properties (__kwargtrans__ ({elength: 20})) (function (time) {
		if (time < 8) {
			return overlay_border (fill (int (time) / 4, easing.linear));
		}
		else if (time < 10) {
			return square_inwards (time);
		}
		else if (time < 12) {
			return dissolve (time / 2, random_leds);
		}
		else if (time < 16) {
			return fill (time / 2);
		}
		var nw_corner = fill (random_colors [0], easing.linear, Math.floor (row / 2), Math.floor (col / 2));
		var ne_corner = rotate90 (fill (random_colors [1], easing.linear, Math.floor (row / 2), Math.floor (col / 2)), 1);
		var se_corner = rotate90 (fill (random_colors [2], easing.linear, Math.floor (row / 2), Math.floor (col / 2)), 2);
		var sw_corner = rotate90 (fill (random_colors [3], easing.linear, Math.floor (row / 2), Math.floor (col / 2)), 3);
		if (time < 17) {
			return nw_corner;
		}
		else if (time < 18) {
			return add ([nw_corner, ne_corner]);
		}
		else if (time < 19) {
			return add ([nw_corner, ne_corner, se_corner]);
		}
		return add ([nw_corner, ne_corner, se_corner, sw_corner]);
	});
	return color_steps;
});
export var wipe_lines_factory = reg (function () {
	var rot1 = random.randint (0, 4);
	var rot2 = random.randint (0, 4);
	var wipe_lines = properties (__kwargtrans__ ({elength: 8})) (function (time) {
		if (time < 4) {
			var static_mask = fill (0.5, easing.triangle, row, Math.floor ((col * int (time)) / 4));
			var moving_stripe = mask_rect (wave (time, 1, easing.linear), 0, row, Math.floor ((col * int (time)) / 4), Math.floor ((col * (int (time) + 1)) / 4));
			return rotate90 (add ([static_mask, moving_stripe]), rot1);
		}
		var time = __mod__ (time, 4);
		var static_mask = rotate90 (fill (0.5, easing.triangle, row, col - Math.floor ((col * (int (time) + 1)) / 4)), 2);
		var moving_stripe = mask_rect (wave (time, 1, easing.inverse), 0, row, Math.floor ((col * int (time)) / 4), Math.floor ((col * (int (time) + 1)) / 4));
		return rotate90 (add_clamped ([static_mask, moving_stripe]), rot2);
	});
	return wipe_lines;
});
export var raindrops_factory = reg (function () {
	var round = random.random () > 0.5;
	var coordinates = (function () {
		var __accu0__ = [];
		for (var i = 0; i < 8; i++) {
			__accu0__.append (tuple ([random.randint (0, row), random.randint (0, col)]));
		}
		return __accu0__;
	}) ();
	var raindrops = properties (__kwargtrans__ ({elength: 8})) (function (time) {
		var t = (time < 4 ? time : -(time));
		if (round) {
			return multiply (circle_inwards (t, __kwargtrans__ ({origin: coordinates [int (time)]})), easing.easeOutCubic (__mod__ (-(t), 1)));
		}
		else {
			return square_inwards (t, __kwargtrans__ ({origin: coordinates [int (time)]}));
		}
	});
	return raindrops;
});
export var timewarp_list = effect_list.Effect_List ();
timewarp_list.add (effect_list.timed ((function __lambda__ (t) {
	return curtain (-(t) / 2.5, easing.spikeInCubic);
}), 0, 2.1), effect_list.timed ((function __lambda__ (t) {
	return clock (easing.gaussianFit (t / 8) * 4);
}), 2, 8), effect_list.timed ((function __lambda__ (t) {
	return curtain (t / 2, easing.spikeInCubic);
}), 9.5, 2), effect_list.timed ((function __lambda__ (t) {
	return circle_inwards (easing.gaussianFit (t / 8) * 4);
}), 12, 8), effect_list.timed ((function __lambda__ (t) {
	return diagonal_wave (easing.easeInOutCubic (t / 6) * 3);
}), 20, 6));
export var timewarp = reg (simple_factory (properties (__kwargtrans__ ({elength: 26})) (function (time) {
	return add_clamped (timewarp_list.get_current (time));
})));
export var fan_open_close = reg (simple_factory (properties (__kwargtrans__ ({elength: 8, intensity: true})) (function (time) {
	return rotate90 (fill_triangle (time, int (__mod__ (time, 2))), int (time / 2));
})));
export var split_triangle_merge = reg (simple_factory (properties (__kwargtrans__ ({elength: 3})) (function (time) {
	var tri = fill_triangle (0.5, 0);
	var trinverse = ease_image (tri, easing.inverse);
	if (time < 1) {
		return add_clamped ([multiply (rotate90 (wave (time / 2), 2), tri), multiply (wave (time / 2), trinverse)]);
	}
	if (time <= 2) {
		return wave (0.5);
	}
	return multiply (rotate90 (wave (time, __kwargtrans__ ({ease: easing.inverse}))), wave (0.5));
})));
export var ditherfill = reg (simple_factory (properties (__kwargtrans__ ({elength: 9})) (function (time) {
	if (time < 6) {
		return gif (time / 6, 'ditherFill');
	}
	if (time <= 7) {
		return flipBottomHalf (wave (-(time), __kwargtrans__ ({ease: easing.linear})));
	}
	return multiply (diagonal_wave (easing.triangle (time / 2)), gif (0.2, 'ditherFill'));
})));
export var ball_bounce = reg (simple_factory (properties (__kwargtrans__ ({elength: 8})) (function (time) {
	var bheight = easing.spikeOutQuad (__mod__ (time, 1));
	return circle_inwards (0.2 + 0.15 * bheight, __kwargtrans__ ({ease: easing.easeOutQuad, origin: tuple ([col - col * bheight, row * easing.triangle (__mod__ (time / 4, 1))])}));
})));
export var spiral_mov = reg (simple_factory (properties (__kwargtrans__ ({elength: 4})) (function (time) {
	var bandpass = function (t) {
		return easing.spikeInCubic (clamp (4 * t - time));
	};
	return ease_image (gif (0, 'squareSpiral'), bandpass);
})));

//# sourceMappingURL=animationChains.map