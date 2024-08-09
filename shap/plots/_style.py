"""Configuration of customisable style options for SHAP plots.

NOTE: This is experimental and subject to change!
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from typing import Union

import numpy as np

from . import colors

# Type hints, adapted from matplotlib.typing
RGBColorType = Union[tuple[float, float, float], str]
RGBAColorType = Union[
    str,  # "none" or "#RRGGBBAA"/"#RGBA" hex strings
    tuple[float, float, float, float],
    # 2 tuple (color, alpha) representations, not infinitely recursive
    # RGBColorType includes the (str, float) tuple, even for RGBA strings
    tuple[RGBColorType, float],
    # (4-tuple, float) is odd, but accepted as the outer float overriding A of 4-tuple
    tuple[tuple[float, float, float, float], float],
]
ColorType = Union[RGBColorType, RGBAColorType, np.ndarray]


@dataclass
class StyleConfig:
    """Configuration of colors across all matplotlib-based shap plots."""

    # Waterfall plot config
    primary_color_positive: ColorType = field(default_factory=lambda: colors.red_rgb)
    primary_color_negative: ColorType = field(default_factory=lambda: colors.blue_rgb)
    secondary_color_positive: ColorType = field(default_factory=lambda: colors.light_red_rgb)
    secondary_color_negative: ColorType = field(default_factory=lambda: colors.light_blue_rgb)
    hlines_color: ColorType = "#cccccc"
    vlines_color: ColorType = "#bbbbbb"
    text_color: ColorType = "white"
    tick_labels_color: ColorType = "#999999"


def load_default_style() -> StyleConfig:
    """Load the default style configuration."""
    # In future, this could allow reading from a persistent config file, like matplotlib rcParams
    return StyleConfig()


# Singleton instance that determines the current style.
# Caution! To ensure the correct object is picked up, this must be used like:
#     from shap.plots import _style
#     color = _style.STYLE.text_color
# And NOT like:
#     from shap.plots._style import STYLE   # Wrong!
#     color = STYLE.text_color

STYLE = load_default_style()


def get_style() -> StyleConfig:
    """Return the current style configuration."""
    return STYLE


def set_style(style: StyleConfig):
    """Set the current style configuration."""
    global STYLE
    STYLE = style


@contextmanager
def style_context(style: StyleConfig):
    """Context manager to temporarily change the style.

    NOTE: This is experimental and subject to change!

    Example
    -------
    with shap.plots.style_context(new_style):
        shap.plots.waterfall(...)
    """
    global STYLE
    old_style = STYLE
    STYLE = style
    yield
    STYLE = old_style


@contextmanager
def style_overrides(**kwargs):
    """Context manager to temporarily override a subset of parameters.

    NOTE: This is experimental and subject to change!

    Example
    -------
    with shap.plots.style_overrides(text="black"):
        shap.plots.waterfall(...)
    """
    global STYLE
    old_style = STYLE
    STYLE = replace(old_style, **kwargs)
    yield
    STYLE = old_style
