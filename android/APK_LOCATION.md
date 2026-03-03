# APK文件位置说明

## 📍 APK文件位置

构建完成后，APK文件位于以下位置：

### Debug版本（开发测试用）
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### Release版本（发布用，需要签名）
```
android/app/build/outputs/apk/release/app-release.apk
```

## 🔍 如何找到APK文件

### 方法1：Android Studio
1. 构建完成后，Android Studio会弹出通知
2. 点击通知中的"locate"按钮
3. 会自动打开APK文件所在文件夹

### 方法2：文件管理器
1. 打开文件管理器
2. 导航到项目目录
3. 进入 `android/app/build/outputs/apk/debug/` 文件夹
4. 找到 `app-debug.apk` 文件

### 方法3：命令行
```bash
# Windows PowerShell
cd android
dir app\build\outputs\apk\debug\app-debug.apk

# 或直接打开文件夹
explorer app\build\outputs\apk\debug\
```

## 📦 APK文件信息

- **文件名**：`app-debug.apk`（Debug版本）或 `app-release.apk`（Release版本）
- **大小**：约 5-10 MB（包含所有资源）
- **版本**：1.0.0
- **包名**：`com.medical.immunology.study`

## ✅ 构建检查清单

构建前确保：
- [ ] Android Studio已安装
- [ ] Android SDK已安装（API 24+）
- [ ] 项目已同步Gradle
- [ ] 没有构建错误

构建后检查：
- [ ] APK文件已生成
- [ ] APK文件大小正常（> 1MB）
- [ ] 可以传输到Android设备
- [ ] 可以在设备上安装

## 🚀 快速构建命令

### Windows
```bash
cd android
gradlew.bat assembleDebug
```

### Linux/Mac
```bash
cd android
./gradlew assembleDebug
```

### 使用脚本（Windows）
```bash
cd android
build-apk.bat
```

## 📱 安装到设备

### 方式1：USB调试
```bash
adb install app-debug.apk
```

### 方式2：直接传输
1. 将APK文件复制到Android设备
2. 在设备上打开文件管理器
3. 点击APK文件安装

## ⚠️ 注意事项

1. **首次构建**：需要下载Gradle和依赖，需要网络连接
2. **Gradle Wrapper**：如果缺少 `gradlew.bat`，需要先运行 `gradle wrapper`
3. **SDK路径**：确保 `local.properties` 中SDK路径正确
4. **构建时间**：首次构建可能需要5-10分钟

## 🔧 如果找不到APK

1. **检查构建是否成功**
   - 查看Android Studio的Build输出
   - 确认没有错误信息

2. **检查构建类型**
   - Debug版本：`app/build/outputs/apk/debug/`
   - Release版本：`app/build/outputs/apk/release/`

3. **清理后重新构建**
   ```bash
   gradlew.bat clean
   gradlew.bat assembleDebug
   ```

4. **检查文件权限**
   - 确保有读取权限
   - Windows可能需要管理员权限

---

**APK文件位置：`android/app/build/outputs/apk/debug/app-debug.apk`**
