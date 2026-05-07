from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RouteOutcome(StrEnum):
    APPROVED = "approved"
    FLAGGED_FOR_REVIEW = "flagged_for_review"
    REJECTED = "rejected"


class ReviewPacketStatus(StrEnum):
    PENDING = "pending"
    CLAIMED = "claimed"
    RESOLVED_APPROVED = "resolved_approved"
    RESOLVED_REJECTED = "resolved_rejected"
    DEAD_LETTER = "dead_letter"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ReasonCode(StrEnum):
    MISSING_REQUIRED_FIELD = "missing_required_field"
    CONFIDENCE_BELOW_THRESHOLD = "confidence_below_threshold"
    ARITHMETIC_MISMATCH = "arithmetic_mismatch"
    DUPLICATE_EXACT = "duplicate_exact"
    DUPLICATE_NEEDS_REVIEW = "duplicate_needs_review"
    CURRENCY_INCONSISTENCY = "currency_inconsistency"
    DATE_SANITY_FAILURE = "date_sanity_failure"
    TAX_ID_ISSUE = "tax_id_issue"
    EXPORT_MAPPING_ISSUE = "export_mapping_issue"
    LINE_ITEM_INCOMPLETE = "line_item_incomplete"


class ExportTarget(StrEnum):
    XERO = "xero"
    FORTNOX = "fortnox"
    QUICKBOOKS = "quickbooks"
    CSV = "csv"


class SourceReference(BaseModel):
    line_number: int | None = None
    snippet: str | None = None
    label: str | None = None


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float
    currency: str | None = None


class InvoiceIngest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_name: str
    source_document_name: str
    document_text: str
    vendor_name: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    currency: str | None = None
    subtotal: float | None = None
    tax_amount: float | None = None
    total: float | None = None
    tax_id: str | None = None
    payment_terms: str | None = None
    line_items: list[LineItem] = Field(default_factory=list)
    currency_mentions: list[str] = Field(default_factory=list)
    known_duplicate: bool = False
    duplicate_reference: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractedField(BaseModel):
    field_name: str
    value: str | float | None
    confidence: float
    extraction_method: str
    source_reference: SourceReference | None = None
    missing_reason: str | None = None

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return value


class ExtractionResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    scenario_name: str
    fields: dict[str, ExtractedField]
    overall_confidence: float
    extraction_methods: list[str]
    required_fields_present: list[str]
    missing_fields: list[str]


class ValidationFinding(BaseModel):
    severity: Severity
    reason_code: ReasonCode
    message: str
    field_name: str | None = None


class ValidationReport(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    findings: list[ValidationFinding]
    approved_candidate: bool
    duplicate_key: str
    exact_duplicate: bool
    arithmetic_delta: float


class RoutingDecision(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    outcome: RouteOutcome
    reasons: list[ReasonCode]
    review_packet_required: bool
    export_allowed: bool
    recommended_next_step: str


class ReviewPacket(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    packet_id: str
    scenario_name: str
    status: ReviewPacketStatus
    reason_codes: list[ReasonCode]
    reason_summary: str
    evidence_snippets: list[str]
    recommended_next_step: str
    claimed_by: str | None = None
    resolution_note: str | None = None


class AccountingExportPreview(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    target: ExportTarget
    payload: dict[str, Any]
    meta: dict[str, Any]


class QueueResolution(BaseModel):
    decision: str
    note: str

    @model_validator(mode="after")
    def validate_decision(self) -> QueueResolution:
        if self.decision not in {"approve", "reject"}:
            raise ValueError("decision must be approve or reject")
        return self
