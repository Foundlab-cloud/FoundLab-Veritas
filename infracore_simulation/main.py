import json
import os
import sys
import time
import hashlib
from datetime import datetime, timezone

# Add the project root to the Python path to allow importing from 'foundlab'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from foundlab.core.veritas import create_genesis_event, create_next_event, generate_decision_id
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.spinner import Spinner

console = Console()

def verify_audit_trail(trail_path: str) -> bool:
    """Cryptographically verifies the integrity of the audit trail chain."""
    with open(trail_path, 'r') as f:
        events = [json.loads(line) for line in f]

    previous_hash = None
    for i, event in enumerate(events):
        # Check if the current event's previous hash matches the last event's hash
        if event.get("previousChainHash") != previous_hash:
            console.print(f"[bold red]Chain broken![/bold red] Event {i} has a mismatched previous hash.")
            return False
        
        # Re-calculate the hash of the current event to ensure it hasn't been tampered with
        event_data = {
            "decisionId": event["decisionId"],
            "timestamp": event["timestamp"],
            "eventType": event["eventType"],
            "payloadHash": event["payloadHash"],
            "previousChainHash": event["previousChainHash"],
        }
        event_string = json.dumps(event_data, sort_keys=True, separators=(',', ':'))
        recalculated_hash = hashlib.sha256(event_string.encode('utf-8')).hexdigest()

        if event.get("chainHash") != recalculated_hash:
            console.print(f"[bold red]Chain broken![/bold red] Event {i} has been tampered with. Hash mismatch.")
            return False

        previous_hash = event.get("chainHash")
    
    return True


def run():
    """
    Runs the self-verifying infrastructure demonstrator.
    """
    console.rule("[bold cyan]FoundLab Infracore: Self-Verifying Demonstrator[/bold cyan]", style="cyan")
    console.print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    # --- Step 1: Ingestion ---
    with console.status("[bold green]STEP 1/6: INGESTION[/bold green] Unauthorized SSO federation request received...", spinner="dots") as status:
        time.sleep(1.5)
        federation_request = {
            "action": "federation_bind",
            "target_organization": "FoundLab",
            "initiator": { "name": "Accenture", "has_verified_relationship": False, "has_active_contract": False },
            "explicit_consent": False
        }
        console.print("[bold green]STEP 1/6: INGESTION[/bold green] Unauthorized SSO federation request received.")
        console.print(Panel(Syntax(json.dumps(federation_request, indent=2), "json", theme="monokai"), title="Request Payload", border_style="yellow"))

    # --- Step 2: Policy Execution ---
    with console.status("[bold green]STEP 2/6: POLICY EXECUTION[/bold green] Simulating execution of 'sso_federation_policy.rego'...", spinner="dots") as status:
        time.sleep(2)
        
        # Simulate the Rego policy logic in Python for maximum portability
        allow = False # Default deny
        reasons = []
        if not federation_request["initiator"]["has_verified_relationship"]:
            reasons.append("REL_001_NO_VERIFIED_RELATIONSHIP")
        if not federation_request["initiator"]["has_active_contract"]:
            reasons.append("POL_403_HARD_DENY_IF_NO_CONTRACT")
        if not reasons and federation_request["explicit_consent"]:
            allow = True

        console.print("[bold green]STEP 2/6: POLICY EXECUTION[/bold green] Simulated execution of 'sso_federation_policy.rego'.")
        console.print(Panel(f"Policy evaluation result: [bold]{'ALLOW' if allow else 'DENY'}[/bold]", border_style="yellow"))

    # --- Step 3: Decision ---
    with console.status("[bold green]STEP 3/6: DECISION[/bold green] Finalizing policy decision...", spinner="dots") as status:
        time.sleep(1)
        if not allow:
            decision = "ACCESS DENIED"
            panel_style = "bold red"
            title = "ACCESS DENIED"
        else:
            decision = "ACCESS GRANTED"
            reasons = []
            panel_style = "bold green"
            title = "ACCESS GRANTED"
        
        console.print("[bold green]STEP 3/6: DECISION[/bold green] Policy evaluation complete.")
        console.print(Panel(f"Reason(s): {', '.join(reasons)}", title=title, border_style=panel_style, padding=(1, 2)))

    # --- Step 4: Veritas Seal ---
    with console.status("[bold green]STEP 4/6: VERITAS SEAL[/bold green] Generating cryptographic proof of the decision...", spinner="dots") as status:
        time.sleep(1.5)
        audit_trail = []
        decision_id = generate_decision_id()
        
        genesis_event = create_genesis_event(decisionId=decision_id, eventType="FEDERATION_REQUEST_RECEIVED", payload=federation_request)
        audit_trail.append(genesis_event)
        
        final_event = create_next_event(previous_event=genesis_event, eventType="POLICY_EVALUATION_COMPLETED", payload={"decision": decision, "reasons": reasons})
        audit_trail.append(final_event)

        console.print("[bold green]STEP 4/6: VERITAS SEAL[/bold green] Cryptographic proof generated.")
        console.print(f"   > DecisionID: [cyan]{decision_id}[/cyan]")
        console.print(f"   > Final Chain Hash: [cyan]{final_event.chainHash[:32]}...[/cyan]")

    # --- Step 5: Proof Generation ---
    audit_trail_path = os.path.join(os.path.dirname(__file__), "veritas_audit_trail.jsonl")
    with console.status("[bold green]STEP 5/6: PROOF GENERATION[/bold green] Writing immutable audit trail to disk...", spinner="dots") as status:
        time.sleep(1)
        with open(audit_trail_path, 'w') as f:
            for event in audit_trail:
                f.write(json.dumps(event.to_dict()) + '\n')
        console.print("[bold green]STEP 5/6: PROOF GENERATION[/bold green] Immutable audit trail written to disk.")
        console.print(f"   > Location: [cyan]{os.path.abspath(audit_trail_path)}[/cyan]")

    # --- Step 6: Self-Verification ---
    with console.status("[bold green]STEP 6/6: SELF-VERIFICATION[/bold green] Cryptographically verifying the generated audit trail...", spinner="dots") as status:
        time.sleep(2)
        is_valid = verify_audit_trail(audit_trail_path)
        console.print("[bold green]STEP 6/6: SELF-VERIFICATION[/bold green] Cryptographically verified the generated audit trail.")
        if is_valid:
            console.print(Panel("[bold green]✓ INTEGRITY CONFIRMED[/bold green]", title="Verification Result", border_style="green"))
        else:
            console.print(Panel("[bold red]✗ INTEGRITY COMPROMISED[/bold red]", title="Verification Result", border_style="red"))

    console.rule("[bold cyan]Demonstration Complete[/bold cyan]", style="cyan")

if __name__ == "__main__":
    run()
