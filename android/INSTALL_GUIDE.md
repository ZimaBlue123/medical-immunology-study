# Android应用安装指南

## 📱 APK文件位置

### 构建后的APK文件位置

**Debug版本（开发测试）：**
```
android/app/build/outputs/apk/debug/app-debug.apk
```

**Release版本（发布用）：**
```
android/app/build/outputs/apk/release/app-release.apk
```

## 🚀 构建APK

### 最简单的方法：使用一键构建脚本

1. **双击运行**
   ```
   一键构建APK.bat
   ```

2. **脚本会自动：**
   - 检查环境
   - 生成Gradle Wrapper（如需要）
   - 检测SDK路径
   - 构建APK
   - 显示APK位置

3. **构建完成后**
   - APK文件在：`app\build\outputs\apk\debug\app-debug.apk`
   - 脚本会询问是否打开文件夹

### 使用Android Studio

1. **打开项目**
   - 启动Android Studio
   - `File -> Open` -> 选择 `android` 目录

2. **构建APK**
   - `Build -> Build Bundle(s) / APK(s) -> Build APK(s)`

3. **找到APK**
   - 构建完成后点击通知中的"locate"
   - 或手动查找：`app/build/outputs/apk/debug/app-debug.apk`

## 📦 安装到Android平板

### 方式1：USB调试安装（推荐）

1. **启用开发者选项**
   - 设置 -> 关于平板电脑
   - 连续点击"版本号"7次

2. **启用USB调试**
   - 设置 -> 开发者选项 -> USB调试

3. **连接设备并安装**
   ```bash
   adb install app-debug.apk
   ```

### 方式2：直接传输安装

1. **传输APK**
   - 通过USB、云盘、邮件等方式
   - 将APK文件传输到Android设备

2. **安装**
   - 在设备上打开文件管理器
   - 找到APK文件
   - 点击APK文件
   - 允许"未知来源"安装（如需要）
   - 点击"安装"

3. **启动应用**
   - 安装完成后，在应用列表中找到"医学免疫学学习"
   - 点击启动

## ✅ 安装后测试

### 功能测试

- [ ] **知识卡片库**
  - [ ] 浏览12个模块
  - [ ] 搜索知识点
  - [ ] 查看概念详情

- [ ] **学习教练**
  - [ ] 输入主题学习
  - [ ] 查看讲解
  - [ ] 跳转练习题

- [ ] **练习系统**
  - [ ] 随机抽题
  - [ ] 答题和查看解析
  - [ ] 错题记录

- [ ] **学习进度**
  - [ ] 查看模块进度
  - [ ] 查看统计
  - [ ] 查看错题本

### 性能测试

- [ ] 应用启动速度
- [ ] 页面切换流畅度
- [ ] 搜索响应速度
- [ ] 数据保存功能

## 🔧 常见问题

### Q: 找不到APK文件

**A:** 
1. 确认构建是否成功完成
2. 检查路径：`android/app/build/outputs/apk/debug/`
3. 尝试清理后重新构建：
   ```bash
   gradlew.bat clean
   gradlew.bat assembleDebug
   ```

### Q: 无法安装APK

**A:**
1. 检查Android版本是否>=7.0
2. 允许"未知来源"安装
3. 检查APK文件是否完整（大小>1MB）

### Q: 应用无法启动

**A:**
1. 检查Android版本
2. 清除应用数据后重试
3. 重新安装APK

### Q: 数据丢失

**A:**
- 数据存储在应用本地（localStorage）
- 卸载应用会清除数据
- 建议定期备份重要学习记录

## 📝 文件说明

### APK文件信息

- **文件名**：`app-debug.apk`
- **大小**：约 5-10 MB
- **版本**：1.0.0
- **包名**：`com.medical.immunology.study`
- **最低Android版本**：7.0 (API 24)

### 项目文件位置

所有Android项目文件在：
```
android/
```

APK构建后位置：
```
android/app/build/outputs/apk/debug/app-debug.apk
```

## 🎯 快速参考

### 构建命令
```bash
cd android
一键构建APK.bat
```

### APK位置
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### 安装命令
```bash
adb install app-debug.apk
```

---

**所有文件已准备就绪！按照上述步骤构建和安装即可。** 📱
