# ... (existing code) ...

## Visualize the Proof

After running the simulation, a `veritas_audit_trail.jsonl` file is created. This file contains the raw, cryptographic proof.

To make this proof easily understandable, you can generate a human-readable HTML report:

```bash
python visualize_trail.py
```

This will create an `audit_report.html` file in this directory. Open it in your browser to see a visual representation of the immutable decision chain.
