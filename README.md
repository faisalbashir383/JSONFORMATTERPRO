# JSON Formatter Pro

A comprehensive web application for formatting, validating, minifying, and converting JSON data. Built with Django backend and modern HTML/CSS/JavaScript frontend.

## Features

- ✨ **Format JSON** - Pretty print with proper indentation
- 📦 **Minify JSON** - Compress by removing whitespace
- ✓ **Validate JSON** - Check structure with detailed error messages
- 🔄 **Convert to XML** - Transform JSON to XML format
- 📊 **Convert to CSV** - Export JSON as CSV
- 🌓 **Dark/Light Mode** - Toggle between themes
- 📁 **File Upload** - Drag and drop JSON files
- ⬇️ **Download Output** - Save results as JSON/XML/CSV
- 📱 **Responsive Design** - Works on all devices

## Installation

1. **Clone the repository**
   ```bash
   cd /Users/faisalahmad/Documents/Projects/JSON/JSONFORMATTERPRO
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers dicttoxml
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   Navigate to `http://127.0.0.1:8000/`

## Usage

### Format JSON
1. Paste your JSON in the input textarea
2. Click "Format JSON" button
3. View the formatted output

### Minify JSON
1. Enter JSON in the input area
2. Click "Minify JSON" to compress

### Validate JSON
1. Paste JSON to validate
2. Click "Validate JSON"
3. See validation result

### Convert Formats
- Click "Convert to XML" for XML output
- Click "Convert to CSV" for CSV output

### File Operations
- **Upload**: Drag and drop `.json` file or click upload area
- **Download**: Click "Download" to save output

### Keyboard Shortcuts
- `Ctrl/Cmd + Enter` - Format JSON
- `Ctrl/Cmd + K` - Clear all

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/format/` | POST | Format JSON |
| `/api/minify/` | POST | Minify JSON |
| `/api/validate/` | POST | Validate JSON |
| `/api/convert/xml/` | POST | Convert to XML |
| `/api/convert/csv/` | POST | Convert to CSV |

### Request Format
```json
{
  "data": "your_json_string_here"
}
```

### Response Format
```json
{
  "success": true,
  "formatted": "formatted_result"
}
```

## Technologies Used

**Backend:**
- Django 6.0
- Django REST Framework
- django-cors-headers
- dicttoxml

**Frontend:**
- HTML5
- CSS3 (custom properties, animations)
- Vanilla JavaScript (ES6+)
- Google Fonts (Inter)

## Project Structure

```
JSONFORMATTERPRO/
├── formatter/              # Main app
│   ├── templates/         # HTML templates
│   │   └── index.html
│   ├── static/           # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   ├── views.py          # API views
│   └── urls.py           # URL routing
├── jsonformatter/         # Project settings
│   ├── settings.py
│   └── urls.py
├── manage.py
└── venv/                 # Virtual environment
```

## Features Documentation

### Theme Toggle
The application supports light and dark modes. Click the sun/moon icon to toggle. Theme preference is saved in localStorage.

### Error Handling
All operations include comprehensive error handling with user-friendly messages displayed as toast notifications.

### Responsive Design
- Desktop: Two-column layout
- Tablet: Optimized spacing
- Mobile: Single column, full-width buttons

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Accessing Admin Panel
Navigate to `http://127.0.0.1:8000/admin/`

## License

This project is for demonstration and educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the repository.
