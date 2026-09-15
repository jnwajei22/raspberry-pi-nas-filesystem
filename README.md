# Raspberry Pi NAS Filesystem

A custom Raspberry Pi 4-based network attached storage system built around a 3D-printed enclosure, a custom USB-to-NVMe carrier PCB, and 4 TB of M.2 NVMe storage.

The goal of this project is to build a compact personal file server from the enclosure up rather than relying on a prebuilt NAS chassis or external SSD enclosure.

## Project Goals

- Raspberry Pi 4B-based NAS
- 4 TB M.2 2280 NVMe storage
- Custom 90 × 90 mm USB-to-NVMe carrier PCB
- USB 3.x connection between the Raspberry Pi and storage board
- Custom 3D-printed enclosure
- Internal mounting system for the Raspberry Pi, storage board, and cooling hardware
- Active cooling
- Small system-status display
- Local monitoring of:
  - CPU temperature
  - CPU usage
  - RAM usage
  - SSD usage
  - SSD temperature and health
  - Read/write activity
  - Network throughput
  - IP address
  - System uptime
  - File-transfer progress

## System Architecture

```text
                  ┌─────────────────────┐
                  │   Raspberry Pi 4B   │
                  │                     │
                  │   NAS / monitoring  │
                  └──────────┬──────────┘
                             │
                          USB 3.x
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Custom NVMe Carrier │
                  │     90 × 90 mm      │
                  │                     │
                  │ USB-C               │
                  │   │                 │
                  │   ▼                 │
                  │ JMS583 Bridge       │
                  │   │                 │
                  │   ▼ PCIe Gen3 ×2    │
                  │ M.2 M-Key Socket    │
                  │   │                 │
                  │   ▼                 │
                  │ 4 TB NVMe SSD       │
                  └─────────────────────┘
```

## Hardware

### Raspberry Pi

The system is based on a Raspberry Pi 4B.

The Pi handles:

- network file sharing
- storage management
- system monitoring
- status-display output
- fan control
- file-transfer monitoring

### Storage

The original concept used raw NAND flash with a custom SSD controller. That architecture was replaced with a standard M.2 NVMe SSD to reduce firmware, NAND-management, and supply-chain complexity.

The current design uses:

- standard M.2 2280 form factor
- M-key NVMe SSD
- target capacity: 4 TB
- PCIe-to-USB bridge
- USB 3.x connection to Raspberry Pi 4B

### Custom NVMe Carrier PCB

Target specifications:

| Parameter | Specification |
|---|---|
| Board size | 90 × 90 mm |
| Layers | 4 |
| SSD | M.2 2280 NVMe |
| Interface | PCIe Gen3 ×2 to USB 3.x |
| Host connector | USB-C |
| SSD power | 3.3 V |
| Input power | 5 V |
| Auxiliary power | Optional 5 V input |

Current primary components:

| Function | Part |
|---|---|
| USB/NVMe bridge | JMicron JMS583 |
| M.2 socket | TE Connectivity 1-2199230-6 |
| USB-C receptacle | Molex 2024100002 |
| SSD regulator | TI TPS54302 |
| SPI configuration flash | Winbond W25Q40JV |
| High-speed ESD protection | TI TPD4E05U06 |
| Bridge clock | 25 MHz crystal |

The PCB is being designed in Autodesk Fusion Electronics.

## Enclosure

The enclosure was designed from scratch in Autodesk Fusion.

The design includes:

- Raspberry Pi mounting
- internal mounting plate
- upper hardware level
- SSD carrier PCB mounting
- ventilation on multiple enclosure walls
- active cooling
- removable lid
- locating lip for lid alignment
- provision for a front-mounted system-status display

The enclosure is intended to be fully 3D printed.

Source CAD and manufacturing exports are stored under:

```text
hardware/enclosure/
```

## Repository Structure

```text
raspberry-pi-nas-filesystem/
├── README.md
│
├── hardware/
│   ├── pcb/
│   │   ├── schematic/
│   │   ├── board/
│   │   ├── bom/
│   │   └── fabrication/
│   │
│   └── enclosure/
│       ├── fusion/
│       ├── exports/
│       │   ├── step/
│       │   ├── stl/
│       │   └── 3mf/
│       ├── drawings/
│       └── print-settings/
│
├── software/
│   ├── display/
│   ├── monitoring/
│   └── nas/
│
└── docs/
```

## Current Status

- [x] Raspberry Pi 4B selected
- [x] Enclosure concept completed
- [x] Internal mounting system modeled
- [x] Ventilation modeled
- [x] Main enclosure sent to print
- [x] Storage architecture selected
- [x] 4 TB M.2 NVMe target selected
- [x] Custom 90 × 90 mm carrier PCB architecture selected
- [ ] NVMe carrier schematic
- [ ] PCB layout
- [ ] PCB fabrication
- [ ] SSD installation
- [ ] Enclosure assembly
- [ ] Cooling installation
- [ ] Status display installation
- [ ] NAS operating-system configuration
- [ ] Monitoring software
- [ ] File-transfer progress display
- [ ] Final testing

## Design Philosophy

The project is intentionally designed as a complete engineering system rather than a collection of off-the-shelf modules.

Where practical, mechanical structure, mounting hardware, electronics, and software are being designed together so that the final system behaves as a single integrated device.

At the same time, standard components such as the Raspberry Pi and M.2 NVMe SSD are used where designing replacements would add significant complexity without improving the final NAS.

## Software

Planned software functions include:

- SMB/NFS file sharing
- storage-health monitoring
- NVMe SMART telemetry
- CPU and memory monitoring
- network throughput monitoring
- fan status/control
- local status-display interface
- transfer-progress visualization

Software development will be added after the mechanical and storage hardware are validated.

## CAD and Manufacturing Files

The repository will contain both editable source files and manufacturing exports.

For the enclosure:

- Fusion source files
- STEP files
- STL files
- 3MF files
- drawings
- print settings

For the PCB:

- Fusion Electronics schematic
- board layout
- BOM
- Gerbers
- drill files
- fabrication notes

## Revision

Current hardware revision:

```text
Enclosure: Rev A
NVMe Carrier PCB: Rev A
```

## Author

Justin Nwajei
