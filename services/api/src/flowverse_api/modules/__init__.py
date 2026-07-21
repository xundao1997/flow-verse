from flowverse_api.modules.creative_content import BOUNDARY as CREATIVE_CONTENT
from flowverse_api.modules.creative_reference import BOUNDARY as CREATIVE_REFERENCE
from flowverse_api.modules.feedback_decision import BOUNDARY as FEEDBACK_DECISION
from flowverse_api.modules.governance_ops import BOUNDARY as GOVERNANCE_OPS
from flowverse_api.modules.identity_access import BOUNDARY as IDENTITY_ACCESS
from flowverse_api.modules.release_cycle import BOUNDARY as RELEASE_CYCLE
from flowverse_api.modules.review_compliance import BOUNDARY as REVIEW_COMPLIANCE
from flowverse_api.modules.task_lifecycle import BOUNDARY as TASK_LIFECYCLE

BOUNDARIES = (
    IDENTITY_ACCESS,
    TASK_LIFECYCLE,
    CREATIVE_REFERENCE,
    CREATIVE_CONTENT,
    REVIEW_COMPLIANCE,
    RELEASE_CYCLE,
    FEEDBACK_DECISION,
    GOVERNANCE_OPS,
)

__all__ = ["BOUNDARIES"]
