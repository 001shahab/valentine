# 💕 Mathematical Valentine's Heart

A stunning animated visualization of the mathematical heart curve, built entirely in Python.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Made with](https://img.shields.io/badge/Made%20with-♥%20%26%20Mathematics-red)

## The Formula

$$y = |x|^{2/3} + 0.9 \cdot \sin(kx) \cdot \sqrt{3 - x^2}$$

As **k** increases from `0` to `50`, a simple mathematical arch transforms into a beautiful, oscillating heart shape. The animation renders this transformation at **3 FPS** with cinematic easing, and the completed heart gently "breathes" with a subtle pulsing effect.

## Features

- **Beautiful Start screen** — a glowing, animated Start button greets you when the window opens; the animation begins only when you're ready
- **Neon glow effect** — the heart curve is rendered with three overlapping layers to create a soft, glowing aesthetic
- **Cinematic easing** — the build-up uses Hermite interpolation (`3t² − 2t³`) for a dramatic slow-start, fast-middle, slow-end feel
- **Interactive controls** — pause, resume, restart, and adjust the animation speed on the fly
- **Breathing effect** — once the heart is fully formed, it gently pulses as if it were alive
- **Dark romantic theme** — deep black background with vibrant red accents, inspired by the original Instagram post by [@mathswithmuza](https://www.instagram.com/mathswithmuza/)
- **Live formula display** — the mathematical formula and current `k` value are shown in real time

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/valentine.git
cd valentine
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv myenv
source myenv/bin/activate   # macOS / Linux
myenv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python valentine.py
```

A window will open with a beautiful Start screen. Click the **♥ Start** button (or press `SPACE` / `ENTER`) and the heart will begin to form, one frame at a time.

## Controls

| Key | Action |
|---|---|
| `SPACE` | Pause / Resume the animation |
| `R` | Restart from the beginning |
| `↑` (Up Arrow) | Increase animation speed |
| `↓` (Down Arrow) | Decrease animation speed |
| `Q` / `ESC` | Quit |

## How It Works

The heart curve is defined by:

```
y = |x|^(2/3) + 0.9 · sin(kx) · √(3 − x²)
```

where `x ∈ [−√3, √3]` (the domain where `3 − x² ≥ 0`).

- **`|x|^(2/3)`** — creates the foundational arch shape
- **`sin(kx)`** — adds oscillations whose frequency is controlled by `k`
- **`√(3 − x²)`** — acts as an envelope that constrains the curve within the valid domain

When `k = 0`, you see a simple U-shaped arch. As `k` increases toward `50`, the oscillations sculpt the arch into a richly detailed heart shape.

The animation uses **smooth easing** (`f(t) = 3t² − 2t³`) so the build-up starts gently, accelerates through the middle, and decelerates at the end — giving it a cinematic quality even at 3 FPS.

## Project Structure

```
valentine/
├── valentine.py        # Main animation script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── myenv/              # Virtual environment (not committed)
```

## Requirements

- Python 3.8+
- NumPy ≥ 1.21
- Matplotlib ≥ 3.5

## Author

**Prof. Shahab Anbarjafari**
- 🏢 3S Holding OÜ
- 📍 Tartu, Estonia
- 📧 [shb@3sholding.com](mailto:shb@3sholding.com)

## Acknowledgments

Inspired by the beautiful mathematical heart visualization shared by [@mathswithmuza](https://www.instagram.com/mathswithmuza/) on Instagram.

---

*Created with ♥ and Mathematics in Tartu, Estonia*
