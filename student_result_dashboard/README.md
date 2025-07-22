# Student Result Dashboard

A comprehensive web-based student result management system built with Python Flask, SQLite, and modern HTML/CSS. This application allows educators to manage student information, enter marks, calculate grades, and generate visual reports.

## Features

### 📊 Core Functionality
- **Student Management**: Add and manage student information
- **Marks Entry**: Enter marks for multiple subjects per student
- **Automatic Calculations**: Calculate percentage, grade, and rank automatically
- **Visual Reports**: Interactive charts and graphs for performance analysis
- **Result Dashboard**: Comprehensive overview with statistics and recent results

### 🎯 Key Features
- **Multi-subject Support**: Default subjects include Mathematics, Science, English, Social Studies, and Computer Science
- **Grade Calculation**: Automatic grade assignment (A+, A, B+, B, C, D, F) based on percentage
- **Ranking System**: Automatic student ranking based on performance
- **Search & Filter**: Advanced filtering by class, grade, and search functionality
- **Export Options**: Export results to CSV format
- **Print Support**: Print-friendly result reports
- **Responsive Design**: Mobile-friendly interface using Bootstrap

### 📈 Visual Analytics
- **Grade Distribution Chart**: Pie chart showing grade distribution across students
- **Subject Performance**: Bar chart displaying average marks per subject
- **Individual Performance**: Detailed student performance analysis
- **Performance Trends**: Visual indicators for student progress

## Tech Stack

- **Backend**: Python 3.7+ with Flask framework
- **Database**: SQLite (file-based, no setup required)
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3
- **Charts**: Chart.js for interactive visualizations
- **Icons**: Font Awesome 6.0

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd student_result_dashboard
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   Open your web browser and navigate to: `http://localhost:5000`

## Usage Guide

### 1. Adding Students
- Navigate to "Add Student" from the main menu
- Fill in student name, roll number, and class
- Roll numbers must be unique for each student

### 2. Entering Marks
- Go to "Enter Marks" section
- Select a student from the dropdown
- Enter marks for each subject (0-100)
- The system automatically calculates percentage and grade
- Click "Save Marks" to store the results

### 3. Viewing Results
- Access "Results" to see all student performance
- Use search and filter options to find specific students
- Click on student names for detailed performance analysis
- Export results to CSV or print reports

### 4. Dashboard Overview
- View key statistics and performance metrics
- Interactive charts showing grade distribution and subject averages
- Recent results and quick action buttons

## Database Schema

### Students Table
- `id`: Primary key
- `name`: Student name
- `roll_no`: Unique roll number
- `class_name`: Student's class
- `created_at`: Timestamp

### Subjects Table
- `id`: Primary key
- `name`: Subject name
- `max_marks`: Maximum marks (default: 100)

### Marks Table
- `id`: Primary key
- `student_id`: Foreign key to students
- `subject_id`: Foreign key to subjects
- `marks`: Marks obtained

## Grading System

| Percentage | Grade |
|------------|-------|
| 90-100%    | A+    |
| 80-89%     | A     |
| 70-79%     | B+    |
| 60-69%     | B     |
| 50-59%     | C     |
| 40-49%     | D     |
| Below 40%  | F     |

## File Structure

```
student_result_dashboard/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── database.db           # SQLite database (created automatically)
│
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard homepage
│   ├── add_student.html  # Add student form
│   ├── enter_marks.html  # Enter marks form
│   ├── results.html      # Results listing
│   └── student_detail.html # Individual student details
│
└── static/              # Static files
    └── style.css        # Custom CSS styles
```

## API Endpoints

- `GET /` - Dashboard homepage
- `GET,POST /add_student` - Add new student
- `GET,POST /enter_marks` - Enter student marks
- `GET /results` - View all results
- `GET /student_detail/<id>` - Individual student details
- `GET /api/chart_data` - JSON data for charts

## Customization

### Adding New Subjects
Edit the `default_subjects` list in `app.py`:
```python
default_subjects = [
    ('Mathematics', 100),
    ('Science', 100),
    ('English', 100),
    ('Social Studies', 100),
    ('Computer Science', 100),
    ('Your New Subject', 100)  # Add here
]
```

### Modifying Grade Boundaries
Update the `calculate_grade()` function in `app.py`:
```python
def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    # Modify boundaries as needed
```

### Styling Changes
Customize the appearance by editing `static/style.css` or modifying Bootstrap classes in templates.

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

2. **Database Errors**
   - Delete `database.db` file and restart the application to recreate

3. **Missing Dependencies**
   - Ensure all packages are installed: `pip install -r requirements.txt`

4. **Permission Errors**
   - Run command prompt/terminal as administrator
   - Check file permissions in the project directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue with detailed description

## Future Enhancements

- User authentication and role management
- Bulk import/export functionality
- Email notifications for results
- Advanced analytics and reporting
- Mobile app version
- Multi-language support

---

**Built with ❤️ using Python Flask and modern web technologies**
