# Alibaba Cloud OSS Plugin

A powerful Dify plugin providing seamless integration with Alibaba Cloud Object Storage Service (OSS). Enables direct file uploads to Alibaba Cloud OSS and efficient file retrieval using URLs, with rich configuration options.


A powerful Dify plugin providing seamless integration with Alibaba Cloud Object Storage Service (OSS). Enables direct file uploads to Alibaba Cloud OSS and efficient file retrieval using URLs, with rich configuration options.

### Version Information

- **Current Version**: v0.0.2
- **Release Date**: 2025-12-14
- **Compatibility**: Dify Plugin Framework
- **Python Version**: 3.12

#### Version History
- **v0.0.2** (2025-12-14): Added batch download OSS files and public file download features
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

#### Batch File Download
- **Multiple URLs Processing**: Download multiple OSS files using semicolon-separated URLs
- **Error Resilience**: Individual file failures don't affect other downloads
- **Progress Tracking**: Provides detailed download status and summary

#### Public File Download
- **Platform Agnostic**: Download publicly accessible files from any platform
- **No Authentication Required**: Works without API keys or credentials
- **Smart File Detection**: Automatically determines file type and extension

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

The plugin provides five powerful tools for interacting with Alibaba Cloud OSS:

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
  - `sign_expired`: Signature expiration time in seconds (optional, default 3600 seconds)
    - Controls how long the generated URL signature remains valid
    - Only effective for private access with complete account permissions
    - After expiration, the URL will no longer provide access to the file

#### 2. Multi Upload Files to OSS (multi_upload_files)

Dedicated tool for uploading multiple files to Alibaba Cloud OSS simultaneously.
- **Parameters**:
  - `files`: The local files to upload (required)
  - `directory`: First-level directory under the bucket (required)
  - `directory_mode`: Optional directory structure mode (default: `no_subdirectory`)
    - `no_subdirectory`: Store directly in specified directory
    - `yyyy_mm_dd_hierarchy`: Store in date-based hierarchical structure
    - `yyyy_mm_dd_combined`: Store in combined date directory
  - `filename_mode`: Optional filename composition mode (default: `filename`)
    - `filename`: Use original filename
    - `filename_timestamp`: Use original filename plus timestamp
  - `sign_expired`: Signature expiration time in seconds (optional, default 3600 seconds)
    - Controls how long the generated URL signature remains valid
    - Only effective for private access with complete account permissions
    - After expiration, the URL will no longer provide access to the files

**Example:**
```python
# Upload multiple files with default signature expiration (1 hour)
result = multi_upload_files(
    files="file1.jpg;file2.pdf;file3.txt",
    directory="uploads/",
    filename_mode="filename_timestamp"
)

# Upload multiple files with custom signature expiration (3 hours)
result = multi_upload_files(
    files="file1.jpg;file2.pdf;file3.txt",
    directory="uploads/",
    filename_mode="filename_timestamp",
    sign_expired=10800
)
```

#### 3. Get File by URL (get_file_by_url)

Dedicated tool for retrieving files from Alibaba Cloud OSS using URLs.
- **Parameters**:
  - `file_url`: The URL of the file in Alibaba Cloud OSS

#### 4. Batch Get Files by URLs (get_files_by_urls)

Dedicated tool for batch retrieving multiple files from Alibaba Cloud OSS using semicolon-separated URLs.
- **Parameters**:
  - `file_urls`: Multiple URLs of files in Alibaba Cloud OSS, separated by semicolon (;)

#### 5. Get Public File by URL (get_public_file_by_url)

Dedicated tool for downloading publicly accessible files from any platform without requiring API keys.
- **Parameters**:
  - `file_url`: The URL of a publicly accessible file from any platform

### Examples

#### Upload File
<img width="2064" height="865" alt="upload-01" src="https://github.com/user-attachments/assets/045985dc-f56c-4d25-9996-eed9a63274a6" />

#### Batch Upload Files
<img width="1981" height="862" alt="upload-02" src="https://github.com/user-attachments/assets/b5de5a4a-aec8-4b70-a98d-9073ad573e84" />

#### Get File by URL
<img width="2014" height="492" alt="download-01" src="https://github.com/user-attachments/assets/bf90e661-5ea9-4080-8592-e4e2c9acefaa" />
<img width="1940" height="499" alt="download-02" src="https://github.com/user-attachments/assets/f5506d0a-0a43-4210-a5a7-8c4010cb95fc" />





### Notes

- Ensure your OSS bucket has the correct permissions configured
- The plugin requires valid Alibaba Cloud credentials with appropriate OSS access permissions
- For very large files, consider using multipart upload functionality (not currently implemented)

### Developer Information

- **Author**: `https://github.com/sawyer-shi`
- **Email**: sawyer36@foxmail.com
- **License**: MIT License
- **Support**: Through Dify platform and GitHub Issues
- **Souce Code**: `https://github.com/sawyer-shi/dify-plugins-aliyun_oss`

---

**Ready to seamlessly integrate with Alibaba Cloud OSS?**



