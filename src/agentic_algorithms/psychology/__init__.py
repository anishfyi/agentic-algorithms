"""Psychology engineering for agent UX, trust, and ethical persuasion."""

from agentic_algorithms.psychology.biases import (
    bias_mitigation_prompt,
    detect_overconfidence_markers,
    detect_sycophancy_markers,
)
from agentic_algorithms.psychology.cognitive_load import (
    progressive_disclosure_plan,
    readability_score,
)
from agentic_algorithms.psychology.framing import (
    gain_frame,
    loss_aversion_frame,
    neutral_frame,
)
from agentic_algorithms.psychology.motivation import sdt_tone_score
from agentic_algorithms.psychology.nudges import (
    commitment_prompt,
    default_option_label,
    social_proof_line,
)
from agentic_algorithms.psychology.persuasion import (
    cialdini_principle_score,
    ethical_persuasion_check,
)
from agentic_algorithms.psychology.trust import agent_trust_score, transparency_checklist

__all__ = [
    "agent_trust_score",
    "bias_mitigation_prompt",
    "cialdini_principle_score",
    "commitment_prompt",
    "default_option_label",
    "detect_overconfidence_markers",
    "detect_sycophancy_markers",
    "ethical_persuasion_check",
    "gain_frame",
    "loss_aversion_frame",
    "neutral_frame",
    "progressive_disclosure_plan",
    "readability_score",
    "sdt_tone_score",
    "social_proof_line",
    "transparency_checklist",
]
