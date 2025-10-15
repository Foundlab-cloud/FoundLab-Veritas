import json
import os
import html

def generate_audit_report(trail_filename="veritas_audit_trail.jsonl", output_filename="audit_report.html"):
    """
    Reads a Veritas audit trail file (JSONL) and generates a professional
    HTML report to visualize the chain of events.
    """
    # Build path relative to this script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    trail_file = os.path.join(base_dir, trail_filename)
    output_file = os.path.join(base_dir, output_filename)

    if not os.path.exists(trail_file):
        print(f"Error: Audit trail file not found at '{trail_file}'.")
        print("Please run 'python main.py' first to generate the trail.")
        return

    with open(trail_file, 'r') as f:
        events = [json.loads(line) for line in f]

    # --- HTML and CSS Template ---
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Veritas Audit Trail Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background-color: #f8f9fa; color: #212529; }}
            .container {{ max-width: 900px; margin: 40px auto; padding: 20px; }}
            .header {{ background-color: #000; color: #fff; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .header p {{ margin: 5px 0 0; color: #adb5bd; }}
            .timeline {{ border-left: 3px solid #dee2e6; margin: 30px 0; padding: 20px 0; }}
            .event {{ margin-left: 30px; padding: 20px; background-color: #fff; border-radius: 8px; margin-bottom: 20px; position: relative; border: 1px solid #e9ecef; }}
            .event:before {{ content: ''; width: 15px; height: 15px; background-color: #fff; border: 3px solid #0d6efd; border-radius: 50%; position: absolute; left: -48px; top: 28px; }}
            .event.denied:before {{ border-color: #dc3545; }}
            .event-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
            .event-type {{ font-weight: bold; font-size: 18px; color: #0d6efd; }}
            .event.denied .event-type {{ color: #dc3545; }}
            .timestamp {{ font-size: 12px; color: #6c757d; }}
            .payload, .hashes {{ background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 4px; font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace; font-size: 13px; white-space: pre-wrap; word-wrap: break-word; }}
            h3 {{ font-size: 14px; color: #495057; margin-top: 0; margin-bottom: 10px; border-bottom: 1px solid #dee2e6; padding-bottom: 5px; }}
            .hash-link {{ display: flex; align-items: center; margin-top: 10px; }}
            .hash-link svg {{ width: 16px; height: 16px; margin-right: 8px; fill: #6c757d; }}
            .footer {{ text-align: center; font-size: 12px; color: #6c757d; margin-top: 40px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Veritas Protocol</h1>
                <p>Immutable Audit Trail Report</p>
            </div>
            <div class="summary">
                <h3>Decision ID: {decision_id}</h3>
            </div>
            <div class="timeline">
                {events_html}
            </div>
            <div class="footer">
                <p>This report was generated automatically. The cryptographic chain ensures the integrity and immutability of this record.</p>
            </div>
        </div>
    </body>
    </html>
    """

    events_html = ""
    for i, event in enumerate(events):
        is_denied = event.get("payload", {}).get("decision") == "ACCESS DENIED"
        event_class = "denied" if is_denied else ""
        
        payload_pretty = json.dumps(event.get("payload", {}), indent=2)
        
        # Visual link for the hash chain
        hash_link_html = ""
        if event.get("previousChainHash"):
            hash_link_html = f'''
            <div class="hash-link">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10.59 13.41c.44.39.44 1.03 0 1.42-.39.39-1.03.39-1.42 0L6 11.71l-2.12 2.12c-.39.39-1.03.39-1.42 0-.39-.39-.39-1.03 0-1.42L4.59 10 2.47 7.88c-.39-.39-.39-1.03 0-1.42.39-.39 1.03-.39 1.42 0L6 8.59l2.12-2.12c.39-.39 1.03-.39 1.42 0 .44.39.44 1.03 0 1.42L7.41 10l3.18 3.41zM17 10l-3.18 3.41c-.44.39-.44 1.03 0 1.42.39.39 1.03.39 1.42 0L18 11.71l2.12 2.12c.39.39 1.03.39 1.42 0 .39-.39.39-1.03 0-1.42L19.41 10l2.12-2.12c.39-.39.39-1.03 0-1.42-.39-.39-1.03-.39-1.42 0L18 8.59l-2.12-2.12c-.39-.39-1.03-.39-1.42 0-.44.39-.44 1.03 0 1.42L17 10z"></path></svg>
                <span>Links to Previous Event Hash: <strong>{html.escape(event["previousChainHash"][:16])}...</strong></span>
            </div>
            '''

        events_html += f"""
        <div class="event {event_class}">
            <div class="event-header">
                <span class="event-type">{html.escape(event.get("eventType", "UNKNOWN_EVENT"))}</span>
                <span class="timestamp">{html.escape(event.get("timestamp", ""))}</span>
            </div>
            <h3>Payload</h3>
            <div class="payload"><pre>{html.escape(payload_pretty)}</pre></div>
            <h3>Cryptographic Hashes</h3>
            <div class="hashes">
                <span>Current Event Hash: <strong>{html.escape(event.get("chainHash", ""))}</strong></span>
                {hash_link_html}
            </div>
        </div>
        """

    decision_id = events[0].get("decisionId", "N/A") if events else "N/A"
    final_html = html_template.format(decision_id=decision_id, events_html=events_html)

    with open(output_file, 'w') as f:
        f.write(final_html)
    
    print(f"Success! Audit report generated at:\n  {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_audit_report()
