// Transcrypt'ed from Python, 2020-07-21 08:24:30
var effect_list = {};
var random = {};
var sph = {};
var time = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_sph__ from './sph.js';
__nest__ (sph, '', __module_sph__);
import * as __module_effect_list__ from './effect_list.js';
__nest__ (effect_list, '', __module_effect_list__);
import * as cmap from './colormap.js';
import * as anim from './animations.js';
import * as animChain from './animationChains.js';
import * as env from './environment.js';
import * as __module_time__ from './time.js';
__nest__ (time, '', __module_time__);
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
var __name__ = '__main__';
export var row = env.rows;
export var col = env.cols;
export var to8bitRgb = function (floatList) {
	return (function () {
		var __accu0__ = [];
		for (var i of floatList) {
			__accu0__.append (tuple ([int (i [0] * 255), int (i [1] * 255), int (i [2] * 255)]));
		}
		return __accu0__;
	}) ();
};
export var start_time_seconds = time.time ();
export var effects = effect_list.Effect_List ();
export var effects_seg = effect_list.Effect_List ();
export var color_list = [];
export var get_time = function () {
	if (time.time () - start_time_seconds > sph.total_song_time) {
		print ('getting new song');
		sph.get_track ();
		build_song_effects ();
	}
	return sph.time_to_beats (time.time () - start_time_seconds);
};
export var colors = function (time) {
	for (var [i, sect] of enumerate (sections_list)) {
		if (time > sect ['beat']) {
			return tuple ([sect ['hue1'], sect ['hue2']]);
		}
	}
	return tuple ([sections_list [0] ['hue1'], sections_list [0] ['hue2']]);
};
export var sections_list = [];
export var build_song_effects = function () {
	effects.py_clear ();
	effects_seg.py_clear ();
	start_time_seconds = time.time () - sph.current_song_time;
	random.seed (sph.currentTrack ['item'] ['id']);
	for (var sect of sph.results ['sections']) {
		var h1 = random.random ();
		var h2 = random.random ();
		if (abs (h1 - h2) < 0.15) {
			var h2 = __mod__ (h2 + 0.15, 1);
		}
		sections_list.append (dict ([['beat', int (sph.time_to_beats (sect ['start']))], ['hue1', h1], ['hue2', h2]]));
	}
	sections_list.reverse ();
	effects.add (effect_list.timed (random.choice (animChain.reg.all) (), 0));
	for (var beatIndex = 0; beatIndex < len (sph.results ['beats']); beatIndex++) {
		if (!(effects.get_current (beatIndex).length > 1)) {
			var anim_choice = random.choice (animChain.reg.all);
			effects.add (effect_list.timed (anim_choice (), beatIndex));
		}
	}
	for (var segment of sph.results ['segments']) {
		var seg_time = sph.time_to_beats (segment ['start']);
		var seg_duration = sph.time_to_beats (4 * segment ['duration'] + segment ['start']) - seg_time;
		if (seg_time) {
			var eff_factory = function (d, py_metatype) {
				var ix = 2 + segment ['pitches'].index (max (segment ['pitches']));
				var snow = animChain.snowflake_single_factory (__kwargtrans__ ({x: ix, y: 0}));
				var eff_func = function (t) {
					return snow (t / d, __kwargtrans__ ({fade: int (3 * d)}));
				};
				return eff_func;
			};
			var eff = eff_factory (seg_duration, colors (seg_time) [1] > 0.5);
			effects_seg.add (effect_list.timed (eff, seg_time, seg_duration));
		}
	}
	print ('effects generated', len (effects.repr ()));
	setInterval (loop, 10);
};
export var haveBeenLoaded = function (arg) {
	if (results != null) {
		clearInterval (hack);
		build_song_effects ();
	}
};
export var hack = setInterval (haveBeenLoaded, 5);
export var map_from_to = function (x, a, b, c, d) {
	if (typeof a == 'undefined' || (a != null && a.hasOwnProperty ("__kwargtrans__"))) {;
		var a = 0;
	};
	if (typeof b == 'undefined' || (b != null && b.hasOwnProperty ("__kwargtrans__"))) {;
		var b = 1;
	};
	if (typeof c == 'undefined' || (c != null && c.hasOwnProperty ("__kwargtrans__"))) {;
		var c = 0;
	};
	if (typeof d == 'undefined' || (d != null && d.hasOwnProperty ("__kwargtrans__"))) {;
		var d = 1;
	};
	return ((x - a) / (b - a)) * (d - c) + c;
};
export var loop = function () {
	if (results != null) {
		var curr_effects = effects.get_current (get_time ());
		var __left0__ = colors (get_time ());
		var hue1 = __left0__ [0];
		var hue2 = __left0__ [1];
		var m = curr_effects [0];
		if (!(m)) {
			var m = (function () {
				var __accu0__ = [];
				for (var i = 0; i < row * col; i++) {
					__accu0__.append (0);
				}
				return __accu0__;
			}) ();
			print ('replacement');
		}
		var coloredImage = cmap.color_map (m, int (hue1 * 18));
		var canvas = document.getElementById ('canvas');
		var ctx = canvas.getContext ('2d');
		var imgData = ctx.getImageData (0, 0, canvas.width, canvas.height);
		for (var [i, color] of enumerate (to8bitRgb (coloredImage))) {
			imgData.data [i * 4 + 0] = color [0];
			imgData.data [i * 4 + 1] = color [1];
			imgData.data [i * 4 + 2] = color [2];
			imgData.data [i * 4 + 3] = 255;
		}
		ctx.putImageData (imgData, 0, 0);
	}
};

//# sourceMappingURL=logic.map