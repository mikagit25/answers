#!/usr/bin/env python3
"""
Script для проверки настройки проекта.
Проверяет зависимости, подключение к БД и структуру файлов.
"""
import sys
from pathlib import Path


def check_python_version():
    """Проверка версии Python"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Проверка установленных зависимостей"""
    print("\n📦 Checking dependencies...")
    required_packages = [
        'fastapi',
        'sqlalchemy',
        'pgvector',
        'langchain',
        'sentence_transformers',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing packages: pip install {' '.join(missing)}")
        return False
    return True


def check_project_structure():
    """Проверка структуры проекта"""
    print("\n📁 Checking project structure...")
    root = Path(__file__).parent
    
    required_files = [
        'backend/main.py',
        'backend/core/config.py',
        'backend/db/models.py',
        'backend/rag/pipeline.py',
        'frontend/package.json',
        'frontend/app/page.tsx',
        'docker-compose.yml',
        'knowledge_base/metadata.json',
    ]
    
    missing = []
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            missing.append(file_path)
    
    if missing:
        print(f"\nMissing files: {', '.join(missing)}")
        return False
    return True


def check_env_file():
    """Проверка .env файла"""
    print("\n⚙️  Checking environment configuration...")
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("❌ .env file not found. Copy .env.example to .env and configure it.")
        return False
    
    print("✓ .env file exists")
    
    # Проверка наличия ключевых переменных
    with open(env_file, 'r') as f:
        content = f.read()
    
    required_vars = ['DATABASE_URL', 'QWEN_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✓ Required environment variables present")
    return True


def main():
    """Запуск всех проверок"""
    print("=" * 60)
    print("Answers Platform - Setup Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_project_structure(),
        check_env_file(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! Project is ready to run.")
        print("\nNext steps:")
        print("1. Start databases: docker-compose up -d")
        print("2. Import data: python ingest.py")
        print("3. Run backend: uvicorn main:app --reload")
        print("4. Run frontend: cd ../frontend && npm run dev")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
