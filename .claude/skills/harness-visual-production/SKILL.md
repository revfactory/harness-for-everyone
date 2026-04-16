---
name: harness-visual-production
description: "하네스 대중화 제안서를 기반으로 교육용 만화 시리즈와 슬라이드 덱을 제작하는 오케스트레이터. 만화 제작, 슬라이드 제작, 교육용 인포그래픽, 하네스 시각 자료, 만화 시리즈, 교육 만화, 하네스 슬라이드, 하네스 프레젠테이션, 하네스 발표 자료, 교육 자료 시각화, 만화로 설명, 그림으로 설명 요청 시 반드시 이 스킬을 사용. 후속: 만화 수정, 슬라이드 수정, 스타일 변경, 에피소드 추가, 패널 재생성, 이미지 재생성, 슬라이드 업데이트 요청 시에도 사용. 단, 텍스트 제안서 작성은 harness-for-everyone 스킬이 담당."
---

# Harness Visual Production — 하네스 대중화 시각 자료 제작 오케스트레이터

하네스 대중화 제안서(`하네스_대중화_제안서.md`)를 기반으로 교육용 만화 시리즈 + 슬라이드 덱을 실제 제작하는 스킬.

## 범위 가드
- 텍스트 제안서 작성/수정 → `harness-for-everyone` 스킬로 안내
- 제품 UX/요금/기술 아키텍처 → 범위 외, 거절

## 실행 모드: 하이브리드 (서브 에이전트 순차 → 병렬)

이미지 생성은 순차적 품질 통제가 필요하고, 만화·슬라이드 스크립팅은 병렬 가능. 팀 통신 오버헤드보다 파이프라인 효율이 우선.

## 에이전트 구성

| 에이전트 | 타입 | Phase | 역할 |
|---------|------|-------|------|
| visual-art-director | 커스텀, opus | 1 | 스타일 바이블 수립 |
| comic-scripter | 커스텀, opus | 2 (병렬) | 만화 스크립트 |
| slide-architect | 커스텀, opus | 2 (병렬) | 슬라이드 구조 |
| visual-producer | 커스텀, opus | 3 | 이미지 생성 + 최종 조립 |

## 워크플로우

### Phase 0: 컨텍스트 확인

1. `하네스_대중화_제안서.md` 존재 확인 → 없으면 `harness-for-everyone` 스킬 먼저 실행 안내
2. `_workspace/visual/` 존재 여부 확인:
   - 미존재 → 초기 실행
   - 존재 + 부분 수정 요청 → 해당 Phase만 재실행
   - 존재 + 새 스타일 요청 → 기존을 `_workspace/visual_{timestamp}/`로 백업 후 전체 재실행
3. 사용자 디자인 참고사항 파싱 (스타일 키워드 추출)

### Phase 1: 스타일 바이블 (서브 에이전트)

**실행 모드:** 서브 에이전트 (단일)

visual-art-director를 Agent로 스폰:
- 입력: 사용자 디자인 참고사항 + 제안서의 Hero Scenario + 캐릭터 정보
- 출력: `_workspace/visual/00_style_bible.md`
- 프롬프트 프리픽스가 반드시 영어로 포함되어야 Phase 3에서 사용 가능

### Phase 2: 스크립트 + 구조 (서브 에이전트, 병렬)

**실행 모드:** 서브 에이전트 2개 병렬 (`run_in_background: true`)

comic-scripter + slide-architect를 동시 스폰:
- 공통 입력: `하네스_대중화_제안서.md` + `_workspace/visual/00_style_bible.md`
- comic-scripter 출력: `_workspace/visual/01_comic_script.md`
- slide-architect 출력: `_workspace/visual/02_slide_structure.md`

### Phase 3: 이미지 생성 + 조립 (서브 에이전트)

**실행 모드:** 서브 에이전트 (단일, 장시간)

visual-producer를 Agent로 스폰:
- 입력: 00_style_bible + 01_comic_script + 02_slide_structure
- `gemini-3-pro-imagegen` 스킬을 활용하여 이미지 생성
- 만화: 개별 PNG → HTML 갤러리 + PDF 합본
- 슬라이드: 개별 PNG → PPTX(document-skills:pptx) + HTML 슬라이드
- 출력 디렉토리:
  - `_workspace/visual/images/` — 모든 이미지
  - `만화_하네스이해/` — HTML 웹 갤러리 (루트)
  - `만화_하네스이해.pdf` — PDF (루트)
  - `하네스_대중화_슬라이드.pptx` — PPTX (루트)
  - `index.html` — HTML 슬라이드 루트 (다국어 버전은 `index_EN.html` / `index_JA.html`)

### Phase 4: 검수 + 정리

1. 모든 산출물 파일 존재 확인
2. 이미지 생성 실패 패널 목록 보고
3. 사용자에게 결과 요약:
   - 만화: {N}개 에피소드, {M}개 패널 (성공 {S}/실패 {F})
   - 슬라이드: {N}장 (PPTX + HTML)
   - 산출물 경로 목록
4. 피드백 수집 — 스타일 변경/에피소드 추가/슬라이드 수정 요청 대응

## 데이터 흐름

```
[오케스트레이터]
    │
    ├─ Phase 1 ─→ visual-art-director
    │               └→ 00_style_bible.md
    │
    ├─ Phase 2 ─→ comic-scripter (병렬)    slide-architect (병렬)
    │               └→ 01_comic_script.md   └→ 02_slide_structure.md
    │
    ├─ Phase 3 ─→ visual-producer
    │               ├→ images/*.png
    │               ├→ 만화_하네스이해/ + .pdf
    │               └→ 슬라이드.pptx + .html
    │
    └─ Phase 4 ─→ 검수 + 사용자 보고
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 제안서 미존재 | `harness-for-everyone` 먼저 실행 안내 |
| 스타일 바이블 생성 실패 | 기본 doodle 스타일로 대체 진행 |
| 이미지 생성 부분 실패 | 성공 이미지로 진행, 실패 패널은 "[placeholder]" 표시 |
| PPTX 생성 실패 | HTML 슬라이드만 생성 |
| PDF 생성 실패 | HTML 갤러리만 생성 |

## 테스트 시나리오

### 정상 흐름
1. "제안서를 만화와 슬라이드로 만들어줘" → Phase 0~4 전체 실행
2. 5개 에피소드 × 5패널 = 25패널 + 슬라이드 10장 = 35 이미지 생성
3. 만화 HTML+PDF + 슬라이드 PPTX+HTML 모두 루트에 저장

### 부분 재실행 흐름
1. "3번 에피소드만 다시 그려줘" → Phase 3만 재실행 (해당 에피소드 패널만)
2. "슬라이드 스타일을 미니멀로 바꿔줘" → Phase 1부터 재실행 (새 스타일 바이블)
