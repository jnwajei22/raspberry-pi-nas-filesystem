# KiCad library preparation report

Prepared and validated 2026-09-14. The first-pass schematic is under `hardware/pcb/kicad/`.

All usable symbols, footprints, and 3D models are stored under `hardware/pcb/libraries/`. The project-local `sym-lib-table` and `fp-lib-table` use `${KIPRJMOD}` paths and do not reference global computer paths.

## Acquisition and verification status

| Part number | Manufacturer | Symbol source | Footprint source | Datasheet source | Exact-match status | Verification status | Notes |
|---|---|---|---|---|---|---|---|
| JMS583-QHFA0A | JMicron | **CUSTOM-VERIFY**, drawn from the public JMicron JMS583 Rev. 2.1 signal table | Exact EasyEDA/LCSC record C9900110183, component UUID `7ed4b3711810454eb69c8505d68afa0a`, footprint UUID `2eb720523592401281967fab13173877`; converted to KiCad | [JMicron JMS583 Rev. 2.1 public datasheet](https://snapeda.s3.amazonaws.com/datasheets/2115-PDS-17001_JMS583_Datasheet_(Rev._2.1)_20190716.pdf); local copy `libraries/datasheets/JMicron_JMS583_datasheet_rev2.1.pdf` | YES for ordering code and exact distributor CAD record | **CUSTOM-VERIFY** | Symbol has pins 1-64 plus exposed pad 65. Footprint is QFN-64, 8.0 x 8.0 mm, 0.40 mm pitch, with 4.5 x 4.5 mm exposed pad 65 and 65 total pads. Exact converted STEP is local. The public datasheet does not explicitly assign the exposed-pad electrical connection; see uncertainty below. |
| 2024100002 | Molex | Official KiCad `USB_C_Receptacle` pin model adapted to the exact MPN and local footprint | Exact EasyEDA/LCSC C586089 CAD, converted to KiCad | [Molex exact product page](https://www.molex.com/en-us/products/part-detail/2024100002), [customer drawing 2024100002](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/202/202410/2024100002_sd.pdf) | YES | **CUSTOM-VERIFY symbol; VERIFIED footprint** | 24 USB-C contacts A1-A12/B1-B12 at 0.50 mm pitch. Four shell/retention pads are all numbered `S1` to match the symbol shield pin. Mid-mount outline, connector orientation, shell holes/tabs, and 0.60/0.70 mm PCB-thickness callout were checked. Exact converted STEP is local. |
| 1-2199230-6 | TE Connectivity | Official KiCad `Bus_M.2_Socket_M` adapted to exact MPN; explicit `SH1`/`SH2` shield pins added | Exact EasyEDA/LCSC C4710843 CAD, converted to KiCad | [TE exact product page](https://www.te.com/fr/product-1-2199230-6.html), [TE customer drawing mirror](https://www.farnell.com/cad/1918022.pdf) | YES | **CUSTOM-VERIFY symbol; VERIFIED footprint** | M-key, 67 signal contacts: 1-58 and 67-75, 0.50 mm pitch; 2 SMD shield tabs `SH1`/`SH2`; 2 unnumbered NPTH locator holes. Keying, orientation, 21.9 x 8.7 x 4.2 mm product envelope, and mounting features checked. Exact converted STEP is local. |
| TPS54302DDCR | Texas Instruments | Official KiCad `TPS54302`, adapted to exact ordering code and local footprint | Official KiCad `SOT-23-6`, copied locally as `TPS54302DDCR_DDC0006A` | [TI exact part page](https://www.ti.com/product/TPS54302/part-details/TPS54302DDCR), [TI TPS54302 datasheet](https://www.ti.com/lit/ds/symlink/tps54302.pdf); local copy `libraries/datasheets/TI_TPS54302_datasheet.pdf` | YES | **VERIFIED** | Pins verified: 1 GND, 2 SW, 3 VIN, 4 FB, 5 EN, 6 BOOT. DDC0006A/SOT-23-6 has 6 pads, 0.95 mm pitch, no exposed pad. Official KiCad package STEP is copied locally. |
| W25Q16JVSNIQ (tape/reel order option `W25Q16JVSNIQ TR`) | Winbond | Official KiCad W25Q-JV pin model, flattened and adapted to the exact orderable package suffix | Official KiCad `SOIC-8_3.9x4.9mm_P1.27mm`, copied locally as `Winbond_W25Q16JVSNIQ_SOIC8_150mil` | [Winbond W25Q16JV documentation](https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q16JV.1), [Winbond W25Q-JV family](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=en), [active stocked tape/reel listing](https://www.digikey.com/en/products/detail/winbond-electronics/W25Q16JVSNIQ-TR/10238303) | YES | **VERIFIED** | Replaces invalid `W25Q40JVSSIQ`. 16 Mbit / 2 MiB, 2.7-3.6 V, SPI/Dual/Quad SPI, SOIC-8 150 mil, -40 to +85 C. Pins: 1 CS#, 2 DO/IO1, 3 WP#/IO2, 4 GND, 5 DI/IO0, 6 CLK, 7 HOLD#/RESET#/IO3, 8 VCC. Eight pads, 1.27 mm pitch, 3.9 x 4.9 mm body, no exposed pad. The older 8 Mbit JV SOIC and the 208 mil W25Q16JVSSIQ were rejected because they are marked obsolete; the W25Q16JVSNIQ tape/reel listing is active and stocked. |
| TPD4E05U06DQAR | Texas Instruments | Official KiCad `TPD4EUSB30` pin-compatible device symbol adapted to the exact MPN | Official KiCad `USON-10_2.5x1.0mm_P0.5mm`, copied locally as `TPD4E05U06DQAR_DQA0010A` | [TI exact part page](https://www.ti.com/product/TPD4E05U06/part-details/TPD4E05U06DQAR), [TI TPD4E05U06 datasheet](https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf); local copy `libraries/datasheets/TI_TPD4E05U06_datasheet.pdf` | YES | **VERIFIED with package-construction note** | Pins verified: 1 D1+, 2 D1-, 3 GND, 4 D2+, 5 D2-, 6 NC, 7 NC, 8 GND, 9 NC, 10 NC. DQA is USON-10, 2.5 x 1.0 mm, 0.50 mm pitch, 10 pads, no center exposed pad in DQA0010A. Official KiCad package STEP is copied locally. |
| ABM8-25.000MHZ-B2-T | Abracon | Official KiCad `Crystal_GND24` adapted to the exact MPN and local footprint | Exact EasyEDA/LCSC C596899 CAD, converted to KiCad | [Abracon ABM8 datasheet](https://abracon.com/Resonators/abm8.pdf); local copy `libraries/datasheets/Abracon_ABM8_datasheet.pdf` | YES | **CUSTOM-VERIFY symbol; VERIFIED footprint** | Four pads: 1/3 crystal electrodes and 2/4 case ground. Verified 3.2 x 2.5 x 0.8 mm body and recommended pads 1.4 x 1.2 mm centered at +/-1.10 mm X and +/-0.85 mm Y. Exact converted STEP is local. |

## Verification details

### Symbol pin checks

- `JMicron_JMS583-QHFA0A`: checked all numbered pins 1-64 against the Rev. 2.1 signal table, including USB SuperSpeed pairs (`U_TXP/N1`, `U_TXP/N2`, `U_RXP/N1`, `U_RXP/N2`), PCIe pairs (`P_TXP/N0`, `P_TXP/N1`, `P_RXP/N0`, `P_RXP/N1`), USB 2.0 `DP`/`DM`, `CLKP`/`CLKN`, `CC1`/`CC2`, rails, reset, GPIO, crystal, and regulator pins. Pad 65 is exposed as `EP` so the footprint cannot silently contain an unmapped electrical pad.
- `Molex_2024100002`: verified the complete reversible USB-C receptacle pin set A1-A12/B1-B12, duplicated VBUS/GND pins, USB 2.0 D+/D- pins, SuperSpeed TX/RX pairs, CC1/CC2, SBU1/SBU2, and shield.
- `TE_1-2199230-6`: verified M-key contact numbering and omitted key positions. Both footprint shell pads are now explicit passive symbol pins `SH1` and `SH2`.
- `TPS54302DDCR`, `TPD4E05U06DQAR`, and `ABM8-25.000MHZ-B2-T`: pin numbers and functions match the manufacturer pin diagrams/tables summarized above.
- `W25Q16JVSNIQ`: verified against the Winbond pin diagram and official KiCad model: 1 CS#, 2 DO/IO1, 3 WP#/IO2, 4 GND, 5 DI/IO0, 6 CLK, 7 HOLD#/RESET#/IO3, and 8 VCC.

### Footprint mechanical checks

| Local footprint | Pad records | Mechanical verification |
|---|---:|---|
| `JMicron_JMS583-QHFA0A.kicad_mod` | 65 | QFN-64, 16 perimeter pads per side, 0.40 mm pitch, 8 x 8 mm body, center exposed pad 65 |
| `Molex_2024100002.kicad_mod` | 28 | 24 signal contacts plus four shell/retention tabs; exact mid-mount cutout and locator features retained |
| `TE_1-2199230-6_M2_M_Key.kicad_mod` | 71 | 67 signal contacts, two shield tabs, and two unnumbered NPTH locator holes; M-key gap retained |
| `TPS54302DDCR_DDC0006A.kicad_mod` | 6 | TI DDC/SOT-23-6, 0.95 mm pitch, no exposed pad |
| `TPD4E05U06DQAR_DQA0010A.kicad_mod` | 10 | TI DQA0010A USON-10, 2.5 x 1.0 mm, 0.50 mm pitch |
| `Abracon_ABM8-25.000MHZ-B2-T.kicad_mod` | 4 | 3.2 x 2.5 mm crystal, correct four-pad geometry and pin-1 marker |
| `Winbond_W25Q16JVSNIQ_SOIC8_150mil.kicad_mod` | 8 | SOIC-8 150 mil, 3.9 x 4.9 mm body, 1.27 mm pitch, no exposed pad; pad 1 marker retained |

## Sources and provenance

- Generic symbol/package bases are from the installed KiCad 9 official libraries and were copied into this repository: [KiCad symbols](https://gitlab.com/kicad/libraries/kicad-symbols) and [KiCad footprints](https://gitlab.com/kicad/libraries/kicad-footprints).
- Exact distributor CAD for JMS583-QHFA0A, 2024100002, 1-2199230-6, and ABM8-25.000MHZ-B2-T was converted to native KiCad format. Exact source UUID records retained for JMS583 are in `libraries/datasheets/source_records/`.
- Every footprint's 3D reference uses `${KIPRJMOD}/../libraries/3dmodels/...` from the requested `hardware/pcb/kicad/` project directory; no global KiCad or arbitrary machine path is used.

## Uncertainties and release gates

1. **JMS583 exposed pad:** the public Rev. 2.1 datasheet gives the QFN exposed-pad geometry but does not explicitly state its electrical net. The custom symbol exposes it as pin 65 `EP`. Confirm the required EP connection with JMicron or an authoritative reference design before board release.
2. **TPD4E05U06 DQA construction:** TI documents DQA0010A and DQA0010B package constructions for this orderable part. The local footprint is explicitly DQA0010A. TI support describes the constructions as interchangeable, but DQA0010B bridges the two GND lead regions. Confirm assembly-land-pattern acceptance if the fabricator requires construction-specific paste/copper details: [TI package discussion](https://e2e.ti.com/support/interface-group/interface/f/interface-forum/1384139/tpd4e05u06-what-is-the-correct-package-drawing).
3. **JMS583 reference design:** the public datasheet provides pin functions but not a complete application schematic. The schematic therefore carries the explicit note `VERIFY AGAINST JMS583 REFERENCE DESIGN BEFORE PCB RELEASE`; review the reset pull-up, activity-LED polarity, crystal load network, internal-regulator topology and decoupling population before layout.
4. **M.2 connector ERC typing repair:** signal pins on the adapted connector were changed from input/output/bidirectional to passive. Pin names, pin numbers, keying and footprint pads are unchanged. This correctly models a connector and removes false driver conflicts.
5. Symbols labeled **CUSTOM-VERIFY** were created or adapted from public documentation because a directly downloadable, authoritative exact-MPN KiCad symbol was not available. They have been checked as documented but should receive an independent engineering review before fabrication.

## Final status

- **Exact libraries acquired:** JMS583-QHFA0A, Molex 2024100002, TE 1-2199230-6, TPS54302DDCR, TPD4E05U06DQAR, and Abracon ABM8-25.000MHZ-B2-T.
- **Flash substitution:** invalid `W25Q40JVSSIQ` replaced by verified, active/stocked tape-reel `W25Q16JVSNIQ`.
- **Parts missing:** none among the seven required exact parts.
- **Custom libraries created/adapted and labeled CUSTOM-VERIFY:** JMS583-QHFA0A symbol; Molex 2024100002 symbol adaptation; TE 1-2199230-6 symbol adaptation including shield pins; Abracon ABM8-25.000MHZ-B2-T symbol adaptation.
- **Pinout/package uncertainties:** JMS583 exposed-pad electrical assignment and incomplete public application information; TPD4E05U06 DQA0010A versus DQA0010B construction.
- **Repository-local KiCad tables ready:** YES. The project tables in `hardware/pcb/kicad/` use `${KIPRJMOD}/../libraries/...`; the library-root tables remain valid for `hardware/pcb/`.
- **Library parser validation:** KiCad 9.0.5 successfully exported the W25Q16JVSNIQ symbol and footprint to SVG.
- **Schematic validation:** KiCad 9.0.5 parses, exports netlist/BOM/PDF/SVG, and reports **0 ERC errors and 0 ERC warnings**.

## Schematic first-pass summary

The single A3 schematic is divided into four labeled sections: USB interface, JMS583 bridge, NVMe/M.2, and power. It contains the exact USB-C receptacle, JMS583, M.2 socket, TPS54302, crystal, flash and three TPD4E05U06 arrays. Four 100 nF capacitors couple the JMS583 USB transmitter pairs, and four 220 nF capacitors couple the JMS583 PCIe transmit lanes. Only PCIe lanes 0 and 1 are connected; lanes 2 and 3 are explicitly unconnected.

The auxiliary-input power path is intentionally represented by a no-footprint, no-internal-connection placeholder. `USB5V` and `AUX5V` are not directly shorted. Selection of a reverse-current-blocking power mux/ideal-diode circuit is a release gate. The TPS54302 3.3 V network uses TI's documented 3.3 V starting values: 6.8 uH, 44 uF, 100 k / 22.1 k feedback and 47 pF feed-forward. Final passive MPN/derating selection remains a human-review item.
