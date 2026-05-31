# Color Contrast Checker for NVDA

Digital accessibility testers routinely need to ensure that color contrast ratios fall within thresholds defined by the Web Content Accessibility Guidelines (WCAG). However, it has historically been difficult for blind testers to do this without relying on sighted colleagues or automated solutions that are not always reliable.

This add-on lets you check the contrast of the focused item with NVDA+F, the item under the review cursor with NVDA+shift+f, and the focus indicator with NVDA+Shift+C.

## Text contrast

Press **NVDA+F** on any text to hear formatting information including the contrast ratio. Example:

- Source Sans 3 ExtraLight
- 10.5pt
- black on white
- align left
- #000000 on #FFFFFF, contrast 21.0:1

Press it twice quickly for a browsable dialog. **NVDA+Shift+F** uses the review cursor position instead of the system caret.

WCAG AA requires 4.5:1 for normal text, 3:1 for large text. WCAG AAA requires 7:1.

## Focus indicator contrast

Press **NVDA+Shift+C** on any focused element to hear the contrast between its focus ring and the surrounding background:

> Focus indicator: #000000 on #FFFFFF, contrast 21.0:1

WCAG requires 3:1 for focus indicators.

## Installation

1. Download the `.nvda-addon` file from the releases page.
2. Open it with NVDA running. NVDA will prompt you to install.

## Try it out

Open [tests/contrast.html](tests/contrast.html) in a browser with NVDA running.
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
