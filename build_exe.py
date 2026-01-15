import os
import shutil
import subprocess

def clean():
    """Очистка старых файлов"""
    folders = ['build', 'dist']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Cleaned {folder}/")

def build():
    """Сборка EXE"""
    print("Building PathOfCount.exe...")
    result = subprocess.run([
        'pyinstaller',
        'PathOfCount.spec',
        '--clean',
        '--noconfirm'
    ])
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print(f"EXE location: {os.path.abspath('dist/PathOfCount.exe')}")
    else:
        print("\n✗ Build failed!")
        return False
    
    return True

def create_release():
    """Создание папки релиза"""
    release_dir = 'release'
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Копируем EXE
    shutil.copy('dist/PathOfCount.exe', release_dir)
    
    # Копируем README
    shutil.copy('README.md', release_dir)
    
    print(f"\n✓ Release package created in {release_dir}/")

if __name__ == '__main__':
    print("=== PathOfCount Build Script ===\n")
    
    clean()
    
    if build():
        create_release()
        print("\n=== Build Complete ===")
    else:
        print("\n=== Build Failed ===")