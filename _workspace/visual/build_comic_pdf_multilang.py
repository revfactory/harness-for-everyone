#!/usr/bin/env python3
"""만화 PDF 다국어 버전 빌드 (KO/EN/JP)

이미지 자체는 공통(영어 말풍선이 섞여 있음). PDF 텍스트 오버레이(타이틀/대사/나레이션)를
언어별로 번역 교체해 3개 PDF를 생성한다.

Usage:
    python3 build_comic_pdf_multilang.py ko
    python3 build_comic_pdf_multilang.py en
    python3 build_comic_pdf_multilang.py ja
    python3 build_comic_pdf_multilang.py all   # 세 언어 모두
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path("/Users/robin/Downloads/harness-easy")
IMG_DIR = BASE / "_workspace/visual/images"

# A4 sized pages at 150 DPI
PAGE_W, PAGE_H = 1240, 1754
BG_COLOR = (255, 248, 240)  # #FFF8F0
TEXT_COLOR = (92, 86, 80)
ACCENT_SAGE = (107, 137, 98)
ACCENT_CORAL = (244, 163, 156)
ACCENT_MUSTARD = (242, 201, 76)
GRAY_LINE = (184, 176, 168)

# 언어별 폰트 후보 (첫 존재 파일 사용)
FONT_CANDIDATES = {
    "ko": [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/Library/Fonts/NanumGothic.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    ],
    "en": [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "ja": [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    ],
}


def find_font(lang, size):
    for path in FONT_CANDIDATES.get(lang, []):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # Fallback to any Korean font (Apple SD Gothic covers KO/JP partial)
    for path in FONT_CANDIDATES["ko"]:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# =====================================================================
# 번역 데이터
# =====================================================================

TRANSLATIONS = {
    "ko": {
        "cover_hook": "만화로 이해하는",
        "cover_title": "하네스",
        "cover_subtitle": "— 일반인을 위한 AI 팀 운영 매뉴얼 입문 —",
        "cover_desc": [
            "AI는 한 대 쓰는 시대에서 팀으로 엮는 시대로 바뀌고 있습니다.",
            "하지만 우리 대부분의 머릿속은 아직 챗봇 한 대에 멈춰 있어요.",
            "",
            "주방 브리게이드 비유로 '하네스'라는 낯선 개념을",
            "자연스럽게 이해할 수 있도록 준비한 입문용 시리즈입니다.",
        ],
        "toc_title": "- 에피소드 목차 -",
        "cover_foot1": "5개 에피소드 · 26개 패널",
        "cover_foot2": "손그림 doodle · 크림색 종이 · 파스텔 팔레트",
        "cover_foot3": "2026-04-16 · 황민호(revfactory@gmail.com)",
        "ep_panels_suffix": "개 패널",
        "page_footer_fmt": "만화로 이해하는 하네스 · EP{ep} · {pid}",
    },
    "en": {
        "cover_hook": "Understanding Through Comics",
        "cover_title": "Harness",
        "cover_subtitle": "— A Beginner's Guide to the AI Team Operating Manual —",
        "cover_desc": [
            "AI is shifting from 'using one' to 'weaving a team.'",
            "But most of us still picture AI as just one chatbot.",
            "",
            "Using the Kitchen Brigade metaphor, this introductory series",
            "helps you naturally grasp the unfamiliar concept of 'Harness.'",
        ],
        "toc_title": "- Episode Index -",
        "cover_foot1": "5 Episodes · 26 Panels",
        "cover_foot2": "Hand-drawn doodle · Cream paper · Pastel palette",
        "cover_foot3": "2026-04-16 · Minho Hwang (revfactory@gmail.com)",
        "ep_panels_suffix": " Panels",
        "page_footer_fmt": "Understanding Harness Through Comics · EP{ep} · {pid}",
    },
    "ja": {
        "cover_hook": "マンガで理解する",
        "cover_title": "ハーネス",
        "cover_subtitle": "— みんなのためのAIチーム運営マニュアル入門 —",
        "cover_desc": [
            "AIは「1台使う時代」から「チームで紡ぐ時代」へ変わりつつあります。",
            "でも私たちの頭の中は、まだチャットボット1台に止まっています。",
            "",
            "キッチンブリゲードの比喩で「ハーネス」という",
            "馴染みのない概念を自然に理解できる入門シリーズです。",
        ],
        "toc_title": "— エピソード目次 —",
        "cover_foot1": "5エピソード · 26パネル",
        "cover_foot2": "手描きdoodle · クリーム紙 · パステルパレット",
        "cover_foot3": "2026-04-16 · ファン・ミンホ (revfactory@gmail.com)",
        "ep_panels_suffix": "パネル",
        "page_footer_fmt": "マンガで理解するハーネス · EP{ep} · {pid}",
    },
}


# =====================================================================
# 에피소드 데이터 (언어별)
# =====================================================================

EPISODES_KO = [
    {"num": 1, "title": "AI 하나에게 다 시키면?",
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
    ]},
    {"num": 2, "title": "주방 브리게이드",
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
    ]},
    {"num": 3, "title": "레시피 카드와 운영 매뉴얼",
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
    ]},
    {"num": 4, "title": "기억을 잃는 셰프",
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
    ]},
    {"num": 5, "title": "우리 일상의 하네스",
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
    ]},
]

EPISODES_EN = [
    {"num": 1, "title": "What if you give one AI everything?",
     "subtitle": "A first step: realizing the limits of a single AI and the need for teamwork",
     "panels": [
        {"id": "EP1-P1", "title": "Intro — Ana's Day",
         "dialogues": [("Ana", "Review the proposal, revise it, and make a report too!")],
         "narration": "One day, Ana asked the AI to do it all at once."},
        {"id": "EP1-P2", "title": "Result — A Jumbled Mess",
         "dialogues": [("Ana", "...What is this?")],
         "narration": "The result was a jumbled mess."},
        {"id": "EP1-P3", "title": "Metaphor — A Chef Cooking Alone",
         "dialogues": [],
         "narration": "Imagine a chef preparing the entire dinner course alone."},
        {"id": "EP1-P4", "title": "Realization — That's Why We Need a Team",
         "dialogues": [("Ana", "Oh, the same goes for AI!")],
         "narration": "AI performs much better when roles are divided."},
        {"id": "EP1-P5", "title": "Wrap-up — Next Episode Preview",
         "dialogues": [("Ana", "Who's inside this kitchen?")],
         "narration": "[Next Episode] Opening the door to the team kitchen."},
    ]},
    {"num": 2, "title": "The Kitchen Brigade",
     "subtitle": "Open the door to the team kitchen — meet Agents and the Orchestrator",
     "panels": [
        {"id": "EP2-P1", "title": "Entering the Team Kitchen",
         "dialogues": [("Ana", "Wow, they each do different things!")],
         "narration": "This isn't a dictatorial kitchen with shouting."},
        {"id": "EP2-P2", "title": "Meet the Head Chef — The Orchestrator",
         "dialogues": [("Head Chef", "I don't cook directly. I assign who does what.")],
         "narration": "Orchestrator = the coordinator"},
        {"id": "EP2-P3", "title": "Meet the Chefs — Agents",
         "dialogues": [("Sauce Chef", "Sauces are my specialty!"),
                       ("Pastry Chef", "I'm in charge of desserts."),
                       ("Plater", "Plating is on me.")],
         "narration": "Agent = an AI with a specific role"},
        {"id": "EP2-P4", "title": "Collaboration — Comments Flow Back and Forth",
         "dialogues": [("Pastry Chef", "How about a drop of lemon there?"),
                       ("Sauce Chef", "Oh, good idea!")],
         "narration": "They build one dish together through mutual feedback."},
        {"id": "EP2-P5", "title": "Hold on! — Misconception Correction",
         "dialogues": [("Ana", "It's a team kitchen, not a dictatorial one!")],
         "narration": "The Orchestrator isn't a commander — they're a coordinator."},
        {"id": "EP2-P6", "title": "Wrap-up — Think About It",
         "dialogues": [],
         "narration": "[Think about it] What's the difference between Agent and Chatbot? Hint: Having a role or not!"},
    ]},
    {"num": 3, "title": "Recipe Cards and the Operating Manual",
     "subtitle": "Skills and Harness — not a product, but a design we craft",
     "panels": [
        {"id": "EP3-P1", "title": "Enter the Recipe Card — Skill",
         "dialogues": [("Sauce Chef", "Just follow this card!")],
         "narration": "Skill = the recipe card an AI chef pulls out"},
        {"id": "EP3-P2", "title": "Multiple Recipe Cards",
         "dialogues": [("Head Chef", "Each chef has their own recipes.")],
         "narration": "Each chef has different recipe cards."},
        {"id": "EP3-P3", "title": "Zoom Out — The Operating Manual (Harness)",
         "dialogues": [("Ana", "Oh, this whole structure is the Harness!")],
         "narration": "Harness = the AI team's operating manual. Not a product, but a design we craft."},
        {"id": "EP3-P4", "title": "Hold on! — Misconception Correction",
         "dialogues": [("Ana", "You don't buy it — you design it yourself!")],
         "narration": "Harness isn't an app. It's a way we design."},
        {"id": "EP3-P5", "title": "Wrap-up — Next Episode Preview",
         "dialogues": [("Ana", "What happens to these chefs after service ends?")],
         "narration": "[Next Episode] The secret of chefs who lose their memory."},
    ]},
    {"num": 4, "title": "The Chef Who Loses Memory",
     "subtitle": "Context Window and Memory — AI is different from humans",
     "panels": [
        {"id": "EP4-P1", "title": "After Service — The Empty Kitchen",
         "dialogues": [("Sauce Chef", "Better write down what I learned today...")],
         "narration": "When service ends, the chefs forget today."},
        {"id": "EP4-P2", "title": "Next Morning — A New Chef?",
         "dialogues": [("Sauce Chef", "Huh... where am I?"),
                       ("Head Chef", "Here's the note you wrote yesterday.")],
         "narration": "The next day's chef doesn't remember yesterday."},
        {"id": "EP4-P3", "title": "The Workbench — Context Window",
         "dialogues": [("Sauce Chef", "No matter how wide the counter, there's a limit.")],
         "narration": "Context Window = the workbench a chef can see at once"},
        {"id": "EP4-P4", "title": "Hold on! — Misconception Correction",
         "dialogues": [("Ana", "You wipe the counter every day even if it's wide?")],
         "narration": "Even a larger context resets when the session ends."},
        {"id": "EP4-P5", "title": "Wrap-up — Think About It",
         "dialogues": [("Ana", "So that's why the notes matter.")],
         "narration": "[Think about it] How does AI memory differ from ours? Hint: Every day is a first day at work!"},
    ]},
    {"num": 5, "title": "Harness in Our Daily Lives",
     "subtitle": "Kimjang · Moving · Picnic — Harness moments we already live",
     "panels": [
        {"id": "EP5-P1", "title": "Kimjang — Dividing Roles",
         "dialogues": [],
         "narration": "Like how we split roles during kimjang (kimchi-making)..."},
        {"id": "EP5-P2", "title": "Moving — Who Does What",
         "dialogues": [("Person with checklist", "Living room first, then the kitchen!")],
         "narration": "Like planning a move..."},
        {"id": "EP5-P3", "title": "Picnic — Each Person's Items",
         "dialogues": [],
         "narration": "Picnic prep also goes much smoother when roles are divided."},
        {"id": "EP5-P4", "title": "Ana's Transfer — I've Already Been Doing Harness!",
         "dialogues": [("Ana", "Our team's quarterly planning was this too!")],
         "narration": "Harness isn't a special technology. It's a way of dividing roles and working together."},
        {"id": "EP5-P5", "title": "Wrap-up — Series Summary",
         "dialogues": [("Ana", "Now you know what Harness is, right?")],
         "narration": "Harness is the AI team's operating manual. Not a product, but a design we craft. Understanding is enough."},
    ]},
]

EPISODES_JA = [
    {"num": 1, "title": "AI 1台に全部任せたら？",
     "subtitle": "単一AIの限界と分業の必要性に気づく第一歩",
     "panels": [
        {"id": "EP1-P1", "title": "導入 — Anaの日常",
         "dialogues": [("Ana", "企画書をチェックして、修正して、レポートも作って！")],
         "narration": "ある日、AnaはAIに一度にお願いしました。"},
        {"id": "EP1-P2", "title": "結果 — ごちゃごちゃ",
         "dialogues": [("Ana", "…これ何？")],
         "narration": "結果はごちゃごちゃでした。"},
        {"id": "EP1-P3", "title": "比喩への転換 — 一人で料理するシェフ",
         "dialogues": [],
         "narration": "一人でディナーコースを全部用意するシェフを想像してみてください。"},
        {"id": "EP1-P4", "title": "気づき — だからチームが必要",
         "dialogues": [("Ana", "あ、AIも同じなんだ！")],
         "narration": "AIも役割を分けると、ずっと上手にやります。"},
        {"id": "EP1-P5", "title": "しめくくり — 次回予告",
         "dialogues": [("Ana", "このキッチンには誰がいるのかな？")],
         "narration": "[次回予告] チームキッチンの扉を開けてみます。"},
    ]},
    {"num": 2, "title": "キッチンブリゲード",
     "subtitle": "チームキッチンの扉を開け、エージェントとオーケストレーターに出会う",
     "panels": [
        {"id": "EP2-P1", "title": "チームキッチン入場",
         "dialogues": [("Ana", "わぁ、みんな違うことをしてる！")],
         "narration": "ここは怒鳴りつける独裁キッチンではありません。"},
        {"id": "EP2-P2", "title": "ヘッドシェフ紹介 — オーケストレーター",
         "dialogues": [("ヘッドシェフ", "私は直接料理しないの。誰が何をするかを振り分けるのよ。")],
         "narration": "オーケストレーター = 調整する人"},
        {"id": "EP2-P3", "title": "シェフたち紹介 — エージェント",
         "dialogues": [("ソースシェフ", "僕はソース担当！"),
                       ("デザートシェフ", "私はデザート担当です。"),
                       ("プレーター", "盛り付けは私に任せて。")],
         "narration": "エージェント = それぞれ役割を持ったAI"},
        {"id": "EP2-P4", "title": "コラボレーション — コメントが行き交う",
         "dialogues": [("デザートシェフ", "そこにレモンひと滴入れてみる？"),
                       ("ソースシェフ", "おっ、いい考え！")],
         "narration": "互いにコメントを交わしながら、一皿を作っていきます。"},
        {"id": "EP2-P5", "title": "ちょっと待って — 誤解の修正",
         "dialogues": [("Ana", "独裁キッチンではなく、チームキッチンですよ！")],
         "narration": "オーケストレーターは命令する人ではなく、調整する人です。"},
        {"id": "EP2-P6", "title": "しめくくり — 考えてみよう",
         "dialogues": [],
         "narration": "[考えてみよう] エージェントとチャットボット、何が違う？ ヒント：役割があるかないか！"},
    ]},
    {"num": 3, "title": "レシピカードと運営マニュアル",
     "subtitle": "スキルとハーネス — 製品ではなく、私たちが作る設計",
     "panels": [
        {"id": "EP3-P1", "title": "レシピカード登場 — スキル",
         "dialogues": [("ソースシェフ", "このカード通りにやればOK！")],
         "narration": "スキル = AIシェフが取り出すレシピカード"},
        {"id": "EP3-P2", "title": "複数のレシピカード",
         "dialogues": [("ヘッドシェフ", "それぞれ担当のレシピがあるわ。")],
         "narration": "シェフごとに違うレシピカードを持っています。"},
        {"id": "EP3-P3", "title": "ズームアウト — 運営マニュアル(ハーネス)",
         "dialogues": [("Ana", "あ、この全体の構造がハーネスなんだ！")],
         "narration": "ハーネス = AIチームの運営マニュアル。製品ではなく、私たちが作る設計。"},
        {"id": "EP3-P4", "title": "ちょっと待って — 誤解の修正",
         "dialogues": [("Ana", "買いに行くのではなく、自分で作るんです！")],
         "narration": "ハーネスはアプリではありません。私たちが設計する方法です。"},
        {"id": "EP3-P5", "title": "しめくくり — 次回予告",
         "dialogues": [("Ana", "営業が終わったらこのシェフたちはどうなるんだろう？")],
         "narration": "[次回予告] 記憶を失うシェフたちの秘密。"},
    ]},
    {"num": 4, "title": "記憶を失うシェフ",
     "subtitle": "コンテキストウィンドウとメモリ — AIは人間と違う",
     "panels": [
        {"id": "EP4-P1", "title": "営業後 — 空っぽのキッチン",
         "dialogues": [("ソースシェフ", "今日学んだこと、書き留めておかないと…")],
         "narration": "営業が終わると、シェフたちは今日を忘れます。"},
        {"id": "EP4-P2", "title": "翌朝 — 新しいシェフ？",
         "dialogues": [("ソースシェフ", "え…ここはどこ？"),
                       ("ヘッドシェフ", "昨日あなたが書いたノート、ここにあるわ。")],
         "narration": "翌日のシェフは昨日を知りません。"},
        {"id": "EP4-P3", "title": "調理台のスペース — コンテキストウィンドウ",
         "dialogues": [("ソースシェフ", "調理台がどんなに広くても限界があるよ。")],
         "narration": "コンテキストウィンドウ = シェフが一度に見られる調理台"},
        {"id": "EP4-P4", "title": "ちょっと待って — 誤解の修正",
         "dialogues": [("Ana", "調理台が広くても毎日片付けるんですか？")],
         "narration": "コンテキストが大きくなっても、セッションが終わればリセットされます。"},
        {"id": "EP4-P5", "title": "しめくくり — 考えてみよう",
         "dialogues": [("Ana", "だからノートが大事なんだ。")],
         "narration": "[考えてみよう] AIの記憶は人とどう違う？ ヒント：毎日が初出勤！"},
    ]},
    {"num": 5, "title": "私たちの日常のハーネス",
     "subtitle": "キムジャン · 引っ越し · ピクニック — すでに生きているハーネス的瞬間",
     "panels": [
        {"id": "EP5-P1", "title": "キムジャン — 役割分担",
         "dialogues": [],
         "narration": "キムジャン(キムチ漬け)で役割を分けるように…"},
        {"id": "EP5-P2", "title": "引っ越し — 誰が何をするか",
         "dialogues": [("チェックリストを持つ人", "リビングから、次にキッチン！")],
         "narration": "引っ越しの計画を立てるように…"},
        {"id": "EP5-P3", "title": "ピクニック — それぞれの持ち物",
         "dialogues": [],
         "narration": "ピクニックの準備も、役割を分けるとずっとうまくいきます。"},
        {"id": "EP5-P4", "title": "Anaの気づき — 私もハーネス的だった！",
         "dialogues": [("Ana", "うちのチームの四半期計画もこれだった！")],
         "narration": "ハーネスは特別な技術ではありません。役割を分けて一緒に働く方法です。"},
        {"id": "EP5-P5", "title": "しめくくり — シリーズまとめ",
         "dialogues": [("Ana", "これでハーネスが何か分かりましたね？")],
         "narration": "ハーネスはAIチームの運営マニュアル。製品ではなく、私たちが作る設計です。理解するだけで十分。"},
    ]},
]

EPISODES_BY_LANG = {"ko": EPISODES_KO, "en": EPISODES_EN, "ja": EPISODES_JA}


# =====================================================================
# 렌더링 (언어 인자 받음)
# =====================================================================

def wrap_text(draw, text, font, max_w):
    if not text:
        return [""]
    # Word-based wrap for English (spaces), char-based for KO/JA
    if ' ' in text and all(ord(c) < 128 for c in text.replace(' ', '').replace("'", '')[:20]):
        # Looks like English — wrap by words
        lines = []
        words = text.split(' ')
        cur = ""
        for w in words:
            test = (cur + ' ' + w).strip()
            if draw.textlength(test, font=font) > max_w and cur:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
        return lines
    # Character-based for KO/JA
    lines = []
    cur = ""
    for ch in text:
        test = cur + ch
        if draw.textlength(test, font=font) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def make_cover_page(lang, fonts, episodes, t):
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, PAGE_W - 40, PAGE_H - 40], outline=GRAY_LINE, width=3)
    d.rectangle([60, 60, PAGE_W - 60, PAGE_H - 60], outline=GRAY_LINE, width=1)
    # Hook
    d.text((PAGE_W / 2, 220), t["cover_hook"], font=fonts["title"], fill=TEXT_COLOR, anchor="mm")
    # Big title
    big_font = find_font(lang, 140)
    d.text((PAGE_W / 2, 360), t["cover_title"], font=big_font, fill=ACCENT_MUSTARD, anchor="mm")
    # Mustard underline — width based on title length
    title_w = d.textlength(t["cover_title"], font=big_font)
    underline_half = max(200, int(title_w / 2) + 40)
    d.rectangle([PAGE_W / 2 - underline_half, 425, PAGE_W / 2 + underline_half, 445], fill=ACCENT_MUSTARD)

    d.text((PAGE_W / 2, 540), t["cover_subtitle"], font=fonts["sub"], fill=TEXT_COLOR, anchor="mm")

    y = 700
    for line in t["cover_desc"]:
        d.text((PAGE_W / 2, y), line, font=fonts["narration"], fill=TEXT_COLOR, anchor="mm")
        y += 50

    y = 1050
    d.text((PAGE_W / 2, y), t["toc_title"], font=fonts["panel_title"], fill=ACCENT_SAGE, anchor="mm")
    y += 80
    for ep in episodes:
        ep_line = f"EP{ep['num']}.  {ep['title']}"
        d.text((PAGE_W / 2, y), ep_line, font=fonts["narration"], fill=TEXT_COLOR, anchor="mm")
        y += 60

    d.text((PAGE_W / 2, PAGE_H - 140), t["cover_foot1"], font=fonts["tag"], fill=GRAY_LINE, anchor="mm")
    d.text((PAGE_W / 2, PAGE_H - 100), t["cover_foot2"], font=fonts["tag"], fill=GRAY_LINE, anchor="mm")
    d.text((PAGE_W / 2, PAGE_H - 60), t["cover_foot3"], font=fonts["tag"], fill=GRAY_LINE, anchor="mm")
    return img


def make_episode_cover(ep, lang, fonts, t):
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)
    big_font = find_font(lang, 280)
    d.text((PAGE_W / 2, 500), f"EP{ep['num']}", font=big_font, fill=ACCENT_MUSTARD, anchor="mm")

    title_lines = wrap_text(d, ep['title'], fonts["title"], PAGE_W - 200)
    y = 800
    for line in title_lines:
        d.text((PAGE_W / 2, y), line, font=fonts["title"], fill=TEXT_COLOR, anchor="mm")
        y += 80

    sub_lines = wrap_text(d, ep['subtitle'], fonts["sub"], PAGE_W - 200)
    y += 40
    for line in sub_lines:
        d.text((PAGE_W / 2, y), line, font=fonts["sub"], fill=GRAY_LINE, anchor="mm")
        y += 50

    d.text((PAGE_W / 2, PAGE_H - 200),
           f"{len(ep['panels'])}{t['ep_panels_suffix']}",
           font=fonts["tag"], fill=GRAY_LINE, anchor="mm")
    return img


def make_panel_page(ep, panel, lang, fonts, t):
    img = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)
    d = ImageDraw.Draw(img)

    d.rectangle([80, 80, 300, 130], fill=ACCENT_CORAL)
    d.text((190, 105), panel['id'], font=fonts["tag"], fill=(255, 255, 255), anchor="mm")
    d.text((PAGE_W - 90, 105), f"EP{ep['num']}", font=fonts["tag"], fill=GRAY_LINE, anchor="rm")

    y = 180
    title_lines = wrap_text(d, panel['title'], fonts["panel_title"], PAGE_W - 160)
    for line in title_lines:
        d.text((80, y), line, font=fonts["panel_title"], fill=TEXT_COLOR)
        y += 55

    # Panel image (shared across languages)
    parts = panel['id'].lower().split("-")
    img_path = IMG_DIR / f"comic_{parts[0]}_{parts[1]}.png"
    if img_path.exists():
        panel_img = Image.open(img_path)
        img_w = PAGE_W - 160
        ratio = panel_img.height / panel_img.width
        img_h = int(img_w * ratio)
        max_img_h = 900
        if img_h > max_img_h:
            img_h = max_img_h
            img_w = int(img_h / ratio)
        panel_img = panel_img.resize((img_w, img_h), Image.LANCZOS)
        img_x = (PAGE_W - img_w) // 2
        img.paste(panel_img, (img_x, y + 20))
        d.rectangle([img_x - 2, y + 18, img_x + img_w + 2, y + 20 + img_h + 2],
                    outline=GRAY_LINE, width=2)
        y += img_h + 50

    # Dialogues
    for who, text in panel.get('dialogues', []):
        d.rectangle([80, y, 90, y + 80], fill=ACCENT_CORAL)
        d.text((110, y + 5), f"{who}:", font=fonts["body"], fill=ACCENT_SAGE)
        who_width = d.textlength(f"{who}:", font=fonts["body"])
        text_lines = wrap_text(d, text, fonts["body"], PAGE_W - 160 - who_width - 30)
        text_y = y + 5
        first = True
        for line in text_lines:
            if first:
                d.text((110 + who_width + 10, text_y), line, font=fonts["body"], fill=TEXT_COLOR)
                first = False
            else:
                d.text((110, text_y), line, font=fonts["body"], fill=TEXT_COLOR)
            text_y += 40
        y = max(y + 80, text_y + 20)

    # Narration
    y += 20
    narration_lines = wrap_text(d, panel['narration'], fonts["narration"], PAGE_W - 160 - 30)
    narration_h = len(narration_lines) * 42 + 30
    d.rectangle([80, y, PAGE_W - 80, y + narration_h], fill=(255, 253, 247), outline=ACCENT_SAGE, width=2)
    d.rectangle([80, y, 90, y + narration_h], fill=ACCENT_SAGE)
    text_y = y + 15
    for line in narration_lines:
        d.text((110, text_y), line, font=fonts["narration"], fill=TEXT_COLOR)
        text_y += 42

    # Footer
    footer_text = t["page_footer_fmt"].format(ep=ep['num'], pid=panel['id'])
    d.text((PAGE_W / 2, PAGE_H - 50), footer_text, font=fonts["lesson"], fill=GRAY_LINE, anchor="mm")
    return img


def build_for_lang(lang):
    t = TRANSLATIONS[lang]
    episodes = EPISODES_BY_LANG[lang]

    # Load all fonts for this language
    fonts = {
        "title": find_font(lang, 56),
        "sub": find_font(lang, 32),
        "panel_title": find_font(lang, 38),
        "tag": find_font(lang, 24),
        "body": find_font(lang, 28),
        "narration": find_font(lang, 26),
        "lesson": find_font(lang, 22),
    }

    # Output path per language
    if lang == "ko":
        out_pdf = BASE / "만화_하네스이해.pdf"
    elif lang == "en":
        out_pdf = BASE / "Harness_Comic_EN.pdf"
    elif lang == "ja":
        out_pdf = BASE / "漫画_ハーネス理解_JP.pdf"

    pages = []
    pages.append(make_cover_page(lang, fonts, episodes, t))
    for ep in episodes:
        pages.append(make_episode_cover(ep, lang, fonts, t))
        for panel in ep['panels']:
            pages.append(make_panel_page(ep, panel, lang, fonts, t))

    pages[0].save(
        out_pdf,
        save_all=True,
        append_images=pages[1:],
        resolution=150.0,
    )
    print(f"[{lang.upper()}] Saved {out_pdf} ({len(pages)} pages)")


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ["all"]
    langs = ["ko", "en", "ja"] if "all" in args else args
    for lang in langs:
        if lang not in TRANSLATIONS:
            print(f"Unknown language: {lang}")
            continue
        build_for_lang(lang)


if __name__ == "__main__":
    main()
