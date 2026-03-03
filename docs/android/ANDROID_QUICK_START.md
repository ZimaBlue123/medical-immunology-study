# Android应用快速开始指南

## ✅ 已完成的工作

### 1. Android项目结构
- ✅ 完整的Android项目结构
- ✅ MainActivity (Kotlin)
- ✅ WebView配置
- ✅ AndroidManifest.xml
- ✅ 资源文件（布局、字符串、样式）

### 2. 数据转换
- ✅ 知识库转换为JavaScript (`knowledge-base.js`)
- ✅ 题库转换为JavaScript (`deck-data.js`)
- ✅ 前端API层 (`api.js`)

### 3. 前端适配
- ✅ 适配Android的HTML文件
- ✅ 响应式设计（平板优化）
- ✅ 触摸优化
- ✅ 所有功能完整保留

### 4. 构建配置
- ✅ Gradle构建文件
- ✅ ProGuard规则
- ✅ 构建脚本

## 🚀 构建APK步骤

### 方法1：使用Android Studio（最简单）

1. **安装Android Studio**
   - 下载：https://developer.android.com/studio
   - 安装时选择"Standard"安装，会自动安装SDK

2. **打开项目**
   - 启动Android Studio
   - `File -> Open` -> 选择 `android` 目录
   - 等待Gradle同步完成（首次可能需要几分钟）

3. **配置SDK路径（如需要）**
   - 如果提示缺少 `local.properties`：
   - `File -> Project Structure -> SDK Location`
   - 或手动创建 `android/local.properties`：
   ```properties
   sdk.dir=C\:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk
   ```

4. **构建APK**
   - `Build -> Build Bundle(s) / APK(s) -> Build APK(s)`
   - 等待构建完成

5. **找到APK**
   - 构建完成后会弹出通知
   - 点击"locate"或手动查找：
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

### 方法2：使用命令行

1. **安装Android SDK**
   - 下载Android Studio或单独SDK
   - 设置环境变量：
   ```bash
   # Windows PowerShell
   $env:ANDROID_HOME = "C:\Users\YourUsername\AppData\Local\Android\Sdk"
   ```

2. **生成Gradle Wrapper（如需要）**
   ```bash
   cd android
   gradle wrapper --gradle-version 8.2
   ```

3. **构建APK**
   ```bash
   # Windows
   gradlew.bat assembleDebug
   
   # 或使用提供的脚本
   build-apk.bat
   ```

4. **APK位置**
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

## 📱 安装到Android平板

### 方式1：USB调试

1. **启用开发者选项**
   - 设置 -> 关于平板电脑 -> 连续点击"版本号"7次

2. **启用USB调试**
   - 设置 -> 开发者选项 -> USB调试

3. **连接设备并安装**
   ```bash
   adb install app-debug.apk
   ```

### 方式2：直接传输

1. 将APK文件复制到Android设备
2. 在设备上打开文件管理器
3. 点击APK文件
4. 允许"未知来源"安装
5. 点击"安装"

## 🧪 测试应用

### 功能测试清单

- [ ] **知识卡片库**
  - [ ] 浏览模块列表
  - [ ] 搜索知识点
  - [ ] 查看概念详情
  - [ ] 按模块筛选

- [ ] **学习教练**
  - [ ] 输入主题学习
  - [ ] 查看讲解内容
  - [ ] 跳转到练习题

- [ ] **练习系统**
  - [ ] 随机抽题
  - [ ] 答题和查看解析
  - [ ] 错题记录
  - [ ] 复习功能

- [ ] **学习进度**
  - [ ] 查看模块进度
  - [ ] 查看统计信息
  - [ ] 查看错题本

### 性能测试

- [ ] 应用启动速度
- [ ] 页面切换流畅度
- [ ] 搜索响应速度
- [ ] 数据加载速度

## 🔧 常见问题

### Q: Gradle同步失败

**解决方案：**
1. 检查网络连接
2. 尝试：`File -> Invalidate Caches / Restart`
3. 检查 `gradle-wrapper.properties` 中的Gradle版本
4. 手动下载Gradle：https://gradle.org/releases/

### Q: 找不到SDK

**解决方案：**
1. 在Android Studio中：`File -> Project Structure -> SDK Location`
2. 或创建 `local.properties` 文件，设置正确的SDK路径

### Q: 构建时内存不足

**解决方案：**
在 `android/gradle.properties` 中增加：
```properties
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
```

### Q: WebView无法加载

**解决方案：**
1. 检查 `AndroidManifest.xml` 中的权限
2. 确保HTML文件在 `assets` 目录
3. 检查文件路径：`file:///android_asset/index.html`

### Q: 应用崩溃

**解决方案：**
1. 查看Logcat错误信息
2. 检查Android版本是否>=7.0
3. 检查WebView是否支持

## 📦 项目文件说明

```
android/
├── app/
│   ├── src/main/
│   │   ├── assets/
│   │   │   ├── index.html              # 主HTML（已适配Android）
│   │   │   └── js/
│   │   │       ├── knowledge-base.js   # 知识库数据（已生成）
│   │   │       ├── deck-data.js        # 题库数据（已生成）
│   │   │       └── api.js              # 前端API层
│   │   ├── java/.../MainActivity.kt    # 主Activity
│   │   └── res/                         # 资源文件
│   └── build.gradle                     # 应用配置
├── build.gradle                         # 项目配置
├── settings.gradle                       # 项目设置
├── BUILD_GUIDE.md                       # 详细构建指南
└── build-apk.bat                        # Windows构建脚本
```

## 🎯 下一步

1. **构建APK**：按照上述步骤构建
2. **安装测试**：安装到Android平板测试
3. **优化调整**：根据测试结果调整界面和功能
4. **发布准备**：如需发布，配置签名并构建Release版本

## 📝 注意事项

1. **首次构建**：可能需要下载Gradle和依赖，需要网络连接
2. **Gradle版本**：使用Gradle 8.2，如不兼容可调整
3. **SDK版本**：最低API 24 (Android 7.0)，目标API 34
4. **数据更新**：如需更新知识库，运行 `convert_to_android.py` 后重新构建

## 🎉 完成！

所有文件已准备就绪，可以开始构建Android应用了！

如有问题，请查看：
- `android/BUILD_GUIDE.md`：详细构建指南
- `ANDROID_README.md`：Android版本说明

---

**构建完成后，APK文件可以安装到Android平板上使用！** 📱
