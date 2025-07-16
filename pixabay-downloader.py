import os
import asyncio
import aiohttp
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import webbrowser
import json
from datetime import datetime
from pathlib import Path
import threading
from urllib.parse import urlparse
import hashlib
from PIL import Image, ImageTk
import requests
from io import BytesIO

class PixabayDownloader:
    def __init__(self):
        self.setup_config()
        self.setup_ui()
        self.session = None
        self.download_tasks = []
        self.is_downloading = False
        
    def setup_config(self):
        """Setup configuration and folders"""
        self.config_file = Path.home() / ".pixabay_downloader" / "config.json"
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Default config
        self.config = {
            "api_key": "",
            "download_folder": str(Path.home() / "Downloads" / "Pixabay"),
            "results_per_page": 100,
            "image_type": "vector",
            "quality": "largeImageURL",
            "create_subfolders": True,
            "avoid_duplicates": True
        }
        
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except Exception as e:
            print(f"Error loading config: {e}")
            
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def setup_ui(self):
        """Setup the modern UI"""
        self.root = tk.Tk()
        self.root.title("Pixabay Image Downloader v2.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Pixabay Image Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # API Key
        ttk.Label(settings_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_key_var = tk.StringVar(value=self.config.get("api_key", ""))
        self.api_key_entry = ttk.Entry(settings_frame, textvariable=self.api_key_var, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, pady=2, padx=(10, 0))
        
        # Download folder
        ttk.Label(settings_frame, text="Download Folder:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.folder_var = tk.StringVar(value=self.config.get("download_folder", ""))
        self.folder_entry = ttk.Entry(settings_frame, textvariable=self.folder_var, width=40)
        self.folder_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=2, padx=(10, 0))
        ttk.Button(settings_frame, text="Browse", command=self.browse_folder).grid(row=1, column=2, pady=2, padx=(5, 0))
        
        # Options frame
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(10, 0))
        
        # Image type
        ttk.Label(options_frame, text="Type:").grid(row=0, column=0, sticky=tk.W)
        self.image_type_var = tk.StringVar(value=self.config.get("image_type", "vector"))
        image_type_combo = ttk.Combobox(options_frame, textvariable=self.image_type_var, 
                                       values=["all", "photo", "illustration", "vector"], width=15)
        image_type_combo.grid(row=0, column=1, padx=(5, 15))
        
        # Quality
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=2, sticky=tk.W)
        self.quality_var = tk.StringVar(value=self.config.get("quality", "largeImageURL"))
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var,
                                    values=["webformatURL", "largeImageURL", "fullHDURL", "vectorURL"], width=15)
        quality_combo.grid(row=0, column=3, padx=(5, 15))
        
        # Results per page
        ttk.Label(options_frame, text="Results:").grid(row=0, column=4, sticky=tk.W)
        self.results_var = tk.StringVar(value=str(self.config.get("results_per_page", 100)))
        results_combo = ttk.Combobox(options_frame, textvariable=self.results_var,
                                    values=["20", "50", "100", "200"], width=8)
        results_combo.grid(row=0, column=5, padx=(5, 0))
        
        # Checkboxes
        checkbox_frame = ttk.Frame(settings_frame)
        checkbox_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        self.subfolder_var = tk.BooleanVar(value=self.config.get("create_subfolders", True))
        ttk.Checkbutton(checkbox_frame, text="Create subfolders", variable=self.subfolder_var).pack(side=tk.LEFT, padx=(0, 20))
        
        self.duplicate_var = tk.BooleanVar(value=self.config.get("avoid_duplicates", True))
        ttk.Checkbutton(checkbox_frame, text="Avoid duplicates", variable=self.duplicate_var).pack(side=tk.LEFT)
        
        # Save settings button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).grid(row=4, column=2, pady=(10, 0))
        
        # Search frame
        search_frame = ttk.LabelFrame(main_frame, text="Search & Download", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search input
        ttk.Label(search_frame, text="Search Query:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=2, padx=(10, 0))
        self.search_entry.bind('<Return>', lambda e: self.start_download())
        
        # Buttons
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.download_btn = ttk.Button(button_frame, text="Download Images", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Open Folder", command=self.open_download_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.pack(anchor=tk.W)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Download Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable text widget
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure grid weights
        settings_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(1, weight=1)
        
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
            
    def save_settings(self):
        """Save current settings"""
        self.config.update({
            "api_key": self.api_key_var.get(),
            "download_folder": self.folder_var.get(),
            "results_per_page": int(self.results_var.get()),
            "image_type": self.image_type_var.get(),
            "quality": self.quality_var.get(),
            "create_subfolders": self.subfolder_var.get(),
            "avoid_duplicates": self.duplicate_var.get()
        })
        self.save_config()
        self.log("Settings saved successfully")
        
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def start_download(self):
        """Start the download process in a separate thread"""
        if not self.api_key_var.get():
            messagebox.showerror("Error", "Please enter your Pixabay API key")
            return
            
        if not self.search_var.get():
            messagebox.showerror("Error", "Please enter a search query")
            return
            
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_images)
        thread.daemon = True
        thread.start()
        
    def cancel_download(self):
        """Cancel the download process"""
        self.is_downloading = False
        self.update_status("Cancelling...")
        self.log("Download cancelled by user")
        
    def download_images(self):
        """Main download function"""
        try:
            asyncio.run(self.async_download())
        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.progress_var.set(0)
            self.update_status("Ready")
            
    async def async_download(self):
        """Async download implementation"""
        query = self.search_var.get()
        self.log(f"Searching for '{query}'...")
        
        # Search for images
        image_urls = await self.search_pixabay_images(query)
        
        if not image_urls:
            self.log("No images found")
            return
            
        self.log(f"Found {len(image_urls)} images")
        
        # Create download folder
        download_path = Path(self.folder_var.get())
        if self.subfolder_var.get():
            download_path = download_path / query.replace(" ", "_")
        download_path.mkdir(parents=True, exist_ok=True)
        
        # Download images
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, url in enumerate(image_urls):
                if not self.is_downloading:
                    break
                task = self.download_image(session, url, download_path, i + 1)
                tasks.append(task)
                
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                
        self.log("Download completed!")
        
    async def search_pixabay_images(self, query):
        """Search Pixabay API"""
        try:
            params = {
                'key': self.api_key_var.get(),
                'q': query,
                'image_type': self.image_type_var.get(),
                'per_page': self.results_var.get(),
                'safesearch': 'true'
            }
            
            url = "https://pixabay.com/api/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        quality_key = self.quality_var.get()
                        return [hit.get(quality_key) for hit in data.get('hits', []) if hit.get(quality_key)]
                    else:
                        self.log(f"API Error: {response.status}")
                        return []
                        
        except Exception as e:
            self.log(f"Search error: {str(e)}")
            return []
            
    async def download_image(self, session, url, download_path, index):
        """Download a single image"""
        try:
            if not self.is_downloading:
                return
                
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # Generate filename
                    parsed_url = urlparse(url)
                    original_name = Path(parsed_url.path).name
                    file_extension = Path(original_name).suffix or '.jpg'
                    
                    filename = f"{self.search_var.get().replace(' ', '_')}_{index:03d}{file_extension}"
                    file_path = download_path / filename
                    
                    # Check for duplicates
                    if self.duplicate_var.get() and file_path.exists():
                        file_hash = hashlib.md5(content).hexdigest()
                        if file_path.exists():
                            with open(file_path, 'rb') as f:
                                existing_hash = hashlib.md5(f.read()).hexdigest()
                            if file_hash == existing_hash:
                                self.log(f"Skipped duplicate: {filename}")
                                return
                    
                    # Save file
                    with open(file_path, 'wb') as f:
                        f.write(content)
                        
                    self.log(f"Downloaded: {filename}")
                    
                    # Update progress
                    current_progress = (index / int(self.results_var.get())) * 100
                    self.progress_var.set(current_progress)
                    self.update_status(f"Downloaded {index} images...")
                    
                else:
                    self.log(f"Failed to download image {index}: HTTP {response.status}")
                    
        except Exception as e:
            self.log(f"Error downloading image {index}: {str(e)}")
            
    def open_download_folder(self):
        """Open the download folder"""
        folder_path = Path(self.folder_var.get())
        if self.subfolder_var.get() and self.search_var.get():
            folder_path = folder_path / self.search_var.get().replace(" ", "_")
            
        if folder_path.exists():
            webbrowser.open(str(folder_path))
        else:
            messagebox.showwarning("Warning", "Folder doesn't exist yet")
            
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PixabayDownloader()
    app.run()
