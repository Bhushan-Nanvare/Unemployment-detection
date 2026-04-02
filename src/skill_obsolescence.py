"""
Skill Obsolescence Detector (Feature 4)

Goal:
  Detect skills that are declining (becoming obsolete) and skills that are emerging
  using *time-series mention counts* extracted from job posting text.

This is not a hardcoded/dummy percentage. Trends are computed from the provided CSV
using `post_date` + the same phrase matching lexicon used across Feature 2/3.

Expected input:
  DataFrame with columns:
    - post_date: parsable to datetime
    - job_title (optional but recommended)
    - description (optional)
    - plus any other columns (ignored)

The loader used by UI ensures `_text` (lowercased job_title + description) exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from src.job_market_pulse import phrase_in_blob, skill_phrase_list


try:
    from scipy.stats import linregress
except Exception as e:  # pragma: no cover
    linregress = None  # type: ignore


def _require_scipy() -> None:
    if linregress is None:
        raise ImportError(
            "scipy is required for Feature 4 trend significance. "
            "Run `pip install scipy`."
        )


def _freq_to_pandas_rule(freq: str) -> str:
    f = (freq or "").upper().strip()
    if f in {"W", "WEEKLY"}:
        return "W"
    if f in {"M", "MONTHLY"}:
        return "M"
    raise ValueError("freq must be 'W'/'WEEKLY' or 'M'/'MONTHLY'")


def _extract_top_skills(
    df: pd.DataFrame,
    top_k: int,
    min_total_mentions: int,
    phrases: Optional[Sequence[str]] = None,
) -> List[str]:
    phrases = list(phrases or skill_phrase_list())
    if df.empty or "_text" not in df.columns:
        return []

    totals: Dict[str, int] = {p: 0 for p in phrases}
    for blob in df["_text"]:
        for p in phrases:
            if phrase_in_blob(p, blob):
                totals[p] += 1

    s = pd.Series(totals).sort_values(ascending=False)
    s = s[s >= int(min_total_mentions)]
    return s.head(int(top_k)).index.tolist()


def _build_time_series_counts(
    df: pd.DataFrame,
    skills: Sequence[str],
    freq_rule: str,
) -> Tuple[pd.DataFrame, List[pd.Timestamp]]:
    if df.empty or "post_date" not in df.columns or "_text" not in df.columns:
        return pd.DataFrame(), []

    d = df.copy()
    d["post_date"] = pd.to_datetime(d["post_date"], errors="coerce")
    d = d.dropna(subset=["post_date"])
    if d.empty:
        return pd.DataFrame(), []

    # Use period start timestamps for stable sorting/plotting.
    d["bucket"] = d["post_date"].dt.to_period(freq_rule).apply(
        lambda p: p.start_time
    )
    buckets = sorted(d["bucket"].unique().tolist())

    rows: List[Dict[str, object]] = []
    for b in buckets:
        sub = d[d["bucket"] == b]
        # Mention count per skill = count of rows whose text contains the phrase.
        for sk in skills:
            cnt = 0
            for blob in sub["_text"]:
                if phrase_in_blob(sk, blob):
                    cnt += 1
            rows.append({"bucket": b, "skill": sk, "mentions": cnt})

    tall = pd.DataFrame(rows)
    if tall.empty:
        return pd.DataFrame(), buckets

    pivot = tall.pivot_table(
        index="bucket",
        columns="skill",
        values="mentions",
        aggfunc="sum",
        fill_value=0,
    ).sort_index()
    return pivot, buckets


@dataclass
class SkillTrend:
    skill: str
    total_mentions: int
    first_mentions: int
    last_mentions: int
    slope_mentions_per_step: float
    slope_log_mentions_per_step: float
    r2_log: float
    p_value: float
    category: str  # Emerging / Declining / Stable-ish
    estimated_months_to_fade: Optional[float] = None
    estimated_months_to_emerge: Optional[float] = None


def _categorize_by_trend(
    slope_log: float,
    p_value: float,
    alpha: float,
    slope_threshold: float,
    category_min_change_ratio: float,
    first_mentions: int,
    last_mentions: int,
) -> str:
    if p_value >= alpha:
        return "Stable-ish"
    if abs(slope_log) < slope_threshold:
        return "Stable-ish"

    # Require meaningful relative change.
    denom = max(1, first_mentions)
    change_ratio = last_mentions / denom
    if slope_log > 0 and change_ratio >= category_min_change_ratio:
        return "Emerging"
    if slope_log < 0 and change_ratio <= 1.0 / max(1e-9, category_min_change_ratio):
        return "Declining"
    return "Stable-ish"


def _estimate_time_to_threshold_log_model(
    x_steps: np.ndarray,
    y_counts: np.ndarray,
    threshold_mentions: int,
    step_duration_months: float,
) -> Optional[float]:
    """
    Fits:
      log1p(count) = a + b * x
    Then solves for x where count == threshold_mentions:
      log1p(threshold) = a + b*x  =>  x = (log1p(threshold)-a)/b
    Returns months from last observed step. Returns None if b is ~0.
    """
    if len(x_steps) < 3:
        return None

    y = np.log1p(y_counts.astype(float))
    if np.all(np.isclose(y, y[0])):
        return None

    # Ordinary least squares (sufficient given small dataset sizes)
    # polyfit returns [slope, intercept] for degree=1.
    slope, intercept = np.polyfit(x_steps, y, 1)

    if abs(slope) < 1e-12:
        return None

    x_thresh = (np.log1p(threshold_mentions) - intercept) / slope
    x_last = float(x_steps.max())
    dx = x_thresh - x_last
    if dx < 0:
        # Already below/above threshold in the observation window.
        return 0.0
    return float(dx * step_duration_months)


def detect_skill_obsolescence(
    df: pd.DataFrame,
    freq: str = "M",
    top_k: int = 12,
    min_total_mentions: int = 8,
    alpha: float = 0.05,
    slope_threshold_log: float = 0.02,
    category_min_change_ratio: float = 1.8,
    phrases: Optional[Sequence[str]] = None,
    fade_threshold_mentions: int = 1,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      - summary_df: per-skill trend classification
      - timeseries_df: pivoted mention counts indexed by bucket (datetime)
    """
    _require_scipy()
    freq_rule = _freq_to_pandas_rule(freq)
    pivot, buckets = _build_time_series_counts(
        df=df,
        skills=_extract_top_skills(
            df=df,
            top_k=top_k,
            min_total_mentions=min_total_mentions,
            phrases=phrases,
        ),
        freq_rule=freq_rule,
    )

    if pivot.empty or pivot.shape[1] == 0:
        return pd.DataFrame(), pd.DataFrame()

    # time index in steps (0..T-1)
    x = np.arange(pivot.shape[0], dtype=float)
    step_duration_months = 1.0 if freq_rule == "M" else (1.0 / 4.0)  # approx: 4 weeks ~ 1 month

    summary_rows: List[Dict[str, object]] = []
    for skill in pivot.columns.tolist():
        y = pivot[skill].values.astype(float)
        total = int(np.sum(y))
        first = int(y[0]) if len(y) else 0
        last = int(y[-1]) if len(y) else 0

        # Use log1p counts to stabilize variance.
        y_log = np.log1p(y)
        lr_log = linregress(x, y_log)
        lr_mentions = linregress(x, y)

        slope_mentions = float(lr_mentions.slope)
        slope_log = float(lr_log.slope)
        r2_log = float(lr_log.rvalue ** 2)
        p_val = float(lr_log.pvalue) if lr_log.pvalue is not None else 1.0

        cat = _categorize_by_trend(
            slope_log=slope_log,
            p_value=p_val,
            alpha=alpha,
            slope_threshold=slope_threshold_log,
            category_min_change_ratio=category_min_change_ratio,
            first_mentions=first,
            last_mentions=last,
        )

        estimated_fade: Optional[float] = None
        estimated_emerge: Optional[float] = None
        if cat == "Declining":
            # How long until counts drop below threshold?
            estimated_fade = _estimate_time_to_threshold_log_model(
                x_steps=x,
                y_counts=y,
                threshold_mentions=fade_threshold_mentions,
                step_duration_months=step_duration_months,
            )
        elif cat == "Emerging":
            # How long until it reaches 2 mentions/month (or equivalent per bucket)?
            # This is heuristic but computed from the fitted log-linear trend.
            estimated_emerge = _estimate_time_to_threshold_log_model(
                x_steps=x,
                y_counts=y,
                threshold_mentions=max(2, fade_threshold_mentions + 1),
                step_duration_months=step_duration_months,
            )

        summary_rows.append(
            {
                "skill": skill,
                "total_mentions": total,
                "first_mentions": first,
                "last_mentions": last,
                "slope_mentions_per_step": round(slope_mentions, 4),
                "slope_log_mentions_per_step": round(slope_log, 4),
                "r2_log": round(r2_log, 4),
                "p_value": round(p_val, 6),
                "category": cat,
                "estimated_months_to_fade": estimated_fade,
                "estimated_months_to_emerge": estimated_emerge,
            }
        )

    summary_df = pd.DataFrame(summary_rows).sort_values(
        by=["category", "p_value", "total_mentions"], ascending=[True, True, False]
    )
    pivot.index.name = "bucket"
    return summary_df, pivot

