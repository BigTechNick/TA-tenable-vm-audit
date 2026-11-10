#!/usr/bin/env python3
"""
eval_test.py - checks the props.conf EVAL logic and the event types agree, using the
regexes read from the app's own props.conf / eventtypes.conf.

  python3 tests/eval_test.py

Python's re supports the same lookahead syntax as Splunk's PCRE for these patterns.
"""
import fnmatch
import os
import re
import sys

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TA-tenable-vm-audit", "default")
props = open(os.path.join(APP, "props.conf"), encoding="utf-8").read()
etypes = open(os.path.join(APP, "eventtypes.conf"), encoding="utf-8").read()

eval_action = re.search(r"^EVAL-action = (.*)$", props, re.M).group(1)
AUTH_RE, CHANGE_RE = re.findall(r'match\(action, "([^"]+)"\)', eval_action)
# every EVAL that classifies account changes must use the same regex
for m in re.findall(r'match\(action, "(\^user\\\.\(\?![^"]+)"\)', props):
    assert m == CHANGE_RE, f"inconsistent account-change regex: {m}"


def eventtype_terms(name):
    search = re.search(rf"^\[{name}\]\nsearch = (.*)$", etypes, re.M).group(1)
    pos = re.findall(r'(?<!NOT )signature="([^"]+)"', search)
    neg = re.findall(r'NOT signature="([^"]+)"', search)
    return pos, neg


def in_eventtype(name, signature):
    pos, neg = eventtype_terms(name)
    return any(fnmatch.fnmatchcase(signature, p) for p in pos) and \
        not any(fnmatch.fnmatchcase(signature, n) for n in neg)


def cim_action(action, crud, is_failure):
    if re.search(AUTH_RE, action):
        return "failure" if str(is_failure).lower() == "true" else "success"
    if re.search(CHANGE_RE, action):
        return {"c": "created", "d": "deleted"}.get(crud, "modified")
    return action


CASES = {
    # action: expected category
    "user.authenticate.password": "auth", "user.authenticate.api_keys": "auth",
    "user.authenticate.mfa": "auth",
    "user.update": "change", "user.roles.update": "change", "user.2fa_reset": "change",
    "user.create": "change", "user.delete": "change",
    "user.logout": None, "session.create": None, "session.delete": None, "audit.log.view": None,
    "api-exports.assets.create": None, "api-exports-jobs.create": None,
    "api-findings-vulnerabilities-host-count.create": None, "api-installedsw-analysis.create": None,
}
fails = 0
for action, want in CASES.items():
    by_eval = "auth" if re.search(AUTH_RE, action) else "change" if re.search(CHANGE_RE, action) else None
    by_etype = ("auth" if in_eventtype("tenable_vm_audit_authentication", action) else
                "change" if in_eventtype("tenable_vm_audit_account_change", action) else None)
    ok = by_eval == want == by_etype
    fails += not ok
    print(("ok   " if ok else "FAIL ") + f"{action:50} eval={by_eval} eventtype={by_etype} want={want}")

checks = [
    (cim_action("user.authenticate.password", "u", False), "success"),
    (cim_action("user.authenticate.password", "u", "true"), "failure"),
    (cim_action("user.update", "u", False), "modified"),
    (cim_action("user.create", "c", False), "created"),
    (cim_action("user.delete", "d", False), "deleted"),
    (cim_action("audit.log.view", "r", False), "audit.log.view"),
]
# src: first address of X-Forwarded-For (documentation addresses)
fields = [{"key": "X-Forwarded-For", "value": "2001:db8::10, 198.51.100.7"}, {"key": "X-Request-Uuid", "value": "x"}]
keys, values = [f["key"] for f in fields], [f["value"] for f in fields]
i = next(n for n, k in enumerate(keys) if re.search("^X-Forwarded-For$", k))
checks.append((values[i].split(",")[0].strip(), "2001:db8::10"))
for got, want in checks:
    ok = got == want
    fails += not ok
    print(("ok   " if ok else "FAIL ") + f"{got!r} == {want!r}")
print("RESULT:", "OK" if not fails else f"{fails} failure(s)")
sys.exit(1 if fails else 0)
