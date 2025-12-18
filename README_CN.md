# 阿里云OSS插件

一个功能强大的Dify插件，提供与阿里云对象存储服务（OSS）的无缝集成。支持将文件直接上传到阿里云OSS，并使用URL高效检索文件，提供丰富的配置选项。

## 版本信息

- **当前版本**: v0.0.2
- **发布日期**: 2025-12-14
- **兼容性**: Dify Plugin Framework
- **Python版本**: 3.12

### 版本历史
- **v0.0.2** (2025-12-14): 新增批量下载OSS文件和公共文件下载功能
- **v0.0.1** (2025-09-22): 初始版本，支持文件上传和检索功能，支持多种目录结构和文件名模式

## 快速开始

1. 从Dify市场下载该插件aliyun_oss
2. 配置阿里云OSS的授权信息
3. 完成上述配置即可马上使用该插件

## 核心特性

### 文件上传至OSS
- **直接文件上传**: 将任何类型的文件直接上传到阿里云OSS
- **灵活的目录结构**: 多种存储目录组织选项
  - 扁平结构 (no_subdirectory)
  - 分层日期结构 (yyyy_mm_dd_hierarchy)
  - 合并日期结构 (yyyy_mm_dd_combined)
- **文件名自定义**: 控制文件在OSS中的存储名称
  - 使用原始文件名
  - 在原始文件名后附加时间戳
- **源文件追踪**: 自动捕获并返回原始文件名
- **智能扩展名检测**: 基于内容类型自动确定文件扩展名

### 通过URL获取文件
- **直接内容访问**: 使用OSS URL直接检索文件内容
- **跨区域支持**: 适用于全球所有阿里云OSS区域

### 批量文件下载
- **多URL处理**: 使用分号分隔的URL下载多个OSS文件
- **错误恢复**: 单个文件失败不影响其他下载
- **进度跟踪**: 提供详细的下载状态和摘要

### 公共文件下载
- **平台无关**: 从任何平台下载公开可访问的文件
- **无需认证**: 无需API密钥或凭证即可工作
- **智能文件检测**: 自动确定文件类型和扩展名

## 技术优势

- **安全认证**: 强大的凭证处理，支持HTTPS
- **高效存储管理**: 智能文件组织选项
- **全面的错误处理**: 详细的错误消息和状态报告
- **多种文件类型支持**: 适用于所有常见文件格式
- **丰富的参数配置**: 用于自定义工作流程的广泛选项
- **源文件追踪**: 保留原始文件名信息

## 要求

- Python 3.12
- 具有有效AccessKey凭证的阿里云OSS账户
- Dify平台访问权限
- 所需的Python包（通过requirements.txt安装）

## 安装与配置

1. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 在Dify中配置插件，输入以下参数：
   - **Endpoint**: 您的阿里云OSS端点（例如：oss-cn-beijing.aliyuncs.com）
   - **Bucket Name**: 您的OSS存储桶名称
   - **AccessKey ID**: 您的阿里云AccessKey ID
   - **AccessKey Secret**: 您的阿里云AccessKey Secret

## 使用方法

该插件提供五个强大的工具用于与阿里云OSS交互：

### 1. 上传文件至OSS (upload_file)

用于将单个文件上传到阿里云OSS的专用工具。
- **参数**:
  - `file`: 要上传的本地文件（必填）
  - `directory`: 存储桶下的一级目录（必填）
  - `directory_mode`: 可选的目录结构模式（默认：`no_subdirectory`）
    - `no_subdirectory`: 直接存储在指定目录中
    - `yyyy_mm_dd_hierarchy`: 存储在基于日期的分层结构中
    - `yyyy_mm_dd_combined`: 存储在合并日期目录中
  - `filename`: 用于OSS存储的可选自定义文件名
  - `filename_mode`: 可选的文件名组成模式（默认：`filename`）
    - `filename`: 使用原始文件名
    - `filename_timestamp`: 使用原始文件名加上时间戳

### 2. 批量上传文件至OSS (multi_upload_files)

用于将多个文件同时上传到阿里云OSS的专用工具。
- **参数**:
  - `files`: 要上传的多个本地文件（必填）
  - `directory`: 存储桶下的一级目录（必填）
  - `directory_mode`: 可选的目录结构模式（默认：`no_subdirectory`）
    - `no_subdirectory`: 直接存储在指定目录中
    - `yyyy_mm_dd_hierarchy`: 存储在基于日期的分层结构中
    - `yyyy_mm_dd_combined`: 存储在合并日期目录中
  - `filename_mode`: 可选的文件名组成模式（默认：`filename`）
    - `filename`: 使用原始文件名
    - `filename_timestamp`: 使用原始文件名加上时间戳

### 3. 通过URL获取文件 (get_file_by_url)

用于使用URL从阿里云OSS检索文件的专用工具。
- **参数**:
  - `file_url`: 阿里云OSS中文件的URL

### 4. 批量通过URL获取文件 (get_files_by_urls)

用于使用分号分隔的URL批量从阿里云OSS检索多个文件的专用工具。
- **参数**:
  - `file_urls`: 阿里云OSS中多个文件的URL，使用分号(;)分隔

### 5. 获取公共文件 (get_public_file_by_url)

用于从任何平台下载公开可访问文件而无需API密钥的专用工具。
- **参数**:
  - `file_url`: 任何平台上公开可访问文件的URL

## 示例

### 上传文件
<img width="2064" height="865" alt="upload-01" src="https://github.com/user-attachments/assets/045985dc-f56c-4d25-9996-eed9a63274a6" />

### 批量上传文件
<img width="1981" height="862" alt="upload-02" src="https://github.com/user-attachments/assets/b5de5a4a-aec8-4b70-a98d-9073ad573e84" />

### 获取(下载)文件
<img width="2014" height="492" alt="download-01" src="https://github.com/user-attachments/assets/bf90e661-5ea9-4080-8592-e4e2c9acefaa" />
<img width="1940" height="499" alt="download-02" src="https://github.com/user-attachments/assets/f5506d0a-0a43-4210-a5a7-8c4010cb95fc" />

## 注意事项

- 确保您的OSS存储桶配置了正确的权限
- 该插件需要具有适当OSS访问权限的有效阿里云凭证
- 对于非常大的文件，请考虑使用分片上传功能（目前未实现）

## 开发者信息

- **作者**: `https://github.com/sawyer-shi`
- **邮箱**: sawyer36@foxmail.com
- **许可证**: MIT License
- **源码地址**: `https://github.com/sawyer-shi/dify-plugins-aliyun_oss`
- **支持**: 通过Dify平台和GitHub Issues

---

**准备好与阿里云OSS无缝集成了吗？**