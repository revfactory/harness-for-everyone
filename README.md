# 하네스 대중화 (Harness for Everyone)

> AI 팀을 짜는 기술 "하네스"를 일반 대중이 **개념적으로 이해**할 수 있게 만든 교육·학습 자료 묶음.

**제안서·만화·슬라이드 모두 한국어/영어/일본어 3개 언어 지원.**

---

## 🎯 프로젝트 목표

하네스 엔지니어링이 무엇이고 왜 필요한지, 주방 브리게이드(협업 팀 주방) 비유로 일반인이 3분~1시간 안에 **개념적 이해**에 도달하도록 설계한 다층 학습 자료.

구현·배포 방법, 제품·UX·요금제 설계는 본 자료의 범위가 **아닙니다**.

---

## 📦 산출물

### 📑 제안서
- [`하네스_대중화_제안서.md`](하네스_대중화_제안서.md) — 핵심 제안서 (53KB, ~680줄)
  - TL;DR · Hero Scenario · 핵심 번역(은유 3종) · 학습 여정(3단 경로) · 오개념 18종 · 교육자 가이드 · 미해결 리스크

### 🎨 슬라이드 덱 (10장)
| 형식 | 한국어 | 영어 | 일본어 |
|------|--------|------|--------|
| HTML | [`index.html`](index.html) | [`index_EN.html`](index_EN.html) | [`index_JA.html`](index_JA.html) |
| PPTX | [`하네스_대중화_슬라이드.pptx`](하네스_대중화_슬라이드.pptx) | — | — |

HTML 슬라이드는 키보드 `←/→`·`Space` 네비게이션, `N` 키로 발표자 노트 토글, `F` 키 전체화면, 우상단 언어 스위처 지원.

### 📚 만화 시리즈 (5 에피소드 · 26 패널)
| 형식 | 한국어 | 영어 | 일본어 |
|------|--------|------|--------|
| HTML 갤러리 | [`만화_하네스이해/`](만화_하네스이해/) | — | — |
| PDF | [`만화_하네스이해.pdf`](만화_하네스이해.pdf) | [`Harness_Comic_EN.pdf`](Harness_Comic_EN.pdf) | [`漫画_ハーネス理解_JP.pdf`](漫画_ハーネス理解_JP.pdf) |

**에피소드 구성**
1. **EP1**: AI 하나에게 다 시키면? — 단일 AI의 한계
2. **EP2**: 주방 브리게이드 — 에이전트 팀
3. **EP3**: 레시피 카드와 운영 매뉴얼 — 스킬과 하네스
4. **EP4**: 기억을 잃는 셰프 — 컨텍스트 윈도우·메모리
5. **EP5**: 우리 일상의 하네스 — 김장·이사·소풍

---

## 🎨 비주얼 스타일

- **손그림 doodle** · 크림색 종이 · 파스텔 팔레트 · 색연필·마카 질감
- 주색 3: Soft Coral · Sage Green · Warm Mustard
- 보조색 4: Lavender Mist · Sky Blue · Peach · Warm Gray
- 캐릭터 다양성: 여성 헤드셰프 · 다양한 연령·인종 셰프

상세 바이블: [`_workspace/visual/00_style_bible.md`](_workspace/visual/00_style_bible.md)

---

## 🧩 중심 은유: 주방 브리게이드

> **"호통치는 독재 주방이 아닌, 서로 '이 간 어때?'라고 코멘트하는 팀 주방"**

| 하네스 개념 | 주방 은유 |
|---|---|
| 하네스 | 주방 운영 매뉴얼 (매일 개정) |
| 에이전트 | 각 파트를 맡은 AI 셰프 |
| 오케스트레이터 | 헤드셰프 (조율자, 독재자 아님) |
| 스킬 | 레시피 카드 |
| 서브에이전트 | 게스트 셰프 |
| 프롬프트 | 손님 주문서 |
| 컨텍스트 윈도우 | 셰프의 조리대 위 공간 |
| 메모리 | 내일의 셰프에게 쓰는 조리 노트 |
| MCP | 주방과 외부 세계를 잇는 USB-C 표준 포트 |

---

## 🤖 제작 과정 — 8인 AI 에이전트 팀의 자율 협업

본 프로젝트 자체가 하네스 엔지니어링으로 구축되었습니다.

### 이해 설계 팀 (4인)
- [`concept-translator`](.claude/agents/concept-translator.md) — 전문 용어·추상 개념을 일상 은유로 번역
- [`learning-experience-designer`](.claude/agents/learning-experience-designer.md) — 단계적 학습 경로 설계
- [`critical-reviewer`](.claude/agents/critical-reviewer.md) — 악마의 대변인, 오개념·편향 파헤치기
- [`synthesis-lead`](.claude/agents/synthesis-lead.md) — 3인 산출물 통합 제안서 작성

### 시각 제작 팀 (4인)
- [`visual-art-director`](.claude/agents/visual-art-director.md) — 스타일 바이블·캐릭터 시트·프롬프트 프리픽스
- [`comic-scripter`](.claude/agents/comic-scripter.md) — 패널 단위 만화 스크립트
- [`slide-architect`](.claude/agents/slide-architect.md) — 10장 슬라이드 구조
- [`visual-producer`](.claude/agents/visual-producer.md) — Gemini 이미지 생성 + HTML·PDF·PPTX 조립

### 공유 스킬
- [`metaphor-library`](.claude/skills/metaphor-library/SKILL.md) — 은유 패턴 라이브러리
- [`accessibility-lens`](.claude/skills/accessibility-lens/SKILL.md) — 이해 접근성 3축 평가 (인식·학습·심리)
- [`harness-for-everyone`](.claude/skills/harness-for-everyone/SKILL.md) — 이해 설계 오케스트레이터
- [`harness-visual-production`](.claude/skills/harness-visual-production/SKILL.md) — 시각 제작 오케스트레이터

---

## 🛠 재빌드 스크립트

```bash
# 만화 PDF 3개 언어 동시 생성
python3 _workspace/visual/build_comic_pdf_multilang.py all

# 슬라이드 HTML 3개 언어 동시 생성
python3 _workspace/visual/build_slides_html_multilang.py

# 개별 생성
python3 _workspace/visual/build_comic_pdf.py
python3 _workspace/visual/build_comic_html.py
python3 _workspace/visual/build_pptx.py
```

필요 Python 패키지: `pillow`, `python-pptx`, `reportlab` (일부 스크립트만 해당).

---

## 📂 디렉토리 구조

```
harness-easy/
├── 하네스_대중화_제안서.md          # 핵심 제안서
├── index.html                        # 슬라이드 KO (메인)
├── index_EN.html / index_JA.html     # 슬라이드 EN/JA
├── 하네스_대중화_슬라이드.pptx      # PPTX
├── 만화_하네스이해/                  # 만화 HTML 갤러리
├── 만화_하네스이해.pdf              # 만화 PDF KO
├── Harness_Comic_EN.pdf              # 만화 PDF EN
├── 漫画_ハーネス理解_JP.pdf          # 만화 PDF JA
├── _workspace/visual/                # 중간 산출물·이미지·빌드 스크립트
│   ├── 00_style_bible.md
│   ├── 01_comic_script.md
│   ├── 02_slide_structure.md
│   ├── images/                       # 생성 이미지 36개
│   └── build_*.py                    # 빌드 스크립트
├── .claude/agents/                   # 8인 에이전트 정의
└── .claude/skills/                   # 4개 스킬 정의
```

---

## 👤 저자

**황민호** (revfactory@gmail.com) · 2026-04-16

---

## 📄 라이선스

본 자료는 교육·학습 목적의 자율 제작물입니다. 인용·번역·재배포 시 출처를 밝혀주세요.
