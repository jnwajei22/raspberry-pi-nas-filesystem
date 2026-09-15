"""Generate the repository-local first-pass KiCad 9 schematic.

The generator deliberately embeds every schematic symbol so the design can be
parsed in a clean KiCad installation while exact-part libraries remain local.
Run from the repository root with Python 3.11+.
"""

from __future__ import annotations

import json
import re
import shutil
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PCB = ROOT / "hardware" / "pcb"
KICAD = PCB / "kicad"
SYMLIB = PCB / "libraries" / "symbols" / "RaspberryPiNAS_Parts.kicad_sym"
FPLIB = PCB / "libraries" / "footprints" / "RaspberryPiNAS.pretty"
MODELS = PCB / "libraries" / "3dmodels"
KICAD_SHARE = Path(r"C:\Program Files\KiCad\9.0\share\kicad")
PROJECT = "raspberry_pi_nas_nvme"


def uid() -> str:
    return str(uuid.uuid4())


def sexp_blocks(text: str, form: str, top_depth: int = 1) -> dict[str, str]:
    """Return named S-expression blocks at the requested parenthesis depth."""
    out: dict[str, str] = {}
    i = 0
    depth = 0
    in_string = False
    escaped = False
    marker = f'({form} "'
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "(":
            if depth == top_depth and text.startswith(marker, i):
                name_start = i + len(marker)
                name_end = text.find('"', name_start)
                name = text[name_start:name_end]
                start = i
                level = 0
                j = i
                quoted = False
                esc = False
                while j < len(text):
                    c = text[j]
                    if quoted:
                        if esc:
                            esc = False
                        elif c == "\\":
                            esc = True
                        elif c == '"':
                            quoted = False
                    else:
                        if c == '"':
                            quoted = True
                        elif c == "(":
                            level += 1
                        elif c == ")":
                            level -= 1
                            if level == 0:
                                out[name] = text[start : j + 1]
                                i = j + 1
                                break
                    j += 1
                continue
            depth += 1
        elif ch == ")":
            depth -= 1
        i += 1
    return out


def prefix_top_symbol(block: str, lib_id: str) -> str:
    return re.sub(r'^\(symbol "[^"]+"', f'(symbol "{lib_id}"', block, count=1)


def pin_records(block: str) -> dict[str, tuple[float, float, int, str]]:
    pins: dict[str, tuple[float, float, int, str]] = {}
    for match in re.finditer(r"\(pin\s+(\w+)\s+\w+", block):
        start = match.start()
        level = 0
        quoted = False
        escaped = False
        end = start
        for end in range(start, len(block)):
            ch = block[end]
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
            else:
                if ch == '"':
                    quoted = True
                elif ch == "(":
                    level += 1
                elif ch == ")":
                    level -= 1
                    if level == 0:
                        break
        pin = block[start : end + 1]
        at = re.search(r"\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)", pin)
        number = re.search(r'\(number\s+"([^"]+)"', pin)
        if at and number:
            pins.setdefault(
                number.group(1),
                (float(at.group(1)), float(at.group(2)), int(float(at.group(3) or 0)), match.group(1)),
            )
    return pins


def make_flash_symbol() -> str:
    source = (KICAD_SHARE / "symbols" / "Memory_Flash.kicad_sym").read_text(encoding="utf-8")
    base = sexp_blocks(source, "symbol")["W25Q32JVSS"]
    base = base.replace("W25Q32JVSS", "W25Q16JVSNIQ")
    base = base.replace("32Mbit / 4MiB", "16Mbit / 2MiB")
    base = re.sub(
        r'http://www\.winbond\.com/resource-files/w25q32jv%20revg%2003272018%20plus\.pdf',
        "https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q16JV.1",
        base,
    )
    base = base.replace(
        "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
        "RaspberryPiNAS:Winbond_W25Q16JVSNIQ_SOIC8_150mil",
    )
    base = base.replace("SOIC-8 (208 mil)", "SOIC-8 (150 mil)")
    return base


def placeholder_symbol() -> str:
    return r'''(symbol "PowerPath_Placeholder"
		(pin_names (offset 1.016))
		(exclude_from_sim no)
		(in_bom no)
		(on_board no)
		(property "Reference" "U" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
		(property "Value" "POWER_PATH_TBD" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(property "Description" "Unselected dual-input power-path controller placeholder; no internal electrical connection is implied" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(symbol "PowerPath_Placeholder_0_1"
			(rectangle (start -10.16 3.81) (end 10.16 -3.81) (stroke (width 0.254) (type default)) (fill (type background))))
		(symbol "PowerPath_Placeholder_1_1"
			(pin power_in line (at -12.7 2.54 0) (length 2.54) (name "USB5V_IN" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			(pin power_in line (at -12.7 -2.54 0) (length 2.54) (name "AUX5V_IN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			(pin power_out line (at 12.7 0 180) (length 2.54) (name "5V_SYS_OUT" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27))))))
		(embedded_fonts no))'''


def snap_symbol_pins(block: str, grid: float = 1.27) -> str:
    def repl(match: re.Match[str]) -> str:
        x = round(float(match.group(2)) / grid) * grid
        y = round(float(match.group(3)) / grid) * grid
        return f"{match.group(1)}{x:g} {y:g}{match.group(4) or ''})"
    return re.sub(
        r"(\(pin\s+\w+\s+\w+\s*\(at\s+)([-0-9.]+)\s+([-0-9.]+)(\s+[-0-9.]+)?\)",
        repl,
        block,
    )


def prepare_libraries() -> dict[str, str]:
    local = SYMLIB.read_text(encoding="utf-8")
    existing = sexp_blocks(local, "symbol")
    changed = False
    if "W25Q16JVSSIQ" in existing:
        local = local.replace(existing["W25Q16JVSSIQ"], "")
        changed = True
    if "PowerPath_Placeholder" in existing:
        local = local.replace(existing["PowerPath_Placeholder"], placeholder_symbol())
        changed = True
    if "JMicron_JMS583-QHFA0A" in existing:
        repaired = snap_symbol_pins(existing["JMicron_JMS583-QHFA0A"])
        local = local.replace(existing["JMicron_JMS583-QHFA0A"], repaired)
        changed = True
    if "TE_1-2199230-6" in existing:
        # A connector does not actively drive the endpoint; passive electrical
        # types prevent false output/output ERC while retaining exact names/numbers.
        repaired = re.sub(r"\(pin (?:input|output|bidirectional) ", "(pin passive ", existing["TE_1-2199230-6"])
        local = local.replace(existing["TE_1-2199230-6"], repaired)
        changed = True
    additions = []
    if 'symbol "W25Q16JVSNIQ"' not in local:
        additions.append(make_flash_symbol())
    if 'symbol "PowerPath_Placeholder"' not in local:
        additions.append(placeholder_symbol())
    if additions:
        close = local.rfind(")")
        local = local[:close].rstrip() + "\n\t" + "\n\t".join(a.replace("\n", "\n\t") for a in additions) + "\n)\n"
        changed = True
    if changed:
        SYMLIB.write_text(local, encoding="utf-8")

    FPLIB.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    src_fp = KICAD_SHARE / "footprints" / "Package_SO.pretty" / "SOIC-8_3.9x4.9mm_P1.27mm.kicad_mod"
    fp_text = src_fp.read_text(encoding="utf-8")
    fp_text = re.sub(r'^\(footprint "[^"]+"', '(footprint "Winbond_W25Q16JVSNIQ_SOIC8_150mil"', fp_text, count=1)
    fp_text = fp_text.replace(
        "${KICAD9_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step",
        "${KIPRJMOD}/../libraries/3dmodels/SOIC-8_3.9x4.9mm_P1.27mm.step",
    )
    (FPLIB / "Winbond_W25Q16JVSNIQ_SOIC8_150mil.kicad_mod").write_text(fp_text, encoding="utf-8")
    src_step = KICAD_SHARE / "3dmodels" / "Package_SO.3dshapes" / "SOIC-8_3.9x4.9mm_P1.27mm.step"
    if src_step.exists():
        shutil.copyfile(src_step, MODELS / src_step.name)

    # Existing exact footprints were prepared before the project moved one level down.
    for footprint in FPLIB.glob("*.kicad_mod"):
        text = footprint.read_text(encoding="utf-8")
        text = text.replace("${KIPRJMOD}/libraries/3dmodels/", "${KIPRJMOD}/../libraries/3dmodels/")
        footprint.write_text(text, encoding="utf-8")

    local_blocks = sexp_blocks(SYMLIB.read_text(encoding="utf-8"), "symbol")
    return local_blocks


def global_symbol(lib: str, name: str) -> str:
    text = (KICAD_SHARE / "symbols" / f"{lib}.kicad_sym").read_text(encoding="utf-8")
    return sexp_blocks(text, "symbol")[name]


class Schematic:
    def __init__(self, symbol_blocks: dict[str, str]):
        self.root_uuid = uid()
        self.symbol_blocks = symbol_blocks
        self.items: list[str] = []
        self.used_libs: set[str] = set()
        self.components: dict[str, dict] = {}
        self.label_keys: set[tuple[float, float, str]] = set()

    def add_text(self, value: str, x: float, y: float, size: float = 1.5, bold: bool = False) -> None:
        value = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        self.items.append(
            f'''\t(text "{value}"
\t\t(exclude_from_sim no)
\t\t(at {x:g} {y:g} 0)
\t\t(effects (font (size {size:g} {size:g}) (thickness 0.3){" (bold yes)" if bold else ""}) (justify left bottom))
\t\t(uuid "{uid()}")
\t)'''
        )

    def add_symbol(
        self,
        lib_id: str,
        ref: str,
        value: str,
        x: float,
        y: float,
        footprint: str = "",
        datasheet: str = "",
        description: str = "",
        in_bom: bool = True,
        on_board: bool = True,
        dnp: bool = False,
    ) -> None:
        x = round(x / 1.27) * 1.27
        y = round(y / 1.27) * 1.27
        block = self.symbol_blocks[lib_id]
        pins = pin_records(block)
        comp_uuid = uid()
        self.used_libs.add(lib_id)
        self.components[ref] = {"x": x, "y": y, "pins": pins}
        pin_entries = "\n".join(f'\t\t(pin "{n}" (uuid "{uid()}"))' for n in pins)
        esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
        self.items.append(
            f'''\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:g} {y:g} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom {"yes" if in_bom else "no"})
\t\t(on_board {"yes" if on_board else "no"})
\t\t(dnp {"yes" if dnp else "no"})
\t\t(uuid "{comp_uuid}")
\t\t(property "Reference" "{esc(ref)}" (at {x:g} {y-4:g} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{esc(value)}" (at {x:g} {y-2:g} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{esc(footprint)}" (at {x:g} {y:g} 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" "{esc(datasheet)}" (at {x:g} {y:g} 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Description" "{esc(description)}" (at {x:g} {y:g} 0) (effects (font (size 1.27 1.27)) (hide yes)))
{pin_entries}
\t\t(instances (project "{PROJECT}" (path "/{self.root_uuid}" (reference "{ref}") (unit 1))))
\t)'''
        )

    def point(self, ref: str, pin: str) -> tuple[float, float]:
        comp = self.components[ref]
        px, py, _rot, _kind = comp["pins"][str(pin)]
        return round(comp["x"] + px, 4), round(comp["y"] - py, 4)

    def label_pin(self, ref: str, pin: str, net: str) -> None:
        x, y = self.point(ref, pin)
        key = (x, y, net)
        if key in self.label_keys:
            return
        self.label_keys.add(key)
        self.items.append(
            f'''\t(global_label "{net}"
\t\t(shape bidirectional)
\t\t(at {x:g} {y:g} 0)
\t\t(effects (font (size 1.0 1.0)) (justify left))
\t\t(uuid "{uid()}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x:g} {y:g} 0) (effects (font (size 1.0 1.0)) (hide yes)))
\t)'''
        )

    def no_connect_pin(self, ref: str, pin: str) -> None:
        x, y = self.point(ref, pin)
        self.items.append(f'\t(no_connect (at {x:g} {y:g}) (uuid "{uid()}"))')

    def connect(self, ref: str, mapping: dict[str, str]) -> None:
        for pin, net in mapping.items():
            self.label_pin(ref, str(pin), net)
        mapped = {str(p) for p in mapping}
        seen_points: set[tuple[float, float]] = set()
        for pin, rec in self.components[ref]["pins"].items():
            if pin in mapped or rec[3] == "no_connect":
                continue
            point = self.point(ref, pin)
            if point not in seen_points:
                self.no_connect_pin(ref, pin)
                seen_points.add(point)

    def render(self) -> str:
        libs = []
        for lib_id in sorted(self.used_libs):
            libs.append(prefix_top_symbol(self.symbol_blocks[lib_id], lib_id).replace("\n", "\n\t\t"))
        libraries_text = "\n\t\t".join(libs)
        items_text = "\n".join(self.items)
        return f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid "{self.root_uuid}")
\t(paper "A3")
\t(lib_symbols
\t\t{libraries_text}
\t)
{items_text}
\t(sheet_instances (path "/" (page "1")))
\t(embedded_fonts no)
)\n'''


def build_schematic(local: dict[str, str]) -> str:
    blocks: dict[str, str] = {}
    for name, block in local.items():
        blocks[f"RaspberryPiNAS_Parts:{name}"] = block
    for name in ("R", "C", "L", "LED"):
        blocks[f"Device:{name}"] = global_symbol("Device", name)
    blocks["Connector_Generic:Conn_01x02"] = global_symbol("Connector_Generic", "Conn_01x02")
    blocks["power:PWR_FLAG"] = global_symbol("power", "PWR_FLAG")

    s = Schematic(blocks)
    s.add_text("RASPBERRY PI NAS — USB 3.x TO NVMe BRIDGE", 15, 15, 2.2, True)
    s.add_text("Board target: 90 mm x 90 mm, 4 layers. SCHEMATIC ONLY — NO PCB LAYOUT.", 15, 20, 1.2)
    s.add_text("1. USB INTERFACE", 15, 30, 1.8, True)
    s.add_text("2. JMS583 BRIDGE", 92, 30, 1.8, True)
    s.add_text("3. NVME / M.2", 195, 30, 1.8, True)
    s.add_text("4. POWER", 15, 185, 1.8, True)

    # USB receptacle and three four-channel ESD arrays (all SS pairs plus USB2 pair).
    s.add_symbol("RaspberryPiNAS_Parts:Molex_2024100002", "J1", "2024100002", 35, 88,
                 "RaspberryPiNAS:Molex_2024100002", "https://www.molex.com/en-us/products/part-detail/2024100002")
    usb = {
        "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
        "A4": "USB5V", "A9": "USB5V", "B4": "USB5V", "B9": "USB5V",
        "A5": "CC1", "B5": "CC2", "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
        "A2": "USB_TX1_P", "A3": "USB_TX1_N", "B11": "USB_RX1_P", "B10": "USB_RX1_N",
        "B2": "USB_TX2_P", "B3": "USB_TX2_N", "A11": "USB_RX2_P", "A10": "USB_RX2_N",
    }
    s.connect("J1", usb)

    for ref, x, nets in (
        ("U2", 28, ("USB_TX1_P", "USB_TX1_N", "USB_RX1_P", "USB_RX1_N")),
        ("U3", 55, ("USB_TX2_P", "USB_TX2_N", "USB_RX2_P", "USB_RX2_N")),
        ("U4", 82, ("USB_DP", "USB_DM", None, None)),
    ):
        s.add_symbol("RaspberryPiNAS_Parts:TPD4E05U06DQAR", ref, "TPD4E05U06DQAR", x, 158,
                     "RaspberryPiNAS:TPD4E05U06DQAR_DQA0010A", "https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf")
        esd_map = {"1": nets[0], "2": nets[1], "3": "GND", "8": "GND"}
        if nets[2] is not None:
            esd_map.update({"4": nets[2], "5": nets[3]})
        s.connect(ref, esd_map)

    # JMS583 bridge. USB-C orientation mapping crosses receptacle TX into JMS RX and vice versa.
    s.add_symbol("RaspberryPiNAS_Parts:JMicron_JMS583-QHFA0A", "U1", "JMS583-QHFA0A", 112, 88,
                 "RaspberryPiNAS:JMicron_JMS583-QHFA0A", "../libraries/datasheets/JMicron_JMS583_datasheet_rev2.1.pdf")
    jms = {
        "1": "5V_SYS", "2": "1V2_JMS", "3": "SPI_MISO", "4": "SPI_SCK", "5": "SPI_MOSI",
        "6": "3V3_JMS", "7": "SPI_CS_N", "11": "3V3_JMS", "15": "JMS_RST_N", "16": "USB5V",
        "17": "USB_DM", "18": "USB_DP", "19": "3V3_JMS", "20": "1V2_JMS",
        "21": "JMS_USB_TX1_P", "22": "JMS_USB_TX1_N", "23": "JMS_USB_TX2_N", "24": "JMS_USB_TX2_P",
        "25": "1V2_JMS", "26": "USB_TX1_P", "27": "USB_TX1_N", "28": "USB_TX2_N", "29": "USB_TX2_P",
        "30": "1V2_JMS", "31": "1V2_JMS", "32": "3V3_JMS", "33": "1V2_JMS",
        "34": "PCIE_RX1_N", "35": "PCIE_RX1_P", "36": "1V2_JMS", "37": "JMS_PCIE_TX1_N", "38": "JMS_PCIE_TX1_P",
        "39": "JMS_REXT", "40": "1V2_JMS", "41": "PCIE_RX0_N", "42": "PCIE_RX0_P", "43": "1V2_JMS",
        "44": "JMS_PCIE_TX0_N", "45": "JMS_PCIE_TX0_P", "46": "1V2_JMS", "47": "PCIE_REFCLK_N", "48": "PCIE_REFCLK_P",
        "49": "1V2_JMS", "50": "XTAL_IN", "51": "XTAL_OUT", "52": "3V3_JMS", "53": "1V2_JMS",
        "54": "PCIE_PERST_N", "55": "PCIE_CLKREQ_N", "56": "3V3_JMS", "57": "ACT_LED_N", "60": "GND",
        "61": "CC2", "62": "CC1", "63": "GND", "64": "JMS_LXO", "65": "GND",
    }
    s.connect("U1", jms)

    # USB transmitter coupling capacitors are on JMS TX outputs only.
    for i, (raw, net) in enumerate((
        ("JMS_USB_TX1_P", "USB_RX1_P"), ("JMS_USB_TX1_N", "USB_RX1_N"),
        ("JMS_USB_TX2_P", "USB_RX2_P"), ("JMS_USB_TX2_N", "USB_RX2_N")), 1):
        ref = f"C{i}"
        s.add_symbol("Device:C", ref, "100nF", 142 + (i - 1) * 12, 145,
                     "Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder")
        s.connect(ref, {"1": raw, "2": net})

    s.add_symbol("RaspberryPiNAS_Parts:Abracon_ABM8-25.000MHZ-B2-T", "Y1", "ABM8-25.000MHZ-B2-T", 154, 48,
                 "RaspberryPiNAS:Abracon_ABM8-25.000MHZ-B2-T", "../libraries/datasheets/Abracon_ABM8_datasheet.pdf")
    s.connect("Y1", {"1": "XTAL_IN", "2": "GND", "3": "XTAL_OUT", "4": "GND"})

    s.add_symbol("RaspberryPiNAS_Parts:W25Q16JVSNIQ", "U6", "W25Q16JVSNIQ TR", 158, 82,
                 "RaspberryPiNAS:Winbond_W25Q16JVSNIQ_SOIC8_150mil",
                 "https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q16JV.1")
    s.connect("U6", {"1": "SPI_CS_N", "2": "SPI_MISO", "3": "FLASH_WP_N", "4": "GND",
                     "5": "SPI_MOSI", "6": "SPI_SCK", "7": "FLASH_HOLD_N", "8": "3V3_JMS"})

    for ref, net, x in (("R4", "FLASH_WP_N", 174), ("R5", "FLASH_HOLD_N", 186)):
        s.add_symbol("Device:R", ref, "10k", x, 96, "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder")
        s.connect(ref, {"1": net, "2": "3V3_JMS"})

    s.add_symbol("Device:R", "R1", "12k 1%", 148, 112, "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder")
    s.connect("R1", {"1": "JMS_REXT", "2": "GND"})
    s.add_symbol("Device:L", "L1", "4.7uH", 166, 112, "Inductor_SMD:L_1210_3225Metric_Pad1.42x2.65mm_HandSolder")
    s.connect("L1", {"1": "JMS_LXO", "2": "1V2_JMS"})
    s.add_symbol("Device:R", "R2", "10k VERIFY", 184, 112, "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder")
    s.connect("R2", {"1": "JMS_RST_N", "2": "3V3_JMS"})
    s.add_symbol("Device:R", "R3", "1k VERIFY", 154, 128, "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder")
    s.connect("R3", {"1": "3V3_JMS", "2": "ACT_LED_A"})
    s.add_symbol("Device:LED", "D1", "ACTIVITY GREEN", 174, 128, "LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder")
    s.connect("D1", {"1": "ACT_LED_N", "2": "ACT_LED_A"})

    # Representative local bypassing on both JMS-generated rails.
    for i, (value, net, x) in enumerate((
        ("100nF", "3V3_JMS", 115), ("1uF", "3V3_JMS", 125), ("4.7uF", "3V3_JMS", 135),
        ("100nF", "1V2_JMS", 145), ("1uF", "1V2_JMS", 155), ("4.7uF", "1V2_JMS", 165)), 1):
        ref = f"C{i + 4}"
        s.add_symbol("Device:C", ref, value, x, 174, "Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder")
        s.connect(ref, {"1": net, "2": "GND"})

    s.add_text("VERIFY AGAINST JMS583 REFERENCE DESIGN BEFORE PCB RELEASE", 92, 36, 1.3, True)
    s.add_text("JMS583 public pin table used. Confirm EP grounding, reset pull-up, crystal load network, internal-regulator rail topology and LED polarity.", 92, 40, 1.0)
    s.add_text("USB-C orientation: A-side TX1/B-side TX2 feed JMS RX1/RX2; JMS TX1/TX2 feed B-side RX1/A-side RX2.", 15, 136, 1.0)

    # M.2 M-key connector: PCIe lanes 0/1 only. M.2 PET is endpoint TX into JMS RX; PER is endpoint RX from JMS TX.
    s.add_symbol("RaspberryPiNAS_Parts:TE_1-2199230-6", "J3", "1-2199230-6", 226, 88,
                 "RaspberryPiNAS:TE_1-2199230-6_M2_M_Key", "https://www.te.com/en/product-1-2199230-6.html")
    m2 = {
        "1": "GND", "2": "3V3_NVME", "3": "GND", "4": "3V3_NVME", "9": "GND",
        "12": "3V3_NVME", "14": "3V3_NVME", "15": "GND", "16": "3V3_NVME", "18": "3V3_NVME",
        "21": "GND", "27": "GND", "29": "PCIE_TX1_N", "31": "PCIE_TX1_P", "33": "GND",
        "35": "PCIE_RX1_N", "37": "PCIE_RX1_P", "39": "GND", "41": "PCIE_TX0_N", "43": "PCIE_TX0_P",
        "45": "GND", "47": "PCIE_RX0_N", "49": "PCIE_RX0_P", "50": "PCIE_PERST_N", "51": "GND",
        "52": "PCIE_CLKREQ_N", "53": "PCIE_REFCLK_N", "55": "PCIE_REFCLK_P", "57": "GND",
        "70": "3V3_NVME", "71": "GND", "72": "3V3_NVME", "73": "GND", "74": "3V3_NVME", "75": "GND",
        "SH1": "GND", "SH2": "GND",
    }
    s.connect("J3", m2)
    s.add_text("M.2 M-Key — 2280 NVMe — PCIe x2 electrically", 195, 145, 1.5, True)
    s.add_text("Lanes 2 and 3 intentionally unconnected. Connector pin names follow host-centric PET/PER convention.", 195, 150, 1.0)

    for i, (raw, net) in enumerate((
        ("JMS_PCIE_TX0_P", "PCIE_TX0_P"), ("JMS_PCIE_TX0_N", "PCIE_TX0_N"),
        ("JMS_PCIE_TX1_P", "PCIE_TX1_P"), ("JMS_PCIE_TX1_N", "PCIE_TX1_N")), 1):
        ref = f"C{i + 10}"
        s.add_symbol("Device:C", ref, "220nF", 205 + (i - 1) * 13, 162,
                     "Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder")
        s.connect(ref, {"1": raw, "2": net})

    # Power path is deliberately a non-functional placeholder until an actual controller is selected.
    s.add_symbol("Connector_Generic:Conn_01x02", "J2", "AUX5V INPUT — CONNECTOR TBD", 28, 218,
                 "", "", "Auxiliary 5V connector electrical and mechanical selection is pending", on_board=False)
    s.connect("J2", {"1": "AUX5V", "2": "GND"})
    s.add_symbol("RaspberryPiNAS_Parts:PowerPath_Placeholder", "U5", "POWER_PATH_TBD", 72, 218,
                 "", "", "Select reverse-current-blocking dual-input power mux before PCB release", in_bom=False, on_board=False, dnp=True)
    s.connect("U5", {"1": "USB5V", "2": "AUX5V", "3": "5V_SYS"})
    s.add_text("POWER-PATH PLACEHOLDER — NO USB5V/AUX5V SHORT IS PRESENT", 15, 194, 1.25, True)
    s.add_text("Select a reverse-current-blocking 5 V power mux / ideal-diode solution and rated AUX connector before PCB release.", 15, 198, 1.0)

    # Power flags express external sources for ERC; they do not imply a copper short.
    for i, (net, x) in enumerate((("USB5V", 20), ("AUX5V", 35), ("GND", 50),
                                  ("1V2_JMS", 65), ("3V3_NVME", 80)), 1):
        ref = f"#FLG0{i:02d}"
        s.add_symbol("power:PWR_FLAG", ref, "PWR_FLAG", x, 205, "", "", in_bom=False, on_board=False)
        s.connect(ref, {"1": net})

    # TPS54302 5 V to 3.3 V reference network per TI Table 7-2 (Rev. C, March 2026).
    s.add_symbol("RaspberryPiNAS_Parts:TPS54302DDCR", "U7", "TPS54302DDCR", 130, 225,
                 "RaspberryPiNAS:TPS54302DDCR_DDC0006A", "../libraries/datasheets/TI_TPS54302_datasheet.pdf")
    s.connect("U7", {"1": "GND", "2": "BUCK_SW", "3": "5V_SYS", "4": "BUCK_FB", "5": "5V_SYS", "6": "BUCK_BOOT"})

    power_parts = [
        ("C15", "Device:C", "10uF", 98, 240, "5V_SYS", "GND"),
        ("C16", "Device:C", "100nF", 108, 240, "5V_SYS", "GND"),
        ("C17", "Device:C", "47uF", 118, 240, "5V_SYS", "GND"),
        ("C18", "Device:C", "100nF", 145, 240, "BUCK_BOOT", "BUCK_SW"),
        ("L2", "Device:L", "6.8uH / >=3A", 160, 225, "BUCK_SW", "3V3_NVME"),
        ("R6", "Device:R", "100k 1%", 180, 215, "3V3_NVME", "BUCK_FB"),
        ("R7", "Device:R", "22.1k 1%", 180, 235, "BUCK_FB", "GND"),
        ("C19", "Device:C", "47pF", 198, 215, "3V3_NVME", "BUCK_FB"),
        ("C20", "Device:C", "22uF", 215, 235, "3V3_NVME", "GND"),
        ("C21", "Device:C", "22uF", 228, 235, "3V3_NVME", "GND"),
        ("C22", "Device:C", "100uF", 241, 235, "3V3_NVME", "GND"),
        ("C23", "Device:C", "100nF", 254, 235, "3V3_NVME", "GND"),
    ]
    for ref, lib, value, x, y, n1, n2 in power_parts:
        footprint = "Inductor_SMD:L_1210_3225Metric_Pad1.42x2.65mm_HandSolder" if lib.endswith(":L") else (
            "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" if lib.endswith(":R") else
            "Capacitor_SMD:C_1210_3225Metric_Pad1.33x2.70mm_HandSolder" if "uF" in value else
            "Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder")
        s.add_symbol(lib, ref, value, x, y, footprint)
        s.connect(ref, {"1": n1, "2": n2})

    s.add_text("TPS54302: 6.8 uH, 44 uF output, 100k/22.1k divider and 47 pF feed-forward follow TI's 3.3 V table.", 95, 258, 1.0)
    s.add_text("Inductor/capacitor voltage, ripple-current, DC-bias and thermal ratings require final MPN selection.", 95, 263, 1.0)
    return s.render()


def main() -> None:
    KICAD.mkdir(parents=True, exist_ok=True)
    local = prepare_libraries()
    schematic = build_schematic(local)
    (KICAD / f"{PROJECT}.kicad_sch").write_text(schematic, encoding="utf-8")

    pro = {
        "board": {}, "boards": [], "cvpcb": {}, "erc": {}, "libraries": {},
        "meta": {"filename": f"{PROJECT}.kicad_pro", "version": 1},
        "net_settings": {"classes": [], "meta": {"version": 3}},
        "pcbnew": {}, "schematic": {}, "text_variables": {}
    }
    (KICAD / f"{PROJECT}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")

    sym_table = '''(sym_lib_table
  (version 7)
  (lib (name "RaspberryPiNAS_Parts")(type "KiCad")(uri "${KIPRJMOD}/../libraries/symbols/RaspberryPiNAS_Parts.kicad_sym")(options "")(descr "Repository-local NAS exact-part symbols"))
)\n'''
    fp_table = '''(fp_lib_table
  (version 7)
  (lib (name "RaspberryPiNAS")(type "KiCad")(uri "${KIPRJMOD}/../libraries/footprints/RaspberryPiNAS.pretty")(options "")(descr "Repository-local NAS exact-part footprints"))
)\n'''
    (KICAD / "sym-lib-table").write_text(sym_table, encoding="utf-8")
    (KICAD / "fp-lib-table").write_text(fp_table, encoding="utf-8")


if __name__ == "__main__":
    main()
