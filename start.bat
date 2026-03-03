@echo off
chcp 65001 >nul
echo ========================================
echo   医学免疫学学习系统
echo   Medical Immunology Study System
echo ========================================
echo.
echo 正在启动Web应用...
echo 启动后请在浏览器访问: http://127.0.0.1:5000
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python app.py

pause
