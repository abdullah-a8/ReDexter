# ReDexter - Rclone Decrypter

A modern PyQt6-based GUI application for decrypting files encrypted with rclone's crypt remote.

## Features

- **Modern Typography**: Professional font hierarchy with recommended modern fonts
- **Multiple Themes**: Choose from 4 different themes
- **Drag & Drop Support**: Easy file selection through drag and drop interface
- **Rclone Config Integration**: Load credentials directly from rclone configuration files with automatic deobfuscation
- **Batch Processing**: Decrypt multiple files simultaneously with progress tracking
- **Secure Credential Storage**: Uses OS keyring for secure password storage
- **Threaded Operations**: Non-blocking UI with background decryption processing

## Installation

### Prerequisites
- Python 3.12+
- rclone (for config file loading functionality)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Recommended Fonts (Optional)
For optimal typography experience:

**Fedora/RHEL:**
```bash
sudo dnf install google-roboto-fonts
```

**Ubuntu/Debian:**
```bash
sudo apt install fonts-roboto fonts-inter
```

**Arch Linux:**
```bash
sudo pacman -S ttf-roboto
```

### Run the Application
```bash
python main.py
```

## Usage

1. **Select Theme**: Use the sidebar to choose your preferred theme from 4 available options
2. **Load Configuration**: 
   - Import your rclone config file to automatically extract crypt remote credentials
   - Or manually enter your crypt password and salt
3. **Add Files**: Drag and drop encrypted files or use the Browse button
4. **Decrypt**: Click "Decrypt Files" to start the batch decryption process

## Technical Working

### Core Architecture

ReDexter implements rclone's crypt file format specification for decryption. The application follows a modular architecture:

- **UI Layer**: PyQt6-based modern interface with theme system
- **Crypto Layer**: Handles file decryption using NaCl (libsodium) cryptographic library
- **Config Layer**: Manages rclone configuration parsing and credential extraction
- **Storage Layer**: Secure credential persistence using OS keyring

### Decryption Process

#### File Format Specification
Rclone crypt files use the following binary format:
- **Magic Header**: 8 bytes (`RCLONE\x00\x00`) for file validation
- **Nonce**: 24 bytes initial nonce for the first block
- **Encrypted Blocks**: Variable number of encrypted data blocks

#### Block Structure
Each encrypted block contains:
- **Block Size**: 64KB (65,536 bytes) of plaintext data
- **MAC**: Message Authentication Code (16 bytes) for integrity verification
- **Total Block Size**: 64KB + 16 bytes MAC = 65,552 bytes per encrypted block

#### Key Derivation
The application uses scrypt key derivation function:
1. **Input**: User password and salt (16 or 32 bytes)
2. **Salt Processing**: 
   - 16-byte salts are doubled to 32 bytes
   - Other lengths are SHA-256 hashed to 32 bytes
   - Default salt used if none provided
3. **Scrypt Parameters**: Interactive opslimit and memlimit for security
4. **Output**: 32-byte key for NaCl SecretBox

#### Decryption Algorithm
```
1. Read and validate magic header
2. Extract 24-byte nonce
3. For each encrypted block:
   a. Read block (up to 65,552 bytes)
   b. Decrypt using NaCl SecretBox with current nonce
   c. Write decrypted data to output file
   d. Increment nonce (little-endian) for next block
4. Complete when all blocks processed
```

#### Nonce Management
- **Initial Nonce**: Read from file header (24 bytes)
- **Increment Strategy**: Little-endian integer increment for each block
- **Purpose**: Ensures unique nonce per block for cryptographic security

### Configuration System

#### Rclone Config Integration
The application can load rclone configuration files through:
1. **Subprocess Call**: Uses `rclone config show` command
2. **Password Handling**: Supports config file passwords via `RCLONE_CONFIG_PASS`
3. **Parsing**: ConfigParser for INI-style rclone config format
4. **Filtering**: Automatically identifies crypt-type remotes

#### Credential Deobfuscation
Rclone obfuscates sensitive credentials in config files:
- **Method**: AES-CTR encryption with hardcoded key
- **Process**: Base64 decode → AES decrypt → UTF-8 decode
- **Purpose**: Prevents plaintext storage of passwords in config files

#### Secure Storage
- **Keyring Integration**: Uses OS-specific secure storage (Keychain/Credential Manager/Secret Service)
- **Scope**: Config file paths and associated passwords
- **Cleanup**: Automatic removal when configs are cleared

### Dependencies

- **PyQt6**: Modern GUI framework for cross-platform interface
- **PyNaCl**: Cryptographic library providing scrypt and SecretBox (libsodium bindings)
- **pycryptodome**: AES implementation for rclone config deobfuscation
- **keyring**: OS keyring integration for secure credential storage
- **qtawesome**: Icon library for modern UI elements

### Performance Features

- **Threaded Decryption**: Background processing prevents UI freezing
- **Progress Tracking**: Real-time updates during batch operations
- **Memory Efficiency**: Block-based processing for large files
- **Error Handling**: Comprehensive error reporting and recovery

### Security Considerations

- **Secure Memory**: NaCl library provides secure memory handling
- **Input Validation**: File format verification before processing
- **Credential Protection**: OS keyring prevents plaintext password storage
- **Process Isolation**: Subprocess calls for rclone operations

---