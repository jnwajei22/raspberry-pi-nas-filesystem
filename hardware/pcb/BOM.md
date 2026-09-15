# Raspberry Pi NAS NVMe schematic BOM

First-pass BOM for `hardware/pcb/kicad/raspberry_pi_nas_nvme.kicad_sch`, prepared 2026-09-14. Quantities are per board. Generic passives retain package/value assignments but require final manufacturer-part selection and derating before PCB release.

## Exact and major parts

| References | Qty | Manufacturer | Manufacturer part number | Description | Footprint | Status |
|---|---:|---|---|---|---|---|
| U1 | 1 | JMicron | JMS583-QHFA0A | USB 3.x to PCIe/NVMe bridge | `RaspberryPiNAS:JMicron_JMS583-QHFA0A` | Exact, custom-verified |
| J1 | 1 | Molex | 2024100002 | Full-featured USB-C receptacle | `RaspberryPiNAS:Molex_2024100002` | Exact, verified orientation/keying |
| J3 | 1 | TE Connectivity | 1-2199230-6 | 67-contact M.2 M-key socket | `RaspberryPiNAS:TE_1-2199230-6_M2_M_Key` | Exact, verified |
| U7 | 1 | Texas Instruments | TPS54302DDCR | 3 A synchronous buck regulator | `RaspberryPiNAS:TPS54302DDCR_DDC0006A` | Exact, verified |
| U2-U4 | 3 | Texas Instruments | TPD4E05U06DQAR | Four-channel low-capacitance ESD array | `RaspberryPiNAS:TPD4E05U06DQAR_DQA0010A` | Exact; two protect all SuperSpeed pairs, one protects USB D+/D- |
| U6 | 1 | Winbond | **W25Q16JVSNIQ TR** | 16 Mbit, 3 V SPI/Dual/Quad NOR flash, SOIC-8 150 mil | `RaspberryPiNAS:Winbond_W25Q16JVSNIQ_SOIC8_150mil` | Exact verified replacement for invalid W25Q40JVSSIQ; active stocked tape/reel option |
| Y1 | 1 | Abracon | ABM8-25.000MHZ-B2-T | 25 MHz crystal, 3.2 x 2.5 mm | `RaspberryPiNAS:Abracon_ABM8-25.000MHZ-B2-T` | Exact, verified |
| D1 | 1 | TBD | TBD | Green activity LED | `LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder` | Value/polarity requires JMS583 reference review |
| J2 | 1 | TBD | TBD | Optional auxiliary 5 V input connector | No footprint assigned | Intentional selection placeholder |
| U5 | 1 | TBD | TBD | Reverse-current-blocking USB5V/AUX5V power path | No footprint; excluded from BOM/board | Intentional non-functional placeholder; mandatory before release |

## Resistors

| References | Qty | Value | Function | Footprint | Status |
|---|---:|---|---|---|---|
| R1 | 1 | 12 kΩ, 1% | JMS583 REXT | `Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder` | Documented value |
| R2 | 1 | 10 kΩ | JMS583 reset pull-up | same 0603 footprint | Verify against reference design |
| R3 | 1 | 1 kΩ | Activity LED current limit | same 0603 footprint | Verify brightness and polarity |
| R4-R5 | 2 | 10 kΩ | Flash WP#/HOLD# pull-ups | same 0603 footprint | Standard W25Q-JV connection |
| R6 | 1 | 100 kΩ, 1% | TPS54302 upper feedback resistor | same 0603 footprint | TI 3.3 V table |
| R7 | 1 | 22.1 kΩ, 1% | TPS54302 lower feedback resistor | same 0603 footprint | TI 3.3 V table |

## Capacitors and inductors

| References | Qty | Value | Function | Footprint/status |
|---|---:|---|---|---|
| C1-C4 | 4 | 100 nF | JMS583 USB TX AC coupling | 0603; documented value |
| C5, C8 | 2 | 100 nF | JMS583 local high-frequency bypass | 0603; final population review |
| C6, C9 | 2 | 1 µF | JMS583 local bypass | 0603; final population review |
| C7, C10 | 2 | 4.7 µF | JMS583 rail bulk bypass | 0603; final DC-bias/voltage-rating selection |
| C11-C14 | 4 | 220 nF | JMS583 PCIe TX AC coupling, lanes 0/1 | 0603; documented value |
| C15 | 1 | 10 µF | TPS54302 input decoupling | 1210; TI minimum recommendation, select voltage/ripple rating |
| C16 | 1 | 100 nF | TPS54302 high-frequency input bypass | 0603 |
| C17 | 1 | 47 µF | 5V_SYS bulk | 1210 placeholder; select rated part |
| C18 | 1 | 100 nF | TPS54302 BOOT-SW | 0603; TI required value |
| C19 | 1 | 47 pF | TPS54302 feed-forward | 0603; TI 3.3 V table |
| C20-C21 | 2 | 22 µF | TPS54302 output, 44 µF total | 1210; TI 3.3 V table, verify DC bias |
| C22 | 1 | 100 µF | M.2 3.3 V bulk | 1210 placeholder; package/technology may need enlargement |
| C23 | 1 | 100 nF | M.2 local high-frequency bypass | 0603 |
| L1 | 1 | 4.7 µH | JMS583 internal regulator | generic 1210 footprint; select current-rated MPN after reference review |
| L2 | 1 | 6.8 µH, ≥3 A | TPS54302 3.3 V buck | generic 1210 footprint; TI table value, select saturation/current-rated MPN |

## Release gates

- Select and design U5 so `USB5V` and `AUX5V` cannot backfeed each other; select a rated auxiliary connector J2.
- Obtain/review the authoritative JMS583 reference design for exposed-pad grounding, reset, activity LED, crystal load network, internal-regulator topology and exact decoupling population.
- Select manufacturer part numbers for every resistor, capacitor, inductor and LED after voltage, DC-bias, ripple, saturation, tolerance and thermal checks.
- Confirm the M.2 3.3 V rail current/transient budget for the chosen 4 TB 2280 NVMe SSD.
