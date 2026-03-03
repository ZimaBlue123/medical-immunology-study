# 医学免疫学学习系统 - Android版本

## 📱 应用简介

这是医学免疫学学习系统的Android应用版本，可以在Android平板上安装使用。

### 主要特性

- ✅ **完全离线**：无需网络连接，所有数据本地存储
- ✅ **完整功能**：包含Web版本的所有功能
  - 📚 知识卡片库（150+概念）
  - 💬 智能学习教练
  - ✏️ 智能练习系统
  - 📊 学习进度追踪
  - 🔍 知识搜索
- ✅ **平板优化**：针对Android平板优化界面
- ✅ **本地存储**：使用localStorage保存学习进度

## 🚀 快速开始

### 方式1：直接安装APK（推荐）

1. **获取APK文件**
   - 如果已有构建好的APK，直接安装
   - 或按照下方说明自行构建

2. **安装到设备**
   - 将APK文件传输到Android设备
   - 在设备上打开文件管理器
   - 点击APK文件安装
   - 允许"未知来源"安装（如需要）

### 方式2：使用Android Studio构建

详细步骤请查看 `android/BUILD_GUIDE.md`

## 📦 构建APK

### 前置要求

1. **Android Studio** (最新版本)
   - 下载：https://developer.android.com/studio
   - 需要安装 Android SDK (API 24+)

2. **JDK 8+**

### 构建步骤

1. **打开项目**
   ```bash
   # 在Android Studio中打开 android 目录
   ```

2. **配置SDK**
   - 创建 `android/local.properties`：
   ```properties
   sdk.dir=C\:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk
   ```

3. **构建APK**
   ```bash
   # 在android目录下
   gradlew.bat assembleDebug  # Windows
   ./gradlew assembleDebug    # Linux/Mac
   ```

4. **APK位置**
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

### 快速构建脚本

Windows用户可以直接运行：
```bash
cd android
build-apk.bat
```

## 📱 系统要求

- **最低Android版本**：Android 7.0 (API 24)
- **推荐设备**：Android平板（7寸以上）
- **存储空间**：约50MB

## 🎯 功能说明

### 1. 知识卡片库

- 浏览12个学习模块
- 搜索150+核心概念
- 查看概念详情、记忆技巧、临床关联

### 2. 智能学习教练

- 引导式学习
- 自适应教学
- 理解检验

### 3. 智能练习

- 随机抽题
- 即时反馈
- 错题本
- 间隔复习

### 4. 学习进度

- 模块掌握度
- 统计报告
- 错题统计

## 💾 数据存储

所有学习数据存储在应用本地：
- 学习进度（SRS算法）
- 错题本
- 做题记录

**注意**：卸载应用会清除所有数据。如需备份，可以导出数据（未来版本支持）。

## 🔧 技术架构

- **前端**：HTML + CSS + JavaScript
- **容器**：Android WebView
- **存储**：localStorage
- **数据**：JavaScript对象（知识库、题库）

## 📝 更新数据

如需更新知识库或题库：

1. **更新Python数据源**
   - 编辑 `immuno_study/knowledge.py`
   - 编辑 `decks/people9-core.json`

2. **重新生成JavaScript文件**
   ```bash
   python convert_to_android.py
   ```

3. **重新构建APK**
   ```bash
   cd android
   gradlew.bat assembleDebug
   ```

## 🐛 问题排查

### 应用无法启动

- 检查Android版本是否>=7.0
- 检查存储权限是否授予

### 数据丢失

- 检查是否清理了应用数据
- 检查是否卸载重装

### 界面显示异常

- 检查WebView是否正常工作
- 尝试清除应用缓存

## 📞 技术支持

详细构建说明请查看：
- `android/BUILD_GUIDE.md`：完整构建指南
- `android/BUILD_GUIDE.md`：常见问题解答

## 📄 许可证

本项目基于《医学免疫学》人卫第9版框架，所有内容仅供学习参考。

---

**祝学习顺利！** 🎉
