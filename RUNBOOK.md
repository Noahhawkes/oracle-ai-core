# Oracle AI Core Runbook

Local prototype for capture, quarantine, and daily review.

## Pipeline

```text
instant_capture.py -> quarantine.py -> quarantine.enc.json -> record_compiler.py -> compiled markdown
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run on macOS

```bash
python instant_capture.py
```

Copy text on the Mac. The watcher queues the clipboard and persists it to quarantine.

Expected confirmation:

```text
Captured into queue. No action taken.
```

## Compile Records

```bash
python record_compiler.py
```

Outputs:

```text
~/Quarantine/compiled
~/Quarantine/clipboard/quarantine.enc.json
~/Quarantine/clipboard/quarantine.audit.jsonl
```

## Test

```bash
pytest
```

## Prototype Boundary

This is a local prototype. Do not use it for sensitive or mission-critical records without review.

## Invariant

```text
Capture. Quarantine. Review. Promote only by human authority.
```