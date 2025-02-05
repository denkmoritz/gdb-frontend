# Frontend Setup Guide

## About the Application
This application is a frontend built using Streamlit that integrates interactive maps with Folium. It allows users to visualize geospatial data and interact with map features dynamically. The application leverages `streamlit_folium` for rendering maps within Streamlit, along with `requests` for API interactions and `watchdog` for monitoring changes.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.11
- `pip3` (Python package manager)

## Setting Up the Virtual Environment
To maintain a clean and isolated Python environment, it is recommended to use a virtual environment.

### Steps:
1. **Create a Virtual Environment:**
   ```sh
   python3 -m venv venv
   ```
2. **Activate the Virtual Environment:**
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```

## Installing Dependencies
After activating the virtual environment, install the required dependencies using `pip3`:
```sh
pip3 install -r requirements.txt
```

## Running the Application
Once the dependencies are installed, you can run the frontend application using:
```sh
streamlit run app.py
```

## Installed Dependencies
The required dependencies are listed in `requirements.txt`, which includes:
- `streamlit`
- `folium`
- `streamlit_folium`
- `requests`
- `watchdog`

## Additional Notes
- Ensure all dependencies are installed in the virtual environment before running the application.
- If any package is missing or you face issues, try running `pip3 install -r requirements.txt` again.