# harness-easy — 하네스 대중화 연구 프로젝트

## 하네스: 하네스 대중화(Harness For Everyone)

**목표:** 하네스 엔지니어링을 일반 대중이 **개념적으로 이해**할 수 있도록 설명·학습 자료를 에이전트 팀이 자율적으로 설계·합의하여 산출한다. 제품 설계·요금/비용 설계·터미널 대체 UX 설계는 본 하네스의 목적이 아니다.

**트리거:** 하네스 쉬운 설명, 하네스 개념 이해, 일반인·비전문가 대상 하네스 설명, 하네스 교육 자료, 하네스 학습 경로, 하네스 은유·용어집, AI 에이전트 개념 대중화 관련 작업 요청 시 `harness-for-everyone` 스킬을 사용하라. 단순 개념 질문은 직접 응답 가능.

**범위 외 (거절 또는 범위 재정의 요청):** 터미널/CLI 의존성 제거 제품 설계, 요금제·BM·MAX 대안 비용 설계, 메신저 봇·앱·웹 대시보드 UX 설계, 기술 실행 아키텍처 설계.

**팀 구성:** 8인 — 이해 설계 4인(concept-translator · learning-experience-designer · critical-reviewer · synthesis-lead) + 시각 제작 4인(visual-art-director · comic-scripter · slide-architect · visual-producer)

**시각 제작 트리거:** 만화 제작, 슬라이드 제작, 교육용 인포그래픽, 하네스 시각 자료, 교육 만화, 발표 자료 요청 시 `harness-visual-production` 스킬을 사용하라.

**변경 이력:**

| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-04-14 | 초기 구성 — 6인 팀 + 오케스트레이터 + 2개 공유 스킬(metaphor-library, accessibility-lens) | 전체 | 하네스 대중화 연구 하네스 신규 구축 |
| 2026-04-15 | 범위 재정의: 이해·설명 중심으로 축소. product-ux-designer/technical-feasibility-engineer/market-strategist 제거, learning-experience-designer 신설. accessibility-lens 가격 축 제거(3축화). 오케스트레이터·목표·트리거 개정, 범위 가드 도입 | 전체 (4인 팀) | 사용자 피드백: "터미널을 카카오톡으로 비유 부적절", "터미널·CLI 의존성 제거 제품 설계가 목적 아님", "비용 설계 불필요" |
| 2026-04-15 | 하네스 실행 — 4인 팀 자율 협업으로 `하네스_대중화_제안서.md` (루트, 53KB/~680줄) 산출. critical-reviewer 22개 이슈(Blocker 3/Major 12/Minor 7) 제기 → 리비전 2회(은유 v2.1, 학습경로 Rev.3) → 최종 PASS Sign-off. 중심 은유 "주방 브리게이드" 채택, 오개념 15~18종, 1분/3분/10분/1시간 구성안 + 미해결 리스크 6건 투명 명기 | 산출물 (팀/스킬 변경 없음) | 사용자 요청: "일반 대중이 아주 쉽게 이해하도록 자료 정리·보고서 작성" |
| 2026-04-16 | 시각 제작 하네스 확장 — 4인 추가(visual-art-director/comic-scripter/slide-architect/visual-producer) + `harness-visual-production` 오케스트레이터. 만화 시리즈(HTML+PDF) + 슬라이드(PPTX+HTML) 제작. 스타일: 손그림 doodle, 크림색 종이, 파스텔, 색연필·마카 | agents/ 4파일 + skills/harness-visual-production/ | 사용자 요청: "제안서 기반 만화 시리즈 + 10장 슬라이드 제작" |
| 2026-04-16 | 시각 제작 하네스 실행 — 4인 팀 Phase1~4 완주. 36개 이미지(만화 26패널 + 슬라이드 10장) 100% 생성(실패 0, 재시도 1건). 산출물: `만화_하네스이해/`(HTML), `만화_하네스이해.pdf`(4.4MB), `하네스_대중화_슬라이드.pptx`(26MB), `하네스_대중화_슬라이드.html`. 5에피소드(EP1 문제인식→EP2 주방 은유→EP3 스킬·하네스→EP4 기억 휘발→EP5 일상 전이) + 10슬라이드(표지→훅→문제→은유→매핑→경로→오개념→전이→정리→다음). 오개념 교정 패널 3개(M3/M5/M6/M10/M14/M18) 삽입. 캐릭터 색상 키 일관 유지(Ana coral/헤드셰프 mustard+sage/소스 coral/디저트 lavender/플레이터 sky blue) | 산출물 (팀/스킬 변경 없음) | 사용자 요청: "진행시켜" |
| 2026-04-16 | 저자 크레딧 일괄 변경: "하네스 대중화 팀" → "황민호(revfactory@gmail.com)". 제안서·만화 HTML·슬라이드 HTML·PPTX·PDF 빌드 스크립트 6파일 수정 후 PPTX/PDF 재빌드 | 외부 산출물 (내부 팀 정의 제외) | 사용자 요청 |
| 2026-04-16 | 만화 PDF 다국어 버전 추가 — `build_comic_pdf_multilang.py` 신설. KO/EN/JA 전용 폰트(AppleSDGothicNeo / Helvetica / ヒラギノ角ゴシック W3)와 에피소드·패널 번역 데이터를 내장. 산출물: `만화_하네스이해.pdf`(KO, 4.4MB) + `Harness_Comic_EN.pdf`(EN, 4.5MB) + `漫画_ハーネス理解_JP.pdf`(JP, 4.5MB). 이미지는 공통 사용, 제목/대사/나레이션/푸터 텍스트만 언어별 치환 | 산출물 | 사용자 요청: "pdf 일본어·영어 버전 추가" |
| 2026-04-16 | 슬라이드 HTML 개편 + 다국어 버전 — `하네스_대중화_슬라이드.html` 삭제, `index.html`로 재생성. `build_slides_html_multilang.py` 신설(템플릿+번역 데이터 분리). 산출물: `index.html`(KO) + `index_EN.html` + `index_JA.html`. 우상단 언어 스위처(🇰🇷/🇺🇸/🇯🇵), 언어별 UI 라벨(이전/다음/노트 버튼·발표자 노트 제목·도움말), `<html lang>` 속성, 언어별 웹폰트(Gaegu/Kalam/Shippori Mincho) 자동 스위칭. 10슬라이드 × 3언어 전부 번역(제목·메시지·불릿·발표자 노트) | 산출물 + agents/visual-producer.md 경로 갱신 + SKILL.md 경로 갱신 | 사용자 요청: "하네스_대중화_슬라이드.html 를 index.html 로 만들고 이것도 일본어와 영어 버전 추가" |
