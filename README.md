# 📘 DivFlow 개발 문서

이 문서는 DivFlow 프로젝트의 개발 아키텍처, 기능 명세, 작업 내역, Codex 프롬프트 등을 문서화한 것입니다.

## 📂 폴더 구조
- `doc/architecture/`: 시스템 설계 및 아키텍처 문서
- `doc/specs/`: 기능 명세서
- `doc/ui/`: UI 자료
- `src/`: 애플리케이션 소스 코드
  - 각 모듈 설명은 `doc/README.md` 참고


## 환경 구축
DivFlow는 파이썬 표준 라이브러리만 사용하므로 별도의 패키지 설치가 필요하지 않습니다. 가상 환경을 사용하려면 다음 명령을 실행하세요.
```bash
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
pip install -U pip
```
## 실행 방법
Python 3.8 이상이 필요합니다. 다음 명령으로 GUI 애플리케이션을 실행할 수 있습니다.

```bash
python -m src
```

`src/__main__.py` 파일을 직접 실행하면 모듈 경로가 인식되지 않아 `ImportError`
가 발생할 수 있습니다. 반드시 위와 같이 패키지 형태로 실행하세요.

포트폴리오 데이터는 저장 시 `data/portfolio.json` 파일로 관리됩니다.
애플리케이션을 처음 실행하면 `data` 폴더가 자동으로 생성됩니다.
모든 UI 텍스트는 한국어로 제공됩니다.