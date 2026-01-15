# Cursor Pro 비용 관리 가이드

## 🛡️ 추가 비용 방지 설정 (필수!)

### ⚠️ 중요: Cursor는 기본적으로 자동 결제가 설정되어 있을 수 있습니다!

---

## ✅ 추가 비용 방지 방법

### 1. **Usage-based Pricing 비활성화** (가장 안전)

**⚠️ 주의**: 이 설정은 **Cursor 웹 대시보드**에서 확인해야 합니다!

**설정 경로 (웹 대시보드)**:
1. 브라우저에서 [cursor.com](https://cursor.com) 접속
2. 로그인
3. **Settings** → **Advanced Account Settings** 또는 **Usage / Billing**
4. **Usage-based Pricing** 또는 **"Opt Out of New Pricing"** 찾기
5. **OFF**로 설정

**또는 Cursor IDE 내부에서**:
1. Cursor IDE 열기
2. `Cmd/Ctrl + ,` → Settings
3. **"Billing"** 또는 **"Usage"** 검색
4. **Usage-based Pricing** 찾기
5. **OFF**로 설정

**⚠️ 문제**: 설정이 보이지 않는 경우
- Cursor IDE 내부에서는 보이지 않을 수 있음
- **반드시 웹 대시보드에서 확인** 필요
- UI 버그로 인해 설정이 숨겨져 있을 수 있음

**효과**:
- ✅ 크레딧($20) 소진 시 자동으로 차단됨
- ✅ 클로드코드 AI처럼 시간 텀을 주거나 확인 메시지 표시
- ✅ 추가 비용 발생 없음
- ✅ 다음 달까지 대기 (크레딧 초기화 대기)

**권장**: 이 방법을 사용하세요!

---

### 2. **Spending Limit 설정** (사용하되 제한)

**설정 경로**:
- Cursor 웹 대시보드 → Settings → Billing
- 또는 Cursor IDE → Settings → Billing
- Spending Limit 설정
- 원하는 금액 입력 (예: $0, $10, $20)

**주의사항**:
- ⚠️ 기본값: $50 (설정이 리셋될 수 있음)
- ⚠️ Usage-based pricing을 켜면 기본값이 $50로 변경될 수 있음
- ✅ 설정 변경 후 **반드시 저장** 확인
- ✅ 주기적으로 설정 확인 (리셋 방지)

**효과**:
- 한도 도달 시 자동 차단
- 추가 비용 발생 방지

---

### 3. **사용량 모니터링**

**확인 경로**:
- Cursor 웹 대시보드 → Settings → Usage
- 또는 Cursor IDE → Settings → Usage
- 현재 사용량 확인
- 크레딧 소진 시 알림 표시
- 한도 도달 전 경고 메시지

**권장**:
- 주 1회 사용량 확인
- 크레딧 50% 소진 시 모델 다운그레이드 고려

---

## 🔍 설정을 찾을 수 없는 경우

### 문제 해결 방법:

1. **웹 대시보드 확인** (가장 확실)
   - [cursor.com](https://cursor.com) 접속
   - 로그인 → Settings → Advanced Account Settings
   - 여기서는 반드시 보여야 함

2. **Cursor IDE 내부 확인**
   - `Cmd/Ctrl + ,` → Settings
   - 검색창에 "billing", "usage", "pricing" 검색
   - 여러 섹션 확인

3. **최신 정보 확인**
   - 일부 사용자는 더 이상 opt-out 옵션이 없다고 함
   - 이 경우 Spending Limit을 $0으로 설정하는 것이 대안

4. **고객 지원 문의**
   - 설정을 찾을 수 없으면 Cursor 고객 지원에 문의
   - support@cursor.com 또는 공식 포럼

---

## ⚠️ 주의사항

### 자동 결제 방지
- ✅ **Usage-based pricing OFF**: 가장 안전 (웹 대시보드에서 확인)
- ✅ **Spending Limit $0**: 추가 비용 없음
- ⚠️ 설정이 리셋되지 않도록 주기적으로 확인

### 크레딧 소진 시
- ✅ 자동 차단됨 (Usage-based pricing OFF인 경우)
- ✅ 다음 달까지 대기
- ⚠️ 또는 추가 결제 선택 가능 (확인 메시지 표시)

### 최신 정책 변경
- ⚠️ Cursor가 정책을 변경하여 opt-out 옵션이 없을 수 있음
- ✅ 이 경우 Spending Limit을 $0으로 설정
- ✅ 사용량 모니터링을 주기적으로 확인

---

## 💡 비용 절감 팁

1. **가벼운 모델 사용**
   - 일반 작업: `claude-sonnet-4` 또는 `gpt-4o-mini`
   - 빠른 작업: `cursor-small` 또는 `claude-haiku`

2. **필요할 때만 프리미엄 모델 사용**
   - 대규모 리팩토링: `claude-opus-4` 또는 `gpt-5.1-codex-max`
   - 일반 작업: `claude-sonnet-4`

3. **사용량 모니터링**
   - 주기적으로 Usage 확인
   - 크레딧 소진 시 모델 다운그레이드

---

## 📋 설정 체크리스트

- [ ] **웹 대시보드에서 Usage-based pricing OFF 확인** (가장 중요!)
- [ ] Spending Limit 설정 확인 ($0 권장)
- [ ] 사용량 모니터링 설정
- [ ] 주기적으로 설정 확인 (리셋 방지)

---

## 🔗 관련 링크

- Cursor 웹 대시보드: https://cursor.com (로그인 필요)
- Cursor Settings: `Cmd/Ctrl + ,` → Billing
- Usage 확인: Settings → Usage
- 공식 문서: https://docs.cursor.com/account/rate-limits

---

## 💬 설정을 찾을 수 없는 경우

**다음 정보를 확인하세요**:
1. Cursor Pro 구독 상태 확인
2. 웹 대시보드에서 Settings → Advanced Account Settings 확인
3. Cursor IDE 버전 확인 (최신 버전인지)
4. 고객 지원 문의

**임시 해결책**:
- Spending Limit을 $0으로 설정
- 사용량을 주기적으로 모니터링
- 크레딧 소진 시 모델 다운그레이드
