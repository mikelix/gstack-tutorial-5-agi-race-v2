#!/usr/bin/env python3
"""verify.py — self-checks for Tutorial #5. Exit code 1 on any failure.

Checks:
  1. arithmetic behind every derived number
  2. every key number appears in both TUTORIAL.md and TUTORIAL.zh.md (parity)
  3. EN/ZH heading-structure parity (same number of Parts and checkpoints)
  4. every relative link / image in both tutorials resolves
  5. all dist/ deliverables exist
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
en = (ROOT / "TUTORIAL.md").read_text(encoding="utf-8")
zh = (ROOT / "TUTORIAL.zh.md").read_text(encoding="utf-8")
fails = []


def check(cond, msg):
    print(("  ok  " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


print("1. arithmetic")
check(round(98 / 58736 * 1000, 2) == 1.67, "CCI V1 = 1.67")
check(round(0.88 * 0.90 * 0.76, 3) == 0.602, "B V1 = 0.602")
check(round(0.92 * 0.89 * 0.94, 3) == 0.770, "B V2 = 0.770")
check(round((77.0 - 60.2) / 60.2 * 100, 1) == 27.9, "+27.9 %")
check(round(0.92 * 0.94, 3) == 0.865, "R x P = 0.865")
check(round((62.49 - 56.34) / 62.49 * 100, 1) == 9.8, "master -9.8 %")
check(round((62.49 - 46.54) / 62.49 * 100, 1) == 25.5, "short -25.5 %")
check(round(4.15 / 46.54 * 100, 1) == 8.9, "hook share 8.9 %")
check(round(8.6 / 56.34 * 100, 1) == 15.3 and round(8.6 / 46.54 * 100, 1) == 18.5, "cliff share 15.3 / 18.5 %")
check(round(2.5 / 46.54 * 100, 2) == 5.37, "end-card share 5.37 %")

print("2. number parity EN/ZH")
for n in ["58,736", "1.67", "0.602", "0.770", "27.9", "0.865", "62.49", "56.34", "46.54", "4.15",
          "2.55", "8.53", "8.6", "1.08", "0.95", "0.84", "0.8.79", "13/13", "139", "61", "144",
          "mEztESwn7mI", "6MnhRmSR_TA", "garrytan/gstack", "heygen-com/hyperframes"]:
    check(n in en and n in zh, f"'{n}' in both")

print("3. structure parity")
ce = len(re.findall(r"^\*\*Checkpoint \d", en, re.M))
cz = len(re.findall(r"^\*\*检查点 \d", zh, re.M))
check(ce == cz == 10, f"checkpoints EN={ce} ZH={cz}")
pe = len(re.findall(r"^## Part \d+", en, re.M))
pz = len(re.findall(r"^## 第 \d+ 部分", zh, re.M))
check(pe == pz == 12, f"parts EN={pe} ZH={pz}")

print("4. links")
for name, txt in (("EN", en), ("ZH", zh)):
    for link in re.findall(r"\]\(([^)#]+?)\)", txt):
        if link.startswith("http"):
            continue
        check((ROOT / link).exists(), f"{name} link {link}")

print("5. deliverables")
for f in ["gstack-tutorial-5_EN.docx", "gstack-tutorial-5_ZH.docx", "gstack-tutorial-5_EN.pptx", "gstack-tutorial-5_ZH.pptx"]:
    check((ROOT / "dist" / f).exists(), f"dist/{f}")

print(f"\n{'ALL CHECKS PASSED' if not fails else str(len(fails)) + ' FAILURE(S)'}")
sys.exit(1 if fails else 0)
