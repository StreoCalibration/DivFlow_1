"""Windows용 실행 파일을 생성하는 빌드 스크립트"""
import PyInstaller.__main__

if __name__ == "__main__":
    PyInstaller.__main__.run([
        "--onefile",
        "--name", "DivFlow",
        "main.py",
    ])
