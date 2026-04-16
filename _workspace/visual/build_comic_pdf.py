#!/usr/bin/env python3
"""만화 PDF 생성 — 이미지 + 대사/캡션을 합쳐 페이지별로 구성"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import glob

BASE = Path("/Users/robin/Downloads/harness-easy")
IMG_DIR = BASE / "_workspace/visual/images"
OUT_PDF = BASE / "만화_하네스이해.pdf"

# A4 sized pages at 150 DPI
PAGE_W, PAGE_H = 1240, 1754
BG_COLOR = (255, 248, 240)  # #FFF8F0
TEXT_COLOR = (92, 86, 80)
ACCENT_SAGE = (107, 137, 98)
ACCENT_CORAL = (244, 163, 156)
ACCENT_MUSTARD = (242, 201, 76)
GRAY_LINE = (184, 176, 168)

# Font candidates for Korean
FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/NanumGothic.ttc",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def find_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


FONT_TITLE = find_font(56)
FONT_SUB = find_font(32)
FONT_PANEL_TITLE = find_font(38)
FONT_TAG = find_font(24)
FONT_BODY = find_font(28)
FONT_NARRATION = find_font(26)
FONT_LESSON = find_font(22)


EPISODES = [
    {
        "num": 1, "title": "AI 하나에게 다 시키면?",
        "subtitle": "단일 AI의 한계와 분업의 필요성을 깨닫는 첫 걸음",
        "panels": [
            {"id": "EP1-P1", "title": "도입 — Ana의 일상",
             "dialogues": [("Ana", "기획서 검토하고, 수정하고, 보고서도 만들어줘!")],
             "narration": "어느 날, Ana는 AI에게 한꺼번에 부탁했습니다."},
            {"id": "EP1-P2", "title": "결과 — 뒤죽박죽",
             "dialogues": [("Ana", "...이게 뭐야?")],
             "narration": "결과는 뒤죽박죽이었습니다."},
            {"id": "EP1-P3", "title": "비유 전환 — 혼자 요리하는 셰프",
             "dialogues": [],
             "narration": "혼자서 저녁 코스를 다 차리는 셰프를 상상해 보세요."},
            {"id": "EP1-P4", "title": "깨달음 — 그래서 팀이 필요하다",
             "dialogues": [("Ana", "아, AI도 마찬가지구나!")],
             "narration": "AI도 역할을 나누면 훨씬 잘합니다."},
            {"id": "EP1-P5", "title": "마무리 — 다음 화 예고",
             "dialogues": [("Ana", "이 주방 안엔 누가 있을까?")],
             "narration": "[다음 화 예고] 팀 주방의 문을 열어봅니다."},
        ],
    },
    {
        "num": 2, "title": "주방 브리게이드",
        "subtitle": "팀 주방의 문을 열고 에이전트와 오케스트레이터를 만나다",
        "panels": [
            {"id": "EP2-P1", "title": "팀 주방 입장",
             "dialogues": [("Ana", "우와, 각자 다른 일을 하고 있네!")],
             "narration": "여긴 호통치는 독재 주방이 아닙니다."},
            {"id": "EP2-P2", "title": "헤드셰프 소개 — 오케스트레이터",
             "dialogues": [("헤드셰프", "나는 직접 요리 안 해. 누가 뭘 할지 나누는 거지.")],
             "narration": "오케스트레이터 = 조율하는 사람"},
            {"id": "EP2-P3", "title": "셰프들 소개 — 에이전트",
             "dialogues": [("소스 셰프", "난 소스 전문!"),
                           ("디저트 셰프", "난 디저트 담당이에요."),
                           ("플레이터", "담기는 내 몫.")],
             "narration": "에이전트 = 각자 역할을 맡은 AI"},
            {"id": "EP2-P4", "title": "협업 장면 — 코멘트가 오간다",
             "dialogues": [("디저트 셰프", "거기 레몬 한 방울 넣어볼래?"),
                           ("소스 셰프", "오, 좋은 생각!")],
             "narration": "서로 코멘트하며 한 접시를 만들어갑니다."},
            {"id": "EP2-P5", "title": "잠깐, 이건 아니에요! — 오개념 교정",
             "dialogues": [("Ana", "독재 주방이 아니라 팀 주방이에요!")],
             "narration": "오케스트레이터는 명령하는 사람이 아니라 조율하는 사람입니다."},
            {"id": "EP2-P6", "title": "마무리 — 생각해보기",
             "dialogues": [],
             "narration": "[생각해보기] 에이전트와 챗봇, 뭐가 다를까요? 힌트: 역할이 있느냐 없느냐!"},
        ],
    },
    {
        "num": 3, "title": "레시피 카드와 운영 매뉴얼",
        "subtitle": "스킬과 하네스 — 제품이 아닌 우리가 짜는 설계 방식",
        "panels": [
            {"id": "EP3-P1", "title": "레시피 카드 등장 — 스킬",
             "dialogues": [("소스 셰프", "이 카드대로 하면 돼!")],
             "narration": "스킬 = AI 셰프가 꺼내보는 레시피 카드"},
            {"id": "EP3-P2", "title": "여러 장의 레시피 카드",
             "dialogues": [("헤드셰프", "각자 맡은 레시피가 따로 있어.")],
             "narration": "셰프마다 다른 레시피 카드를 갖고 있습니다."},
            {"id": "EP3-P3", "title": "줌아웃 — 운영 매뉴얼(하네스)",
             "dialogues": [("Ana", "아, 이 전체 구조가 하네스구나!")],
             "narration": "하네스 = AI 팀의 운영 매뉴얼. 제품이 아니라, 우리가 짜는 설계 방식."},
            {"id": "EP3-P4", "title": "잠깐, 이건 아니에요! — 오개념 교정",
             "dialogues": [("Ana", "사러 가는 게 아니라 직접 짜는 거예요!")],
             "narration": "하네스는 앱이 아닙니다. 우리가 설계하는 방식이에요."},
            {"id": "EP3-P5", "title": "마무리 — 다음 화 예고",
             "dialogues": [("Ana", "영업이 끝나면 이 셰프들은 어떻게 되지?")],
             "narration": "[다음 화 예고] 기억을 잃는 셰프들의 비밀."},
        ],
    },
    {
        "num": 4, "title": "기억을 잃는 셰프",
        "subtitle": "컨텍스트 윈도우와 메모리 — AI는 사람과 다르다",
        "panels": [
            {"id": "EP4-P1", "title": "영업 후 — 텅 빈 주방",
             "dialogues": [("소스 셰프", "오늘 배운 거, 적어놔야지...")],
             "narration": "영업이 끝나면 셰프들은 오늘을 잊습니다."},
            {"id": "EP4-P2", "title": "다음 날 아침 — 새 셰프?",
             "dialogues": [("소스 셰프", "어...여기가 어디지?"),
                           ("헤드셰프", "어제 네가 쓴 노트, 여기 있어.")],
             "narration": "다음 날의 셰프는 어제를 모릅니다."},
            {"id": "EP4-P3", "title": "조리대 공간 — 컨텍스트 윈도우",
             "dialogues": [("소스 셰프", "조리대가 아무리 넓어도 한계가 있어.")],
             "narration": "컨텍스트 윈도우 = 셰프가 한 번에 볼 수 있는 조리대"},
            {"id": "EP4-P4", "title": "잠깐, 이건 아니에요! — 오개념 교정",
             "dialogues": [("Ana", "조리대가 넓어도 매일 치운다고요?")],
             "narration": "컨텍스트가 커져도 세션이 끝나면 리셋됩니다."},
            {"id": "EP4-P5", "title": "마무리 — 생각해보기",
             "dialogues": [("Ana", "그래서 노트가 중요하구나.")],
             "narration": "[생각해보기] AI의 기억은 사람과 어떻게 다를까요? 힌트: 매일 첫 출근!"},
        ],
    },
    {
        "num": 5, "title": "우리 일상의 하네스",
        "subtitle": "김장 · 이사 · 소풍 — 우리가 이미 살고 있는 하네스적 순간",
        "panels": [
            {"id": "EP5-P1", "title": "김장 — 역할 분담",
             "dialogues": [],
             "narration": "김장할 때 역할을 나누듯이..."},
            {"id": "EP5-P2", "title": "이사 — 누가 뭘 할지",
             "dialogues": [("체크리스트 든 사람", "거실 먼저, 그 다음 주방!")],
             "narration": "이사할 때 계획을 짜듯이..."},
            {"id": "EP5-P3", "title": "소풍 — 각자의 준비물",
             "dialogues": [],
             "narration": "소풍 준비도 역할을 나누면 훨씬 잘됩니다."},
            {"id": "EP5-P4", "title": "Ana의 전이 — 나도 하네스적이었어!",
             "dialogues": [("Ana", "우리 팀 분기 기획도 이거였어!")],
             "narration": "하네스는 특별한 기술이 아닙니다. 역할을 나누고 함께 일하는 방식이에요."},
            {"id": "EP5-P5", "title": "마무리 — 시리즈 종합",
             "dialogues": [("Ana", "이제 하네스가 뭔지 알겠죠?")],
             "narration": "하네스는 AI 팀의 운영 매뉴얼. 제품이 아니라 우리가 짜는 설계 방식입니다. 이해만으로도 충분해요."},
        ],
    },
]


def wrap_text(draw, text, font, max_w):
    """간단한 wrapping (한글 포함)"""
    if not text:
        return [""]
    lines = []
    cur = ""
    for ch in text:
        test = cur + ch
        w = draw.textlength(test, font=font)
        if w > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def make_cover_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)
    # Border
    d.rectangle([40, 40, PAGE_W - 40, PAGE_H - 40], outline=GRAY_LINE, width=3)
    d.rectangle([60, 60, PAGE_W - 60, PAGE_H - 60], outline=GRAY_LINE, width=1)
    # Title
    title = "만화로 이해하는"
    d.text((PAGE_W / 2, 220), title, font=FONT_TITLE, fill=TEXT_COLOR, anchor="mm")
    big_title = "하네스"
    big_font = find_font(140)
    d.text((PAGE_W / 2, 360), big_title, font=big_font, fill=ACCENT_MUSTARD, anchor="mm")
    # Mustard underline
    d.rectangle([PAGE_W / 2 - 200, 415, PAGE_W / 2 + 200, 435], fill=ACCENT_MUSTARD)

    sub = "— 일반인을 위한 AI 팀 운영 매뉴얼 입문 —"
    d.text((PAGE_W / 2, 520), sub, font=FONT_SUB, fill=TEXT_COLOR, anchor="mm")

    # Description box
    desc_lines = [
        "AI는 한 대 쓰는 시대에서 팀으로 엮는 시대로 바뀌고 있습니다.",
        "하지만 우리 대부분의 머릿속은 아직 챗봇 한 대에 멈춰 있어요.",
        "",
        "주방 브리게이드 비유로 '하네스'라는 낯선 개념을",
        "자연스럽게 이해할 수 있도록 준비한 입문용 시리즈입니다.",
    ]
    y = 700
    for line in desc_lines:
        d.text((PAGE_W / 2, y), line, font=FONT_NARRATION, fill=TEXT_COLOR, anchor="mm")
        y += 50

    # Episode list
    y = 1050
    d.text((PAGE_W / 2, y), "- 에피소드 목차 -", font=FONT_PANEL_TITLE, fill=ACCENT_SAGE, anchor="mm")
    y += 80
    for ep in EPISODES:
        ep_line = f"EP{ep['num']}.  {ep['title']}"
        d.text((PAGE_W / 2, y), ep_line, font=FONT_NARRATION, fill=TEXT_COLOR, anchor="mm")
        y += 60

    # Footer
    d.text((PAGE_W / 2, PAGE_H - 140), "5개 에피소드 · 26개 패널", font=FONT_TAG, fill=GRAY_LINE, anchor="mm")
    d.text((PAGE_W / 2, PAGE_H - 100), "손그림 doodle · 크림색 종이 · 파스텔 팔레트", font=FONT_TAG, fill=GRAY_LINE, anchor="mm")
    d.text((PAGE_W / 2, PAGE_H - 60), "2026-04-16 · 황민호(revfactory@gmail.com)", font=FONT_TAG, fill=GRAY_LINE, anchor="mm")
    return img


def make_episode_cover(ep):
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)
    # Big episode number
    big_font = find_font(280)
    d.text((PAGE_W / 2, 500), f"EP{ep['num']}", font=big_font, fill=ACCENT_MUSTARD, anchor="mm")
    # Title
    title_lines = wrap_text(d, ep['title'], FONT_TITLE, PAGE_W - 200)
    y = 800
    for line in title_lines:
        d.text((PAGE_W / 2, y), line, font=FONT_TITLE, fill=TEXT_COLOR, anchor="mm")
        y += 80

    # Subtitle
    sub_lines = wrap_text(d, ep['subtitle'], FONT_SUB, PAGE_W - 200)
    y += 40
    for line in sub_lines:
        d.text((PAGE_W / 2, y), line, font=FONT_SUB, fill=GRAY_LINE, anchor="mm")
        y += 50

    # Panel count
    d.text((PAGE_W / 2, PAGE_H - 200), f"{len(ep['panels'])}개 패널", font=FONT_TAG, fill=GRAY_LINE, anchor="mm")
    return img


def make_panel_page(ep, panel):
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Top bar: EP number + panel tag
    d.rectangle([80, 80, 300, 130], fill=ACCENT_CORAL)
    d.text((190, 105), panel['id'], font=FONT_TAG, fill=(255, 255, 255), anchor="mm")
    d.text((PAGE_W - 90, 105), f"EP{ep['num']}", font=FONT_TAG, fill=GRAY_LINE, anchor="rm")

    # Panel title
    y = 180
    title_lines = wrap_text(d, panel['title'], FONT_PANEL_TITLE, PAGE_W - 160)
    for line in title_lines:
        d.text((80, y), line, font=FONT_PANEL_TITLE, fill=TEXT_COLOR)
        y += 55

    # Panel image
    parts = panel['id'].lower().split("-")
    img_path = IMG_DIR / f"comic_{parts[0]}_{parts[1]}.png"
    if img_path.exists():
        panel_img = Image.open(img_path)
        img_w = PAGE_W - 160
        ratio = panel_img.height / panel_img.width
        img_h = int(img_w * ratio)
        # Cap image height
        max_img_h = 900
        if img_h > max_img_h:
            img_h = max_img_h
            img_w = int(img_h / ratio)
        panel_img = panel_img.resize((img_w, img_h), Image.LANCZOS)
        img_x = (PAGE_W - img_w) // 2
        img.paste(panel_img, (img_x, y + 20))
        # Border
        d.rectangle([img_x - 2, y + 18, img_x + img_w + 2, y + 20 + img_h + 2],
                    outline=GRAY_LINE, width=2)
        y += img_h + 50

    # Dialogues
    for who, text in panel.get('dialogues', []):
        d.rectangle([80, y, 90, y + 80], fill=ACCENT_CORAL)
        d.text((110, y + 5), f"{who}:", font=FONT_BODY, fill=ACCENT_SAGE)
        who_width = d.textlength(f"{who}:", font=FONT_BODY)
        text_lines = wrap_text(d, text, FONT_BODY, PAGE_W - 160 - who_width - 30)
        text_y = y + 5
        first = True
        for line in text_lines:
            if first:
                d.text((110 + who_width + 10, text_y), line, font=FONT_BODY, fill=TEXT_COLOR)
                first = False
            else:
                d.text((110, text_y), line, font=FONT_BODY, fill=TEXT_COLOR)
            text_y += 40
        y = max(y + 80, text_y + 20)

    # Narration
    y += 20
    narration_w = PAGE_W - 160
    narration_lines = wrap_text(d, panel['narration'], FONT_NARRATION, narration_w - 30)
    narration_h = len(narration_lines) * 42 + 30
    d.rectangle([80, y, PAGE_W - 80, y + narration_h], fill=(255, 253, 247), outline=ACCENT_SAGE, width=2)
    d.rectangle([80, y, 90, y + narration_h], fill=ACCENT_SAGE)
    text_y = y + 15
    for line in narration_lines:
        d.text((110, text_y), line, font=FONT_NARRATION, fill=TEXT_COLOR)
        text_y += 42

    # Footer page marker
    d.text((PAGE_W / 2, PAGE_H - 50), f"만화로 이해하는 하네스 · EP{ep['num']} · {panel['id']}",
           font=FONT_LESSON, fill=GRAY_LINE, anchor="mm")
    return img


def main():
    pages = []
    # Cover
    pages.append(make_cover_page())
    # For each episode, add episode cover + panels
    for ep in EPISODES:
        pages.append(make_episode_cover(ep))
        for panel in ep['panels']:
            pages.append(make_panel_page(ep, panel))

    # Save
    pages[0].save(
        OUT_PDF,
        save_all=True,
        append_images=pages[1:],
        resolution=150.0,
    )
    print(f"Saved {OUT_PDF} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
