"""
policy_playbook.py

Purpose:
    Central registry for policy levers and how they conceptually
    map to unemployment shock/recovery scenarios.

This module is intentionally simple and rule-based instead of
using ML. The structure and naming are designed to make the
policy layer clearly identifiable as a unique part of the system.
"""

from typing import Dict, Optional


class PolicyPlaybook:
    """
    Lightweight, opinionated mapping between named policy levers
    and their narrative/analytical interpretation.
    """

    _POLICIES: Dict[str, Dict[str, object]] = {
        "None": {
            "label": "No explicit policy lever",
            "description": (
                "Scenario assumes market-driven adjustment only, without a "
                "targeted employment stabilization programme."
            ),
            "relative_cost": "None",
        },
        "Youth Employment Boost": {
            "label": "Targeted youth employment schemes",
            "description": (
                "Programmes such as apprenticeships, hiring subsidies and "
                "skill-bridging for young workers. Typically accelerates "
                "recovery after an unemployment shock."
            ),
            "relative_cost": "Medium",
        },
        "SME Support Package": {
            "label": "Support package for small and medium enterprises",
            "description": (
                "Credit guarantees, tax relief and wage support targeted at "
                "SMEs to prevent large-scale layoffs during downturns."
            ),
            "relative_cost": "High",
        },
        "Rural Job Guarantee": {
            "label": "Rural public works / job guarantee",
            "description": (
                "Expansion of rural employment guarantee or public works "
                "schemes that cushion job losses for vulnerable households."
            ),
            "relative_cost": "High",
        },
    }

    @classmethod
    def list_policies(cls) -> Dict[str, Dict[str, object]]:
        """
        Returns the internal policy registry.
        """
        return cls._POLICIES

    @classmethod
    def get_policy(cls, name: Optional[str]) -> Dict[str, object]:
        """
        Fetch a policy configuration by name. If the policy is unknown
        or not provided, a neutral 'None' configuration is returned.
        """
        if not name:
            return cls._POLICIES["None"]

        return cls._POLICIES.get(name, cls._POLICIES["None"])

