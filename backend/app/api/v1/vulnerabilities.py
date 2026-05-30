from fastapi import APIRouter, Depends
from backend.app.services.threat_intel.intel import VulnerabilityManager
from backend.app.core.auth import get_current_user, require_role
from backend.app.db.session import get_tenant_db, TenantAwareSession
from typing import List, Dict, Any

router = APIRouter()

@router.post("/ingest")
async def ingest_vulnerabilities(
    source: str,
    data: List[Dict[str, Any]],
    db: TenantAwareSession = Depends(get_tenant_db),
    user: dict = Depends(require_role(["analyst", "admin"]))
):
    vm = VulnerabilityManager(db)
    await vm.ingest_scan_data(source, data)
    return {"status": "success", "count": len(data)}

@router.post("/{vuln_id}/remediate")
async def remediate_vulnerability(
    vuln_id: str,
    db: TenantAwareSession = Depends(get_tenant_db),
    user: dict = Depends(require_role(["admin"]))
):
    vm = VulnerabilityManager(db)
    await vm.trigger_remediation(vuln_id)
    return {"status": "triggered"}
