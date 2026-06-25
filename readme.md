# Color Contrast Checker for NVDA

Digital accessibility testers routinely need to ensure that color contrast ratios fall within thresholds defined by the Web Content Accessibility Guidelines (WCAG). However, it has historically been difficult for blind testers to do this without relying on sighted colleagues or automated solutions. Most automated solutions in-market, including WAVE and axe DevTools, only filter contrast issues as "suggestions", miss things, and do not examine the focus indicator.

This add-on lets you check the contrast of the focused item with NVDA+F, the item under the review cursor with NVDA+Shift+F, the focus indicator with NVDA+Shift+C, and run a page-wide audit of all text contrast failures with NVDA+Shift+Ctrl+F.

| Task | Command | Scope |
| --- | --- | --- |
| Check focused text contrast | **NVDA+F** | Formatting information for the focused item, including contrast ratio |
| Check review cursor text contrast | **NVDA+Shift+F** | Formatting information at the review cursor position, including contrast ratio |
| Check focus indicator contrast | **NVDA+Shift+C** | Focus ring against the surrounding background |
| Run a page-wide text audit | **NVDA+Shift+Ctrl+F** | Visible text on the current page, grouped by WCAG contrast threshold |

## Text contrast

This add-on extends NVDA's existing format information commands. Press **NVDA+F** on any text to hear formatting information including the contrast ratio. Example:

- Source Sans 3 ExtraLight
- 10.5pt
- black on white
- align left
- `#000000 on #FFFFFF, contrast 21.0:1`

Press it twice quickly for a browsable dialog. **NVDA+Shift+F** uses the review cursor position instead of the system caret.

WCAG AA requires 4.5:1 for normal text, 3:1 for large text. WCAG AAA requires 7:1.

## Focus indicator contrast

Press **NVDA+Shift+C** on any focused element to hear the contrast between its focus ring and the surrounding background:

> `Focus indicator: #000000 on #FFFFFF, contrast 21.0:1`

WCAG evaluates focus indicators through related requirements. Non-text contrast requires the visual focus indicator to have at least 3:1 contrast against adjacent colors, and WCAG 2.2 focus appearance adds requirements around the contrast of the change and the indicator's size. This add-on reports the contrast measurement; testers should still evaluate the full focus appearance requirement.

## Page-wide contrast audit

Press **NVDA+Shift+Ctrl+F** to scan every piece of text on the current page at once. Results open in a browsable dialog, grouped by severity:

- Below 3:1 (large text)
- Below 4.5:1 (normal or small text)
- Below 7:1 (AAA text contrast)

Text that meets 7:1 or better passes all WCAG thresholds and is omitted. If nothing fails, NVDA says so instead of opening the dialog.

Please note that this command only checks text that is visible in the current page state. You still need to reveal and test other states such as focus, hover, expanded or collapsed content, lazy-loaded content, and custom-rendered or image-based text. Focus-ring contrast is checked separately with **NVDA+Shift+C**.

## Installation

1. Install from the NVDA add-on store (NVDA menu -> Tools -> Addon store -> Available add-ons tab -> Color contrast checker for NVDA -> Actions -> Install). Alternatively, download the latest release from [this link](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/).
2. If you aren't obtaining it from the add-on store, open the .nvda-addon file with NVDA running. NVDA will prompt you to install.

## Try it out

Open `tests/test_contrast.html` locally, or [the rendered test page](https://ctemm.me/files/test_contrast.html) in a browser with NVDA running.
It covers various common scenarios like text contrast, focus rings at known ratios, missing rings, box-shadow rings, non-white backgrounds, and different element types.

## Building from source

Requires Git, Python, and SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

The built `.nvda-addon` file appears in the project root.

## License

GPL 2.0
