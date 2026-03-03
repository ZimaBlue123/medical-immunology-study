@echo off
chcp 65001 >nul
title 构建Android APK
color 0A
setlocal EnableExtensions EnableDelayedExpansion

echo ========================================
echo   医学免疫学学习系统 - Android构建工具
echo   Medical Immunology Study - Android Builder
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查环境...
echo.

REM 检查Java版本（Gradle 8.2 不能在 Java 20+ 上运行）
call :ensure_compatible_java
if %ERRORLEVEL% NEQ 0 exit /b 1

REM 检查是否在android目录
if not exist "app\src\main\AndroidManifest.xml" (
    echo [错误] 请在android目录下运行此脚本
    echo [错误] Please run this script in the android directory
    pause
    exit /b 1
)

REM 检查Gradle Wrapper
if not exist "gradlew.bat" (
    echo [警告] 未找到gradlew.bat
    echo [警告] 将尝试生成Gradle Wrapper（需要本机存在gradle命令）
    echo.
    
    REM 检查是否有gradle命令
    where gradle >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 未找到gradle命令
        echo [错误] 解决办法（推荐Android Studio方案A）：
        echo [错误] - 在Android Studio中打开 android 工程并完成Sync
        echo [错误] - 然后在 Gradle 面板运行任务: Tasks ^> other ^> wrapper
        echo [错误]   运行后会生成 gradlew.bat 和 gradle\wrapper\gradle-wrapper.jar
        echo [错误] - 再回到这里重新运行本脚本
        pause
        exit /b 1
    )
    
    echo 正在生成Gradle Wrapper...
    REM 注意：本项目使用AGP 8.2.0，对应Gradle 8.2
    gradle wrapper --gradle-version 8.2
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] Gradle Wrapper生成失败
        echo [错误] 请使用Android Studio打开项目
        pause
        exit /b 1
    )
    echo [成功] Gradle Wrapper已生成
    echo.
)

REM 检查local.properties
if not exist "local.properties" (
    echo [提示] 未找到local.properties文件
    echo [提示] 正在尝试自动检测SDK路径...
    echo.
    
    REM 尝试常见SDK路径
    set "SDK_PATH="
    
    if exist "%LOCALAPPDATA%\Android\Sdk" (
        set "SDK_PATH=%LOCALAPPDATA%\Android\Sdk"
    ) else if exist "%USERPROFILE%\AppData\Local\Android\Sdk" (
        set "SDK_PATH=%USERPROFILE%\AppData\Local\Android\Sdk"
    ) else if exist "C:\Users\%USERNAME%\AppData\Local\Android\Sdk" (
        set "SDK_PATH=C:\Users\%USERNAME%\AppData\Local\Android\Sdk"
    )
    
    if defined SDK_PATH (
        echo [信息] 检测到SDK路径: %SDK_PATH%
        (
            echo ## This file must *NOT* be checked into Version Control Systems,
            echo ## as it contains information specific to your local configuration.
            echo.
            echo ## Location of the SDK. This is only used by Gradle.
            echo sdk.dir=%SDK_PATH:\=\\%
        ) > local.properties
        echo [成功] 已创建local.properties文件
    ) else (
        echo [警告] 无法自动检测SDK路径
        echo [警告] 请手动创建local.properties文件
        echo [警告] 参考 local.properties.example
        echo.
        echo 按任意键继续（可能会失败）...
        pause >nul
    )
    echo.
)

echo [2/4] 清理旧构建文件...
echo.
REM 确保JAVA_HOME已设置（用于gradlew.bat）
if defined JAVA_HOME (
    echo [信息] 使用JAVA_HOME: %JAVA_HOME%
)
call ".\gradlew.bat" clean

echo [3/4] 开始构建Debug APK...
echo.
echo 这可能需要几分钟时间，请耐心等待...
echo This may take a few minutes, please wait...
echo.

call ".\gradlew.bat" assembleDebug

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   [成功] 构建完成！
    echo   [Success] Build Complete!
    echo ========================================
    echo.
    
    set "APK_PATH=app\build\outputs\apk\debug\app-debug.apk"
    
    if exist "%APK_PATH%" (
        echo [APK位置] %CD%\%APK_PATH%
        echo.
        
        REM 获取文件大小
        for %%A in ("%APK_PATH%") do set "APK_SIZE=%%~zA"
        set /a APK_SIZE_MB=%APK_SIZE% / 1048576
        echo [文件大小] 约 %APK_SIZE_MB% MB
        echo.
        
        echo ========================================
        echo   下一步操作：
        echo   Next Steps:
        echo ========================================
        echo.
        echo 1. 将APK文件传输到Android设备
        echo 2. 在设备上点击APK文件安装
        echo 3. 允许"未知来源"安装
        echo.
        echo 是否打开APK所在文件夹？(Y/N)
        set /p "OPEN_FOLDER="
        if /i "%OPEN_FOLDER%"=="Y" (
            explorer /select,"%CD%\%APK_PATH%"
        )
    ) else (
        echo [警告] APK文件未找到，但构建显示成功
        echo [警告] 请检查构建输出
    )
) else (
    echo.
    echo ========================================
    echo   [失败] 构建失败
    echo   [Failed] Build Failed
    echo ========================================
    echo.
    echo 常见问题：
    echo 1. 检查Android SDK是否安装
    echo 2. 检查网络连接（需要下载依赖）
    echo 3. 检查local.properties中的SDK路径
    echo 4. 尝试使用Android Studio打开项目
    echo.
    echo 详细错误信息请查看上方输出
)

echo.
pause
exit /b 0

:ensure_compatible_java
REM 目标：让Gradle(8.2)运行在 Java <= 19 上

REM 先检查系统PATH中是否有java
set "JAVA_EXE="
where java >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "JAVA_EXE=java"
) else (
    REM 尝试自动检测Android Studio的JDK
    set "AS_JDK_PATH="
    set "JAVA_EXE_FOUND="
    
    REM 检查每个可能的JDK路径
    call :find_java_in_path "D:\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "%LOCALAPPDATA%\Android\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "%LOCALAPPDATA%\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "%PROGRAMFILES%\Android\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "%PROGRAMFILES(X86)%\Android\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "C:\Android Studio\jbr"
    if not defined JAVA_EXE_FOUND call :find_java_in_path "E:\Android Studio\jbr"
    
    if defined JAVA_EXE_FOUND (
        echo [信息] 检测到Android Studio JDK: %AS_JDK_PATH%
        echo [信息] Java可执行文件: %JAVA_EXE%
        set "JAVA_HOME=%AS_JDK_PATH%"
        
        REM 设置PATH（确保bin目录在PATH中）
        for %%P in ("%JAVA_EXE%") do set "JAVA_BIN_DIR=%%~dpP"
        set "PATH=%JAVA_BIN_DIR%;%PATH%"
    ) else (
        echo [错误] 未找到java命令，且无法自动检测Android Studio JDK
        echo [错误] 请手动设置JAVA_HOME环境变量，或确保java在PATH中
        echo [错误] Android Studio JDK通常位于: %LOCALAPPDATA%\Android\Android Studio\jbr
        echo [调试] 尝试查找的路径包括:
        echo [调试]   - D:\Android Studio\jbr
        echo [调试]   - %LOCALAPPDATA%\Android\Android Studio\jbr
        echo [调试]   - %PROGRAMFILES%\Android\Android Studio\jbr
        exit /b 1
    )
)

:find_java_in_path
set "TEST_PATH=%~1"
if not defined TEST_PATH exit /b

REM 检查标准位置: jbr\bin\java.exe
if exist "%TEST_PATH%\bin\java.exe" (
    set "AS_JDK_PATH=%TEST_PATH%"
    set "JAVA_EXE=%TEST_PATH%\bin\java.exe"
    set "JAVA_EXE_FOUND=1"
    exit /b
)

REM 如果目录存在但bin\java.exe不存在，尝试递归查找
if exist "%TEST_PATH%" (
    for /r "%TEST_PATH%" %%F in (java.exe) do (
        if not defined JAVA_EXE_FOUND (
            set "AS_JDK_PATH=%TEST_PATH%"
            set "JAVA_EXE=%%F"
            set "JAVA_EXE_FOUND=1"
            exit /b
        )
    )
)
exit /b

REM 检查Java版本
set "JAVA_VER="
if defined JAVA_EXE (
    REM 先测试Java是否能运行
    "%JAVA_EXE%" -version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 无法执行Java: %JAVA_EXE%
        exit /b 1
    )
    
    REM 使用临时文件获取版本信息
    "%JAVA_EXE%" -version 2> "%TEMP%\java_ver.tmp"
    for /f "tokens=3" %%A in ('type "%TEMP%\java_ver.tmp" ^| findstr /i "version"') do set "JAVA_VER=%%A"
    del "%TEMP%\java_ver.tmp" >nul 2>&1
    
    REM 移除引号
    if defined JAVA_VER set "JAVA_VER=%JAVA_VER:"=%"
) else (
    REM 如果JAVA_EXE未定义，尝试使用java命令
    java -version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        for /f "tokens=3" %%A in ('java -version 2^>^&1 ^| findstr /i "version"') do set "JAVA_VER=%%~A"
        set "JAVA_VER=%JAVA_VER:"=%"
    )
)

set "JAVA_MAJOR="
for /f "tokens=1 delims=." %%M in ("%JAVA_VER%") do set "JAVA_MAJOR=%%M"

REM 如果检测不到版本，就不阻塞（后续Gradle会给出明确错误）
if not defined JAVA_MAJOR (
    echo [警告] 无法检测Java版本，继续执行（Gradle会验证）
    exit /b 0
)

if %JAVA_MAJOR% GEQ 20 (
    echo [警告] 检测到当前Java版本: %JAVA_VER%
    echo [警告] Gradle 8.2 无法在 Java 20+ 上运行，会导致Android Studio无法Sync/命令行无法构建。
    echo.
    echo [解决方案A] 在Android Studio中设置Gradle JDK为 JDK 17（或19）：
    echo   Settings ^> Build, Execution, Deployment ^> Build Tools ^> Gradle ^> Gradle JDK
    echo   然后设置JAVA_HOME环境变量指向该JDK路径
    echo.
    echo [解决方案B] 安装JDK 17后，设置JAVA_HOME指向JDK 17，再重试。
    echo.
    exit /b 1
) else (
    echo [信息] 检测到Java版本: %JAVA_VER% ^(主版本: %JAVA_MAJOR%^)
)

exit /b 0
