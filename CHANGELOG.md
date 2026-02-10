# CHANGELOG

## Version 1.1.0 (2025-02-10)

### ✨ New Features
- **Added:** Excel file upload support (.xlsx, .xls)
  - Replaced CSV upload with Excel upload
  - Better compatibility with business workflows
  - Support for both modern (.xlsx) and legacy (.xls) formats
  
- **Added:** Enhanced error handling for Excel files
  - Clear error messages for file format issues
  - Validation for proper data structure
  - Helpful tips when upload fails

### 📦 Dependencies
- **Added:** openpyxl 3.1.5 for Excel support

### 📁 Sample Files
- **Updated:** All sample data files now in .xlsx format
  - contoh_data_radar.xlsx
  - contoh_data_grouped.xlsx
  - contoh_data_histogram.xlsx
  - contoh_data_bar.xlsx

### 📝 Documentation
- **Updated:** README.md with Excel upload instructions
- **Updated:** QUICKSTART.md with Excel tutorial
- **Removed:** CSV references (replaced with Excel)

---

## Version 1.0.1 (2025-02-10)

### 🐛 Bug Fixes
- **Fixed:** Error "float object cannot be interpreted as an integer"
  - Improved number parsing to properly handle both integers and floats
  - Added better validation for user input
  - Enhanced error messages with specific error details
  
- **Fixed:** Empty string handling in data parsing
  - Now properly filters out empty strings from comma-separated input
  - Prevents crashes from trailing commas or extra spaces

### ✨ Enhancements
- **Added:** Developer credit section in sidebar
- **Added:** Professional footer with contact information
- **Improved:** Input validation with better error messages
- **Improved:** Number type detection (automatic int/float conversion)

### 👨‍💻 Developer
- Tubagus Robbi Megantara (tubagusrobbimegantara@gmail.com)

---

## Version 1.0.0 (2025-02-10)

### 🎉 Initial Release

#### Features
- 7 types of visualizations:
  - Radar/Spider Chart
  - Horizontal Bar Chart
  - Vertical Bar Chart
  - Histogram with density curve
  - Pie Chart
  - Grouped Bar Chart
  - Stacked Bar Chart

- Data input methods:
  - Manual input (comma-separated)
  - CSV file upload
  
- Customization options:
  - 5 color schemes + custom color picker
  - Adjustable size (8-20 x 6-18)
  - Resolution control (100-300 DPI)
  - Custom titles
  
- Export formats:
  - PNG (high quality)
  - PDF (vector)
  - SVG (scalable)

- UI/UX:
  - Professional dark theme
  - Responsive 2-column layout
  - Interactive sidebar controls
  - Real-time preview

#### Technology Stack
- Streamlit 1.40.2
- Matplotlib 3.9.3
- Seaborn 0.13.2
- Pandas 2.2.3
- NumPy 2.2.1
- SciPy 1.15.0

#### Known Issues
- None reported

---

## Upcoming Features (Planned)

### Version 1.1.0
- [ ] Box plot visualization
- [ ] Scatter plot with trend line
- [ ] Heatmap visualization
- [ ] Multiple chart export (batch download)
- [ ] Chart templates (save/load settings)
- [ ] Data table preview
- [ ] Statistics summary panel

### Version 1.2.0
- [ ] Interactive plotly charts
- [ ] Chart animation options
- [ ] Dark/Light theme toggle
- [ ] Multi-language support (EN/ID)
- [ ] Chart comparison view
- [ ] Export to PowerPoint
- [ ] Database integration (PostgreSQL/MySQL)

### Version 2.0.0
- [ ] Dashboard builder (drag & drop)
- [ ] Real-time data updates
- [ ] User authentication
- [ ] Shared dashboard links
- [ ] Advanced analytics (predictions, forecasting)
- [ ] Mobile app version

---

## Bug Reports & Feature Requests

Please contact: tubagusrobbimegantara@gmail.com

---

**Maintained by:** Tubagus Robbi Megantara  
**License:** MIT  
**Last Updated:** February 10, 2025
