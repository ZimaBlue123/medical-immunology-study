@echo off
chcp 65001 >nul
echo ========================================
echo   构建Android APK
echo   Building Android APK
echo ========================================
echo.

cd /d "%~dp0"

if not exist "gradlew.bat" (
    echo 错误：未找到gradlew.bat
    echo 请确保在android目录下运行此脚本
    pause
    exit /b 1
)

echo 正在构建Debug APK...
echo.

call gradlew.bat assembleDebug

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   构建成功！
    echo   Build Success!
    echo ========================================
    echo.
    echo APK位置：
    echo app\build\outputs\apk\debug\app-debug.apk
    echo.
) else (
    echo.
    echo ========================================
    echo   构建失败
    echo   Build Failed
    echo ========================================
    echo.
    echo 请检查错误信息
)

pause
