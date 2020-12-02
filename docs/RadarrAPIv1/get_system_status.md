---
layout: default
title: get_system_status
parent: RadarrAPIv1
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
    'version': '0.2.0.1480',
    'buildTime': '2020-04-28T20:00:56.444971Z',
    'isDebug': False,
    'isProduction': True,
    'isAdmin': False,
    'isUserInteractive': False,
    'startupPath': '/opt/radarr',
    'appData': '/config',
    'osName': 'ubuntu',
    'osVersion': '18.04',
    'isMonoRuntime': True,
    'isMono': True,
    'isLinux': True,
    'isOsx': False,
    'isWindows': False,
    'branch': 'develop',
    'authentication': 'forms',
    'sqliteVersion': '3.22.0',
    'urlBase': '',
    'runtimeVersion': '5.20.1.34',
    'runtimeName': 'mono'
}
```
