import os
import uuid
import json
import time
import logging
import re
from contextlib import asynccontextmanager
from typing import Dict, Any, List
import jwt

# Core Third-Party Frameworks
try:
    from fastapi import Header, FastAPI, HTTPException, Security, status, Depends
    from fastapi.security.api_key import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
except ImportError:
    FastAPI = None
    Security = Depends = Any
    class APIKeyHeader:
        def __init__(self, *args, **kwargs):
            pass
            
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail

try:
    from pydantic import BaseModel, Field
except ImportError:
    from dataclasses import dataclass, field
    BaseModel = dataclass
    def Field(default=..., **kwargs):
        default_val = None if default is ... else default
        return field(default=default_val, metadata=kwargs)

# Async Database Driver
import asyncpg

# Environment Configurations
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/lending_db")
API_KEY_NAME = "X-Agent-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# --- LAYER 1: PRODUCTION LOGGING & GOVERNANCE ---
class JSONComplianceFormatter(logging.Formatter):
    """Custom logging formatter to output logs safely in structured JSON format."""
    def format(self, record):
        safe_extra = {}
        for k, v in record.__dict__.items():
            if k not in ["msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process"]:
                if isinstance(v, (str, int, float, bool, type(None), dict, list)):
                    try:
                        json.dumps({k: v})
                        safe_extra[k] = v
                    except Exception:
                        continue

        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "tx_id": getattr(record, "tx_id", None),
            "request_id": getattr(record, "request_id", None),
            "extra": safe_extra,
        }
        return json.dumps(log_record)

# Configure system log layers
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
for h in logger.handlers[:]:
    logger.removeHandler(h)

handler = logging.StreamHandler()
handler.setFormatter(JSONComplianceFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# --- LIFESPAN MANAGER (Database Pool Connection Lifecycles) ---
class DatabaseManager:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=5,
                max_size=20,
                command_timeout=60.0
            )
            logger.info("Successfully established asynchronous PostgreSQL connection pool.")
        except Exception as e:
            logger.critical(f"Database connection pool initialization failed: {str(e)}")
            raise e

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool safely disassembled.")

db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(app: FastAPI): # pyright: ignore[reportInvalidTypeForm]
    await db_manager.connect()
    yield
    await db_manager.disconnect()

app = FastAPI(lifespan=lifespan) if FastAPI is not None else None


# --- LAYER 2: MULTILINGUAL BANKING LEXICON ---
class BankingLexicon:
    def __init__(self):
        self.lexicon = {
            "ස්ථිර රැකියාව - ABC සමාගම": "PERMANENT_EMPLOYMENT_ABC_COMPANY",
            "නිවස අලුත්වැඩියා කිරීම": "HOME_RENOVATION"
        }

    def translate_term(self, local_term: str) -> str:
        if not local_term:
            return "local_term_not_found"
        return self.lexicon.get(local_term.strip(), "local_term_not_found")


# --- LAYER 3: INGESTION INPUT SCHEMA ---
class OCRInboundPayload(BaseModel):
    ocr_confidence_score: float = Field(..., description="Layout validation score", json_schema_extra={"example": 0.92})
    raw_employment_sinhala: str = Field(..., description="Raw employment script value", json_schema_extra={"example": "ස්ථිර රැකියාව - ABC සමාගම"})
    raw_loan_purpose_sinhala: str = Field(..., description="Raw purpose script value", json_schema_extra={"example": "නිවස අලුත්වැඩියා කිරීම"})
    raw_monthly_income: float = Field(..., description="Stated base salary", json_schema_extra={"example": 50000.0})
    received_at: str = Field(..., description="ISO Ingress Timestamp", json_schema_extra={"example": "2026-05-30T10:20:00Z"})
    request_id: str = Field(..., description="Unique tracking identification string", json_schema_extra={"example": "req_2026_12345678"})
    requested_loan_amount: float = Field(..., description="Stated asset load request", json_schema_extra={"example": 200000.0})
    crib_score: int = Field(..., description="Central Credit Bureau Rating", json_schema_extra={"example": 750})
    existing_debts: float = Field(..., description="Stated active dynamic liability tier", json_schema_extra={"example": 15000.0})

class CorrectedFeatures(BaseModel):
    target_verdict: str = Field(..., description="'APPROVE' or 'REJECT'")
    verified_net_income: float = Field(..., description="Manually corrected human asset tracking value")

class ManualOverrideRequest(BaseModel):
    application_id: str = Field(..., description="Corresponds to application asset token context")
    officer_id: str = Field(..., description="Underwriting management ID signature")
    override_reason: str = Field(..., description="Audit rationale text metadata logs")
    corrected_features: CorrectedFeatures


# --- LAYER 4: DETAILED FINANCIAL FEATURE EXTRACTION ENGINE ---
class FinancialFeatureExtractionEngine:
    def clean_currency(self, text: str) -> float:
        cleaned = re.sub(r'[^\d.]', '', text)
        return float(cleaned) if cleaned else 0.0
    
    def extract_features(self, payload: OCRInboundPayload) -> Dict[str, Any]:
        raw_inc = getattr(payload, "raw_monthly_income", 0.0)
        req_amt = getattr(payload, "requested_loan_amount", 0.0)
        ex_debts = getattr(payload, "existing_debts", 0.0)
        emp_sinhala = getattr(payload, "raw_employment_sinhala", "")
        purp_sinhala = getattr(payload, "raw_loan_purpose_sinhala", "")
        c_score = getattr(payload, "crib_score", 0)

        monthly_income = self.clean_currency(str(raw_inc))
        requested_loan_amount = self.clean_currency(str(req_amt))
        existing_debts = self.clean_currency(str(ex_debts))
        
        total_monthly_obligations = existing_debts + (requested_loan_amount / 12)
        dti_ratio = total_monthly_obligations / monthly_income if monthly_income > 0 else 1.0

        return {
            "employment_status": BankingLexicon().translate_term(emp_sinhala),
            "loan_purpose": BankingLexicon().translate_term(purp_sinhala),
            "monthly_income": monthly_income,
            "requested_loan_amount": requested_loan_amount,
            "crib_score": c_score,
            "existing_debts": existing_debts,
            "total_monthly_obligations": total_monthly_obligations,
            "dti_ratio": dti_ratio
        }


# --- LAYER 5: DETERMINISTIC BANKING RULES ENGINE ---
class DeterministicBankingRulesEngine:  # Fixed spelling typo from Dterministic
    def apply_rules(self, features: Dict[str, Any]) -> Dict[str, Any]:
        decision = "REJECT"
        reasons = []
        
        if features["crib_score"] < 600:
            reasons.append("Low CRIB score")
        if features["dti_ratio"] > 0.4:
            reasons.append("High DTI ratio")
        if features["employment_status"] == "local_term_not_found":
            reasons.append("Unknown employment status")
        if features["loan_purpose"] == "local_term_not_found":
            reasons.append("Unknown loan purpose")
        
        if not reasons:
            decision = "APPROVE"
        
        return {
            "decision": decision,
            "reasons": reasons
        }


# --- LAYER 6: MULTI-AGENT STATE MACHINE RUNTIME ---
class UnderwritingOrchestrator:
    def _generate_mock_embedding(self) -> List[float]:
        base_vector = [0.01536] * 1536
        return base_vector

    async def execute_pipeline(self, payload: OCRInboundPayload, tx_id: str, api_key: str) -> Dict[str, Any]:
        req_id = getattr(payload, "request_id", "unknown_req")
        logger.info(f"Starting underwriting pipeline for transaction {tx_id}", extra={"tx_id": tx_id, "request_id": req_id})

        financial_features = {
            "monthly_income": getattr(payload, "raw_monthly_income", 0.0),
            "dti_ratio": 1.0,
            "requested_loan_amount": getattr(payload, "requested_loan_amount", 0.0),
            "crib_score": getattr(payload, "crib_score", 0),
            "employment_status": "UNKNOWN",
            "loan_purpose": "UNKNOWN"
        }
        decision_result = {"decision": "ESCALATED TO HUMAN REVIEW", "reasons": []}
        curated_context_summary = "Abrupt termination payload execution."
        compliance_rationale = ""

        try:
            # 1. Validate OCR confidence         
            conf = getattr(payload, "ocr_confidence_score", 0.0)
            if conf < 0.85:
                decision_result["reasons"] = ["OCR confidence score is below acceptable threshold."]
                return self.handle_low_confidence(payload, tx_id, "LOW_OCR_CONFIDENCE", decision_result["reasons"][0])
            
            # 2. Extract and translate features
            financial_features = FinancialFeatureExtractionEngine().extract_features(payload)
            
            # 3. Translation validation        
            if financial_features["employment_status"] == "local_term_not_found":
                decision_result["reasons"] = ["Failed to translate employment status from OCR data."]
                return self.handle_low_confidence(payload, tx_id, "TRANSLATION_FAILURE", decision_result["reasons"][0])
            if financial_features["loan_purpose"] == "local_term_not_found":
                decision_result["reasons"] = ["Failed to translate loan purpose from OCR data."]
                return self.handle_low_confidence(payload, tx_id, "TRANSLATION_FAILURE", decision_result["reasons"][0])     

            # 4: Apply deterministic rules
            rules_engine = DeterministicBankingRulesEngine()
            decision_result = rules_engine.apply_rules(financial_features)

            # 5. Dynamic context setup
            c_score = financial_features["crib_score"]
            dti = financial_features["dti_ratio"]
            curated_context_summary = (
                f"Applicant exhibits credit indicators (CRIB score: {c_score}, DTI ratio: {dti:.2f}), "
                f"Normalized lexicon status mapped to standard status categories."
            )

            if decision_result["decision"] == "APPROVE":
                compliance_rationale = "Applicant meets all criteria for approval based on strong credit indicators and low risk profile."
                output_payload = self._compile_approval_payload(tx_id, payload, financial_features, decision_result, curated_context_summary, compliance_rationale)
            else:
                decision_result["decision"] = "ESCALATED TO HUMAN REVIEW"
                output_payload = self._compile_escalation_payload(tx_id, payload, financial_features, decision_result, curated_context_summary)

            return output_payload

        finally:
            # --- LAYER 8: ASYNCHRONOUS DATABASE WRITER FOR COMPLIANCE AUDITING ---
            if db_manager.pool:
                try:
                    async with db_manager.pool.acquire() as connection:
                        async with connection.transaction():
                            embedding_vector = self._generate_mock_embedding()
                            
                            await connection.execute(
                                """
                                INSERT INTO document_embeddings (
                                    application_id, ocr_confidence, applicant_name, salary_lkr, 
                                    calculated_dti, crib_score, loan_amount, final_decision, 
                                    compliance_rationale, embedding
                                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                                ON CONFLICT (application_id) DO UPDATE SET
                                    ocr_confidence = EXCLUDED.ocr_confidence,
                                    salary_lkr = EXCLUDED.salary_lkr,
                                    calculated_dti = EXCLUDED.calculated_dti,
                                    crib_score = EXCLUDED.crib_score,
                                    loan_amount = EXCLUDED.loan_amount,
                                    final_decision = EXCLUDED.final_decision,
                                    compliance_rationale = EXCLUDED.compliance_rationale,
                                    embedding = EXCLUDED.embedding,
                                    updated_at = NOW();
                                """,
                                req_id,
                                float(payload.ocr_confidence_score),
                                "Anonymous Applicant",
                                float(financial_features["monthly_income"]),
                                float(financial_features["dti_ratio"]),
                                int(financial_features["crib_score"]),
                                float(financial_features["requested_loan_amount"]),
                                decision_result["decision"],
                                compliance_rationale if compliance_rationale else str(decision_result["reasons"]),
                                embedding_vector
                            )

                            await connection.execute(
                                """
                                INSERT INTO agent_security (
                                    api_key, application_id, active_agent_id, log_level, telemetry_data
                                ) VALUES ($1, $2, $3, $4, $5);
                                """,
                                api_key if api_key else "anonymous_system_key",
                                req_id,
                                "automated_underwriter_agent",
                                "INFO" if decision_result["decision"] == "APPROVE" else "WARNING",
                                json.dumps({
                                    "transaction_id": tx_id,
                                    "context_summary": curated_context_summary,
                                    "reasons": decision_result.get("reasons", [])
                                })
                            )
                            logger.info(f"Successfully serialized transactional logs to relational DB storage for {tx_id}")
                except Exception as db_err:
                    logger.error(f"Failed critical persistence write for tx {tx_id}: {str(db_err)}", extra={"tx_id": tx_id, "request_id": req_id})

    def handle_low_confidence(self, payload: OCRInboundPayload, tx_id: str, reason_code: str, reason_message: str) -> Dict[str, Any]:
        req_id = getattr(payload, "request_id", "unknown_req")
        return {
            "transaction_id": tx_id,
            "decision_result": {
                "decision": "ESCALATED TO HUMAN REVIEW",
                "reasons": [reason_message]
            },
            "timestamp": time.time(),
            "request_id": req_id,
        }

    def _compile_escalation_payload(self, tx_id: str, payload: OCRInboundPayload, features: Dict[str, Any], decision_result: Dict[str, Any], curated_context_summary: str) -> Dict[str, Any]:
        req_id = getattr(payload, "request_id", "unknown_req")
        return {
            "transaction_id": tx_id,
            "features": features,
            "decision_result": decision_result,
            "curated_context_summary": curated_context_summary,
            "timestamp": time.time(),
            "request_id": req_id,
        }

    def _compile_approval_payload(self, tx_id: str, payload: OCRInboundPayload, features: Dict[str, Any], decision_result: Dict[str, Any], curated_context_summary: str, rationale: str) -> Dict[str, Any]:
        req_id = getattr(payload, "request_id", "unknown_req")
        return {
            "transaction_id": tx_id,
            "features": features,
            "decision_result": decision_result,
            "curated_context_summary": curated_context_summary,
            "rationale": rationale,
            "timestamp": time.time(),
            "request_id": req_id,
        }

orchestrator = UnderwritingOrchestrator()


# --- LAYER 7: FASTAPI API ENDPOINTS ---
if app is not None:

    # Automatic security guard and audit log pipeline
    async def verify_bank_employee_badge(
        secret_badge_token: str = Header(..., alias="X-Employee-Token"),
        application_id: str = Header("SYSTEM-AUDIT", alias="X-Application-Id")
    ) -> str:
        """
        FastAPI Security Dependency: Scans incoming requests for a valid corporate badge token.
        Automatically generates immutable forensic log traces inside the agent_security table.
        """
        is_valid = (secret_badge_token == "TRUSTED_BANKER_2026")
        log_level = "INFO" if is_valid else "WARNING"
        telemetry_msg = (
            "[SECURITY-PASSED] Valid bank employee token verified. Opening castle gate."
            if is_valid else 
            "[SECURITY-ALERT] WARNING! Unknown person tried to access banking data without a badge!"
        )
        
        active_agent_id = f"AGENT_{uuid.uuid4().hex[:8].upper()}" if is_valid else "UNKNOWN_INTRUDER"

        if db_manager.pool:
            try:
                async with db_manager.pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO agent_security 
                        (api_key, application_id, active_agent_id, log_level, telemetry_data)
                        VALUES ($1, $2, $3, $4, $5);
                        """,
                        secret_badge_token[:15] + "...", 
                        application_id,
                        active_agent_id,
                        log_level,
                        telemetry_msg
                    )
            except Exception as db_err:
                logger.error(f"Failed to commit security telemetry to database: {db_err}")

        if not is_valid:
            logger.warning(telemetry_msg)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Denied: Invalid or missing secret badge token."
            )

        logger.info(telemetry_msg)
        return active_agent_id


    # --- FIXED: WIRED ENDPOINT CAPTURING COMPLETE SYSTEM RUNTIME ---
    @app.post("/api/v1/underwrite")
    async def run_underwriting_pipeline(
        payload: OCRInboundPayload,                         # Updated from loose dict to strict schema validations
        agent_id: str = Depends(verify_bank_employee_badge) # This triggers the guard above!
    ):
        """
        Core underwriting processing pipeline.
        Parses inbound OCR text and passes execution right to the Multi-Agent state machine orchestrator.
        """
        transaction_id = f"tx_2026_{uuid.uuid4().hex[:8]}"
        logger.info(f"Underwriting execution authorized for operational session: {agent_id}", extra={"tx_id": transaction_id, "request_id": payload.request_id})
        
        # Call your live orchestrator state engine sequence
        result = await orchestrator.execute_pipeline(
            payload=payload, 
            tx_id=transaction_id, 
            api_key="TRUSTED_BANKER_2026"
        )
        return result
        
        
    @app.post("/v1/underwriting/override-submit")
    async def handle_manual_override_submission(payload: ManualOverrideRequest):
        audit_tracking_index = f"audit_tx_2026_{uuid.uuid4().hex[:8]}"
    
        logger.info(
            f"Processing manual override for application {payload.application_id}", 
            extra={"tx_id": audit_tracking_index, "request_id": payload.application_id}
        )

        if not db_manager.pool:
            raise HTTPException(status_code=500, detail="Relational database pool not available.")

        async with db_manager.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    # 1. Ensure structural row safety mapping
                    await connection.execute(
                        """
                        INSERT INTO document_embeddings (
                            application_id, ocr_confidence, applicant_name, salary_lkr, 
                            calculated_dti, crib_score, loan_amount, final_decision, 
                            compliance_rationale, embedding
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        ON CONFLICT (application_id) DO UPDATE SET
                            final_decision = EXCLUDED.final_decision,
                            compliance_rationale = EXCLUDED.compliance_rationale,
                            salary_lkr = EXCLUDED.salary_lkr,
                            updated_at = NOW();
                        """,
                        payload.application_id,
                        1.0,  
                        "Verified Applicant",
                        float(payload.corrected_features.verified_net_income),
                        0.0,  
                        750,  
                        0.0,
                        f"MANUAL_{payload.corrected_features.target_verdict}",
                        payload.override_reason,
                        [0.01536] * 1536  
                    )

                    # 2. Log explicit details down into historical security ledger
                    await connection.execute(
                        """
                        INSERT INTO agent_security (
                            api_key, application_id, active_agent_id, log_level, telemetry_data
                        ) VALUES ($1, $2, $3, $4, $5);
                        """,
                        payload.officer_id,
                        payload.application_id,
                        "human_underwriter_workbench",
                        "INFO",
                        json.dumps({
                            "audit_tracking_index": audit_tracking_index,
                            "override_reason": payload.override_reason,
                            "target_verdict": payload.corrected_features.target_verdict,
                            "verified_income": payload.corrected_features.verified_net_income
                        })
                    )

                    return {
                        "status": "SUCCESS",
                        "audit_tracking_index": audit_tracking_index,
                        "application_id": payload.application_id
                    }

                except Exception as e:
                    logger.error(f"Transaction aborted for application {payload.application_id}: {str(e)}")
                    raise HTTPException(status_code=400, detail=f"Database update failure: {str(e)}")