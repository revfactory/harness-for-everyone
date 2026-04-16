#!/usr/bin/env python3
"""슬라이드 HTML 다국어 버전 빌드 (KO/EN/JA)

공통 CSS/JS + 언어별 슬라이드 데이터로 index.html / index_EN.html / index_JA.html 생성.
이미지(slide_01~10.png)는 공통 사용.

Usage:
    python3 build_slides_html_multilang.py
"""

import html as _html
from pathlib import Path

BASE = Path("/Users/robin/Downloads/harness-easy")

# =====================================================================
# 공통 CSS (언어와 무관)
# =====================================================================

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Nanum+Pen+Script&family=Kalam:wght@400;700&family=Shippori+Mincho:wght@500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  background: #2a2520;
  color: #5C5650;
  font-family: var(--deck-font), 'Gaegu', 'Nanum Pen Script', sans-serif;
  overflow: hidden;
  height: 100%;
}
html[lang="en"] { --deck-font: 'Kalam', 'Gaegu', sans-serif; }
html[lang="ja"] { --deck-font: 'Shippori Mincho', 'ヒラギノ角ゴシック W3', 'Gaegu', sans-serif; }
html[lang="ko"] { --deck-font: 'Gaegu', 'Nanum Pen Script', sans-serif; }
body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.deck {
  position: relative;
  width: 95vw;
  max-width: 1600px;
  aspect-ratio: 16 / 9;
  background: #FFF8F0;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  overflow: hidden;
  border-radius: 12px;
}
.slide {
  position: absolute;
  inset: 0;
  padding: 4% 5%;
  display: none;
  flex-direction: column;
  background: #FFF8F0;
}
.slide.active { display: flex; }
.slide::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(rgba(184,176,168,0.05) 1px, transparent 1px),
    radial-gradient(rgba(184,176,168,0.03) 1px, transparent 1px);
  background-size: 24px 24px, 37px 37px;
  background-position: 0 0, 12px 19px;
  pointer-events: none;
}
.slide-content {
  position: relative;
  display: flex;
  gap: 3%;
  width: 100%;
  height: 100%;
  z-index: 1;
}
.slide-layout-center { flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.slide-layout-image-text { flex-direction: row; align-items: center; }
.slide-layout-text-image { flex-direction: row-reverse; align-items: center; }
.slide-layout-full-image { flex-direction: column; align-items: center; justify-content: center; }
.illustration { flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.illustration img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(2px 3px 0 rgba(184,176,168,0.3));
}
.slide-layout-full-image .illustration { flex: none; width: 80%; height: 70%; }
.text-area { flex: 1; padding: 0 2%; display: flex; flex-direction: column; justify-content: center; }
.text-area.center { text-align: center; align-items: center; }
h1 { font-size: 3.6rem; color: #5C5650; margin-bottom: 1rem; line-height: 1.2; }
h1 .mustard {
  background: linear-gradient(to bottom, transparent 62%, #F2C94C 62%, #F2C94C 92%, transparent 92%);
  padding: 0 6px;
}
h1 .coral { color: #F4A39C; }
.subtitle { font-size: 1.8rem; color: #8A7F75; margin-bottom: 1.2rem; }
.message {
  font-size: 1.6rem;
  color: #6B8962;
  font-weight: 700;
  margin-bottom: 1.5rem;
  padding: 0.6rem 1rem;
  background: rgba(168,197,160,0.18);
  border-left: 5px solid #A8C5A0;
  border-radius: 6px;
}
ul.bullets { list-style: none; padding: 0; margin: 0; }
ul.bullets li {
  font-size: 1.6rem;
  color: #5C5650;
  padding: 0.5rem 0 0.5rem 2.4rem;
  position: relative;
  line-height: 1.5;
}
ul.bullets li::before {
  content: "\u2726";
  position: absolute;
  left: 0.5rem;
  color: #F2C94C;
  font-size: 1.8rem;
}
.slide-layout-center h1 { font-size: 4.8rem; }
.slide-layout-center .subtitle { font-size: 2rem; }
.slide-meta {
  position: absolute;
  bottom: 1.5%;
  right: 2%;
  font-size: 1rem;
  color: #B8B0A8;
  z-index: 2;
}
.slide-num {
  position: absolute;
  top: 2%;
  right: 2%;
  font-size: 1.1rem;
  color: #B8B0A8;
  padding: 4px 12px;
  border: 1.5px dashed #B8B0A8;
  border-radius: 20px;
  z-index: 2;
}
.controls {
  position: fixed;
  bottom: 2vh;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  background: rgba(0,0,0,0.3);
  padding: 8px 16px;
  border-radius: 30px;
  backdrop-filter: blur(6px);
  z-index: 100;
  color: #fff;
  font-size: 0.95rem;
}
.controls button {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-family: inherit;
  font-size: 1rem;
}
.controls button:hover { background: rgba(255,255,255,0.25); }
.counter { align-self: center; padding: 0 8px; }
.help {
  position: fixed;
  bottom: 2vh;
  right: 2vw;
  color: rgba(255,255,255,0.5);
  font-size: 0.9rem;
  z-index: 100;
}
.lang-switcher {
  position: fixed;
  top: 2vh;
  right: 2vw;
  display: flex;
  gap: 6px;
  background: rgba(0,0,0,0.3);
  padding: 6px 10px;
  border-radius: 20px;
  backdrop-filter: blur(6px);
  z-index: 100;
  font-size: 0.9rem;
}
.lang-switcher a {
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  padding: 3px 10px;
  border-radius: 14px;
  transition: all 0.15s;
}
.lang-switcher a:hover { color: #fff; background: rgba(255,255,255,0.15); }
.lang-switcher a.active {
  color: #2a2520;
  background: #F2C94C;
  font-weight: 700;
}
.speaker-notes { display: none; }
body.notes-visible .speaker-notes {
  display: block;
  position: fixed;
  bottom: 8vh;
  left: 2vw;
  width: 30vw;
  max-height: 40vh;
  overflow: auto;
  background: rgba(255,253,247,0.95);
  border: 2px solid #A8C5A0;
  border-radius: 12px;
  padding: 16px;
  font-size: 0.95rem;
  color: #5C5650;
  line-height: 1.5;
  z-index: 99;
}
.speaker-notes h4 { color: #6B8962; margin-bottom: 8px; }
"""

COMMON_JS = """
const slides = document.querySelectorAll('.slide');
let currentIndex = 0;
const curNum = document.getElementById('curNum');
const noteContent = document.getElementById('noteContent');

function show(idx) {
  slides.forEach((s, i) => s.classList.toggle('active', i === idx));
  curNum.textContent = idx + 1;
  noteContent.textContent = slides[idx].getAttribute('data-notes') || '';
  currentIndex = idx;
  history.replaceState(null, '', '#slide-' + (idx + 1));
}

function next() { if (currentIndex < slides.length - 1) show(currentIndex + 1); }
function prev() { if (currentIndex > 0) show(currentIndex - 1); }

document.getElementById('nextBtn').addEventListener('click', next);
document.getElementById('prevBtn').addEventListener('click', prev);
document.getElementById('notesBtn').addEventListener('click', () => {
  document.body.classList.toggle('notes-visible');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { next(); e.preventDefault(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { prev(); e.preventDefault(); }
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(slides.length - 1);
  else if (e.key === 'n' || e.key === 'N') document.body.classList.toggle('notes-visible');
  else if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});

const m = location.hash.match(/#slide-(\\d+)/);
if (m) { const i = parseInt(m[1]) - 1; if (i >= 0 && i < slides.length) show(i); }
else show(0);
"""

# =====================================================================
# UI 라벨 (언어별)
# =====================================================================

UI = {
    "ko": {
        "lang_code": "ko",
        "page_title": "하네스 대중화 슬라이드 — AI 팀 운영 매뉴얼, 하네스",
        "btn_prev": "← 이전",
        "btn_next": "다음 →",
        "btn_notes": "노트",
        "notes_heading": "발표자 노트",
        "help": "←/→ 또는 Space · N: 노트 · F: 전체화면",
        "meta_prefix": "하네스 대중화",
        "slide_word": "슬라이드",
        "last_meta_suffix": "감사합니다",
    },
    "en": {
        "lang_code": "en",
        "page_title": "Harness for Everyone — AI Team Operating Manual",
        "btn_prev": "← Prev",
        "btn_next": "Next →",
        "btn_notes": "Notes",
        "notes_heading": "Speaker Notes",
        "help": "←/→ or Space · N: Notes · F: Fullscreen",
        "meta_prefix": "Harness for Everyone",
        "slide_word": "Slide",
        "last_meta_suffix": "Thank you",
    },
    "ja": {
        "lang_code": "ja",
        "page_title": "ハーネス大衆化スライド — AIチーム運営マニュアル、ハーネス",
        "btn_prev": "← 前へ",
        "btn_next": "次へ →",
        "btn_notes": "ノート",
        "notes_heading": "発表者ノート",
        "help": "←/→ または Space · N: ノート · F: 全画面",
        "meta_prefix": "ハーネス大衆化",
        "slide_word": "スライド",
        "last_meta_suffix": "ありがとうございました",
    },
}

# 언어 스위처 타겟 파일
LANG_FILES = {
    "ko": ("index.html", "한국어"),
    "en": ("index_EN.html", "English"),
    "ja": ("index_JA.html", "日本語"),
}


# =====================================================================
# 슬라이드 데이터 (언어별)
# =====================================================================

SLIDES_KO = [
    # 1
    {"layout": "center", "img": "slide_01.png", "alt": "표지 일러스트",
     "h1": 'AI 팀 <span class="mustard">운영 매뉴얼</span>, 하네스',
     "subtitle": "일반인도 이해할 수 있는 하네스 엔지니어링",
     "footer": "2026-04-16 · 황민호(revfactory@gmail.com)",
     "notes": "안녕하세요. 오늘 약 10분간 하네스라는 개념에 대해 이야기하겠습니다. 이 발표의 목표는 하네스가 무엇인지 개념적으로 이해하는 것. 코딩을 배우거나 실습하는 자리가 아닙니다. 레시피를 읽는 시간입니다."},
    # 2
    {"layout": "image-text", "img": "slide_02.png", "alt": "훅 일러스트",
     "h1": 'AI 하나에게 <span class="coral">다 시키면</span>?',
     "message": "혼자 코스 요리를 다 차리면 헤맨다.",
     "bullets": [
        "\"기획서 검토하고 수정하고 보고서 만들어줘\"",
        "결과는? 뒤죽박죽",
        "우리도 혼자서 코스 요리를 다 차리지 않는다"],
     "notes": "AI 챗봇에게 한 번에 너무 많은 일을 시키면 뒤죽박죽이 됩니다. AI가 멍청해서가 아니라, 사람도 혼자 코스 요리를 차릴 수 없듯이요. 그래서 여러 셰프, 여러 역할이 필요합니다."},
    # 3
    {"layout": "image-text", "img": "slide_03.png", "alt": "문제 정의 일러스트",
     "h1": '왜 지금 <span class="mustard">하네스 이해</span>가 필요한가',
     "message": "AI는 팀으로 엮는 시대인데, 우리 개념은 챗봇 한 대에 멈춰 있다.",
     "bullets": [
        "AI는 \"한 대 쓰는 시대\"에서 \"팀으로 엮는 시대\"로 변화",
        "만들지 않더라도, 읽을 수는 있어야 한다",
        "이해는 기초 리터러시 — 코딩 몰라도 된다"],
     "notes": "AI는 '한 대 쓰는 시대'에서 '팀으로 엮는 시대'로 바뀌고 있는데, 우리 개념은 챗봇 한 대에 멈춰 있습니다. 이 격차가 커지면 과신·불신이 생깁니다. 만들지 않더라도 읽을 수는 있어야 합니다."},
    # 4
    {"layout": "image-text", "img": "slide_04.png", "alt": "팀 주방 일러스트",
     "h1": '호통치는 주방이 아닌, <span class="mustard">협업</span>하는 팀 주방',
     "message": "하네스는 우리가 AI 팀에게 역할을 나눠주는 주방 운영 매뉴얼이다.",
     "bullets": [
        "이건 독재 주방이 아니에요",
        "서로 \"이 간은 어때?\"라고 코멘트하는 팀",
        "이 주방의 운영 매뉴얼 = 하네스"],
     "notes": "호통치는 주방이 아니라 서로 '이 간 어때?'라고 코멘트하는 팀 주방입니다. 각 셰프는 역할이 있고, 헤드셰프가 조율합니다. 이 전체를 매일 잘 돌아가게 만드는 운영 매뉴얼이 바로 하네스입니다."},
    # 5
    {"layout": "image-text", "img": "slide_05.png", "alt": "개념 매핑 일러스트",
     "h1": '주방의 역할 = <span class="coral">AI의 역할</span>',
     "message": "에이전트 · 오케스트레이터 · 스킬 · 하네스가 어떤 주방 역할인지 안다.",
     "bullets": [
        "에이전트 = AI 셰프 (역할을 맡은 AI)",
        "오케스트레이터 = 헤드셰프 (조율자)",
        "스킬 = 레시피 카드 / 하네스 = 운영 매뉴얼"],
     "notes": "각 역할을 AI 용어로 이어봅니다. 에이전트 = AI 셰프, 오케스트레이터 = 헤드셰프, 스킬 = 레시피 카드, 하네스 = 운영 매뉴얼. 하네스는 사고파는 제품이 아니라 우리가 짜는 설계 방식입니다."},
    # 6
    {"layout": "image-text", "img": "slide_06.png", "alt": "학습 경로 일러스트",
     "h1": '<span class="mustard">3분</span>이면 감, <span class="mustard">30분</span>이면 그림, <span class="mustard">1시간</span>이면 설명',
     "message": "3단계 학습 경로로 누구나 자기 속도에 맞게 이해할 수 있다.",
     "bullets": [
        "입문 (1~10분): 하네스를 한 문장으로 말할 수 있다",
        "중급 (30분): 다섯 요소의 흐름도를 그릴 수 있다",
        "심화 (60~90분): 타인에게 10분간 설명할 수 있다"],
     "notes": "하네스 이해는 3단계로 나뉩니다. 입문 1~10분이면 한 문장으로 말할 수 있고, 중급 30분이면 흐름도를 그릴 수 있고, 심화 60~90분이면 10분 설명이 가능합니다. 첫 단계에서 멈춰도 됩니다."},
    # 7
    {"layout": "image-text", "img": "slide_07.png", "alt": "오개념 일러스트",
     "h1": '이건 <span class="coral">아니에요</span> — 흔한 오해 5가지',
     "message": "가장 흔한 5가지 오해를 미리 바로잡는다.",
     "bullets": [
        "✗ \"AI 제품이다\" → ✓ 설계 방식이다",
        "✗ \"AI가 스스로 판단\" → ✓ 설계된 범위 안에서 선택",
        "✗ \"사람 없이 돌아간다\" → ✓ 사람이 짜고 사람이 고친다"],
     "notes": "가장 흔한 5가지 오해를 바로잡습니다. 1) 하네스는 제품이 아니라 설계 방식. 2) AI는 스스로 판단하는 게 아니라 설계 범위 안에서 선택. 3) 사람 없이 돌아가는 게 아니라 사람이 짜고 고친다. 4) 한 번 배우면 기억하는 게 아니라 매번 기억을 잃는다. 5) 코딩 몰라도 이해 가능."},
    # 8
    {"layout": "full-image", "img": "slide_08.png", "alt": "일상 장면",
     "h1": '일상에서 찾는 <span class="mustard">하네스적 순간</span>',
     "message": "내 일상에서 하네스적 순간을 찾을 수 있다.",
     "bullets_horizontal": [
        "김장: 절이기·양념·속 — 역할 분담",
        "이사: 포장·운반·배치 — 조율자",
        "소풍: 장보기·요리·자리 — 체크리스트"],
     "notes": "김장, 이사, 소풍. 일상에도 하네스적 구조가 있습니다. 역할을 나누고, 누군가 조율하고, 매뉴얼이 있는 순간이요. 여러분의 일상에서도 비슷한 순간을 하나 찾아보세요."},
    # 9
    {"layout": "image-text", "img": "slide_09.png", "alt": "핵심 정리 일러스트",
     "h1": '<span class="mustard">세 문장</span>으로 기억하세요',
     "message": "하네스의 본질을 세 문장과 자가 점검으로 다진다.",
     "bullets": [
        "하네스는 AI 팀 운영 매뉴얼이다 — 제품이 아니라 설계 방식",
        "사람이 짜고, AI가 실행한다 — 주어는 항상 \"우리\"",
        "AI 셰프는 매번 기억을 잃는다 — 그래서 메모리 설계가 필요"],
     "notes": "세 문장으로 요약합니다. 1) 하네스는 AI 팀 운영 매뉴얼 — 제품이 아니라 설계 방식. 2) 사람이 짜고 AI가 실행한다 — 주어는 '우리'. 3) AI 셰프는 매번 기억을 잃는다 — 그래서 메모리 설계가 필요."},
    # 10
    {"layout": "image-text", "img": "slide_10.png", "alt": "다음 단계 일러스트",
     "h1": '더 알고 <span class="coral">싶다면</span>',
     "message": "이해 다음의 길이 열려 있다.",
     "bullets": [
        "이해만으로 충분 — 오늘 여기까지가 입문 완료",
        "중급 30분 · 심화 90분 경로 준비됨",
        "만들기는 별도 경로 — 이해와 만들기는 다른 능력"],
     "notes": "이해만으로 충분합니다. 오늘 10분을 함께하셨다면 입문 목표는 달성입니다. 더 알고 싶다면 중급 30분, 심화 90분 경로가 있습니다. 이해와 만들기는 다른 능력입니다. 감사합니다."},
]

SLIDES_EN = [
    {"layout": "center", "img": "slide_01.png", "alt": "Cover illustration",
     "h1": 'AI Team <span class="mustard">Operating Manual</span>: Harness',
     "subtitle": "Harness Engineering for Everyone",
     "footer": "2026-04-16 · Minho Hwang (revfactory@gmail.com)",
     "notes": "Hello. For about 10 minutes today, we'll talk about the concept of 'Harness.' The goal isn't to learn coding — it's to understand what a Harness is, conceptually. Today is about reading the recipe, not becoming the chef."},
    {"layout": "image-text", "img": "slide_02.png", "alt": "Hook illustration",
     "h1": 'What if one AI <span class="coral">does it all</span>?',
     "message": "A lone chef trying to plate a full course will flounder.",
     "bullets": [
        "\"Review the proposal, revise it, and write the report too.\"",
        "The result? A jumbled mess.",
        "We don't cook a full course alone, either."],
     "notes": "Hand a chatbot too many things at once and it gets jumbled — not because AI is stupid, but because even we don't plate a full course alone. That's why multiple chefs, multiple roles, are needed."},
    {"layout": "image-text", "img": "slide_03.png", "alt": "Problem illustration",
     "h1": 'Why <span class="mustard">understanding Harness</span> matters now',
     "message": "AI is becoming a team, but our vocabulary is still stuck on \"just one chatbot.\"",
     "bullets": [
        "AI is shifting from \"using one\" to \"weaving a team\"",
        "Even if you don't build one, you should be able to read one",
        "Understanding is basic literacy — no coding required"],
     "notes": "AI is shifting from 'using one' to 'weaving a team,' but our mental model still stops at one chatbot. When that gap widens, we get overconfidence and mistrust. You don't have to build Harnesses — but you should be able to read them."},
    {"layout": "image-text", "img": "slide_04.png", "alt": "Team kitchen illustration",
     "h1": 'Not a dictatorial kitchen — a <span class="mustard">collaborative</span> team kitchen',
     "message": "Harness is the kitchen operating manual we write to divide roles among AI chefs.",
     "bullets": [
        "This isn't a dictatorial kitchen",
        "Chefs say \"how's the seasoning?\" to each other",
        "This kitchen's operating manual = Harness"],
     "notes": "Not a kitchen of shouting orders, but a team kitchen where chefs comment 'how's the seasoning?' Each chef has a role; the head chef coordinates. The operating manual that keeps it running day after day — that's Harness."},
    {"layout": "image-text", "img": "slide_05.png", "alt": "Concept mapping illustration",
     "h1": 'Kitchen roles = <span class="coral">AI roles</span>',
     "message": "Know which kitchen role each term — Agent, Orchestrator, Skill, Harness — maps to.",
     "bullets": [
        "Agent = AI chef (an AI with a role)",
        "Orchestrator = head chef (coordinator)",
        "Skill = recipe card / Harness = operating manual"],
     "notes": "Now we map each role to its AI term. Agent = AI chef. Orchestrator = head chef. Skill = recipe card. Harness = operating manual. A Harness isn't a product you buy — it's a design we craft."},
    {"layout": "image-text", "img": "slide_06.png", "alt": "Learning path illustration",
     "h1": '<span class="mustard">3 min</span> for a feel, <span class="mustard">30 min</span> for the picture, <span class="mustard">1 hour</span> to explain',
     "message": "A three-stage path — anyone can grasp it at their own pace.",
     "bullets": [
        "Beginner (1–10 min): Say Harness in one sentence",
        "Intermediate (30 min): Draw the flow of five parts",
        "Advanced (60–90 min): Explain it to someone for 10 min"],
     "notes": "Understanding Harness has three stages. Beginner (1–10 min): one sentence. Intermediate (30 min): draw the flow. Advanced (60–90 min): explain for 10 minutes. Stopping at stage one is perfectly fine."},
    {"layout": "image-text", "img": "slide_07.png", "alt": "Misconceptions illustration",
     "h1": 'Not this — <span class="coral">5 common myths</span>',
     "message": "Clear up the five most common misconceptions up front.",
     "bullets": [
        "✗ \"It's an AI product\" → ✓ It's a design approach",
        "✗ \"AI decides on its own\" → ✓ It chooses within a designed scope",
        "✗ \"It runs without humans\" → ✓ Humans write and fix it"],
     "notes": "Five common misunderstandings. 1) Harness isn't a product — it's a design. 2) AI doesn't decide on its own — it picks within a scope. 3) It doesn't run without humans — we write and maintain it. 4) It doesn't learn permanently — it forgets each session. 5) No coding needed to understand it."},
    {"layout": "full-image", "img": "slide_08.png", "alt": "Daily life scene",
     "h1": '<span class="mustard">Harness moments</span> in everyday life',
     "message": "You can spot a harness-like moment in your own everyday life.",
     "bullets_horizontal": [
        "Kimjang: salting · seasoning · stuffing — role split",
        "Moving: packing · carrying · placing — coordinator",
        "Picnic: shopping · cooking · seating — checklist"],
     "notes": "Kimjang, moving, a picnic — everyday life already has harness-like structures. Dividing roles, coordinating, following a plan. Try to find a moment like that in your own week."},
    {"layout": "image-text", "img": "slide_09.png", "alt": "Key summary illustration",
     "h1": 'Remember it in <span class="mustard">three sentences</span>',
     "message": "Lock in the essence of Harness with three sentences and a self-check.",
     "bullets": [
        "Harness is the AI team operating manual — not a product, a design",
        "Humans write, AI runs — the subject is always \"we\"",
        "AI chefs forget each time — so memory design matters"],
     "notes": "Three sentences to carry away. 1) Harness is the AI team operating manual — not a product, but a design. 2) Humans write, AI runs — the subject is always 'we.' 3) AI chefs forget each time — which is why memory design matters."},
    {"layout": "image-text", "img": "slide_10.png", "alt": "Next steps illustration",
     "h1": 'If you want to <span class="coral">go further</span>',
     "message": "A path opens beyond understanding.",
     "bullets": [
        "Understanding is enough — today completes the beginner goal",
        "Intermediate (30 min) and advanced (90 min) paths are ready",
        "Building is a separate track — different skill from understanding"],
     "notes": "Understanding alone is enough. If you stayed 10 minutes with us, the beginner goal is done. Want more? 30-minute intermediate and 90-minute advanced paths await. Understanding and building are different skills. Thank you."},
]

SLIDES_JA = [
    {"layout": "center", "img": "slide_01.png", "alt": "表紙イラスト",
     "h1": 'AIチーム<span class="mustard">運営マニュアル</span>、ハーネス',
     "subtitle": "みんなが理解できるハーネスエンジニアリング",
     "footer": "2026-04-16 · ファン・ミンホ (revfactory@gmail.com)",
     "notes": "こんにちは。今日は約10分間、「ハーネス」という概念についてお話しします。このプレゼンの目標は、ハーネスが何かを概念的に理解すること。コーディングや実習の場ではありません。レシピを読む時間です。"},
    {"layout": "image-text", "img": "slide_02.png", "alt": "フックイラスト",
     "h1": 'AI 1台に<span class="coral">全部任せたら</span>？',
     "message": "一人でコース料理を全部作ると、手が回らなくなります。",
     "bullets": [
        "「企画書をチェックして、修正して、レポートも作って」",
        "結果は？ ごちゃごちゃ",
        "私たちも一人でコース料理は作りません"],
     "notes": "AIチャットボットに一度に大量の仕事を頼むと、ごちゃごちゃになります。AIがバカなのではなく、私たちも一人でコース料理を作れないのと同じです。だから複数のシェフ、複数の役割が必要なのです。"},
    {"layout": "image-text", "img": "slide_03.png", "alt": "問題定義イラスト",
     "h1": 'なぜ今<span class="mustard">ハーネスを理解</span>することが必要か',
     "message": "AIはチームで紡ぐ時代なのに、私たちの概念はまだチャットボット1台に止まっている。",
     "bullets": [
        "AIは「1台使う時代」から「チームで紡ぐ時代」へ変化",
        "作らなくても、読めるようにはなっておきたい",
        "理解は基礎リテラシー — コーディング不要"],
     "notes": "AIは「1台使う時代」から「チームで紡ぐ時代」へ変わっているのに、私たちの概念はまだチャットボット1台に止まっています。このギャップが広がると過信や不信が生まれます。作らなくても、読めるようにはなっておきたい。"},
    {"layout": "image-text", "img": "slide_04.png", "alt": "チームキッチンイラスト",
     "h1": '怒鳴るキッチンではなく、<span class="mustard">協力する</span>チームキッチン',
     "message": "ハーネスは、AIチームに役割を振り分ける、私たちが作るキッチン運営マニュアルです。",
     "bullets": [
        "これは独裁キッチンではありません",
        "「この味つけどう？」とコメントし合うチーム",
        "このキッチンの運営マニュアル = ハーネス"],
     "notes": "怒鳴るキッチンではなく、「この味つけどう？」とコメントし合うチームキッチンです。各シェフに役割があり、ヘッドシェフが調整します。これを毎日回す運営マニュアルがハーネスです。"},
    {"layout": "image-text", "img": "slide_05.png", "alt": "概念マッピングイラスト",
     "h1": 'キッチンの役割 = <span class="coral">AIの役割</span>',
     "message": "エージェント・オーケストレーター・スキル・ハーネスが、それぞれどのキッチン役割か分かる。",
     "bullets": [
        "エージェント = AIシェフ (役割を持ったAI)",
        "オーケストレーター = ヘッドシェフ (調整役)",
        "スキル = レシピカード / ハーネス = 運営マニュアル"],
     "notes": "各役割をAI用語につなげます。エージェント=AIシェフ、オーケストレーター=ヘッドシェフ、スキル=レシピカード、ハーネス=運営マニュアル。ハーネスは売買する製品ではなく、私たちが作る設計方法です。"},
    {"layout": "image-text", "img": "slide_06.png", "alt": "学習パスイラスト",
     "h1": '<span class="mustard">3分</span>で感覚、<span class="mustard">30分</span>で絵、<span class="mustard">1時間</span>で説明',
     "message": "3段階の学習パスで、誰でも自分のペースで理解できる。",
     "bullets": [
        "入門 (1~10分)：ハーネスを1文で言える",
        "中級 (30分)：5つの要素の流れ図を書ける",
        "上級 (60~90分)：他人に10分間説明できる"],
     "notes": "ハーネスの理解は3段階に分かれます。入門1~10分：1文で言える。中級30分：流れ図が書ける。上級60~90分：10分間他人に説明できる。最初の段階で止まっても大丈夫です。"},
    {"layout": "image-text", "img": "slide_07.png", "alt": "誤解イラスト",
     "h1": 'これは<span class="coral">違います</span> — よくある5つの誤解',
     "message": "最もよくある5つの誤解を先に正します。",
     "bullets": [
        "✗「AI製品だ」→ ✓ 設計方法だ",
        "✗「AIが自分で判断」→ ✓ 設計された範囲内で選ぶ",
        "✗「人なしで動く」→ ✓ 人が作って人が直す"],
     "notes": "最もよくある5つの誤解を正します。1) ハーネスは製品ではなく設計方法。2) AIは自分で判断するのではなく、設計範囲内で選ぶ。3) 人なしで動くのではなく、人が作って直す。4) 一度学んだら記憶するのではなく、毎回記憶を失う。5) コーディングを知らなくても理解できる。"},
    {"layout": "full-image", "img": "slide_08.png", "alt": "日常シーン",
     "h1": '日常に見つける<span class="mustard">ハーネス的瞬間</span>',
     "message": "自分の日常の中で、ハーネス的瞬間を見つけることができる。",
     "bullets_horizontal": [
        "キムジャン：塩漬け・ヤンニョム・具 — 役割分担",
        "引っ越し：梱包・運搬・配置 — 調整役",
        "ピクニック：買出し・料理・席 — チェックリスト"],
     "notes": "キムジャン、引っ越し、ピクニック。日常にもハーネス的な構造があります。役割を分けて、誰かが調整して、マニュアルがある瞬間です。あなたの日常でも、そんな瞬間を一つ探してみてください。"},
    {"layout": "image-text", "img": "slide_09.png", "alt": "要点整理イラスト",
     "h1": '<span class="mustard">3つの文</span>で覚えましょう',
     "message": "ハーネスの本質を3つの文と自己チェックで固める。",
     "bullets": [
        "ハーネスはAIチームの運営マニュアル — 製品ではなく設計方法",
        "人が作り、AIが実行する — 主語は常に「私たち」",
        "AIシェフは毎回記憶を失う — だからメモリ設計が必要"],
     "notes": "3つの文で要約します。1) ハーネスはAIチームの運営マニュアル — 製品ではなく設計方法。2) 人が作り、AIが実行する — 主語は常に「私たち」。3) AIシェフは毎回記憶を失う — だからメモリ設計が必要。"},
    {"layout": "image-text", "img": "slide_10.png", "alt": "次のステップイラスト",
     "h1": 'もっと<span class="coral">知りたければ</span>',
     "message": "理解のその先に、道が開かれている。",
     "bullets": [
        "理解だけで十分 — 今日ここまでで入門完了",
        "中級30分・上級90分のパスを準備",
        "作るのは別パス — 理解と作るは別の能力"],
     "notes": "理解だけで十分です。今日10分ご一緒しただけで、入門目標は達成です。もっと知りたい方は中級30分、上級90分のパスが用意されています。理解することと作ることは別の能力です。ありがとうございました。"},
]

SLIDES_BY_LANG = {"ko": SLIDES_KO, "en": SLIDES_EN, "ja": SLIDES_JA}


# =====================================================================
# HTML 렌더링
# =====================================================================

def render_slide(idx, total, slide, ui):
    n = idx + 1
    layout = slide["layout"]
    img = slide["img"]
    alt = _html.escape(slide["alt"])
    notes = _html.escape(slide["notes"], quote=True)

    # Meta text (bottom right)
    if n == total:
        meta = f'{ui["meta_prefix"]} · {ui["slide_word"]} {n}/{total} · {ui["last_meta_suffix"]}'
    else:
        meta = f'{ui["meta_prefix"]} · {ui["slide_word"]} {n}/{total}'

    active_cls = " active" if idx == 0 else ""

    if layout == "center":
        # Cover slide
        subtitle = slide.get("subtitle", "")
        footer = slide.get("footer", "")
        body = f'''
    <div class="slide-content slide-layout-center">
      <div class="illustration" style="height: 55%;">
        <img src="_workspace/visual/images/{img}" alt="{alt}">
      </div>
      <div class="text-area center" style="flex: none; margin-top: 2rem;">
        <h1>{slide["h1"]}</h1>
        <p class="subtitle">{_html.escape(subtitle)}</p>
        <p style="color:#B8B0A8; font-size:1.2rem;">{_html.escape(footer)}</p>
      </div>
    </div>'''
    elif layout == "full-image":
        bullets_html = "".join(f'          <li>{_html.escape(b)}</li>\n'
                               for b in slide.get("bullets_horizontal", []))
        body = f'''
    <div class="slide-content slide-layout-full-image">
      <div class="text-area center" style="flex: none; margin-bottom: 1rem;">
        <h1>{slide["h1"]}</h1>
        <p class="message">{_html.escape(slide["message"])}</p>
      </div>
      <div class="illustration"><img src="_workspace/visual/images/{img}" alt="{alt}"></div>
      <div class="text-area center" style="flex: none; margin-top: 1rem;">
        <ul class="bullets" style="display:flex; gap:2rem; justify-content:center; flex-wrap:wrap;">
{bullets_html}        </ul>
      </div>
    </div>'''
    else:  # image-text
        bullets_html = "".join(f'          <li>{_html.escape(b)}</li>\n'
                               for b in slide.get("bullets", []))
        body = f'''
    <div class="slide-content slide-layout-image-text">
      <div class="illustration"><img src="_workspace/visual/images/{img}" alt="{alt}"></div>
      <div class="text-area">
        <h1>{slide["h1"]}</h1>
        <p class="message">{_html.escape(slide["message"])}</p>
        <ul class="bullets">
{bullets_html}        </ul>
      </div>
    </div>'''

    return f'''  <section class="slide{active_cls}" data-notes="{notes}">
    <span class="slide-num">{n} / {total}</span>{body}
    <div class="slide-meta">{_html.escape(meta)}</div>
  </section>'''


def render_lang_switcher(current_lang):
    links = []
    for code, (filename, label) in LANG_FILES.items():
        active = " active" if code == current_lang else ""
        links.append(f'<a href="{filename}" class="{active.strip()}">{label}</a>')
    return f'<div class="lang-switcher">{"".join(links)}</div>'


def build_html(lang):
    ui = UI[lang]
    slides = SLIDES_BY_LANG[lang]
    total = len(slides)

    slides_html = "\n\n".join(render_slide(i, total, s, ui) for i, s in enumerate(slides))
    lang_switcher = render_lang_switcher(lang)

    html = f'''<!DOCTYPE html>
<html lang="{ui["lang_code"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_html.escape(ui["page_title"])}</title>
<style>{COMMON_CSS}</style>
</head>
<body>
{lang_switcher}
<div class="deck" id="deck">

{slides_html}

</div>

<div class="speaker-notes">
  <h4>{_html.escape(ui["notes_heading"])}</h4>
  <p id="noteContent"></p>
</div>

<div class="controls">
  <button id="prevBtn">{_html.escape(ui["btn_prev"])}</button>
  <span class="counter"><span id="curNum">1</span> / {total}</span>
  <button id="nextBtn">{_html.escape(ui["btn_next"])}</button>
  <button id="notesBtn">{_html.escape(ui["btn_notes"])}</button>
</div>

<div class="help">{_html.escape(ui["help"])}</div>

<script>{COMMON_JS}</script>
</body>
</html>
'''
    return html


def main():
    for lang, (filename, _label) in LANG_FILES.items():
        out = BASE / filename
        out.write_text(build_html(lang), encoding="utf-8")
        print(f"[{lang.upper()}] Saved {out}")


if __name__ == "__main__":
    main()
