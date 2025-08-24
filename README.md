# 📘 DivFlow 개발 문서

이 문서는 DivFlow 프로젝트의 개발 아키텍처, 기능 명세, 작업 내역, Codex 프롬프트 등을 문서화한 것입니다.

## 📂 폴더 구조
- `doc/architecture/`: 시스템 설계 및 아키텍처 문서
- `doc/specs/`: 기능 명세서
- `doc/ui/`: UI 자료
- `src/`: 애플리케이션 소스 코드
  - 각 모듈 설명은 `doc/README.md` 참고

## 의존성
DivFlow는 다음의 외부 패키지를 사용합니다:
- `yfinance`: Yahoo Finance에서 주가 및 환율 정보를 가져오기 위해 사용

## 환경 구축
Python 3.8 이상이 필요합니다. 가상 환경을 생성하고 의존성을 설치하세요:

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 실행 방법
다음 명령으로 GUI 애플리케이션을 실행할 수 있습니다:

```bash
python -m src
```

`src/__main__.py` 파일을 직접 실행하면 모듈 경로가 인식되지 않아 `ImportError`가 발생할 수 있습니다. 반드시 위와 같이 패키지 형태로 실행하세요.

## 데이터 저장
- 포트폴리오 데이터는 저장 시 `data/portfolio.json` 파일로 관리됩니다.
- 환율 정보는 `data/exchange_rate.json` 파일에 별도로 저장됩니다.
- 애플리케이션을 처음 실행하면 `data` 폴더가 자동으로 생성됩니다.

## 주요 기능
- 모든 UI 텍스트는 한국어로 제공됩니다.
- 시세 조회 기능(`PriceFetcher`)은 `yfinance` 패키지를 이용해 Yahoo Finance 데이터로 가격과 환율을 조회합니다.
- API 호출이 실패하면 예외 메시지를 출력하고 0을 반환합니다.
- 환율과 종가 조회는 1시간 캐시를 사용하여 외부 API 호출을 최소화합니다.
- 목표 비중뿐 아니라 현재 비중도 테이블에 표시되어 포트폴리오 상황을 즉시 파악할 수 있습니다.
- 리밸런싱 계산은 남은 입금액을 반복적으로 사용하여 목표 비중에 최대한 맞춰주도록 개선되었습니다.

## Windows 실행 파일 빌드
PyInstaller의 `--onefile` 모드가 일부 환경에서 `struct.error`를 일으킬 수 있어
기본 빌드를 디렉터리 모드(`--onedir`)로 제공합니다.

```bash
pip install --upgrade pyinstaller
python build_exe.py
```

빌드가 끝나면 `dist/DivFlow/` 폴더에 실행 파일이 생성됩니다.
리소스를 정리해 크기를 줄인 뒤 단일 파일이 필요하다면 `build_exe.py`에서
`--onefile` 옵션으로 변경해 사용할 수 있습니다.
