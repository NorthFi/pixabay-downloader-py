# 🎨 Pixabay Downloader v2.0

> A modern, feature-rich desktop application for bulk downloading high-quality images from Pixabay

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/NorthFi/pixabay-downloader-py)

## ✨ Features

### 🚀 **Modern Interface**
- Clean, intuitive GUI built with tkinter
- Real-time progress tracking
- Comprehensive download logs with timestamps
- Responsive design that adapts to window resizing

### ⚙️ **Advanced Configuration**
- **Persistent Settings**: Your preferences are saved between sessions
- **Multiple Image Types**: Photos, illustrations, vectors, or all
- **Quality Selection**: Web format, large, full HD, or vector quality
- **Flexible Results**: Download 20 to 200 images per search
- **Smart Organization**: Optional subfolder creation per search query

### 🔧 **Intelligent Features**
- **Duplicate Detection**: MD5 hashing prevents downloading identical images
- **Robust Error Handling**: Graceful handling of network issues and API errors
- **Concurrent Downloads**: Asynchronous downloading for maximum speed
- **Cancellation Support**: Stop downloads at any time
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📸 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x600/2c3e50/ffffff?text=Modern+Clean+Interface)

### Settings Panel
![Settings Panel](https://via.placeholder.com/800x300/34495e/ffffff?text=Comprehensive+Settings)

### Download in Progress
![Download Progress](https://via.placeholder.com/800x200/27ae60/ffffff?text=Real-Time+Progress+Tracking)

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Pixabay API key (free registration required)

### Required Dependencies
```bash
pip install aiohttp pillow requests pathlib
```

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/NorthFi/pixabay-downloader-py.git
   cd pixabay-downloader-py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Pixabay API key**
   - Visit [Pixabay API Documentation](https://pixabay.com/api/docs/)
   - Create a free account
   - Generate your API key

4. **Run the application**
   ```bash
   python pixabay_downloader.py
   ```

## 🎯 Usage

### Basic Usage
1. **Configure Settings**: Enter your Pixabay API key in the settings section
2. **Choose Options**: Select image type, quality, and number of results
3. **Search & Download**: Enter your search query and click "Download Images"
4. **Monitor Progress**: Watch real-time progress and check the download log

### Advanced Configuration

#### Image Types
- **All**: Download any type of image
- **Photo**: Real photographs only
- **Illustration**: Digital artwork and illustrations
- **Vector**: Scalable vector graphics (SVG, AI)

#### Quality Options
- **Web Format**: Optimized for web use (smaller file size)
- **Large**: High-quality images suitable for most uses
- **Full HD**: Maximum quality for professional use
- **Vector**: Original vector format (when available)

#### Organization Features
- **Create Subfolders**: Automatically organize downloads by search query
- **Avoid Duplicates**: Skip files that have already been downloaded
- **Custom Download Path**: Choose where to save your images

## 🔧 Configuration

The application stores settings in `~/.pixabay_downloader/config.json`:

```json
{
  "api_key": "your-api-key-here",
  "download_folder": "/path/to/downloads",
  "results_per_page": 100,
  "image_type": "vector",
  "quality": "largeImageURL",
  "create_subfolders": true,
  "avoid_duplicates": true
}
```

## 🚀 Features in Detail

### Asynchronous Downloads
- Concurrent downloading for maximum speed
- Non-blocking UI during operations
- Efficient resource management

### Smart Duplicate Detection
- MD5 hash comparison prevents duplicate downloads
- Maintains download history across sessions
- Saves bandwidth and storage space

### Error Handling
- Graceful handling of network timeouts
- API rate limit respect
- Detailed error logging for troubleshooting

### File Management
- Sequential numbering with original extensions
- Safe filename generation (replaces invalid characters)
- Automatic folder creation

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/NorthFi/pixabay-downloader-py.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📋 Requirements

```txt
aiohttp>=3.8.0
pillow>=8.0.0
requests>=2.25.0
pathlib>=1.0.0
```

## 🐛 Known Issues

- Vector downloads may not work for all images (depends on Pixabay availability)
- Large batch downloads may be rate-limited by Pixabay API
- Some antivirus software may flag the executable (false positive)

## 🔮 Roadmap

- [ ] **Image Preview**: Thumbnail preview before downloading
- [ ] **Batch Search**: Multiple search queries in one session
- [ ] **Filter Options**: Size, color, category filters
- [ ] **Export Lists**: Save search results for later
- [ ] **Download History**: Track all previous downloads
- [ ] **Image Metadata**: Save image tags and descriptions
- [ ] **Dark Mode**: Toggle between light and dark themes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Pixabay](https://pixabay.com/) for providing the excellent free image API
- [aiohttp](https://aiohttp.readthedocs.io/) for async HTTP client capabilities
- [Pillow](https://pillow.readthedocs.io/) for image processing features

## 📞 Support

Having issues? Here's how to get help:

1. **Check the [Issues](https://github.com/NorthFi/pixabay-downloader-py/issues)** page
2. **Search existing issues** before creating a new one
3. **Provide detailed information** when reporting bugs:
   - Operating system
   - Python version
   - Error messages
   - Steps to reproduce

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=NorthFi/pixabay-downloader-p&type=Date)](https://star-history.com/#NorthFi/pixabay-downloader-py&Date)

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/NorthFi">Your Name</a></p>
  <p>If this project helped you, please consider giving it a ⭐!</p>
</div>
