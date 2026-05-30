# Linearize, luminence, and contrast derivation formulae taken from
# https://www.w3.org/TR/WCAG20-TECHS/G17.html

import globalPluginHandler
import speech
import colors


_orig = None


def _linearize(c: int) -> float:
	s = c / 255.0
	return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def _luminance(rgb: colors.RGB) -> float:
	return 0.2126 * _linearize(rgb.red) + 0.7152 * _linearize(rgb.green) + 0.0722 * _linearize(rgb.blue)


def _contrast_ratio(fg: colors.RGB, bg: colors.RGB) -> float:
	l1, l2 = _luminance(fg), _luminance(bg)
	if l2 > l1:
		l1, l2 = l2, l1
	return (l1 + 0.05) / (l2 + 0.05)


def _hex(rgb: colors.RGB) -> str:
	return f"#{rgb.red:02X}{rgb.green:02X}{rgb.blue:02X}"


# Overly complex function, this signature is likely to change in later versions of NVDA
def _patched_getFormatFieldSpeech(attrs, attrsCache=None, formatConfig=None, **kwargs):
	sequence = _orig(attrs, attrsCache=attrsCache, formatConfig=formatConfig, **kwargs)
	if not formatConfig or not formatConfig.get("reportColor"):
		return sequence
	fg = attrs.get("color")
	bg = attrs.get("background-color")
	if not isinstance(fg, colors.RGB) or not isinstance(bg, colors.RGB):
		return sequence
	if getattr(bg, "alphaValue", colors.ALPHA_OPAQUE) == colors.ALPHA_TRANSPARENT:
		return sequence
	ratio = _contrast_ratio(fg, bg)
	return list(sequence) + [f"{_hex(fg)} on {_hex(bg)}, contrast {ratio:.1f}:1"]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		global _orig
		_orig = speech.getFormatFieldSpeech
		speech.getFormatFieldSpeech = _patched_getFormatFieldSpeech

	def terminate(self):
		speech.getFormatFieldSpeech = _orig
		super().terminate()
