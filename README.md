# DucoBox API

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/sysadm1/ducobox-api.svg)](https://github.com/sysadm1/ducobox-api/releases)
[![License](https://img.shields.io/github/license/sysadm1/ducobox-api.svg)](LICENSE)

A Home Assistant integration for DucoBox ventilation systems using the Connectivity Board 2.0 local REST API. This is the REST-only variant: it has no Modbus TCP dependency or control path. For a Modbus-only variant, see [ducobox-mb](https://github.com/sysadm1/ducobox-mb).

## Features

- **Broad compatibility**: Works with any DucoBox model compatible with the Connectivity Board 2.0
- **Local API**: Communicates directly with the Duco Connectivity Board 2.0 over the local network
- **Automatic discovery**: The box and all its connected nodes are automatically discovered and represented as separate devices in Home Assistant

The following table lists entities supported by this integration for each node type:

| Entity | Type | BOX | BSCO2 | BSRH | BSVOC | UCBAT | UCCO2 | UCRH | UCVOC | VLV | VLVCO2 | VLVCO2RH | VLVRH | VLVVOC |
|---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ventilation | Fan | ✓ | | | | | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ventilation Mode | Sensor | ✓ | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ventilation State | Sensor | ✓ | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ventilation State End Time | Sensor | ✓ | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ventilation State Remaining Time | Sensor | ✓ | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Target Flow Level | Sensor | ✓ | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Relative Humidity | Sensor | | | ✓ | | | | ✓ | | | | ✓ | ✓ | |
| Relative Humidity Air Quality Index | Sensor | | | ✓ | | | | ✓ | | | | ✓ | ✓ | |
| CO2 | Sensor | | ✓ | | | | ✓ | | | | ✓ | ✓ | | |
| CO2 Air Quality Index | Sensor | | ✓ | | | | ✓ | | | | ✓ | ✓ | | |
| VOC† | Sensor | | | | ✓ | | | | ✓ | | | | | ✓ |
| VOC Air Quality Index† | Sensor | | | | ✓ | | | | ✓ | | | | | ✓ |
| Network Type | Sensor | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Identify | Button | ✓ | | | | | | | | | | | | |
| Wi-Fi Signal Strength | Sensor | ✓ | | | | | | | | | | | | |
| API Writes Remaining | Sensor | ✓ | | | | | | | | | | | | |
| Cloud Registration | Binary Sensor | ✓ | | | | | | | | | | | | |
| Cloud Remote Intervention Allowed | Binary Sensor | ✓ | | | | | | | | | | | | |
| Outdoor/Supply/Extract/Exhaust Air Temperature‡ | Sensor | ✓ | | | | | | | | | | | | |
| Filter Time Remaining‡ | Sensor | ✓ | | | | | | | | | | | | |
| Ventilation/Filter/Ventilative-Cooling/Sun-Control Diagnostic Status¶ | Sensor | ✓ | | | | | | | | | | | | |
| Outdoor Temperature, Wind Speed, Light Intensity (S/E/W)§ | Sensor | ✓ | | | | | | | | | | | | |
| Rain§ | Binary Sensor | ✓ | | | | | | | | | | | | |

† VOC support follows the same `Sensor.Voc`/`Sensor.IaqVoc` naming convention as the confirmed CO2/RH fields, and BSVOC/UCVOC/VLVVOC are all documented node types in DUCO's official `DucoDevice API` v2.5 spec (the local Connectivity Board API, more authoritative than the cloud spec for this integration), but no VOC-sensor hardware was available to verify any of this against a real board. If you have one and it doesn't show up, [open an issue](https://github.com/sysadm1/ducobox-api/issues) with its raw `/info/nodes` response.

‡ Heat-recovery-only values (e.g. DucoBox Energy). They read as unknown on models without heat recovery, such as the Focus this integration is primarily verified against. Any writable, ranged configuration value the box advertises for the bypass/supply-temperature targets documented for DucoBox Energy is already covered generically by the `number` entities described below, without needing a model-specific code path.

§ Requires a DUCO weather station accessory attached to the box; read as unknown without one. Verified against DUCO's official API schema, but not against real weather-station hardware. If something looks off, [open an issue](https://github.com/sysadm1/ducobox-api/issues).

¶ Four separate sensors, one per `Diag.SubSystems` entry: Ventilation, Filter, VentCool (ventilative cooling) and SunCtrl (sun control). Only Ventilation is populated on every tested box; the other three require that specific feature and read as unknown otherwise. Note that DUCO's cloud OpenAPI spec documents this list's key as `SubSystem`, but the Connectivity Board's real local response uses `Component` instead; this integration accepts either.

DUCO's `DucoDevice API` v2.5 spec also documents dozens of other node types (IAV/EAV valve families, digital I/O, motor relays, Perilex, etc.) and zone-level endpoints (`/info/zones`, `/config/zones`) that this integration does not yet support. These weren't added speculatively since their exact data shape and behavior isn't confirmed against real hardware; [open an issue](https://github.com/sysadm1/ducobox-api/issues) if you have one of these and want support added.

Ventilation control selects are created dynamically for each node whose API advertises the `SetVentilationState` action.

Any integer configuration value the board advertises with a `Min`/`Max`/`Inc` range is exposed as a writable `number` entity (e.g. time zone, DST, automatic reboot schedule, and any ranged per-node setting). LAN settings are excluded, since a bad write there can disconnect the board from Home Assistant. Board-level diagnostics (Wi-Fi signal strength, API write budget remaining, cloud registration) and ranged settings are polled hourly rather than on the 30-second node poll, since the board documents most of them as changing at most once a day.

Two Home Assistant services expose other actions and settings advertised by the board:

- `ducobox_api.execute_action` runs an advertised box action or node action. For example, use `SetVentilationState` with a node ID and one of that node's advertised enum values, or run a no-value action such as `ScanWifi` without a value.
- `ducobox_api.patch_config` changes one configuration field. Use the dotted path from the live `/config` response, such as `General.Time.TimeZone`. For node configuration, provide the node ID and a path from `/config/nodes/{node}`.

Both services require the DucoBox API integration entry. They check the current action list or configuration metadata before sending a request and serialize writes to respect the board's two-second write interval. The API 2.7 catalog supplied for the verified device does not advertise zone, zone-group, or firmware routes; those pages return 404 or 401, so this integration does not expose those operations. Changes to network configuration can interrupt the connection to Home Assistant.

Example service data:

```yaml
action: ducobox_api.execute_action
data:
  entry_id: YOUR_DUCOBOX_ENTRY_ID
  node_id: 1
  action: SetVentilationState
  value: AUTO
```

```yaml
action: ducobox_api.patch_config
data:
  entry_id: YOUR_DUCOBOX_ENTRY_ID
  path: General.Time.TimeZone
  value: 1
```

In Home Assistant's service/action editor, select the DucoBox API entry instead of typing its ID manually. For a box action or box configuration, leave out `node_id`. The action and config names and allowed values are read from the board each time the service runs.

## Verified device

The maintainer's device reports a DucoBox FOCUS with Connectivity Board 2.0 Public API version 2.7. Its node list contains the box, three VLVCO2 valves, one VLVRH valve, and two UCBAT controls. The API also advertises ventilation-state actions for nodes 1–7. This confirms the device's API shape; full control behavior still needs testing in Home Assistant.

## REST-only by design

This integration talks to the Connectivity Board exclusively over its local REST API (via [DucoPy](https://github.com/sysadm1/ducopy)). It has no Modbus TCP code path, no Modbus options step, and no Modbus diagnostics — if you want ventilation control to keep working during a REST outage, or want a path with no dependency on the board's REST API key mechanism at all, use [ducobox-mb](https://github.com/sysadm1/ducobox-mb) instead (or run both side by side; they use separate domains).

If you are missing a node or entity, feel free to [open an issue](https://github.com/sysadm1/ducobox-api/issues) or [create a pull request](https://github.com/sysadm1/ducobox-api/pulls).

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner and select "Custom repositories"
3. Add repository `https://github.com/sysadm1/ducobox-api` with category "Integration"
4. Search for "DucoBox API", select the integration, and download it
5. Restart Home Assistant

### Manual

1. Download the latest release from [Releases](https://github.com/sysadm1/ducobox-api/releases)
2. Extract the `custom_components/ducobox_api` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

### Automatic discovery (recommended)

1. Make sure your connectivity board is on the same network as Home Assistant
2. Go to "Settings" → "Devices & Services"
3. A "DucoBox API" entry will appear
4. Click "Add" and confirm

### Manual

1. Go to "Settings" → "Devices & Services"
2. Click "Add Integration"
3. Search for "DucoBox API"
4. Enter the IP address or hostname of your connectivity board
5. Click "Submit"

## Contribution

The integration has been updated against a DucoBox FOCUS reporting Connectivity Board 2.0 API 2.7. Feedback from Home Assistant use will help confirm entity behavior and broaden support for other devices.

If you encounter an unsupported node or entity, or have an improvement in mind, feel free to [open an issue](https://github.com/sysadm1/ducobox-api/issues) or [create a pull request](https://github.com/sysadm1/ducobox-api/pulls).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
