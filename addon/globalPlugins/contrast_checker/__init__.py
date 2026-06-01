# Linearize, luminence, and contrast derivation formulae taken from
# https://www.w3.org/TR/WCAG20-TECHS/G17.html

import ctypes
import logging
from collections import namedtuple
log = logging.getLogger(__name__)
import addonHandler
import api
import globalPluginHandler
import speech
import ui
import colors
import html
import config
import textInfos

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")


_orig = None
_ScreenCapture = namedtuple("_ScreenCapture", ("buf", "left", "top", "width", "height"))
_ContrastEntry = namedtuple("_ContrastEntry", ("text", "fg", "bg", "ratio"))


class _BITMAPINFOHEADER(ctypes.Structure):
	_fields_ = [
		("biSize", ctypes.c_uint32),
		("biWidth", ctypes.c_int32),
		("biHeight", ctypes.c_int32),
		("biPlanes", ctypes.c_uint16),
		("biBitCount", ctypes.c_uint16),
		("biCompression", ctypes.c_uint32),
		("biSizeImage", ctypes.c_uint32),
		("biXPelsPerMeter", ctypes.c_int32),
		("biYPelsPerMeter", ctypes.c_int32),
		("biClrUsed", ctypes.c_uint32),
		("biClrImportant", ctypes.c_uint32),
	]


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


def _capture_region(left: int, top: int, width: int, height: int):
	"""Capture a screen region into a pixel buffer via a single BitBlt. Returns _ScreenCapture or None."""
	if width <= 0 or height <= 0:
		return None
	screen_dc = ctypes.windll.user32.GetDC(0)
	mem_dc = ctypes.windll.gdi32.CreateCompatibleDC(screen_dc)
	bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(screen_dc, width, height)
	if not bitmap:
		ctypes.windll.gdi32.DeleteDC(mem_dc)
		ctypes.windll.user32.ReleaseDC(0, screen_dc)
		return None
	old_bmp = ctypes.windll.gdi32.SelectObject(mem_dc, bitmap)
	ctypes.windll.gdi32.BitBlt(mem_dc, 0, 0, width, height, screen_dc, left, top, 0x00CC0020)  # SRCCOPY
	bmi = _BITMAPINFOHEADER()
	bmi.biSize = ctypes.sizeof(_BITMAPINFOHEADER)
	bmi.biWidth = width
	bmi.biHeight = -height  # negative = top-down row order
	bmi.biPlanes = 1
	bmi.biBitCount = 32
	bmi.biCompression = 0  # BI_RGB
	buf = (ctypes.c_ubyte * (width * height * 4))()
	ctypes.windll.gdi32.GetDIBits(mem_dc, bitmap, 0, height, buf, ctypes.byref(bmi), 0)
	ctypes.windll.gdi32.SelectObject(mem_dc, old_bmp)
	ctypes.windll.gdi32.DeleteObject(bitmap)
	ctypes.windll.gdi32.DeleteDC(mem_dc)
	ctypes.windll.user32.ReleaseDC(0, screen_dc)
	return _ScreenCapture(buf, left, top, width, height)


def _pixel_at(capture: _ScreenCapture, x: int, y: int):
	"""Read a pixel from a _ScreenCapture by screen coordinates. Returns colors.RGB or None if out of bounds."""
	rx = x - capture.left
	ry = y - capture.top
	if rx < 0 or rx >= capture.width or ry < 0 or ry >= capture.height:
		return None
	offset = (ry * capture.width + rx) * 4
	# 32-bit DIB pixel order: [B, G, R, reserved]
	return colors.RGB(capture.buf[offset + 2], capture.buf[offset + 1], capture.buf[offset])


def _sample_perimeter(capture: _ScreenCapture, left: int, top: int, width: int, height: int, distance: int):
	"""Sample pixels along all four edges at `distance` pixels outside the element bounding box."""
	pixels = []
	step = max(2, min(width, height) // 8)
	right = left + width - 1
	bottom = top + height - 1
	for x in range(left, right + 1, step):
		p = _pixel_at(capture, x, top - distance)
		if p is not None:
			pixels.append(p)
		p = _pixel_at(capture, x, bottom + distance)
		if p is not None:
			pixels.append(p)
	for y in range(top, bottom + 1, step):
		p = _pixel_at(capture, left - distance, y)
		if p is not None:
			pixels.append(p)
		p = _pixel_at(capture, right + distance, y)
		if p is not None:
			pixels.append(p)
	return pixels


def _dominant_color(pixels):
	"""Return the most common color from a list of RGB samples, quantized to reduce anti-aliasing noise."""
	if not pixels:
		return None
	buckets = {}
	for p in pixels:
		key = (p.red >> 4, p.green >> 4, p.blue >> 4)
		if key not in buckets:
			buckets[key] = []
		buckets[key].append(p)
	dominant = max(buckets.values(), key=len)
	r = sum(p.red for p in dominant) // len(dominant)
	g = sum(p.green for p in dominant) // len(dominant)
	b = sum(p.blue for p in dominant) // len(dominant)
	return colors.RGB(r, g, b)


def _collect_from_text_info(info):
	format_config = {k: False for k in config.conf["documentFormatting"]}
	format_config["reportColor"] = True
	format_config["detectFormatAfterCursor"] = True
	fg = None
	bg = None
	results = []
	for item in info.getTextWithFields(format_config):
		if isinstance(item, textInfos.FieldCommand) and item.command == "formatChange":
			attrs = item.field
			c = attrs.get("color")
			bc = attrs.get("background-color")
			if isinstance(c, colors.RGB):
				fg = c
			if isinstance(bc, colors.RGB):
				bg = bc
		elif isinstance(item, str) and item.strip() and fg is not None and bg is not None:
			results.append((item, fg, bg))
	return results


def _collect_from_obj_tree(obj, depth=0):
	if depth >= 50:
		return []
	try:
		info = obj.makeTextInfo(textInfos.POSITION_ALL)
		results = _collect_from_text_info(info)
		if results:
			return results
	except Exception:
		pass
	results = []
	try:
		children = obj.children
	except Exception:
		return results
	for child in children:
		results.extend(_collect_from_obj_tree(child, depth + 1))
	return results


def _collect_contrast_data(obj):
	try:
		info = obj.treeInterceptor.makeTextInfo(textInfos.POSITION_ALL)
		results = _collect_from_text_info(info)
		if results:
			return results
	except Exception:
		pass
	try:
		info = obj.makeTextInfo(textInfos.POSITION_ALL)
		results = _collect_from_text_info(info)
		if results:
			return results
	except Exception:
		pass
	return _collect_from_obj_tree(obj)


def _bucket_results(entries):
	seen = set()
	deduped = []
	for e in entries:
		key = (e.text[:255], e.fg, e.bg)
		if key not in seen:
			seen.add(key)
			deduped.append(e)
	# Entries at or above 7:1 pass all WCAG thresholds and are excluded from output.
	below_3 = [e for e in deduped if e.ratio < 3.0]
	below_4_5 = [e for e in deduped if 3.0 <= e.ratio < 4.5]
	below_7 = [e for e in deduped if 4.5 <= e.ratio < 7.0]
	return below_3, below_4_5, below_7


def _build_audit_html(below_3, below_4_5, below_7):
	parts = []
	for heading, bucket in (
		(_("Below 3:1 (large text or UI components)"), below_3),
		(_("Below 4.5:1 (normal or small text)"), below_4_5),
		(_("Below 7:1 (AAA level)"), below_7),
	):
		if not bucket:
			continue
		parts.append(f"<h1>{html.escape(heading)}</h1><ul>")
		for e in bucket:
			text = html.escape(e.text[:255])
			parts.append(f"<li>{text}: {_hex(e.fg)} on {_hex(e.bg)}, {e.ratio:.1f}:1</li>")
		parts.append("</ul>")
	if not parts:
		return f"<p>{html.escape(_('No contrast failures found'))}</p>"
	return "".join(parts)


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
	# Translators: Spoken message reporting the foreground color, background color, and their contrast ratio. {fg} and {bg} are hex color codes, {ratio} is a number like 4.5
	return list(sequence) + [_("{fg} on {bg}, contrast {ratio}:1").format(fg=_hex(fg), bg=_hex(bg), ratio=f"{ratio:.1f}")]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Contrast Checker")

	def __init__(self):
		super().__init__()
		global _orig
		_orig = speech.getFormatFieldSpeech
		speech.getFormatFieldSpeech = _patched_getFormatFieldSpeech

	def terminate(self):
		speech.getFormatFieldSpeech = _orig
		super().terminate()

	def script_checkFocusIndicator(self, gesture):
		obj = api.getFocusObject()
		if obj is None:
			# Translators: Spoken when no element has keyboard focus
			ui.message(_("No focused element"))
			return
		loc = obj.location
		if loc is None:
			# Translators: Spoken when the focused element has no reported screen location
			ui.message(_("Focused element has no screen location"))
			return
		try:
			left, top, width, height = loc.left, loc.top, loc.width, loc.height
		except AttributeError:
			left, top, width, height = loc[0], loc[1], loc[2], loc[3]
		if width <= 0 or height <= 0:
			# Translators: Spoken when the focused element has zero size
			ui.message(_("Focused element has no visible area"))
			return
		# Capture the element plus a 10px margin in one BitBlt, then all pixel reads are
		# just array indexing into the in-memory buffer with no further GDI calls.
		MARGIN = 10
		capture = _capture_region(left - MARGIN, top - MARGIN, width + 2 * MARGIN, height + 2 * MARGIN)
		if capture is None:
			# Translators: Spoken when screen capture fails
			ui.message(_("Could not capture screen region"))
			return
		# Background reference at 8px outside; well within the captured margin.
		bg_pixels = _sample_perimeter(capture, left, top, width, height, distance=8)
		bg = _dominant_color(bg_pixels)
		if bg is None:
			# Translators: Spoken when no pixels could be sampled (e.g. element is at the screen edge)
			ui.message(_("Could not sample screen colors"))
			return
		# Scan 1-4px outside to find the highest-contrast transition, this usually points to the focus ring.
		best_ratio = 1.0
		best_color = bg
		for d in (1, 2, 3, 4):
			pixels = _sample_perimeter(capture, left, top, width, height, distance=d)
			color = _dominant_color(pixels)
			if color is None:
				continue
			r = _contrast_ratio(color, bg)
			if r > best_ratio:
				best_ratio = r
				best_color = color
		# Translators: Reports the focus indicator color, surrounding background color, and contrast ratio. {indicator} and {bg} are hex color codes, {ratio} is a number like 4.5
		ui.message(
			_("Focus indicator: {indicator} on {bg}, contrast {ratio}:1").format(
				indicator=_hex(best_color),
				bg=_hex(bg),
				ratio=f"{best_ratio:.1f}",
			)
		)

	# Translators: Description of the script that checks focus indicator contrast, shown in the Input Gestures dialog
	script_checkFocusIndicator.__doc__ = _("Report the contrast of the focus indicator for the focused element")

	def script_pageContrastAudit(self, gesture):
		obj = api.getFocusObject()
		if obj is None:
			# Translators: Spoken when no element has keyboard focus
			ui.message(_("No focused element"))
			return
		raw = _collect_contrast_data(obj)
		if not raw:
			ui.message(_("No text with color information found"))
			return
		entries = [
			_ContrastEntry(text=text, fg=fg, bg=bg, ratio=_contrast_ratio(fg, bg))
			for text, fg, bg in raw
		]
		below_3, below_4_5, below_7 = _bucket_results(entries)
		if not below_3 and not below_4_5 and not below_7:
			ui.message(_("No contrast failures found"))
			return
		html_content = _build_audit_html(below_3, below_4_5, below_7)
		ui.browseableMessage(html_content, _("Page contrast audit"), isHtml=True)

	# Translators: Description of the script that scans the page for contrast failures, shown in the Input Gestures dialog
	script_pageContrastAudit.__doc__ = _("Scan the current document for color contrast failures")

	__gestures = {
		"kb:NVDA+shift+c": "checkFocusIndicator",
		"kb:NVDA+shift+control+f": "pageContrastAudit",
	}
