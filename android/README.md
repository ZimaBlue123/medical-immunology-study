# 医学免疫学学习系统 - Android应用

## 📱 项目说明

这是完整的Android应用项目，包含所有源代码和资源文件。

## 📦 项目结构

```
android/
├── app/                          # 应用模块
│   ├── src/main/
│   │   ├── assets/              # 资源文件（HTML、JS）
│   │   │   ├── index.html       # 主HTML文件
│   │   │   └── js/              # JavaScript文件
│   │   │       ├── knowledge-base.js  # 知识库数据
│   │   │       ├── deck-data.js        # 题库数据
│   │   │       └── api.js              # 前端API层
│   │   ├── java/.../MainActivity.kt   # 主Activity
│   │   ├── res/                 # Android资源
│   │   └── AndroidManifest.xml   # 应用清单
│   ├── build.gradle             # 应用构建配置
│   └── proguard-rules.pro       # ProGuard规则
├── build.gradle                  # 项目构建配置
├── settings.gradle               # 项目设置
├── gradle.properties             # Gradle属性
├── gradle/wrapper/               # Gradle Wrapper
│   └── gradle-wrapper.properties
├── BUILD_GUIDE.md               # 详细构建指南
├── build-apk.bat                # Windows构建脚本
└── local.properties.example      # SDK配置示例
```

## 🚀 快速构建APK

### 方法1：使用Android Studio（推荐）

1. **安装Android Studio**
   - 下载：https://developer.android.com/studio
   - 安装时选择"Standard"安装

2. **打开项目**
   - 启动Android Studio
   - `File -> Open` -> 选择 `android` 目录
   - 等待Gradle同步（首次需要下载依赖）

3. **构建APK**
   - `Build -> Build Bundle(s) / APK(s) -> Build APK(s)`
   - 等待构建完成

4. **APK位置**
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

### 方法2：使用命令行

```bash
cd android

# Windows
gradlew.bat assembleDebug

# Linux/Mac
./gradlew assembleDebug
```

**APK位置：**
```
android/app/build/outputs/apk/debug/app-debug.apk
```

## 📱 安装APK

1. 将APK文件传输到Android设备
2. 在设备上点击APK文件
3. 允许"未知来源"安装
4. 点击"安装"

## 📄 详细说明

- `BUILD_GUIDE.md` - 完整构建指南
- `../docs/android/ANDROID_QUICK_START.md` - 快速开始指南
- `../docs/android/ANDROID_README.md` - Android版本说明

---

**所有文件已准备就绪，可以开始构建！**
