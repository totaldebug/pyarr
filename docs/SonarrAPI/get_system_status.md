---
layout: default
title: get_system_status
parent: SonarrAPI
nav_order: 4
---

## Summary

Returns the systems status.

## Parameters

Required: None

Optional: None

## Example

```python
get_system_status()
```

## Returns JsonArray

```json
{
  "version": "2.0.0.5344",
  "buildTime": "2020-04-28T15:34:41.741682Z",
  "isDebug": False,
  "isProduction": True,
  "isAdmin": False,
  "isUserInteractive": False,
  "startupPath": "/opt/NzbDrone",
  "appData": "/config",
  "osName": "ubuntu",
  "osVersion": "18.04",
  "isMonoRuntime": True,
  "isMono": True,
  "isLinux": True,
  "isOsx": False,
  "isWindows": False,
  "branch": "master",
  "authentication": "forms",
  "sqliteVersion": "3.22.0",
  "urlBase": "",
  "runtimeVersion": "5.20.1.34",
  "runtimeName": "mono"
}
```
