---
name: harness-for-everyone
description: "하네스 엔지니어링을 일반 대중이 개념적으로 이해할 수 있도록 설명·학습 자료를 설계하는 오케스트레이터. 하네스 쉽게 설명, 하네스 개념 이해, 하네스 진입장벽(이해 차원), 일반인 하네스 설명, 하네스 교육 자료, 하네스 학습 경로, 하네스 은유, 하네스 용어집, AI 에이전트 개념 대중화, 비전문가 대상 하네스 설명 관련 초기 요청 시 반드시 이 스킬을 사용. 후속 작업: 제안서 수정, 재실행, 업데이트, 보완, 다시 실행, 이전 결과 개선, 특정 섹션만 다시, 은유·학습경로·비판 영역별 부분 재실행 요청 시에도 반드시 이 스킬을 사용. 단, 제품·UX·요금제·비용 설계·터미널 대체 인터페이스 제작 요청은 본 스킬의 범위가 아니며 거절하거나 범위 재정의를 요청한다."
---

# Harness For Everyone — 하네스 이해 전달 오케스트레이터

하네스 엔지니어링을 일반 대중이 **개념적으로 이해**할 수 있도록 개념 번역·학습 경로 설계·비판적 검토·통합의 4단계로 설명·학습 자료 제안서를 생성하는 통합 스킬. 본 스킬은 제품을 만들지 않고, 비용·요금·터미널 대체 UX를 설계하지 않는다.

## 범위 가드

다음 요청은 본 스킬의 범위 밖이다. 요청이 들어오면 팀을 구성하지 않고 사용자에게 범위 재정의를 요청한다:
- 터미널·CLI 의존성을 제거한 하네스 제품 설계
- 요금제·비용 아키텍처·MAX 대안 BM 설계
- 하네스 기술 실행 환경(브라우저 런타임·서버리스 등) 아키텍처 설계
- 하네스 앱·메신저 봇·웹 대시보드 UX 설계

본 스킬은 오직 "하네스라는 개념을 일반 대중이 이해하도록 돕는 설명·학습 자료"만 산출한다.

## 실행 모드: 에이전트 팀

4명의 전문가(3명 팀원 + 1명 리드)가 `TeamCreate` + `SendMessage` + `TaskCreate`로 자체 조율하며 단일 제안서를 산출.

## 에이전트 구성

| 팀원 | 에이전트 타입 | 모델 | 역할 | 출력 |
|------|-------------|------|------|------|
| concept-translator | 커스텀 | opus | 하네스 개념을 일반인 은유·설명 레이어로 번역 | `_workspace/01_concept_translator_metaphors.md` |
| learning-experience-designer | 커스텀 | opus | 개념 지도·3단 학습 경로·오개념 카탈로그 설계 | `_workspace/02_learning_experience_designer_curriculum.md` |
| critical-reviewer | 커스텀 | opus | 악마의 대변인·전달 실패 시나리오·오개념 유발 지적 | `_workspace/03_critical_reviewer_redteam.md` |
| synthesis-lead (리더) | 커스텀 | opus | 통합·최종 제안서 작성 | `_workspace/04_synthesis_lead_proposal.md` + `하네스_대중화_제안서.md` |

## 워크플로우

### Phase 0: 컨텍스트 확인 (후속 작업 지원)

1. 사용자 요청이 범위 가드에 해당하는지 먼저 확인. 해당하면 팀 구성 중단 후 사용자에게 범위 재정의 요청
2. 작업 디렉토리의 `_workspace/` 디렉토리 존재 여부 확인
3. 실행 모드 결정:
   - **`_workspace/` 미존재** → 초기 실행. Phase 1로 진행
   - **`_workspace/` 존재 + 사용자가 부분 수정 요청** (예: "은유 2번 수정", "학습 경로 보완", "비판 다시") → **부분 재실행**. 해당 팀원만 재호출, 이전 산출물을 입력으로 제공
   - **`_workspace/` 존재 + 새 입력 제공** (예: 새 타겟·전면 재검토) → **새 실행**. 기존 `_workspace/`를 `_workspace_{YYYYMMDD_HHMMSS}/`로 이동 후 Phase 1 진행

### Phase 1: 준비
1. 사용자 입력 분석 — (a) 타겟 대상 언급 여부 (b) 전달 길이(1분/3분/10분/1시간 등) (c) 톤 요구 (d) 특별히 강조할 축(은유/학습경로/오개념/비판)
2. 작업 디렉토리에 `_workspace/` 생성 (초기 실행 시)
3. 사용자 입력 원문을 `_workspace/00_input/user_request.md`에 저장
4. 타겟이 미지정이면 기본 가정 사용 — "한국 기반, 디지털 친숙도 중간 이상의 일반 성인, 1시간 이내 이해 가능 분량"

### Phase 2: 팀 구성

```
TeamCreate(
  team_name: "harness-understanding-team",
  members: [
    { name: "concept-translator", agent_type: "concept-translator", model: "opus",
      prompt: "하네스 이해 팀의 개념 번역 담당. .claude/agents/concept-translator.md 전부 준수. 사용자 입력: _workspace/00_input/user_request.md 참조. metaphor-library 스킬을 반드시 참조. 최종 출력: _workspace/01_concept_translator_metaphors.md" },
    { name: "learning-experience-designer", agent_type: "learning-experience-designer", model: "opus",
      prompt: "학습 경로 담당. .claude/agents/learning-experience-designer.md 전부 준수. concept-translator의 은유를 수신하여 학습 단계에 매핑. 최종 출력: _workspace/02_learning_experience_designer_curriculum.md" },
    { name: "critical-reviewer", agent_type: "critical-reviewer", model: "opus",
      prompt: "악마의 대변인. .claude/agents/critical-reviewer.md 전부 준수. 다른 2명의 산출물이 완성되면 교차 검토. 제품·UX·비용 관련 지적은 범위 밖이므로 제외. 최종 출력: _workspace/03_critical_reviewer_redteam.md" },
    { name: "synthesis-lead", agent_type: "synthesis-lead", model: "opus",
      prompt: "팀 리드. .claude/agents/synthesis-lead.md 전부 준수. 3명 산출물 전체 통합. 범위 가드 적용(제품·UX·비용 언급은 '범위 외' 섹션으로 분리). 최종 출력: _workspace/04_synthesis_lead_proposal.md + 하네스_대중화_제안서.md" }
  ]
)

TaskCreate(tasks: [
  { title: "개념 은유·설명 레이어 초안", assignee: "concept-translator" },
  { title: "학습 경로·오개념 카탈로그 초안", assignee: "learning-experience-designer", depends_on: ["개념 은유·설명 레이어 초안"] },
  { title: "교차 비판 검토", assignee: "critical-reviewer", depends_on: ["개념 은유·설명 레이어 초안", "학습 경로·오개념 카탈로그 초안"] },
  { title: "팀 피드백 반영 리비전", assignee: "concept-translator", depends_on: ["교차 비판 검토"] },
  { title: "팀 피드백 반영 리비전", assignee: "learning-experience-designer", depends_on: ["교차 비판 검토"] },
  { title: "최종 제안서 통합", assignee: "synthesis-lead", depends_on: ["팀 피드백 반영 리비전"] }
])
```

### Phase 3: 탐색·초안 (팀원 자체 조율)

**실행 방식:** 의존성 순서에 따라 팀원들이 작업 요청(claim) → 독립 수행 → 완료 시 파일 저장 + 리더 알림.

**팀원 간 통신 규칙:**
- concept-translator의 은유 초안 완료 → learning-experience-designer에게 SendMessage (은유를 학습 단계에 매핑 요청)
- learning-experience-designer의 학습 경로 초안 완료 → concept-translator에게 SendMessage (은유 공백 피드백)
- 팀원 간 상충 발견 시 SendMessage로 직접 조율, 불일치 지속 시 synthesis-lead에게 에스컬레이션

### Phase 4: 교차 비판 검토

1. concept-translator / learning-experience-designer 2명의 산출물이 모두 완료되면 critical-reviewer 진입
2. critical-reviewer는 2개 산출물을 Read → 교차 검토 → Blocker/Major/Minor 등급으로 이슈 정리
3. 범위 외(제품·UX·비용) 지적은 자체적으로 제외
4. 각 팀원에게 SendMessage로 해당 이슈 개별 전달
5. critical-reviewer의 최종 보고서 `_workspace/03_critical_reviewer_redteam.md` 생성

### Phase 5: 피드백 반영 리비전

1. 각 팀원이 critical-reviewer의 지적을 반영하여 자기 산출물 수정
2. 반박이 있으면 SendMessage로 critical-reviewer와 조율
3. 합의 불가 상충은 "양안 병기" 표시하여 synthesis-lead에게 판단 위임

### Phase 6: 최종 제안서 통합

1. synthesis-lead가 모든 수정된 산출물과 팀 토론 로그를 Read
2. 상충 조정 → 단일 내러티브로 통합
3. 범위 가드 적용: 제품·UX·비용 관련 내용이 섞여 들어왔으면 "범위 외" 섹션으로 이동
4. `_workspace/04_synthesis_lead_proposal.md` 생성 후 모든 팀원에게 회람
5. 팀원 최종 확인 → 필요 시 synthesis-lead가 수정
6. critical-reviewer의 최종 Sign-off 확보 (Blocker 해결 여부)
7. 사용자 최종 산출물 `하네스_대중화_제안서.md`를 작업 디렉토리 루트에 저장

### Phase 7: 정리

1. 팀원들에게 종료 요청 (SendMessage)
2. `TeamDelete("harness-understanding-team")`
3. `_workspace/` 보존 (감사 추적·후속 재실행용)
4. 사용자에게 결과 요약 보고 — 제안서 파일 경로 + TL;DR 3문장 + 의사결정 요청 3개

### Phase 8: 피드백 수집 (진화 루프)

1. 사용자에게 피드백 요청 — "개선할 섹션이 있나요? 팀 구성이나 워크플로우에 바꿀 점이 있나요?"
2. 피드백 수령 시 유형 판단:
   - 결과물 품질 → 해당 에이전트의 정의 파일 수정
   - 팀 구성 → 오케스트레이터 + 에이전트 추가/병합
   - 트리거 누락 → description 확장
   - 범위 이탈 → 범위 가드 문서 강화
3. 변경 이력을 CLAUDE.md의 변경 이력 테이블에 기록

## 데이터 흐름

```
[synthesis-lead/리더]
    ├── TeamCreate(4명)
    ├── TaskCreate(의존성 그래프)
    │
    ├→ concept-translator ──SendMessage──→ learning-experience-designer
    │                         ↑      │
    │                         │      ↓
    │                         └── 02_learning_experience_designer_curriculum.md
    │
    ├→ critical-reviewer ──Read──→ 01~02 전부
    │                    │
    │                    ├── SendMessage ──→ 2명 (이슈 개별 전달, 범위 외 제외)
    │                    ↓
    │              03_critical_reviewer_redteam.md
    │
    ├→ 2명 리비전 ──→ 01~02 업데이트
    │
    └→ synthesis-lead ──Read──→ 01~03 전부
                      │
                      ↓  (범위 가드 적용)
              04_synthesis_lead_proposal.md
                      │
                      ↓
              하네스_대중화_제안서.md (최종)
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 사용자 요청이 범위 가드에 걸림(제품/UX/비용 요구) | 팀 구성 중단, 사용자에게 범위 재정의 요청 ("이 하네스는 하네스 개념의 이해·설명 자료 생성만 담당합니다. 제품/UX/비용 설계는 별도 하네스가 필요합니다.") |
| 팀원 1명이 산출물 미완료 | synthesis-lead가 감지 → SendMessage로 상태 확인 → 재시작 또는 대체 가정으로 해당 섹션 표시 |
| critical-reviewer가 다수 Blocker 발견 | Phase 5 반복 — 해결되지 않으면 "미해결 리스크" 섹션으로 제안서에 명시 |
| 팀원 간 상충 지속 | 양안 병기 + 의사결정권자 판단 요청 문구 포함 |
| 타임아웃 | 현재까지 수집된 산출물로 Phase 6 진행, 누락 명시 |
| 반복 재실행 요청 | Phase 0에서 부분/전체 재실행 분기, 이전 산출물은 `_workspace_{timestamp}/`로 백업 |
| 팀원 산출물에 제품·UX·비용 내용이 섞임 | synthesis-lead가 "범위 외" 섹션으로 분리, 본문에서 제거 |

## 테스트 시나리오

### 정상 흐름
1. 사용자가 "하네스라는 개념을 일반인도 이해할 수 있게 설명 자료를 만들어달라" 요청
2. Phase 1에서 기본 타겟(한국, 디지털 친숙 중 이상 성인) 가정
3. Phase 2에서 4인 팀 구성 + 6개 작업 등록
4. Phase 3~5에서 팀원들이 자체 조율하며 산출물 생성·리비전
5. Phase 6에서 synthesis-lead가 통합 제안서 작성
6. Phase 7에서 팀 정리 및 `하네스_대중화_제안서.md` 생성
7. Phase 8에서 피드백 수집

### 범위 가드 흐름
1. 사용자가 "하네스를 카카오톡 봇으로 만들어서 대중화하자"고 요청
2. Phase 0에서 범위 가드 적용 — 팀 구성 중단
3. 사용자에게 "이 하네스는 개념 이해·설명 자료만 생성합니다. 제품·봇 설계가 필요하면 별도 하네스 구축을 권장합니다"라고 안내
4. 사용자가 범위를 이해 중심으로 재정의하면 재진입

### 에러 흐름
1. Phase 4에서 critical-reviewer가 "은유 A가 AI 자율성 과신을 유발" Blocker 지적
2. concept-translator에게 SendMessage로 전달
3. concept-translator가 은유 수정 또는 실패 지점 명시 강화 → 재제출
4. critical-reviewer가 재검토 → Blocker 해소 확인
5. Phase 6 진입 → 최종 제안서에 "오개념 카탈로그" 섹션 강화 반영

### 부분 재실행 흐름
1. 사용자가 "학습 경로만 중장년층 관점으로 다시 써줘" 요청
2. Phase 0에서 `_workspace/` 존재 확인 → 부분 재실행 판정
3. learning-experience-designer 재호출, 이전 산출물 + "중장년층 관점" 지시 제공
4. synthesis-lead가 제안서의 학습 여정 섹션만 교체 후 재저장

## 후속 작업 트리거

이 스킬은 다음 후속 요청에도 반드시 트리거되어야 한다:
- "제안서 다시 써줘", "이해 제안서 업데이트"
- "{섹션명}만 다시" (예: "은유만 다시", "오개념 카탈로그 보완")
- "{타겟 추가} 반영해줘" (예: 초중고생용, 시니어용)
- "{비판 지적} 반영해서 개선"
- "하네스 쉬운 설명", "하네스 개념 이해", "일반인용 설명"

다음 요청은 범위 밖이므로 거절 또는 범위 재정의 요청:
- "카카오톡/슬랙에서 쓰는 하네스" (제품 설계)
- "월 얼마로 대중화" (비용 설계)
- "노코드 하네스 만들어줘" (제품 설계)
