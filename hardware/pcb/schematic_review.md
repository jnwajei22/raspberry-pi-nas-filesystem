# Corrective schematic review

Reviewed and regenerated 2026-09-15. Scope is schematic only; no PCB layout was created or started.

## Validation result

- KiCad version: 9.0.5
- ERC: 0 errors, 0 warnings (`kicad/erc.json`)
- Netlist export: successful (`kicad/raspberry_pi_nas_nvme.net`)
- BOM export: successful (`kicad/raspberry_pi_nas_nvme_bom.csv`)
- PDF export: successful (`kicad/raspberry_pi_nas_nvme_review.pdf`)
- SVG export: successful (`kicad/raspberry_pi_nas_nvme.svg`)

## 1. JMS583 supply correction

The incorrect `1V2_JMS` rail was removed everywhere and replaced by `1V0_JMS`.

| JMS583 pins | Function | Corrected net |
|---|---|---|
| 2, 31, 53 | VCCK, digital core | `1V0_JMS` |
| 20, 25, 30, 33, 36, 40, 43, 46, 49 | AVDDL, analog core | `1V0_JMS` |
| 6, 11, 32, 56 | VCCO, 3.3 V I/O | `3V3_JMS` |
| 52 | XAVDDH, crystal pad supply | `3V3_JMS` |
| 64 | LXO switching node | `JMS_LXO` → L1 4.7 µH → `1V0_JMS` |
| 1 | VDDREG, internal-regulator 5 V input | `USB5V` |
| 19 | AVDD33, internal 3.3 V output | `3V3_JMS` |

The 1.0 V bypass network is C8 = 100 nF, C9 = 1 µF and C10 = 4.7 µF. Final distribution and per-pin capacitor placement must be completed during layout.

## 2. Reset RC

The former pull-up-only reset was electrically incomplete. RST pin 15 now has:

- R2 = 330 kΩ, 1%, from `3V3_JMS` to `JMS_RST_N`
- C26 = 1 µF, X7R, 10%, from `JMS_RST_N` to GND

The JMS583 datasheet defines T4 as the RST rise time from 0 V to 1.77 V and requires 120–500 ms for an RC implementation. For a 3.3 V exponential charge:

`t = -RC × ln(1 - 1.77/3.3) = 0.768RC`

Nominally, `t = 0.768 × 330 kΩ × 1 µF = 254 ms`. With the stated resistor and capacitor tolerances, the component-tolerance range is approximately 226–282 ms, inside the documented 120–500 ms interval. Capacitor leakage and effective capacitance must be checked when selecting the exact C26 MPN.

## 3. Crystal network

Y1 remains the ABM8-25.000MHZ-B2-T: 25 MHz, specified load capacitance 18 pF. The completed network is:

- C24 = 30 pF C0G 5% from XIN to GND
- C25 = 30 pF C0G 5% from XOUT to GND
- R8 = 510 kΩ from XIN to XOUT, following the JMS583 reference topology
- Crystal case pads 2 and 4 to GND

For equal load capacitors, `CL = C/2 + Cstray`. Using a documented design assumption of 3 pF combined IC-pin/trace/land stray capacitance gives `CL = 30/2 + 3 = 18 pF`. This is a calculated starting network, not an arbitrary value. Actual parasitics depend on placement and routing, so C24/C25 must be revisited using extracted or measured board parasitics before release.

## 4. USB ESD audit

The existing TPD4E05U06 signal implementation was **not electrically wrong**. Each channel was already a shunt branch from a signal net to the ESD device, with pins 3 and 8 grounded. No ESD device was placed in series. The corrected schematic preserves that topology.

| Protected net | Continuous signal path | ESD branch |
|---|---|---|
| `USB_TX1_P/N` | J1 A2/A3 directly to U1 U_RXP1/U_RXN1 pins 26/27 | U2 pins 1/2 |
| `USB_TX2_P/N` | J1 B2/B3 directly to U1 U_RXP2/U_RXN2 pins 29/28 | U3 pins 1/2 |
| `USB_RX1_P/N` | J1 B11/B10 to C1/C2; capacitor inner nets go to U1 U_TXP1/U_TXN1 pins 21/22 | U2 pins 4/5 on connector side |
| `USB_RX2_P/N` | J1 A11/A10 to C3/C4; capacitor inner nets go to U1 U_TXP2/U_TXN2 pins 24/23 | U3 pins 4/5 on connector side |
| `USB_DP/DM` | J1 A6/B6 and A7/B7 directly to U1 DP/DM pins 18/17 | U4 pins 1/2 |

U4's unused channels are no-connect. All three devices connect both ground pins, 3 and 8, to common GND. The physical placement/routing requirement remains: place the ESD arrays close to J1 with a short, low-inductance ground return and avoid stubs on the SuperSpeed pairs.

## 5. Split power architecture

The unresolved U5 power-mux placeholder was removed. The schematic now implements:

- `USB5V` from J1 powers JMS583 VDDREG pin 1 and VBUS pin 16.
- The JMS583 generates its local `3V3_JMS` and `1V0_JMS` rails.
- `AUX5V` from J2 powers TPS54302 VIN and EN plus its input capacitors.
- TPS54302 generates `3V3_NVME` only for the M.2/NVMe load.
- USB and auxiliary supplies share GND but are not tied together on their positive rails.

This split is valid provided AUX5V and `3V3_NVME` are stable when the bridge enumerates and attempts to discover the SSD. If AUX5V can arrive later than USB5V, system-level sequencing or a re-enumeration/reset policy is required.

USB cable presence is handled in both documented ways: U1 VBUS pin 16 is tied to USB5V, and GPIO6 pin 10 receives `USB_VBUS_SENSE` through a 100 kΩ/100 kΩ divider. The nominal GPIO6 level is 2.5 V at 5.0 V VBUS.

## 6. PCIe topology

PCIe lanes 0 and 1 remain connected for x2 operation. Lanes 2 and 3 remain intentionally unconnected. C11–C14 remain 220 nF series capacitors on the two JMS583 PCIe transmit differential pairs. No topology change was made.

## 7. TPS54302 review

The TI 3.3 V starting network remains unchanged:

- L2 = 6.8 µH
- C20 + C21 = 44 µF nominal output capacitance
- R6/R7 = 100 kΩ / 22.1 kΩ
- C19 = 47 pF feed-forward

The TPS54302's 3 A maximum is a release gate. The actual 4 TB NVMe SSD must be selected and its startup, peak and transient current verified before release. Effective ceramic output capacitance under 3.3 V DC bias must also meet the regulator stability/transient requirements.

## 8. EPAD and test mode

- U1 exposed pad pin 65 is explicitly tied to GND.
- U1 ground pin 63 is tied to GND.
- U1 TME pin 60 is tied to GND, holding test mode at logic 0 for normal operation.

The eventual layout must use the exposed-pad copper/via pattern required for electrical grounding and thermal performance.

## 9. Activity LED correction

The previous schematic was electrically wrong here: D1 was connected to GPIO12, pin 57. It is now connected to the documented default LED output, GPIO4 pin 8.

The corrected active-low sink path is `3V3_JMS → R3 (1 kΩ) → D1 anode → D1 cathode → GPIO4`. GPIO12 is no-connect. The exact LED MPN and brightness remain component-selection items.

## Remaining release gates

- Select the exact J2 connector and define the AUX5V source requirements.
- Select and derate every generic passive, inductor and LED.
- Confirm reset-capacitor leakage/effective capacitance with the selected MPN.
- Extract or measure the crystal network parasitics and tune C24/C25 if necessary.
- Define system sequencing behavior if AUX5V can be absent or late relative to USB5V.
- Select the 4 TB NVMe SSD and verify the TPS54302 3 A limit and transient response.
