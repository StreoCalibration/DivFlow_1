"""Windows용 실행 파일을 생성하는 빌드 스크립트."""

import PyInstaller.__main__


if __name__ == "__main__":
    PyInstaller.__main__.run(
        [
            "--onedir",  # 단일 아카이브 대신 디렉터리 모드 사용
            "--name",
            "DivFlow",
            "main.py",
        ]
    )
