#!/usr/bin/env python3
"""
make_figures.py — regenerates every figure in assets/ (EN + ZH).

    python _build/make_figures.py

Figures:
  fig_pipeline_{en,zh}.png   three-layer production system
  fig_timeline_{en,zh}.png   V1 vs V2 master vs V2 Short timing diagram
  fig_rap_{en,zh}.png        CSR-RAP score, V1 vs V2
  mock_0N_*_{en,zh}.png      annotated Windows 11 screenshots (ILLUSTRATIVE MOCK-UPS)

Every number drawn here comes from docs/SOURCES.md. Do not add a number that
is not in that file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

# ---- palette (shared with the deck and memo builders) ----------------------
INK = "#1B1F2A"      # dominant
AMBER = "#E8872B"    # safety / Anthropic-side coding inherited from V1 grade
TEAL = "#1F8A8A"     # production system / HyperFrames
GREY = "#8A8F98"
LIGHT = "#EEF0F3"
RED = "#C0392B"
WHITE = "#FFFFFF"

CJK = "Noto Sans CJK JP"
plt.rcParams["font.family"] = ["DejaVu Sans", CJK]
plt.rcParams["axes.unicode_minus"] = False

T = {
    "en": {
        "pipe_title": "Three layers, one loop: decide → build → render → measure",
        "pipe_boxes": [
            ("YouTube\nAnalytics", "V1: 58,736 views\n98 comments\nCCI 1.67", GREY),
            ("CSR-RAP\nagent (GPT)", "Decides WHAT\nto change\nR × A × P", AMBER),
            ("Opus 5.5 in\nClaude Code", "Plans & writes the\ncomposition\n+ gstack discipline", INK),
            ("HyperFrames", "Renders deterministically\nlint → check →\nsnapshot → render", TEAL),
            ("V2 on\nYouTube", "56.34s master (16:9)\n46.54s Short (9:16)\nA/B test", GREY),
        ],
        "pipe_loop": "72 h later: real analytics return to CSR-RAP → Observed RAP Score",
        "tl_title": "V1 vs V2: where the seconds went",
        "tl_rows": ["V1 (published)\n62.49 s", "V2 master 16:9\n56.34 s", "V2 Short 9:16\n46.54 s"],
        "v1_segs": [(0, 50, "Lineup / title → race gags (47 shots, median 1.08 s)"),
                    (50, 60.1, "Fastest cutting\n(avg 0.95 s)"),
                    (60.1, 61.65, ""),
                    (61.65, 62.49, "")],
        "v1_marks": [(54.45, "Late entrant 54.45 s")], "nf": "near-freeze ≈1.5 s + 0.84 s black",
        "cold": "Cold\nopen", "title": "Title\nslam", "roll": "Roll call\n+ role tags",
        "body_m": "Gag escalation → \"slow down\" → late entrant",
        "body_s": "Roll call (trimmed) + gags → late entrant\n(Patron block cut; GPU montage trimmed)",
        "cliff": "Cliff + CTA\n8.6 s", "hold": "", "hold_out": "end-card hold ≈2.5 s",
        "mark40": "≈40 s checkpoint",
        "hook": "Hook complete at 4.15 s",
        "axis": "seconds",
        "tl_note": "Anchors: V1 from Episode1_Visual_DNA (FFmpeg-measured); V2 from the V2 storyboard as quoted in the CSR-RAP V2 analysis. "
                   "Inner beat boundaries not labelled are in the storyboard file.",
        "rap_title": "CSR-RAP structural score: V1 → V2",
        "rap_cats": ["R  Rules of\nBusiness", "A  Attributes\nof Industry", "P  Production\nCapability", "B = R×A×P"],
        "rap_note": "Design-quality score, not a view forecast. V2's A-layer still needs real YouTube behaviour data.",
        "mock_banner": "ILLUSTRATIVE MOCK-UP — replace with your own screenshot",
    },
    "zh": {
        "pipe_title": "三层系统，一个闭环：决策 → 制作 → 渲染 → 度量",
        "pipe_boxes": [
            ("YouTube\n后台数据", "V1：58,736 播放\n98 条评论\nCCI 1.67", GREY),
            ("CSR-RAP\n智能体（GPT）", "决定“改什么”\nR × A × P", AMBER),
            ("Claude Code 中的\nOpus 5.5", "规划并编写合成\n+ gstack 工程纪律", INK),
            ("HyperFrames", "确定性渲染\nlint → check →\nsnapshot → render", TEAL),
            ("V2 上线\nYouTube", "56.34 秒横版（16:9）\n46.54 秒竖版（9:16）\nA/B 测试", GREY),
        ],
        "pipe_loop": "72 小时后：真实数据回流 CSR-RAP → 观测型 RAP 得分（Observed RAP Score）",
        "tl_title": "V1 与 V2：每一秒花在了哪里",
        "tl_rows": ["V1（已发布）\n62.49 秒", "V2 横版 16:9\n56.34 秒", "V2 竖版 9:16\n46.54 秒"],
        "v1_segs": [(0, 50, "开场阵容/片名 → 赛车笑点（47 个镜头，中位数 1.08 秒）"),
                    (50, 60.1, "最快剪辑区\n（均 0.95 秒）"),
                    (60.1, 61.65, ""),
                    (61.65, 62.49, "")],
        "v1_marks": [(54.45, "迟到者入场 54.45 秒")], "nf": "近似定格约 1.5 秒 + 0.84 秒黑场",
        "cold": "冷开场", "title": "片名\n砸出", "roll": "角色点名\n+ 身份标签",
        "body_m": "笑点升级 → “慢下来” → 迟到者入场",
        "body_s": "角色点名（精简）+ 笑点 → 迟到者\n（删除 Patron 段；GPU 蒙太奇精简）",
        "cliff": "悬念 + CTA\n8.6 秒", "hold": "", "hold_out": "结尾卡停留约 2.5 秒",
        "mark40": "约 40 秒检查点",
        "hook": "4.15 秒完成钩子",
        "axis": "秒",
        "tl_note": "锚点来源：V1 取自 Episode1_Visual_DNA（FFmpeg 实测）；V2 取自 CSR-RAP V2 分析所引用的 V2 分镜表。"
                   "未标注的中间节拍边界见分镜文件。",
        "rap_title": "CSR-RAP 结构得分：V1 → V2",
        "rap_cats": ["R 商业共性", "A 行业特性", "P 企业个性\n（生产能力）", "B = R×A×P"],
        "rap_note": "这是设计质量得分，不是播放量预测。V2 的 A 层仍需真实 YouTube 用户行为数据验证。",
        "mock_banner": "示意图（模拟画面）— 请替换为你本机的实际截图",
    },
}


# ---------------------------------------------------------------------------
def fig_pipeline(lang):
    t = T[lang]
    fig, ax = plt.subplots(figsize=(14, 5.2), dpi=160)
    ax.set_xlim(0, 14); ax.set_ylim(0, 5.2); ax.axis("off")
    fig.patch.set_facecolor(WHITE)
    ax.text(0.3, 4.8, t["pipe_title"], fontsize=17, weight="bold", color=INK, va="center")
    w, h, y = 2.3, 2.7, 1.45
    xs = [0.3 + i * 2.75 for i in range(5)]
    for i, (x, (head, body, col)) in enumerate(zip(xs, t["pipe_boxes"])):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             fc=col, ec="none")
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.55, head, ha="center", va="center", fontsize=13,
                weight="bold", color=WHITE, linespacing=1.15)
        ax.text(x + w / 2, y + 0.85, body, ha="center", va="center", fontsize=10.2,
                color=WHITE, linespacing=1.35)
        if i < 4:
            ax.annotate("", xy=(xs[i + 1] - 0.05, y + h / 2), xytext=(x + w + 0.05, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=INK))
    # feedback loop
    ly = 0.95
    ax.plot([xs[4] + w / 2, xs[4] + w / 2], [y - 0.05, ly], color=AMBER, lw=1.8, ls="--")
    ax.plot([xs[4] + w / 2, xs[1] + w / 2], [ly, ly], color=AMBER, lw=1.8, ls="--")
    ax.annotate("", xy=(xs[1] + w / 2, y - 0.03), xytext=(xs[1] + w / 2, ly),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=AMBER))
    ax.text(7.0, 0.45, t["pipe_loop"], ha="center", va="center", fontsize=11, color=AMBER,
            style="italic")
    fig.savefig(OUT / f"fig_pipeline_{lang}.png", bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


# ---------------------------------------------------------------------------
def seg(ax, y, x0, x1, label, fc, tc=WHITE, fs=9.5, h=0.62):
    ax.barh(y, x1 - x0, left=x0, height=h, color=fc, edgecolor=WHITE, linewidth=1.5)
    if label:
        ax.text((x0 + x1) / 2, y, label, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.1)


def fig_timeline(lang):
    t = T[lang]
    fig, ax = plt.subplots(figsize=(15, 6.4), dpi=160)
    fig.patch.set_facecolor(WHITE)
    Y = [2.6, 1.5, 0.4]
    # V1
    for (a, b, lab), col in zip(t["v1_segs"], [GREY, "#6B7079", "#4A4F58", "#111111"]):
        seg(ax, Y[0], a, b, lab, col)
    for x, lab in t["v1_marks"]:
        ax.plot([x, x], [Y[0] + 0.33, Y[0] + 0.5], color=INK, lw=1.4)
        ax.text(x, Y[0] + 0.56, lab, ha="center", va="bottom", fontsize=9, color=INK)
    ax.annotate(t["nf"], xy=(61.3, Y[0] - 0.31), xytext=(61.3, Y[0] - 0.55), ha="right",
                fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    # V2 master
    seg(ax, Y[1], 0, 2.55, t["cold"], RED, fs=8.5)
    seg(ax, Y[1], 2.55, 4.15, t["title"], INK, fs=7.5)
    seg(ax, Y[1], 4.15, 8.53, t["roll"], "#3A4152", fs=8.5)
    seg(ax, Y[1], 8.53, 47.74, t["body_m"], TEAL)
    seg(ax, Y[1], 47.74, 56.34, t["cliff"], AMBER, fs=9)
    ax.plot([40, 40], [Y[1] - 0.31, Y[1] + 0.31], color=WHITE, lw=1.6, ls=":")
    ax.text(40, Y[1] + 0.36, t["mark40"], ha="center", va="bottom", fontsize=9, color=INK)
    # V2 short
    seg(ax, Y[2], 0, 2.55, t["cold"], RED, fs=8.5)
    seg(ax, Y[2], 2.55, 4.15, t["title"], INK, fs=7.5)
    seg(ax, Y[2], 4.15, 37.94, t["body_s"], TEAL, fs=9)
    seg(ax, Y[2], 37.94, 44.04, t["cliff"], AMBER, fs=9)
    seg(ax, Y[2], 44.04, 46.54, t["hold"], "#B5651D", fs=8.5)
    ax.annotate(t["hold_out"], xy=(45.3, Y[2] + 0.31), xytext=(47.3, Y[2] + 0.55), ha="left",
                fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    # hook marker
    for y in Y[1:]:
        ax.plot([4.15, 4.15], [y - 0.42, y + 0.42], color=RED, lw=1.2)
    ax.text(4.3, Y[2] - 0.5, t["hook"], fontsize=9, color=RED, va="top")
    ax.set_yticks(Y); ax.set_yticklabels(t["tl_rows"], fontsize=10.5, color=INK)
    ax.set_xlim(0, 63.5); ax.set_ylim(-0.35, 3.35)
    ax.set_xticks(range(0, 65, 5)); ax.set_xlabel(t["axis"], color=GREY)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
    ax.set_title(t["tl_title"], loc="left", fontsize=16, weight="bold", color=INK, pad=14)
    fig.text(0.01, -0.02, t["tl_note"], fontsize=8.5, color=GREY, wrap=True)
    fig.savefig(OUT / f"fig_timeline_{lang}.png", bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_rap(lang):
    t = T[lang]
    v1 = [88, 90, 76, 60.2]
    v2 = [92, 89, 94, 77.0]
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=160)
    fig.patch.set_facecolor(WHITE)
    import numpy as np
    x = np.arange(4); bw = 0.36
    b1 = ax.bar(x - bw / 2, v1, bw, color=GREY, label="V1")
    b2 = ax.bar(x + bw / 2, v2, bw, color=[TEAL, TEAL, TEAL, AMBER], label="V2")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2, f"{b.get_height():g}",
                    ha="center", fontsize=11, color=INK, weight="bold")
    ax.text(3 + bw / 2, 84, "+27.9%", ha="center", fontsize=12, color=AMBER, weight="bold")
    ax.text(2 + bw / 2, 101, "+18", ha="center", fontsize=11, color=TEAL, weight="bold")
    ax.set_xticks(x); ax.set_xticklabels(t["rap_cats"], fontsize=10.5, color=INK)
    ax.set_ylim(0, 108); ax.set_yticks([])
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title(t["rap_title"], loc="left", fontsize=15, weight="bold", color=INK, pad=12)
    fig.text(0.01, -0.03, t["rap_note"], fontsize=9, color=GREY)
    fig.savefig(OUT / f"fig_rap_{lang}.png", bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Annotated terminal mock-ups
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
CJK_FILE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CJK_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

C_PROMPT = (97, 214, 214); C_TEXT = (204, 204, 204); C_OK = (22, 198, 12)
C_DIM = (140, 140, 140); C_WARN = (249, 241, 165); C_CLAUDE = (215, 119, 87)

MOCKS = {
    "01_prereqs": {
        "tab": "Windows PowerShell",
        "lines": [
            ("PS C:\\Users\\Admin> ", C_PROMPT, "git --version", C_TEXT),
            ("git version 2.47.1.windows.1", C_TEXT),
            ("PS C:\\Users\\Admin> ", C_PROMPT, "node --version", C_TEXT),
            ("v22.12.0", C_TEXT),
            ("PS C:\\Users\\Admin> ", C_PROMPT, "ffmpeg -version | Select-Object -First 1", C_TEXT),
            ("ffmpeg version 7.1-essentials_build-www.gyan.dev", C_TEXT),
            ("PS C:\\Users\\Admin> ", C_PROMPT, "bun --version", C_TEXT),
            ("1.2.4", C_TEXT),
            ("PS C:\\Users\\Admin> ", C_PROMPT, "claude --version", C_TEXT),
            ("2.x.x (Claude Code)", C_TEXT),
        ],
        "boxes": [(3, 3, 1), (5, 5, 2), (7, 7, 3), (9, 9, 4)],
        "notes": {
            "en": ["Node.js must be 22 or newer — HyperFrames will not run on older Node.",
                   "FFmpeg must be on PATH — HyperFrames renders with it; you also use it to extract V1 frames.",
                   "Bun 1.0+ is required by gstack's ./setup script.",
                   "If 'claude' is not recognized: add C:\\Users\\<you>\\AppData\\Local\\Microsoft\\WinGet\\Links to PATH, then open a NEW PowerShell."],
            "zh": ["Node.js 必须为 22 或更高版本 —— 否则 HyperFrames 无法运行。",
                   "FFmpeg 必须在 PATH 中 —— HyperFrames 用它渲染；抽取 V1 关键帧也要用它。",
                   "gstack 的 ./setup 脚本需要 Bun 1.0 以上。",
                   "若提示 'claude' 无法识别：把 C:\\Users\\<你>\\AppData\\Local\\Microsoft\\WinGet\\Links 加入 PATH，再新开一个 PowerShell。"],
        },
    },
    "02_gstack": {
        "tab": "Claude Code — D:\\ipason\\claude\\projects",
        "lines": [
            ("> ", C_CLAUDE, "Install gstack. Run exactly:", C_TEXT),
            ("  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git", C_TEXT),
            ("  ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup", C_TEXT),
            ("", C_TEXT),
            ("● Bash(git clone --single-branch --depth 1 https://github.com/garrytan/...)", C_OK),
            ("  ⎿  Cloning into 'C:/Users/Admin/.claude/skills/gstack'...", C_DIM),
            ("● Bash(cd ~/.claude/skills/gstack && ./setup)", C_OK),
            ("  ⎿  ... setup finished (output abridged)", C_DIM),
            ("● Update(CLAUDE.md)  — added a \"gstack\" section listing the skills", C_OK),
            ("", C_TEXT),
            ("> ", C_CLAUDE, "/office-hours", C_WARN),
        ],
        "boxes": [(1, 2, 1), (8, 8, 2), (10, 10, 3)],
        "notes": {
            "en": ["Paste the one-line install from the gstack README into Claude Code — about 1 minute.",
                   "Claude adds a \"gstack\" section to CLAUDE.md so later sessions know the skills exist.",
                   "Smoke test: type /office-hours. If it responds, gstack is live."],
            "zh": ["把 gstack README 中的一行安装命令粘贴进 Claude Code —— 约 1 分钟。",
                   "Claude 会在 CLAUDE.md 中加入 \"gstack\" 段落，让后续会话知道这些技能存在。",
                   "冒烟测试：输入 /office-hours，有回应即表示 gstack 已生效。"],
        },
    },
    "03_hyperframes": {
        "tab": "Windows PowerShell",
        "lines": [
            ("PS D:\\ipason\\claude\\projects> ", C_PROMPT, "claude plugin marketplace add heygen-com/hyperframes", C_TEXT),
            ("✔ Marketplace added: hyperframes", C_OK),
            ("PS D:\\ipason\\claude\\projects> ", C_PROMPT, "claude plugin install hyperframes@hyperframes", C_TEXT),
            ("✔ Plugin installed: hyperframes", C_OK),
            ("PS D:\\ipason\\claude\\projects> ", C_PROMPT, "npx hyperframes init agi-race-v2", C_TEXT),
            ("  Created agi-race-v2/  (index.html, hyperframes.json, package.json ...)", C_DIM),
            ("PS D:\\ipason\\claude\\projects> ", C_PROMPT, "cd agi-race-v2; npx hyperframes doctor", C_TEXT),
            ("  ✔ Node.js   ✔ FFmpeg   ✔ headless browser   ✔ CLI version pinned", C_OK),
        ],
        "boxes": [(0, 3, 1), (4, 5, 2), (6, 7, 3)],
        "notes": {
            "en": ["Two commands install the HyperFrames plugin; restart Claude Code so /hyperframes appears.",
                   "init creates a composition project: plain HTML + data-start / data-duration timing.",
                   "Run doctor BEFORE designing — the Shot Playbook's rule: check the machine first."],
            "zh": ["两条命令安装 HyperFrames 插件；重启 Claude Code 后即可使用 /hyperframes。",
                   "init 生成合成项目：纯 HTML + data-start / data-duration 时间属性。",
                   "设计之前先跑 doctor —— Shot Playbook 的规则：先检查机器能力。"],
        },
    },
    "04_gates": {
        "tab": "Windows PowerShell — agi-race-v2",
        "lines": [
            ("PS D:\\...\\agi-race-v2> ", C_PROMPT, "npx hyperframes lint", C_TEXT),
            ("  0 errors", C_OK),
            ("PS D:\\...\\agi-race-v2> ", C_PROMPT, "npx hyperframes check", C_TEXT),
            ("  contrast 13/13 passed", C_OK),
            ("PS D:\\...\\agi-race-v2> ", C_PROMPT, "npx hyperframes snapshot", C_TEXT),
            ("  contact-sheet.jpg  (frames at 0.4s, 2.2s, 3.7s, 5.25s, 5.75s)", C_DIM),
            ("PS D:\\...\\agi-race-v2> ", C_PROMPT, "npx hyperframes render", C_TEXT),
            ("  rendered → out.mp4", C_OK),
            ("PS D:\\...\\agi-race-v2> ", C_PROMPT, "ffprobe -v error -show_entries stream=codec_name,width,height out.mp4", C_TEXT),
            ("  codec_name=h264 width=1920 height=1080 | codec_name=aac", C_TEXT),
        ],
        "boxes": [(0, 3, 1), (4, 5, 2), (8, 9, 3)],
        "notes": {
            "en": ["Automated gates: lint (0 errors) and check (contrast 13/13) — values from the C24 Hero Pilot v2 QA report.",
                   "snapshot writes a contact sheet. A human must open it — automated gates never replace your eyes.",
                   "Probe the rendered file itself: codec, size, audio. Trust the file, not the preview."],
            "zh": ["自动闸门：lint（0 错误）与 check（对比度 13/13）—— 数值取自 C24 Hero Pilot v2 的 QA 报告。",
                   "snapshot 生成联系表（contact sheet），必须由人亲自打开查看 —— 自动闸门不能替代人眼。",
                   "对渲染出的文件本身做 probe：编码、尺寸、音轨。相信文件，而不是预览。"],
        },
    },
}


def _font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def mock(name, spec, lang):
    W = 1600
    line_h = 30
    pad = 28
    n = len(spec["lines"])
    term_h = 44 + pad * 2 + n * line_h
    notes = spec["notes"][lang]
    note_font = _font(CJK_FILE, 21)
    note_bold = _font(CJK_BOLD, 21)
    # wrap notes
    wrapped = []
    maxw = W - 2 * 40 - 70
    tmp = Image.new("RGB", (10, 10)); d0 = ImageDraw.Draw(tmp)
    for s in notes:
        lines, cur = [], ""
        tokens = list(s) if lang == "zh" else s.split(" ")
        for tok in tokens:
            cand = (cur + tok) if lang == "zh" else ((cur + " " + tok) if cur else tok)
            if d0.textlength(cand, font=note_font) > maxw:
                lines.append(cur); cur = tok
            else:
                cur = cand
        lines.append(cur)
        wrapped.append(lines)
    notes_h = sum(len(l) * 32 + 16 for l in wrapped) + 40
    banner_h = 52
    H = banner_h + 30 + term_h + 30 + notes_h
    img = Image.new("RGB", (W, H), (243, 244, 246))
    d = ImageDraw.Draw(img)
    # banner
    d.rectangle([0, 0, W, banner_h], fill=(192, 57, 43))
    bf = _font(CJK_BOLD, 24)
    d.text((W / 2, banner_h / 2), T[lang]["mock_banner"], font=bf, fill=(255, 255, 255), anchor="mm")
    # window
    x0, y0 = 40, banner_h + 30
    x1, y1 = W - 40, y0 + term_h
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(12, 12, 12), outline=(60, 60, 60))
    d.rounded_rectangle([x0, y0, x1, y0 + 44], radius=10, fill=(32, 32, 32))
    d.rectangle([x0, y0 + 30, x1, y0 + 44], fill=(32, 32, 32))
    tabf = _font(CJK_FILE, 17)
    d.rounded_rectangle([x0 + 12, y0 + 7, x0 + 12 + d.textlength(spec["tab"], font=tabf) + 60, y0 + 44],
                        radius=6, fill=(12, 12, 12))
    d.text((x0 + 30, y0 + 25), spec["tab"], font=tabf, fill=(230, 230, 230), anchor="lm")
    for i, (cx) in enumerate(["—", "□", "✕"]):
        d.text((x1 - 110 + i * 38, y0 + 22), cx, font=tabf, fill=(200, 200, 200), anchor="mm")
    mf = _font(MONO, 20)
    ty = y0 + 44 + pad
    for li, parts in enumerate(spec["lines"]):
        xx = x0 + 24
        for j in range(0, len(parts), 2):
            txt, col = parts[j], parts[j + 1]
            d.text((xx, ty + li * line_h), txt, font=mf, fill=col)
            xx += d.textlength(txt, font=mf)
    # annotation boxes
    circ_f = _font(MONO_B, 20)
    for a, b, num in spec["boxes"]:
        by0 = ty + a * line_h - 5
        by1 = ty + (b + 1) * line_h - 3
        d.rounded_rectangle([x0 + 14, by0, x1 - 70, by1], radius=6, outline=(232, 135, 43), width=3)
        cx, cy = x1 - 42, (by0 + by1) / 2
        d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(232, 135, 43))
        d.text((cx, cy), str(num), font=circ_f, fill=(255, 255, 255), anchor="mm")
    # notes
    ny = y1 + 30
    for k, lines in enumerate(wrapped, start=1):
        cx, cy = 40 + 17, ny + 16
        d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(232, 135, 43))
        d.text((cx, cy), str(k), font=circ_f, fill=(255, 255, 255), anchor="mm")
        for m, ln in enumerate(lines):
            d.text((40 + 50, ny + m * 32), ln, font=note_bold if False else note_font, fill=(27, 31, 42))
        ny += len(lines) * 32 + 16
    img.save(OUT / f"mock_{name}_{lang}.png", optimize=True)


if __name__ == "__main__":
    for lang in ("en", "zh"):
        fig_pipeline(lang)
        fig_timeline(lang)
        fig_rap(lang)
        for name, spec in MOCKS.items():
            mock(name, spec, lang)
    print("\n".join(sorted(p.name for p in OUT.glob("*.png"))))
