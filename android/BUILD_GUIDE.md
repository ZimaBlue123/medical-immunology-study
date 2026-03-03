# Android应用构建指南

## 📱 项目说明

这是医学免疫学学习系统的Android版本，使用WebView包装前端应用，所有数据存储在本地。

## 🛠️ 构建要求

### 必需软件

1. **Android Studio** (最新版本)
   - 下载：https://developer.android.com/studio
   - 需要安装 Android SDK (API 24+)

2. **JDK 8 或更高版本**
   - Android Studio通常自带

3. **Gradle** (会自动下载)

## 🚀 构建步骤

### 方法1：使用Android Studio（推荐）

1. **打开项目**
   ```bash
   # 在Android Studio中
   File -> Open -> 选择 android 目录
   ```

2. **配置SDK路径**
   - 如果提示缺少 `local.properties`，创建该文件：
   ```properties
   sdk.dir=C\:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk
   ```
   - 或让Android Studio自动检测

3. **同步Gradle**
   - Android Studio会自动提示同步
   - 或点击 `File -> Sync Project with Gradle Files`

4. **构建APK**
   - `Build -> Build Bundle(s) / APK(s) -> Build APK(s)`
   - 或使用菜单：`Build -> Make Project`

5. **生成签名APK（用于发布）**
   - `Build -> Generate Signed Bundle / APK`
   - 选择APK
   - 创建新的密钥库或使用现有密钥库
   - 选择release构建类型
   - 完成构建

### 方法2：使用命令行

1. **设置环境变量**
   ```bash
   # Windows PowerShell
   $env:ANDROID_HOME = "C:\Users\YourUsername\AppData\Local\Android\Sdk"
   ```

2. **进入项目目录**
   ```bash
   cd android
   ```

3. **构建Debug APK**
   ```bash
   # Windows
   gradlew.bat assembleDebug
   
   # Linux/Mac
   ./gradlew assembleDebug
   ```

4. **构建Release APK（需要签名）**
   ```bash
   # 先创建签名配置（见下方）
   gradlew.bat assembleRelease
   ```

5. **APK位置**
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   android/app/build/outputs/apk/release/app-release.apk
   ```

## 📦 签名配置（Release版本）

### 创建密钥库

```bash
keytool -genkey -v -keystore medical-immunology.keystore -alias medical -keyalg RSA -keysize 2048 -validity 10000
```

### 配置签名

在 `android/app/build.gradle` 的 `android` 块中添加：

```gradle
signingConfigs {
    release {
        storeFile file('../medical-immunology.keystore')
        storePassword 'your_store_password'
        keyAlias 'medical'
        keyPassword 'your_key_password'
    }
}

buildTypes {
    release {
        signingConfig signingConfigs.release
        minifyEnabled false
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

## 📱 安装到设备

### 方法1：通过USB调试

1. **启用开发者选项**
   - 设置 -> 关于手机 -> 连续点击"版本号"7次

2. **启用USB调试**
   - 设置 -> 开发者选项 -> USB调试

3. **连接设备**
   ```bash
   adb install app-debug.apk
   ```

### 方法2：直接传输

1. 将APK文件传输到Android设备
2. 在设备上打开文件管理器
3. 点击APK文件安装
4. 允许"未知来源"安装（如需要）

## 🔧 常见问题

### Q: Gradle同步失败

**A:** 
- 检查网络连接（需要下载依赖）
- 检查 `gradle-wrapper.properties` 中的Gradle版本
- 尝试：`File -> Invalidate Caches / Restart`

### Q: SDK路径错误

**A:**
- 创建 `local.properties` 文件
- 设置正确的 `sdk.dir` 路径

### Q: 构建时内存不足

**A:**
在 `gradle.properties` 中增加：
```properties
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
```

### Q: WebView无法加载本地文件

**A:**
- 检查 `AndroidManifest.xml` 中的权限
- 确保HTML文件在 `assets` 目录下
- 检查文件路径是否正确

## 📝 项目结构

```
android/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── assets/
│   │       │   ├── index.html          # 主HTML文件
│   │       │   └── js/
│   │       │       ├── knowledge-base.js  # 知识库数据
│   │       │       ├── deck-data.js      # 题库数据
│   │       │       └── api.js            # 前端API层
│   │       ├── java/.../MainActivity.kt  # 主Activity
│   │       ├── res/                      # 资源文件
│   │       └── AndroidManifest.xml      # 清单文件
│   └── build.gradle                     # 应用构建配置
├── build.gradle                          # 项目构建配置
├── settings.gradle                       # 项目设置
└── gradle.properties                     # Gradle属性
```

## 🎯 功能特性

- ✅ 完全离线运行
- ✅ 本地数据存储（localStorage）
- ✅ 响应式设计，适配平板
- ✅ 所有Web功能完整保留
- ✅ 无需网络连接

## 📞 技术支持

如有问题，请检查：
1. Android Studio版本是否最新
2. SDK是否完整安装
3. Gradle版本是否兼容
4. 项目文件是否完整

---

**构建完成后，APK文件位于：**
- Debug: `app/build/outputs/apk/debug/app-debug.apk`
- Release: `app/build/outputs/apk/release/app-release.apk`
