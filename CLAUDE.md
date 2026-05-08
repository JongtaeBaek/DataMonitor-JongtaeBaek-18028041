# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 현재 작업: 1.1.3 데이터 모니터링 Tool (PoC)

**목적**: 1.1.2에서 구축한 JSON 파일에 저장된 데이터 상태를 콘솔에서 실시간 조회할 수 있는 독립 관리자 도구를 만든다. 메인 시스템(1.1.2)과 별도로 실행되는 standalone 툴이다.

Git 저장소: https://github.com/JongtaeBaek/DataMonitor-JongtaeBaek-18028041.git

**참고 — 이전 저장소**
- 1.1.1 MVC 스켈레톤: https://github.com/JongtaeBaek/ConsoleMVC-JongtaeBaek-18028041.git
- 1.1.2 데이터 영속성: https://github.com/JongtaeBaek/DataPersistence-JongtaeBaek-18028041.git

## 개발 환경

- Python 3.14 (`.venv` 가상환경)
- 앱 의존성: 표준 라이브러리만 사용
- 개발 의존성: `pytest`, `pytest-cov`

```bash
.venv\Scripts\activate
pip install pytest pytest-cov

python main.py

# 테스트 실행 (커버리지 100% 강제 + HTML 리포트 자동 산출)
pytest
```

HTML 커버리지 리포트: `htmlcov/index.html` (`pytest.ini`의 `addopts`에 고정)

## 1.1.2에서 이어받는 구조

model/과 repository/는 1.1.2와 동일하게 가져오고, `monitor/` 패키지를 신규 추가한다.

```
DataMonitor/
├── main.py              # 모니터링 툴 진입점 및 메뉴 루프
├── data/                # 1.1.2가 생성한 JSON 파일 읽기 전용 (git 제외)
│   ├── samples.json
│   └── orders.json
├── model/               # 1.1.2와 동일 (sample.py, order.py, production.py)
├── repository/          # 1.1.2와 동일 (SampleRepository, OrderRepository)
└── monitor/             # 신규: 모니터링 표시 로직
    ├── __init__.py
    └── data_monitor.py  # 저장된 데이터를 읽어 콘솔에 표시
```

## 아키텍처

```
main.py → DataMonitor → Repository → JSON 파일 (읽기 전용)
                      ↘ Model
```

- **DataMonitor**: Repository에서 데이터를 로드하여 콘솔에 표시하는 단일 책임 클래스
- **Repository**: 1.1.2와 동일한 `load()`만 사용 (이 툴에서는 `save()` 호출 없음)
- **main.py**: 메뉴 루프로 원하는 조회 항목 선택

## DataMonitor 조회 항목

| 메뉴 | 내용 |
|------|------|
| 시료 현황 | 전체 시료 목록 + 재고 수량 |
| 주문 현황 | 상태별 주문 수 (RESERVED/PRODUCING/CONFIRMED/RELEASE) |
| 재고 현황 | 시료별 재고 + 여유/부족/고갈 상태 |
| 전체 조회 | 위 3개를 한 번에 출력 |

## 1.1.2 도메인 모델 (변경 없음)

**Sample**: `sample_id`, `name`, `avg_production_time`, `yield_rate`, `stock`

**Order**: `order_id`, `sample_id`, `customer_name`, `quantity`, `status`(OrderStatus)

**OrderStatus**: `RESERVED` / `REJECTED` / `PRODUCING` / `CONFIRMED` / `RELEASE`
- REJECTED는 모니터링 제외

**JSON 파일 경로**: `data/samples.json`, `data/orders.json` (1.1.2 기준 기본 경로)

## 테스트 전략

- **목표**: 커버리지 100% (`# pragma: no cover` 사용 금지)
- **프레임워크**: `pytest` + `pytest-cov`
- **리포트**: `pytest` 실행 시 `htmlcov/index.html` 자동 생성 (`addopts` 고정)
- **DataMonitor 테스트**: Repository를 mock하여 표시 로직 검증, `capsys`로 출력 내용 확인
- `pytest.ini`에 `pythonpath = .`, `testpaths = tests` 설정
