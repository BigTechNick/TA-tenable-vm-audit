# Tenable Vulnerability Management Audit Log Add-on

Splunk add-on `TA-tenable-vm-audit`, version 1.0.0.

Search-time CIM mappings for Tenable Vulnerability Management (formerly Tenable.io) audit logs collected by the Tenable Add-on for Splunk (sourcetype tenable:io:audit_logs): Authentication for password, API key and MFA sign-ins, and Change (Account_Management) for user account changes. Not affiliated with Tenable.

## Layout

- `TA-tenable-vm-audit/`: the app exactly as shipped to Splunkbase (unpacked from the release package)
- `tools/package.py`: builds the Splunkbase package and runs offline AppInspect-style checks
- `tools/make_icons.py`: draws the app icons in `static/`
- `tests/`: tests with synthetic data (no Splunk or vendor account needed)

## Build

```
python3 tools/package.py TA-tenable-vm-audit dist --vendor tenable
```

Good: `RESULT: OK`. Then AppInspect:

```
splunk-appinspect inspect dist/TA-tenable-vm-audit-<version>.tgz --mode precert --included-tags cloud
```

## Tests

```
python3 tests/eval_test.py
```

## Packages

`packages/` holds each version's package exactly as uploaded to Splunkbase, with `MD5SUMS`.
Each version is also its own commit (`git log`).

## License

Apache-2.0. Independent project, not affiliated with or endorsed by Tenable.
