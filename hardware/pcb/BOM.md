# Raspberry Pi NAS NVMe schematic BOM

Corrected schematic BOM for `hardware/pcb/kicad/raspberry_pi_nas_nvme.kicad_sch`, reviewed 2026-09-15. Quantities are per board. Generic passives retain package/value assignments but require final manufacturer-part selection and derating before PCB release.

## Exact and major parts

| References | Qty | Manufacturer | Manufacturer part number | Description | Footprint | Status |
|---|---:|---|---|---|---|---|
| U1 | 1 | JMicron | JMS583-QHFA0A | USB 3.x to PCIe/NVMe bridge | `RaspberryPiNAS:JMicron_JMS583-QHFA0A` | Exact; corrected 1.0 V rails, reset, crystal, VBUS sense, GPIO4 LED, TME and EPAD connections |
| J1 | 1 | Molex | 2024100002 | Full-featured USB-C receptacle | `RaspberryPiNAS:Molex_2024100002` | Exact, verified orientation/keying |
| J3 | 1 | TE Connectivity | 1-2199230-6 | 67-contact M.2 M-key socket | `RaspberryPiNAS:TE_1-2199230-6_M2_M_Key` | Exact, verified; PCIe Gen3 x2 electrically |
| U7 | 1 | Texas Instruments | TPS54302DDCR | 3 A synchronous buck regulator | `RaspberryPiNAS:TPS54302DDCR_DDC0006A` | Exact; AUX5V-powered 3.3 V NVMe supply |
| U2-U4 | 3 | Texas Instruments | TPD4E05U06DQAR | Four-channel low-capacitance shunt ESD array | `RaspberryPiNAS:TPD4E05U06DQAR_DQA0010A` | Exact; branched from continuous USB nets, never used in series |
| U6 | 1 | Winbond | W25Q16JVSNIQ TR | 16 Mbit, 3 V SPI/Dual/Quad NOR flash | `RaspberryPiNAS:Winbond_W25Q16JVSNIQ_SOIC8_150mil` | Exact verified replacement for invalid W25Q40JVSSIQ |
| Y1 | 1 | Abracon | ABM8-25.000MHZ-B2-T | 25 MHz, 18 pF load crystal | `RaspberryPiNAS:Abracon_ABM8-25.000MHZ-B2-T` | Exact; 30 pF calculated load capacitors and 510 kΩ bias resistor added |
| D1 | 1 | TBD | TBD | Green activity LED | `LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder` | Active-low: 3V3_JMS → R3 → anode/cathode → JMS583 GPIO4 |
| J2 | 1 | TBD | TBD | Auxiliary 5 V input connector | No footprint assigned | Powers only the TPS54302/NVMe rail; connector selection remains open |

## Resistors

| References | Qty | Value | Function | Footprint/status |
|---|---:|---|---|---|
| R1 | 1 | 12 kΩ, 1% | JMS583 REXT | 0603; documented value |
| R2 | 1 | 330 kΩ, 1% | JMS583 active-low reset pull-up | 0603; with C26 gives 254 ms nominal to 1.77 V |
| R3 | 1 | 1 kΩ | GPIO4 activity LED current limiting | 0603; active-low sink arrangement |
| R4-R5 | 2 | 10 kΩ | Flash WP#/HOLD# pull-ups | 0603 |
| R6 | 1 | 100 kΩ, 1% | TPS54302 upper feedback resistor | 0603; TI 3.3 V starting value |
| R7 | 1 | 22.1 kΩ, 1% | TPS54302 lower feedback resistor | 0603; TI 3.3 V starting value |
| R8 | 1 | 510 kΩ | Crystal XIN-to-XOUT bias/feedback | 0603; follows the JMS583 reference topology |
| R9-R10 | 2 | 100 kΩ, 1% | USB VBUS divider to GPIO6 | 0603; 5 V produces nominal 2.5 V sense level |

## Capacitors and inductors

| References | Qty | Value | Function | Footprint/status |
|---|---:|---|---|---|
| C1-C4 | 4 | 100 nF | JMS583 USB TX AC coupling | 0603; retained |
| C5, C8 | 2 | 100 nF | JMS583 3.3 V / 1.0 V high-frequency bypass | 0603 |
| C6, C9 | 2 | 1 µF | JMS583 3.3 V / 1.0 V local bypass | 0603 |
| C7, C10 | 2 | 4.7 µF | JMS583 3.3 V / 1.0 V bulk bypass | 0603; verify DC bias |
| C11-C14 | 4 | 220 nF | JMS583 PCIe TX coupling, lanes 0/1 | 0603; retained |
| C15 | 1 | 10 µF | TPS54302 AUX5V input decoupling | 1210; select voltage/ripple rating |
| C16 | 1 | 100 nF | TPS54302 AUX5V high-frequency bypass | 0603 |
| C17 | 1 | 47 µF | AUX5V bulk | 1210 placeholder; select rated part |
| C18 | 1 | 100 nF | TPS54302 BOOT-SW | 0603 |
| C19 | 1 | 47 pF | TPS54302 feed-forward | 0603; TI 3.3 V starting value |
| C20-C21 | 2 | 22 µF | TPS54302 output, 44 µF nominal total | 1210; verify effective capacitance under DC bias |
| C22 | 1 | 100 µF | M.2 3.3 V bulk | 1210 placeholder; package/technology may need enlargement |
| C23 | 1 | 100 nF | M.2 local high-frequency bypass | 0603 |
| C24-C25 | 2 | 30 pF, C0G, 5% | 25 MHz crystal load | 0603; calculated for 18 pF CL with 3 pF combined parasitic assumption |
| C26 | 1 | 1 µF, X7R, 10% | JMS583 reset timing capacitor | 0603; use a low-leakage part with adequate effective capacitance |
| L1 | 1 | 4.7 µH | JMS583 LXO to 1V0_JMS regulator inductor | 1210; select current-rated MPN |
| L2 | 1 | 6.8 µH, ≥3 A | TPS54302 3.3 V buck | 1210 placeholder; select saturation/current-rated MPN |

## Release gates

- Select a rated AUX5V connector and define the required source voltage/current tolerance.
- Select manufacturer part numbers for passives, inductors and LED after voltage, DC-bias, leakage, ripple, saturation, tolerance and thermal checks.
- Measure or extract actual crystal pin/trace parasitics during layout and tune C24/C25 if the assumed 3 pF is not valid.
- Confirm AUX5V and 3V3_NVME sequencing is valid before USB enumeration in the finished system.
- Confirm the selected 4 TB NVMe SSD's peak and transient current is compatible with the TPS54302's 3 A maximum.
