## Alibaba Cloud OSS Plugin

**Author:** sawyer-shi
**Version:** 0.0.1
**Type:** tool

### Description

This is a Dify plugin that provides integration with Alibaba Cloud Object Storage Service (OSS). It allows users to upload files to Alibaba Cloud OSS and retrieve files from OSS using their URLs.

### Features

1. **Upload Files to OSS**: Upload local files to Alibaba Cloud OSS and get the file URL
2. **Retrieve Files by URL**: Get the content of files from Alibaba Cloud OSS using their URLs

### Requirements

- Python 3.12
- Alibaba Cloud OSS account
- Dify Platform

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the plugin in Dify with the following credentials:
   - **Endpoint**: The endpoint of your Alibaba Cloud OSS service (e.g., oss-cn-beijing.aliyuncs.com)
   - **Bucket Name**: The name of your Alibaba Cloud OSS bucket
   - **AccessKey ID**: Your Alibaba Cloud AccessKey ID
   - **AccessKey Secret**: Your Alibaba Cloud AccessKey Secret
   - **Use HTTPS**: Whether to use HTTPS for OSS requests (default: true)

### Usage

The plugin provides two dedicated tools:

#### 1. Upload File to OSS (upload_file)

A dedicated tool for uploading files to Alibaba Cloud OSS.
- **Parameters**:
  - `file`: The local file to upload (required)
  - `directory`: The first-level directory under the bucket where the file will be stored (required)
  - `directory_mode`: (Optional) The parent directory structure mode (default: `no_subdirectory`)
    - `no_subdirectory`: Store the file directly in the specified directory (directory/filename)
    - `yyyy_mm_dd_hierarchy`: Store the file in a hierarchical directory structure based on the current date (directory/YYYY/MM/DD/filename)
    - `yyyy_mm_dd_combined`: Store the file in a directory structure with combined date (directory/YYYYMMDD/filename)
  - `filename`: (Optional) The filename to use when storing the file in OSS (default is a timestamp if not specified)
  - `filename_mode`: (Optional) The way to compose the filename stored in OSS (default: `filename`)
    - `filename`: Use the original filename
    - `filename_timestamp`: Use the original filename plus timestamp

#### 2. Get File by URL (get_file_by_url)

A dedicated tool for retrieving files from Alibaba Cloud OSS using their URLs.
- **Parameters**:
  - `file_url`: The URL of the file in Alibaba Cloud OSS

### Examples

#### Using Upload File Tool - Basic Usage

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents"
}
```

#### Using Upload File Tool - With Custom Filename

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "filename": "uploaded_file.txt"
}
```

#### Using Upload File Tool - With Year/Month/Day Hierarchical Structure

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "directory_mode": "yyyy_mm_dd_hierarchy",
  "filename": "uploaded_file.txt"
}
```

#### Using Upload File Tool - With Combined Date Structure

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "directory_mode": "yyyy_mm_dd_combined",
  "filename": "uploaded_file.txt"
}
```

#### Using Upload File Tool - With Filename + Timestamp Mode

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "filename": "uploaded_file.txt",
  "filename_mode": "filename_timestamp"
}```

#### Using Dedicated Get File by URL Tool

```python
{
  "file_url": "https://your-bucket.oss-cn-beijing.aliyuncs.com/example.txt"
}
```

### Notes

- Make sure your Alibaba Cloud OSS bucket has the correct permissions set
- The plugin requires valid Alibaba Cloud AccessKey with appropriate permissions to access the OSS bucket
- For large files, consider using multipart upload (not currently implemented in this plugin)

### License

This project is licensed under the MIT License.

### Support

For any issues or questions, please contact the author or refer to the [Alibaba Cloud OSS documentation](https://www.alibabacloud.com/help/en/oss).

---

## 阿里云OSS 插件

**作者:** sawyer-shi
**版本:** 0.0.1
**类型:** 工具

### 描述

这是一个Dify插件，提供与阿里云对象存储服务（OSS）的集成。它允许用户将文件上传到阿里云OSS，并使用URL从OSS检索文件。

### 功能

1. **上传文件到OSS**: 将本地文件上传到阿里云OSS并获取文件URL
2. **通过URL获取文件**: 使用URL从阿里云OSS获取文件内容

### 要求

- Python 3.12
- 阿里云OSS账号
- Dify平台

### 安装

1. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 在Dify中配置插件，输入以下凭证：
   - **Endpoint**: 您的阿里云OSS服务端点（例如：oss-cn-beijing.aliyuncs.com）
   - **Bucket Name**: 您的阿里云OSS存储桶名称
   - **AccessKey ID**: 您的阿里云AccessKey ID
   - **AccessKey Secret**: 您的阿里云AccessKey Secret
   - **Use HTTPS**: 是否使用HTTPS进行OSS请求（默认：true）

### 使用方法

该插件提供两个专用工具：

#### 1. 上传文件到OSS (upload_file)

用于将文件上传到阿里云OSS的专用工具。
- **参数**:
  - `file`: 要上传的本地文件（必填）
  - `directory`: 存储桶下文件将存储的一级目录（必填）
  - `directory_mode`: （可选）文件上级目录结构模式（默认：`no_subdirectory`）
    - `no_subdirectory`: 将文件直接存储在指定目录中（directory/filename）
    - `yyyy_mm_dd_hierarchy`: 按当前日期的层次结构存储文件（directory/YYYY/MM/DD/filename）
    - `yyyy_mm_dd_combined`: 按合并日期目录存储文件（directory/YYYYMMDD/filename）
  - `filename`: （可选）在OSS中存储文件时使用的文件名（未指定时默认使用时间戳）
  - `filename_mode`: （可选）存储在OSS上的文件名组成方式（默认：`filename`）
    - `filename`: 使用原始文件名
    - `filename_timestamp`: 使用原始文件名加上时间戳

#### 2. 通过URL获取文件 (get_file_by_url)

用于使用URL从阿里云OSS检索文件的专用工具。
- **参数**:
  - `file_url`: 阿里云OSS中文件的URL

### 示例

#### 使用上传文件工具 - 基本用法

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents"
}
```

#### 使用上传文件工具 - 自定义文件名

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "filename": "uploaded_file.txt"
}
```

#### 使用上传文件工具 - 年月日层级结构

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "directory_mode": "yyyy_mm_dd_hierarchy",
  "filename": "uploaded_file.txt"
}
```

#### 使用上传文件工具 - 合并日期结构

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "directory_mode": "yyyy_mm_dd_combined",
  "filename": "uploaded_file.txt"
}
```

#### 使用上传文件工具 - 文件名+时间戳模式

```python
{
  "file": "/path/to/your/file.txt",
  "directory": "documents",
  "filename": "uploaded_file.txt",
  "filename_mode": "filename_timestamp"
}```

#### 使用专用的通过URL获取文件工具

```python
{
  "file_url": "https://your-bucket.oss-cn-beijing.aliyuncs.com/example.txt"
}
```

### 注意事项

- 确保您的阿里云OSS存储桶设置了正确的权限
- 该插件需要具有适当权限的有效阿里云AccessKey才能访问OSS存储桶
- 对于大文件，请考虑使用分片上传（本插件目前未实现）

### 许可证

本项目采用MIT许可证。

### 支持

如有任何问题或疑问，请联系作者或参考[阿里云OSS文档](https://help.aliyun.com/product/31815.html)。



