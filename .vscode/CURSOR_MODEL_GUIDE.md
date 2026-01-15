# Cursor AI 모델 선택 가이드

## 📋 현재 워크스페이스 설정

이 프로젝트는 **소규모 아키텍처** (19파일, 1,359줄):
- **Composer**: `claude-sonnet-4` (균형잡힌 선택, 권장)
- **Cmd+K**: `gpt-4o-mini` (빠른 편집)
- **Background**: `gpt-4o-mini` (비용 효율)

**참고**: 다른 모델 옵션은 아래 "제 조언" 섹션 참조

---

## 🏗️ 복잡한 아키텍처 프로젝트를 위한 모델 선택 전략

### 1. **모놀리식 → 마이크로서비스 아키텍처**
```json
{
  "aiSettings": {
    "composerModel": "claude-opus-4.1",  // 복잡한 아키텍처 분석
    "cmdKModel": "gpt-4o",                // 중간 복잡도
    "backgroundComposerModel": "gpt-4o-mini"
  }
}
```
**이유**: 
- Opus는 긴 컨텍스트와 복잡한 의존성 분석에 강함
- 마이크로서비스 간 통신 패턴 이해에 우수

### 2. **Monorepo (여러 패키지/워크스페이스)**
```json
{
  "aiSettings": {
    "composerModel": "gpt-4o",            // 패키지 간 관계 이해
    "cmdKModel": "gpt-4o-mini",
    "backgroundComposerModel": "cursor-small"
  },
  // Monorepo 모드 활성화
  "cursor.monorepo.enabled": true
}
```
**이유**:
- Monorepo 모드로 여러 패키지 컨텍스트 인식
- 패키지 간 의존성 자동 추적

### 3. **레거시 코드베이스 (오래된 코드 + 새 코드 혼재)**
```json
{
  "aiSettings": {
    "composerModel": "claude-opus-4.1",    // 레거시 코드 이해
    "cmdKModel": "gpt-4o",
    "backgroundComposerModel": "gpt-4o-mini"
  }
}
```
**이유**:
- Opus는 오래된 패턴과 새로운 패턴 모두 이해
- 점진적 리팩토링 제안에 강함

### 4. **멀티모달 프로젝트 (이미지/비디오 처리)**
```json
{
  "aiSettings": {
    "composerModel": "gpt-4o",             // 멀티모달 지원
    "cmdKModel": "gpt-4o-mini",
    "backgroundComposerModel": "gpt-4o-mini"
  },
  "mcpServers": {
    "image-analysis": {
      "command": "npx imagegen-mcp",
      "env": {
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  }
}
```
**이유**:
- GPT-4o는 이미지/코드 동시 분석 가능
- MCP 서버로 추가 모달리티 지원

### 5. **대규모 팀 프로젝트 (엄격한 코드 리뷰 필요)**
```json
{
  "aiSettings": {
    "composerModel": "claude-opus-4.1",    // 엄격한 코드 품질
    "cmdKModel": "gpt-4o",
    "backgroundComposerModel": "gpt-4o-mini"
  }
}
```
**이유**:
- Opus는 코드 품질과 보안 이슈를 더 잘 발견
- 팀 코딩 컨벤션 준수에 강함

---

## 🎯 모델별 특징 비교

| 모델 | 속도 | 정확도 | 컨텍스트 | 비용 | 추천 용도 |
|------|------|--------|----------|------|-----------|
| **cursor-small** | ⚡⚡⚡ | ⭐⭐ | 32K | 💰 | 빠른 편집, 간단한 작업 |
| **gpt-4o-mini** | ⚡⚡ | ⭐⭐⭐ | 128K | 💰💰 | 중간 복잡도, 비용 효율 |
| **gpt-4o** | ⚡ | ⭐⭐⭐⭐ | 128K | 💰💰💰 | 복잡한 코드, 멀티모달 |
| **claude-opus-4.1** | ⚡ | ⭐⭐⭐⭐⭐ | 200K | 💰💰💰💰 | 매우 복잡한 아키텍처, 레거시 |

---

## 💡 제 조언

### ✅ **현재 프로젝트 (소규모 아키텍처)**

**현재 프로젝트 규모**: 19개 파일, 약 1,359줄

**현재 설정**:
- `gpt-5.1-codex-max` (Composer): 최신 프론티어 모델 사용
- `gpt-4o-mini` (Cmd+K): 빠른 편집

**제 조언**:
- ⚠️ **현재 프로젝트 규모에서는 과함**: 소규모 프로젝트이므로 `gpt-5.1-codex-max`는 크레딧 낭비
- ✅ **권장 설정 (다양한 모델 옵션)**:
  ```json
  {
    "composerModel": "claude-sonnet-4",  // 가장 균형잡힌 선택 (권장)
    // 또는
    "composerModel": "gpt-4o",           // 멀티모달 필요 시
    // 또는
    "composerModel": "gpt-4o-mini",      // 비용 절감
    "cmdKModel": "gpt-4o-mini"            // 빠른 편집
  }
  ```
- 💡 **모델별 추천**:
  - **Claude Sonnet 4**: 일반 코딩 작업에 최적 (가장 권장)
  - **GPT-4o**: 멀티모달 필요 시
  - **GPT-4o-mini**: 비용 절감
  - **GPT-5.1-Codex-Max**: 프로젝트가 50개 파일 이상으로 확장될 때만

### ✅ **복잡한 아키텍처 프로젝트**
다음 설정을 권장합니다:
```json
{
  "composerModel": "gpt-5.1-codex-max",  // 최고 성능
  "cmdKModel": "gpt-4o",
  "backgroundComposerModel": "gpt-4o-mini"
}
```

**선택 기준**:
- **GPT-5.1-Codex-Max**: 🏆 최고 성능, 대규모 프로젝트, 자율 작업, 프론티어 코딩
- **Claude Opus**: 매우 복잡한 아키텍처, 긴 컨텍스트 필요, 레거시 코드
- **GPT-4o**: 멀티모달 필요, 빠른 응답 중요, 비용 고려

### ✅ **멀티모달 체크박스 활용**
- ✅ **활성화 권장**: 이미지/다이어그램 분석, 코드+이미지 동시 작업
- ❌ **비활성화**: 순수 텍스트/코드만 작업하는 경우

---

## 🔄 워크스페이스별 설정 방법

각 프로젝트의 `.vscode/settings.json`에 위 설정을 복사하면 됩니다.

**전역 설정** (모든 프로젝트에 적용):
- Cursor Settings → AI Settings에서 설정
- 또는 `~/.config/Cursor/User/settings.json` 수정

**워크스페이스 설정** (현재 프로젝트만):
- `.vscode/settings.json` 파일 사용 (현재 파일)
- 전역 설정보다 우선순위 높음

---

## 📝 설정 변경 방법

1. **Cursor UI에서**:
   - `Cmd/Ctrl + ,` → Settings
   - "AI Settings" 검색
   - 모델 선택

2. **직접 파일 수정**:
   - `.vscode/settings.json` 편집
   - Cursor 재시작 (필요시)

---

## ⚠️ 주의사항

### 💰 **Cursor Pro 구독료와 모델 사용 비용**

**중요**: Cursor Pro를 구독하면 ($20/월):
- ✅ **모든 모델 선택 가능** (gpt-4o, gpt-5.1-codex-max, claude-opus 등)
- ✅ **$20 크레딧 포함** (매월 초기화)
- ⚠️ **비싼 모델 사용 시 크레딧 빠르게 소진**

**구체적 예시**:
- `gpt-4o-mini`: 크레딧 소진 느림 (일반 사용 시 $20로 충분)
- `gpt-4o`: 크레딧 소진 중간 (적당한 사용량)
- `gpt-5.1-codex-max`: 크레딧 소진 빠름 (복잡한 작업 시 며칠 내 소진 가능)

**추가 비용 발생 시**:
- 크레딧 소진 후에도 계속 사용 가능 (Usage-based pricing)
- 추가 사용량에 대해 별도 과금
- 또는 다음 달까지 대기 (크레딧 초기화 대기)

**결론**: 
- ✅ Cursor Pro 구독료 안에서 모델 선택 가능
- ⚠️ 비싼 모델을 많이 사용하면 추가 비용 발생 가능
- 💡 **현재 프로젝트 수준(19파일, 1,359줄)**: `gpt-4o` 또는 `gpt-4o-mini`로도 충분

---

### 📊 **프로젝트 규모별 모델 추천**

| 프로젝트 규모 | 파일 수 | 코드 라인 | 추천 모델 |
|--------------|---------|-----------|-----------|
| **소규모** | 1-20개 | ~2,000줄 | `gpt-4o-mini` |
| **중규모** | 20-50개 | 2,000-10,000줄 | `gpt-4o` |
| **대규모** | 50-200개 | 10,000-50,000줄 | `gpt-5.1-codex-max` |
| **초대규모** | 200개+ | 50,000줄+ | `gpt-5.1-codex-max` (필수) |

**현재 프로젝트**: 소규모 → `gpt-4o-mini` 또는 `gpt-4o` 권장

---

### 🎯 **속도 vs 정확도**

- **빠른 작업**: `gpt-4o-mini` 또는 `cursor-small`
- **정확한 작업**: `gpt-5.1-codex-max` 또는 `claude-opus-4.1`

### 📏 **컨텍스트 크기**

- **작은 프로젝트** (현재 수준): `gpt-4o-mini` 충분
- **큰 프로젝트**: `gpt-5.1-codex-max` (수백만 토큰 지원)
- **매우 큰 프로젝트**: `gpt-5.1-codex-max` + compaction 기술 활용

### 🖼️ **멀티모달**

- 이미지 분석이 필요할 때만 활성화

### 🔧 **GPT-5.1-Codex-Max 특별 주의사항**

- Reasoning effort 설정으로 성능/비용 조절 가능
- 장시간 자율 작업 시 주기적인 검토 필요
