#!/usr/bin/env python3
"""만화 에피소드 HTML 페이지 빌더"""

import os
from pathlib import Path

BASE = Path("/Users/robin/Downloads/harness-easy/만화_하네스이해")

EPISODES = [
    {
        "num": 1, "title": "AI 하나에게 다 시키면?",
        "subtitle": "단일 AI의 한계와 분업의 필요성을 깨닫는 첫 걸음",
        "panels": [
            {
                "id": "EP1-P1", "title": "도입 — Ana의 일상",
                "dialogues": [("Ana", "기획서 검토하고, 수정하고, 보고서도 만들어줘!")],
                "narration": "어느 날, Ana는 AI에게 한꺼번에 부탁했습니다.",
                "lesson": "<strong>[P1]</strong> AI는 글·코드·표를 생성하는 도구 — 하지만 한 번에 너무 많이 시키면?",
            },
            {
                "id": "EP1-P2", "title": "결과 — 뒤죽박죽",
                "dialogues": [("Ana", "...이게 뭐야?")],
                "narration": "결과는 뒤죽박죽이었습니다.",
                "lesson": "<strong>[P1]</strong> 부탁 방식에 따라 결과가 달라진다.",
            },
            {
                "id": "EP1-P3", "title": "비유 전환 — 혼자 요리하는 셰프",
                "dialogues": [],
                "narration": "혼자서 저녁 코스를 다 차리는 셰프를 상상해 보세요.",
                "lesson": "<strong>[P3]</strong> 사람도 혼자보다 분업하면 잘한다 — 주방 은유 첫 등장.",
            },
            {
                "id": "EP1-P4", "title": "깨달음 — 그래서 팀이 필요하다",
                "dialogues": [("Ana", "아, AI도 마찬가지구나!")],
                "narration": "AI도 역할을 나누면 훨씬 잘합니다.",
                "lesson": "<strong>[P3]</strong> 분업의 원리는 AI에도 적용된다 — 에이전트 개념 예고.",
            },
            {
                "id": "EP1-P5", "title": "마무리 — 다음 화 예고",
                "dialogues": [("Ana", "이 주방 안엔 누가 있을까?")],
                "narration": "[다음 화 예고] 팀 주방의 문을 열어봅니다.",
                "lesson": "다음 에피소드(에이전트 팀) 호기심 유발.",
            },
        ],
    },
    {
        "num": 2, "title": "주방 브리게이드",
        "subtitle": "팀 주방의 문을 열고 에이전트와 오케스트레이터를 만나다",
        "panels": [
            {
                "id": "EP2-P1", "title": "팀 주방 입장",
                "dialogues": [("Ana", "우와, 각자 다른 일을 하고 있네!")],
                "narration": "여긴 호통치는 독재 주방이 아닙니다.",
                "lesson": "<strong>[선단서]</strong> 위계가 아닌 협업 팀 프레임 1차 각인.",
            },
            {
                "id": "EP2-P2", "title": "헤드셰프 소개 — 오케스트레이터",
                "dialogues": [("헤드셰프", "나는 직접 요리 안 해. 누가 뭘 할지 나누는 거지.")],
                "narration": "오케스트레이터 = 조율하는 사람",
                "lesson": "<strong>[C3]</strong> 오케스트레이터는 실행자가 아니라 조율자.",
            },
            {
                "id": "EP2-P3", "title": "셰프들 소개 — 에이전트",
                "dialogues": [
                    ("소스 셰프", "난 소스 전문!"),
                    ("디저트 셰프", "난 디저트 담당이에요."),
                    ("플레이터", "담기는 내 몫."),
                ],
                "narration": "에이전트 = 각자 역할을 맡은 AI",
                "lesson": "<strong>[C1]</strong> 에이전트는 역할을 부여받은 AI. 챗봇과 다르다.",
            },
            {
                "id": "EP2-P4", "title": "협업 장면 — 코멘트가 오간다",
                "dialogues": [
                    ("디저트 셰프", "거기 레몬 한 방울 넣어볼래?"),
                    ("소스 셰프", "오, 좋은 생각!"),
                ],
                "narration": "서로 코멘트하며 한 접시를 만들어갑니다.",
                "lesson": "<strong>[M5·M18 방어]</strong> 위계가 아닌 수평 협업. 에이전트끼리 피드백.",
            },
            {
                "id": "EP2-P5", "title": "잠깐, 이건 아니에요! — 오개념 교정",
                "dialogues": [("Ana", "독재 주방이 아니라 팀 주방이에요!")],
                "narration": "오케스트레이터는 명령하는 사람이 아니라 조율하는 사람입니다.",
                "lesson": "<strong>[오개념 교정]</strong> M5(상명하복) + M18(절대 복종) 동시 교정.",
            },
            {
                "id": "EP2-P6", "title": "마무리 — 생각해보기",
                "dialogues": [],
                "narration": "[생각해보기] 에이전트와 챗봇, 뭐가 다를까요? 힌트: 역할이 있느냐 없느냐!",
                "lesson": "<strong>[자가 점검]</strong> 에이전트와 AI 중 어느 쪽이 더 좁은 개념인지 생각 유도.",
            },
        ],
    },
    {
        "num": 3, "title": "레시피 카드와 운영 매뉴얼",
        "subtitle": "스킬과 하네스 — 제품이 아닌 우리가 짜는 설계 방식",
        "panels": [
            {
                "id": "EP3-P1", "title": "레시피 카드 등장 — 스킬",
                "dialogues": [("소스 셰프", "이 카드대로 하면 돼!")],
                "narration": "스킬 = AI 셰프가 꺼내보는 레시피 카드",
                "lesson": "<strong>[C2]</strong> 스킬은 에이전트가 수행할 수 있는 구체적 능력·절차.",
            },
            {
                "id": "EP3-P2", "title": "여러 장의 레시피 카드",
                "dialogues": [("헤드셰프", "각자 맡은 레시피가 따로 있어.")],
                "narration": "셰프마다 다른 레시피 카드를 갖고 있습니다.",
                "lesson": "<strong>[C2]</strong> 스킬은 에이전트별로 다르다 — 좁을수록 잘한다.",
            },
            {
                "id": "EP3-P3", "title": "줌아웃 — 운영 매뉴얼(하네스)",
                "dialogues": [("Ana", "아, 이 전체 구조가 하네스구나!")],
                "narration": "하네스 = AI 팀의 운영 매뉴얼. 제품이 아니라, 우리가 짜는 설계 방식.",
                "lesson": "<strong>[C4]</strong> 하네스의 본 정의. 제품이 아닌 설계 방식.",
            },
            {
                "id": "EP3-P4", "title": "잠깐, 이건 아니에요! — 오개념 교정",
                "dialogues": [("Ana", "사러 가는 게 아니라 직접 짜는 거예요!")],
                "narration": "하네스는 앱이 아닙니다. 우리가 설계하는 방식이에요.",
                "lesson": "<strong>[오개념 교정]</strong> M3(하네스는 AI 제품) 직접 교정.",
            },
            {
                "id": "EP3-P5", "title": "마무리 — 다음 화 예고",
                "dialogues": [("Ana", "영업이 끝나면 이 셰프들은 어떻게 되지?")],
                "narration": "[다음 화 예고] 기억을 잃는 셰프들의 비밀.",
                "lesson": "다음 에피소드(메모리·컨텍스트) 호기심 유발.",
            },
        ],
    },
    {
        "num": 4, "title": "기억을 잃는 셰프",
        "subtitle": "컨텍스트 윈도우와 메모리 — AI는 사람과 다르다",
        "panels": [
            {
                "id": "EP4-P1", "title": "영업 후 — 텅 빈 주방",
                "dialogues": [("소스 셰프", "오늘 배운 거, 적어놔야지...")],
                "narration": "영업이 끝나면 셰프들은 오늘을 잊습니다.",
                "lesson": "<strong>[E3]</strong> AI는 세션이 끝나면 기억을 잃는다 — 기억 휘발.",
            },
            {
                "id": "EP4-P2", "title": "다음 날 아침 — 새 셰프?",
                "dialogues": [
                    ("소스 셰프", "어...여기가 어디지?"),
                    ("헤드셰프", "어제 네가 쓴 노트, 여기 있어."),
                ],
                "narration": "다음 날의 셰프는 어제를 모릅니다.",
                "lesson": "<strong>[E3]</strong> 메모리 = 내일의 셰프에게 쓰는 조리 노트.",
            },
            {
                "id": "EP4-P3", "title": "조리대 공간 — 컨텍스트 윈도우",
                "dialogues": [("소스 셰프", "조리대가 아무리 넓어도 한계가 있어.")],
                "narration": "컨텍스트 윈도우 = 셰프가 한 번에 볼 수 있는 조리대",
                "lesson": "<strong>[E2]</strong> 컨텍스트 윈도우는 한정된 작업 공간. 영업 끝나면 치워진다.",
            },
            {
                "id": "EP4-P4", "title": "잠깐, 이건 아니에요! — 오개념 교정",
                "dialogues": [("Ana", "조리대가 넓어도 매일 치운다고요?")],
                "narration": "컨텍스트가 커져도 세션이 끝나면 리셋됩니다.",
                "lesson": "<strong>[오개념 교정]</strong> M6(한 번 배우면 기억) + M10(컨텍스트 무한) 교정.",
            },
            {
                "id": "EP4-P5", "title": "마무리 — 생각해보기",
                "dialogues": [("Ana", "그래서 노트가 중요하구나.")],
                "narration": "[생각해보기] AI의 기억은 사람과 어떻게 다를까요? 힌트: 매일 첫 출근!",
                "lesson": "<strong>[자가 점검]</strong> AI 기억 휘발의 핵심 이해 확인.",
            },
        ],
    },
    {
        "num": 5, "title": "우리 일상의 하네스",
        "subtitle": "김장 · 이사 · 소풍 — 우리가 이미 살고 있는 하네스적 순간",
        "panels": [
            {
                "id": "EP5-P1", "title": "김장 — 역할 분담",
                "dialogues": [],
                "narration": "김장할 때 역할을 나누듯이...",
                "lesson": "<strong>[전이]</strong> 일상의 분업 = 하네스적 구조.",
            },
            {
                "id": "EP5-P2", "title": "이사 — 누가 뭘 할지",
                "dialogues": [("체크리스트 든 사람", "거실 먼저, 그 다음 주방!")],
                "narration": "이사할 때 계획을 짜듯이...",
                "lesson": "<strong>[전이]</strong> 체크리스트·계획 = 하네스. 조율하는 사람 = 오케스트레이터.",
            },
            {
                "id": "EP5-P3", "title": "소풍 — 각자의 준비물",
                "dialogues": [],
                "narration": "소풍 준비도 역할을 나누면 훨씬 잘됩니다.",
                "lesson": "<strong>[전이]</strong> 개인별 할 일 = 스킬, 전체 계획 = 하네스.",
            },
            {
                "id": "EP5-P4", "title": "Ana의 전이 — 나도 하네스적이었어!",
                "dialogues": [("Ana", "우리 팀 분기 기획도 이거였어!")],
                "narration": "하네스는 특별한 기술이 아닙니다. 역할을 나누고 함께 일하는 방식이에요.",
                "lesson": "<strong>[전이 완료]</strong> 자기 일상에서 유사한 예를 들 수 있다. M14(나와 상관없다) 교정.",
            },
            {
                "id": "EP5-P5", "title": "마무리 — 시리즈 종합",
                "dialogues": [("Ana", "이제 하네스가 뭔지 알겠죠?")],
                "narration": "하네스는 AI 팀의 운영 매뉴얼. 제품이 아니라 우리가 짜는 설계 방식입니다. 이해만으로도 충분해요.",
                "lesson": "<strong>[종합 정리]</strong> 핵심 정의 재확인 + '이해만으로 충분' 메시지.",
            },
        ],
    },
]


def panel_html(panel, ep_num):
    """패널 하나를 HTML로 렌더"""
    panel_id_lower = panel["id"].lower().replace("-", "_")
    # EP1-P1 -> ep1_p1 -> comic_ep1_p1.png
    parts = panel["id"].lower().split("-")
    img_file = f"comic_{parts[0]}_{parts[1]}.png"

    dialogues = "".join(
        f'<div class="dialogue"><span class="who">{who}:</span>{text}</div>'
        for who, text in panel["dialogues"]
    ) if panel["dialogues"] else ""

    return f"""
    <article class="panel" id="{panel['id']}">
      <span class="panel-tag">{panel['id']}</span>
      <h3>{panel['title']}</h3>
      <img src="../_workspace/visual/images/{img_file}" alt="{panel['title']} 이미지" loading="lazy">
      {dialogues}
      <div class="narration">{panel['narration']}</div>
      <div class="lesson">{panel['lesson']}</div>
    </article>
    """


def build_episode_page(ep, prev_ep, next_ep):
    panels_html = "".join(panel_html(p, ep["num"]) for p in ep["panels"])
    prev_link = f'<a href="ep{prev_ep}.html">← 이전 화 (EP{prev_ep})</a>' if prev_ep else '<a class="disabled">이전 화 없음</a>'
    next_link = f'<a href="ep{next_ep}.html">다음 화 (EP{next_ep}) →</a>' if next_ep else '<a class="disabled">다음 화 없음</a>'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EP{ep['num']}. {ep['title']} — 만화로 이해하는 하네스</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a href="index.html">← 전체 목차</a>
    <a href="all.html">전체 이어 읽기</a>
  </div>

  <header class="ep-header">
    <span class="ep-num">EP{ep['num']}</span>
    <h1>{ep['title']}</h1>
    <p class="ep-sub">{ep['subtitle']}</p>
  </header>

  {panels_html}

  <nav class="nav">
    {prev_link}
    {next_link}
  </nav>
</div>
</body>
</html>
"""


def build_all_page():
    """전체 에피소드를 이어 보는 페이지"""
    sections = ""
    for ep in EPISODES:
        panels_html = "".join(panel_html(p, ep["num"]) for p in ep["panels"])
        sections += f"""
  <header class="ep-header" id="ep{ep['num']}">
    <span class="ep-num">EP{ep['num']}</span>
    <h1>{ep['title']}</h1>
    <p class="ep-sub">{ep['subtitle']}</p>
  </header>
  {panels_html}
  <hr style="border:0;border-top:2px dashed #B8B0A8;margin:40px 0 48px;">
"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>전체 이어 읽기 — 만화로 이해하는 하네스</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a href="index.html">← 전체 목차</a>
    <div>
      <a href="#ep1">EP1</a> · <a href="#ep2">EP2</a> · <a href="#ep3">EP3</a> · <a href="#ep4">EP4</a> · <a href="#ep5">EP5</a>
    </div>
  </div>
  {sections}
  <nav class="nav">
    <a href="index.html">전체 목차로 돌아가기</a>
  </nav>
</div>
</body>
</html>
"""


def main():
    for i, ep in enumerate(EPISODES):
        prev_ep = EPISODES[i - 1]["num"] if i > 0 else None
        next_ep = EPISODES[i + 1]["num"] if i < len(EPISODES) - 1 else None
        html = build_episode_page(ep, prev_ep, next_ep)
        (BASE / f"ep{ep['num']}.html").write_text(html, encoding="utf-8")
        print(f"Built ep{ep['num']}.html")

    (BASE / "all.html").write_text(build_all_page(), encoding="utf-8")
    print("Built all.html")


if __name__ == "__main__":
    main()
