# Tenable Vulnerability Management Audit Log Add-on

Version 1.0.0. App ID (folder name): `TA-tenable-vm-audit`.

Search-time CIM mappings for Tenable Vulnerability Management (formerly Tenable.io)
audit logs, sourcetype `tenable:io:audit_logs`. The Tenable Add-on for Splunk
collects these events but maps only vulnerability data to the CIM; this add-on
adds the Authentication and Change mappings for the audit log.

| Audit log action | CIM data model |
|---|---|
| `user.authenticate.password`, `user.authenticate.api_keys`, `user.authenticate.mfa` | Authentication |
| Other `user.*` actions (`user.update`, `user.roles.update`, `user.2fa_reset`, `user.create`, `user.delete`, ...) | Change (Account_Management) |
| `session.*`, `audit.log.view`, `api-*` (exports, findings and other API calls) | Not mapped; searchable by `signature` |

> Independent project, not affiliated with or endorsed by Tenable. Tenable and
> Tenable Vulnerability Management are trademarks of Tenable, Inc. See NOTICE.

## Requirements

* The Tenable Add-on for Splunk (`TA-tenable`), with its Tenable Vulnerability
  Management audit logs input collecting events as `tenable:io:audit_logs`.
* This add-on does not collect data.

## Where to install

| Splunk instance | Install? |
|---|---|
| Search heads (including Splunk Cloud and Enterprise Security) | Yes |
| Heavy forwarders, indexers | No (search-time settings only) |

For Enterprise Security, add the audit log index to the CIM index macros
`cim_Authentication_indexes` and `cim_Change_indexes`.

## Fields

| Field | Value |
|---|---|
| `signature` | Tenable's action, e.g. `user.authenticate.password`, `user.update` |
| `action` | Sign-ins: `success` / `failure` (from `is_failure`). Account changes: `created`, `deleted` or `modified` (from `crud`). Other events: Tenable's action |
| `status` | `success` / `failure` (from `is_failure`) |
| `authentication_method` | `password`, `api_keys` or `mfa` (sign-ins only) |
| `user` | Sign-ins: the account that signed in (`actor.name`). Account changes: the account changed (`target.name`) |
| `src_user` | Who performed the action (`actor.name`) |
| `src` | Client address: the first address in the `X-Forwarded-For` field |
| `dest` | The Tenable site (`IO_address`, e.g. `cloud.tenable.com`) |
| `object`, `object_id`, `object_category` | `target.name`, `target.id`, `target.type` (lowercase) |
| `change_type` | `AAA` (account changes only) |
| `app`, `vendor_product` | `tenable_io`, `Tenable Vulnerability Management` |

The add-on sets `KV_MODE = json` for the sourcetype so the JSON fields are available
even where the Tenable Add-on for Splunk is not installed on the search head.

## Event types and tags

| Event type | Tags | CIM |
|---|---|---|
| `tenable_vm_audit` | | (all audit log events) |
| `tenable_vm_audit_authentication` | authentication | Authentication |
| `tenable_vm_audit_account_change` | change, account | Change (Account_Management) |

## Notes

* When users sign in through SSO, Tenable does not write their user actions to the
  audit log; the identity provider's logs cover those sign-ins.
* API key sign-ins and `api-*` export calls include the account used by the Tenable
  Add-on for Splunk itself. Exclude that account in detections.

## Check after installing

```
index=<audit log index> sourcetype="tenable:io:audit_logs" earliest=-24h
| stats count by signature action status tag
```

```
| datamodel Authentication Authentication search
| search sourcetype="tenable:io:audit_logs"
| stats count by Authentication.action Authentication.authentication_method Authentication.user
```

```
| datamodel Change Account_Management search
| search sourcetype="tenable:io:audit_logs"
| stats count by All_Changes.action All_Changes.user All_Changes.src_user
```

## Release notes

### 1.0.0

* First release.

## Support

Community-supported, best effort, through Splunkbase. Licensed under Apache 2.0.
