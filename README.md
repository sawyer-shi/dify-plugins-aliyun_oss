# Alibaba Cloud OSS Plugin / 阿里云OSS插件

[English](#english) | [中文](#中文)

---

## English

A powerful Dify plugin providing seamless integration with Alibaba Cloud Object Storage Service (OSS). Enables direct file uploads to Alibaba Cloud OSS and efficient file retrieval using URLs, with rich configuration options.

### Version Information

- **Current Version**: v0.0.1
- **Release Date**: 2025-09-22
- **Compatibility**: Dify Plugin Framework
- **Python Version**: 3.12

#### Version History
- **v0.0.1** (2025-09-22): Initial release with file upload and retrieval capabilities, support for multiple directory structures and filename modes

### Quick Start

1. Download the aliyun_oss plugin from the Dify marketplace
2. Configure Alibaba Cloud OSS authorization information
3. After completing the above configuration, you can immediately use the plugin

### Core Features

#### File Upload to OSS
- **Direct File Upload**: Upload any file type directly to Alibaba Cloud OSS
- **Flexible Directory Structure**: Multiple storage directory organization options
  - Flat structure (no_subdirectory)
  - Hierarchical date structure (yyyy_mm_dd_hierarchy)
  - Combined date structure (yyyy_mm_dd_combined)
- **Filename Customization**: Control how filenames are stored in OSS
  - Use original filename
  - Append timestamp to original filename
- **Source File Tracking**: Automatically captures and returns the original filename
- **Smart Extension Detection**: Automatically determine file extensions based on content type

#### File Retrieval by URL
- **Direct Content Access**: Retrieve file content directly using OSS URLs
- **Cross-Region Support**: Works with all Alibaba Cloud OSS regions worldwide

### Technical Advantages

- **Secure Authentication**: Robust credential handling with support for HTTPS
- **Efficient Storage Management**: Intelligent file organization options
- **Comprehensive Error Handling**: Detailed error messages and status reporting
- **Multiple File Type Support**: Works with all common file formats
- **Rich Parameter Configuration**: Extensive options for customized workflows
- **Source File Tracking**: Preserves original filename information

### Requirements

- Python 3.12
- Alibaba Cloud OSS account with valid AccessKey credentials
- Dify Platform access
- Required Python packages (installed via requirements.txt)

### Installation & Configuration

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the plugin in Dify with the following parameters:
   - **Endpoint**: Your Alibaba Cloud OSS endpoint (e.g., oss-cn-beijing.aliyuncs.com)
   - **Bucket Name**: Your OSS bucket name
   - **AccessKey ID**: Your Alibaba Cloud AccessKey ID
   - **AccessKey Secret**: Your Alibaba Cloud AccessKey Secret

### Usage

The plugin provides two powerful tools for interacting with Alibaba Cloud OSS:

#### 1. Upload File to OSS (upload_file)

Dedicated tool for uploading files to Alibaba Cloud OSS.
- **Parameters**:
  - `file`: The local file to upload (required)
  - `directory`: First-level directory under the bucket (required)
  - `directory_mode`: Optional directory structure mode (default: `no_subdirectory`)
    - `no_subdirectory`: Store directly in specified directory
    - `yyyy_mm_dd_hierarchy`: Store in date-based hierarchical structure
    - `yyyy_mm_dd_combined`: Store in combined date directory
  - `filename`: Optional custom filename for OSS storage
  - `filename_mode`: Optional filename composition mode (default: `filename`)
    - `filename`: Use original filename
    - `filename_timestamp`: Use original filename plus timestamp

#### 2. Get File by URL (get_file_by_url)

Dedicated tool for retrieving files from Alibaba Cloud OSS using URLs.
- **Parameters**:
  - `file_url`: The URL of the file in Alibaba Cloud OSS

### Examples

#### Upload File
<img width="2192" height="1002" alt="upload-01" src="https://github.com/user-attachments/assets/01eb05bd-e1b0-4d55-be31-821ef55ea952" />
<img width="2183" height="500" alt="upload-02" src="https://github.com/user-attachments/assets/7cfdc7ae-a9a8-4497-a9cf-978977741062" />



#### Get File by URL

<img width="1743" height="541" alt="download-01" src="https://github.com/user-attachments/assets/83c50b57-321d-453d-bbc7-fb0673dd7ffa" />
<img width="1757" height="621" alt="download-02" src="https://github.com/user-attachments/assets/844dc2cb-cf63-4624-91c7-bb852222f3bb" />



### Notes

- Ensure your OSS bucket has the correct permissions configured
- The plugin requires valid Alibaba Cloud credentials with appropriate OSS access permissions
- For very large files, consider using multipart upload functionality (not currently implemented)

### Developer Information

- **Author**: `https://github.com/sawyer-shi`
- **Email**: sawyer36@foxmail.com
- **License**: MIT License
- **Support**: Through Dify platform and GitHub Issues

---

## 中文

一个功能强大的Dify插件，提供与阿里云对象存储服务（OSS）的无缝集成。支持将文件直接上传到阿里云OSS，并使用URL高效检索文件，提供丰富的配置选项。

### 版本信息

- **当前版本**: v0.0.1
- **发布日期**: 2025-09-22
- **兼容性**: Dify Plugin Framework
- **Python版本**: 3.12

#### 版本历史
- **v0.0.1** (2025-09-22): 初始版本，支持文件上传和检索功能，支持多种目录结构和文件名模式

### 快速开始

1. 从Dify市场下载该插件aliyun_oss
2. 配置阿里云OSS的授权信息
3. 完成上述配置即可马上使用该插件

### 核心特性

#### 文件上传至OSS
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

#### 通过URL获取文件
- **直接内容访问**: 使用OSS URL直接检索文件内容
- **跨区域支持**: 适用于全球所有阿里云OSS区域

### 技术优势

- **安全认证**: 强大的凭证处理，支持HTTPS
- **高效存储管理**: 智能文件组织选项
- **全面的错误处理**: 详细的错误消息和状态报告
- **多种文件类型支持**: 适用于所有常见文件格式
- **丰富的参数配置**: 用于自定义工作流程的广泛选项
- **源文件追踪**: 保留原始文件名信息

### 要求

- Python 3.12
- 具有有效AccessKey凭证的阿里云OSS账户
- Dify平台访问权限
- 所需的Python包（通过requirements.txt安装）

### 安装与配置

1. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 在Dify中配置插件，输入以下参数：
   - **Endpoint**: 您的阿里云OSS端点（例如：oss-cn-beijing.aliyuncs.com）
   - **Bucket Name**: 您的OSS存储桶名称
   - **AccessKey ID**: 您的阿里云AccessKey ID
   - **AccessKey Secret**: 您的阿里云AccessKey Secret
   - **Use HTTPS**: 是否使用HTTPS进行OSS请求（默认：true）

### 使用方法

该插件提供两个强大的工具用于与阿里云OSS交互：

#### 1. 上传文件至OSS (upload_file)

用于将文件上传到阿里云OSS的专用工具。
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

#### 2. 通过URL获取文件 (get_file_by_url)

用于使用URL从阿里云OSS检索文件的专用工具。
- **参数**:
  - `file_url`: 阿里云OSS中文件的URL

### 示例

#### 上传文件 
<img width="2192" height="1002" alt="upload-01" src="https://github.com/user-attachments/assets/01eb05bd-e1b0-4d55-be31-821ef55ea952" />
<img width="2183" height="500" alt="upload-02" src="https://github.com/user-attachments/assets/7cfdc7ae-a9a8-4497-a9cf-978977741062" />




#### 通过URL获取文件
<img width="1743" height="541" alt="download-01" src="https://github.com/user-attachments/assets/83c50b57-321d-453d-bbc7-fb0673dd7ffa" />
<img width="1757" height="621" alt="download-02" src="https://github.com/user-attachments/assets/844dc2cb-cf63-4624-91c7-bb852222f3bb" />





### 注意事项

- 确保您的OSS存储桶配置了正确的权限
- 该插件需要具有适当OSS访问权限的有效阿里云凭证
- 对于非常大的文件，请考虑使用分片上传功能（目前未实现）

### 开发者信息

- **作者**: `https://github.com/sawyer-shi`
- **邮箱**: sawyer36@foxmail.com
- **许可证**: MIT License
- **源码地址**: `https://github.com/sawyer-shi/dify-plugins-aliyun_oss`
- **支持**: 通过Dify平台和GitHub Issues

---

**Ready to seamlessly integrate with Alibaba Cloud OSS? / 准备好与阿里云OSS无缝集成了吗？**



