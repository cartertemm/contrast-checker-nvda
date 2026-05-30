# Color Contrast Checker for NVDA

An NVDA add-on that announces the WCAG contrast ratio between foreground and background colors whenever NVDA reads color information.

Blind accessibility testers often need to verify that text meets WCAG contrast thresholds without relying on sighted colleagues, a process which has historically been difficult to impossible to do without automated checkers. However, this add-on makes it possible by augmenting format information announcements and the format information dialog.

## How it works

When NVDA reads an element with both foreground and background colors, the add-on appends a message like:

> `#1A1A1A on #FFFFFF, contrast 16.1:1`

to format information (NVDA+f or NVDA+shift+f).

WCAG AA requires 4.5:1 for normal text and 3:1 for large text. WCAG AAA requires 7:1.

## Setup

1. Download the `.nvda-addon` file from the releases page.
2. Open it with NVDA running. NVDA will prompt you to install.


### For the contrast of a single object

Press NVDA+f to hear the formatting information of the text under the system carrot (or current focus). Press NVDA+shift+f for the same information, but relative to the review cursor's position. You can also press them two times quickly to get the information presented in a browsable dialog.

In either case, you will be presented with NVDAs typical formatting information, plus the contrast foreground:background, in the form

- Source Sans 3 ExtraLight
- 10.5 pt
- black on white
- align left
- #000000 on #FFFFFF, contrast 21.0:1

## Building from source

Requires Git, Python, and SCons.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

The built `.nvda-addon` file will appear in the project root.

## License

GPL 2.0
