# Rendering the video

The scene uses **Manim Community Edition** and **Text only** (no LaTeX), so it
renders without a TeX install.

## Install

```bash
pip install manim
# system deps if needed (Debian/Ubuntu):
#   sudo apt-get install -y libcairo2-dev libpango1.0-dev ffmpeg pkg-config
```

## Render

```bash
# 720p preview
manim -qm fibrosis_selectivity.py FibrosisSelectivity

# 1080p final
manim -qh fibrosis_selectivity.py FibrosisSelectivity

# animated GIF (for platforms that prefer it)
manim -qh --format=gif fibrosis_selectivity.py FibrosisSelectivity
```

Output lands in `media/videos/fibrosis_selectivity/<quality>/`.

## Mobile / feed aspect ratios

LinkedIn feed favors square (1:1) or vertical (4:5). Render 16:9, then crop with
ffmpeg:

```bash
# 1:1 square
ffmpeg -i FibrosisSelectivity.mp4 -vf "crop=ih:ih" -c:a copy square.mp4
# 4:5 vertical
ffmpeg -i FibrosisSelectivity.mp4 -vf "crop=ih*4/5:ih" vertical.mp4
```

Or set a custom resolution in the scene via `config.pixel_width` /
`config.pixel_height` before rendering.

## Edit the closing card

Update the GitHub handle in `fibrosis_selectivity.py` (`closing()` method,
the `cta` Text) before rendering the final version.
