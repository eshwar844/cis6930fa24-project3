Name : Venkata Sai Eshwar Idupulapati


## Project Description:

This project, part of the CIS 6930 course, focuses on building an interactive web interface for visualizing and analyzing incident data collected from the Norman Police Department. Users can upload NormanPD-style incident PDFs or provide URLs for processing. The system extracts data, stores it in a database, and provides three distinct visualizations: clustering of incident types, a bar graph of incident frequencies, and a custom line chart. This project demonstrates the final stages of a data pipeline, emphasizing user interaction and statistical insights.

##video link: 

## Assignment Objectives
## Data Extraction:

Develop functionality to extract incident data from NormanPD-style PDFs, either through file upload or URL input.
Process and structure the data for further analysis.
`Data Storage:` 

Store the extracted data in a SQLite database for efficient querying and retrieval.
Ensure the database structure supports handling multiple incident records.
`Data Analysis:`

Perform clustering and statistical analysis on the extracted data to identify patterns and trends.
Utilize machine learning techniques like K-Means clustering and PCA for dimensionality reduction.
`Data Visualization:`

Provide users with three interactive visualizations:
Clustering: Group incident types based on frequency and visualize using PCA.
Bar Graph: Display the frequency of incident types as a bar chart.
Custom Line Chart: Show frequency trends of incidents over time or categories.

`How to install`
```bash pip install pipenv```

```bash pipenv install flask```
```bash pipenv install pandas```
```bash pipenv install matplotlib```
```bash pipenv install plotly```
```bash pipenv install scikit-learn```
```bash pipenv install pypdf```
```bash pipenv install werkzeug```
```bash pipenv install pytest```
## How to run 
To execute the project , navigate to the project directory 

## 1. `To output a page use command` 
     ```bash pipenv run python main.py```

## 2. `Running test cases` 
   ```bash pipenv run python -m pytest ```

## Project Workflow Description
The Norman PD Incident Visualization project is designed to process police incident data from NormanPD-style reports and provide interactive visualizations. Here is an explanation of how each part of the project functions:

## 1. ` Input `
`The project accepts incident data through two methods:`

`File Upload:` Users can upload one or more PDF files containing NormanPD-style incident reports directly via the web interface.
`URL Input:` Users can input URLs pointing to incident PDF files. The application downloads the files and processes the data.
This ensures flexibility, allowing users to work with locally stored files or remotely hosted data. The application is designed to handle multiple files or URLs simultaneously for batch processing.

## 2. `PDF Processing`
After receiving the files or URLs, the system extracts meaningful information from the PDFs. It utilizes the PyPDF library to read the content of the PDFs. The text is parsed line by line to identify relevant fields such as:

`Incident Time`
`Incident Number`
`Incident Location`
`Nature of the Incident`
`Incident ORI (Originating Agency Identifier)`
The extracted data is validated to ensure it is structured correctly. For instance, the application checks if the date format is valid and combines lines if data is split across them in the PDF.

This step transforms unstructured incident reports into structured data suitable for analysis and storage.

## 3. `Data Storage`
The extracted incident data is stored in a SQLite database. The database schema is designed to include columns for all key fields (time, number, location, nature, and ORI). This database acts as the backbone for retrieving and analyzing data.

Before storing the data, the application checks if an existing database exists. If so, it clears it to ensure the database reflects the latest data.
Data is inserted in bulk to ensure efficiency, especially when processing multiple PDFs or URLs.
This structured storage enables quick querying and supports seamless integration with visualization tools.

## 4. ` Visualization`
The project provides three interactive visualizations to help users analyze the incident data:

## a. ` Clustering Visualization`
This visualization groups incident types by their frequency using K-Means clustering. To make the data suitable for visualization, the application applies Principal Component Analysis (PCA) to reduce the dimensions of the data. The clusters are plotted interactively, allowing users to observe patterns and relationships between different types of incidents.

For example, incidents like "Vandalism" and "Trespassing" may cluster together based on frequency, providing insights into common occurrences.

## b. `Bar Graph Visualization`
This visualization presents a bar chart showing the frequency of each incident type. It helps users quickly identify which types of incidents are most or least frequent. For instance, "Noise Complaints" might appear more frequently than "Kidnapping," highlighting trends in the data.

## c. `Custom Visualization`
The custom visualization displays the frequency trends of incidents using a line chart. This chart helps users see how certain types of incidents compare over time or categories. Markers on the line chart make it easy to observe peak frequencies.

Each visualization is designed to be interactive and intuitive, allowing users to explore the data from multiple perspectives.

## End-to-End Workflow
`Input:` Users provide the incident data via file upload or URL.
`PDF Processing:` The system extracts structured data from the PDFs, ensuring all fields are correctly parsed and validated.
`Storage:` The structured data is stored in a SQLite database, enabling efficient querying and analysis.
`Visualization:` The data is analyzed and presented as:
A clustering chart for grouping incidents by frequency.
A bar graph for comparing incident types.
A custom line chart for visualizing trends.


`Functions`
`main.py` 

## 1. `validate_date(date_string, date_format="%m/%d/%Y")`
Purpose: This function checks if a given string is a valid date in the specified format (MM/DD/YYYY by default).
Input:
date_string: A string representing the date (e.g., "12/01/2024").
date_format: The expected date format (default: "%m/%d/%Y").
How It Works:
Attempts to parse the date_string using Python's datetime.strptime() method.
If the string does not match the format, a ValueError is raised, and the function returns False.
Output: Returns True if the date is valid, otherwise False.
Expected Use: Ensures that incident records from PDFs contain valid dates.

 ## 2. `fetchincidents(url)`
Purpose: Downloads a PDF from a given URL.
Input:
url: The URL of the PDF file to be downloaded.
How It Works:
Sends an HTTP request to the provided URL with a user-agent header to simulate a browser request.
Checks the response's Content-Type header to ensure the file is a PDF.
Saves the downloaded file as incident_report.pdf in the uploads folder.
Output: Returns the file path of the saved PDF.
Expected Use: Downloads incident reports from online sources for further processing.

## 3. `extractincidents(pdf_file)`
Purpose: Reads a PDF file and extracts incident data.
Input:
pdf_file: The file path to the PDF file.
How It Works:
Opens the PDF using the PdfReader library.
Extracts text from each page of the PDF.
Processes each line of text to extract structured data like dates, incident numbers, and descriptions.
Combines multi-line entries and ensures only valid data (e.g., lines with valid dates) is included.
Output: A list of incident records (each as a single string).
Expected Use: Converts raw PDF text into structured incident data for storage and analysis.
Database Functions

## 4. `createdb()`
Purpose: Creates a new SQLite database and a table for storing incidents.
Input: None (operates on the database file specified in the configuration).
How It Works:
Deletes the existing database file if it exists.
Connects to the database and creates a table named incidents with columns for:
incident_time: Date and time of the incident.
incident_number: Unique identifier for the incident.
incident_location: Where the incident occurred.
nature: Type of incident (e.g., "Theft," "Vandalism").
incident_ori: Originating agency identifier.
Output: None (creates the database schema).
Expected Use: Sets up the database structure for storing incident data.

## 5. `populatedb(db, incidents, nature_list)`
Purpose: Inserts extracted incident data into the database.
Input:
db: The database file path.
incidents: A list of incident records extracted from PDFs.
nature_list: A predefined list of valid incident types (e.g., "Theft," "Burglary").
How It Works:
Parses each incident string to extract fields (e.g., date, incident number, nature).
Matches the incident nature with the nature_list and extracts location data.
Inserts structured records into the incidents table.
Output: None (populates the database).
Expected Use: Converts raw incident strings into structured records in the database.

# 6. `fetch_incidents()`
Purpose: Retrieves all stored incident data from the database.
Input: None.
How It Works:
Connects to the database and executes a query to fetch all rows from the incidents table.
Converts the data into a pandas DataFrame for easy manipulation and analysis.
Output: A pandas DataFrame containing all incident records.
Expected Use: Provides structured incident data for visualization or reporting.

`Flask Routes`
# 7. `/upload`
Purpose: Handles file uploads from users.
Input:
Uploaded PDF files containing incident data.
How It Works:
Saves the uploaded files to the uploads folder.
Calls extractincidents() to extract data from each file.
Calls createdb() and populatedb() to store the extracted data in the database.
Output: Returns a JSON response indicating the number of files processed.
Expected Use: Allows users to upload incident reports for analysis.

# 8. `/process_url`
Purpose: Processes URLs pointing to incident PDFs.
Input:
A list of URLs provided in the request body (JSON or form data).
How It Works:
Downloads each PDF using fetchincidents().
Extracts and processes the data using extractincidents().
Populates the database using createdb() and populatedb().
Output: Returns a JSON response indicating the number of URLs processed.
Expected Use: Allows users to process remotely hosted incident reports.

# 9. `/visualize/<viz_type>`
Purpose: Provides different visualizations based on the requested type.
Input:
viz_type: A string indicating the visualization type (clustering, bargraph, or custom).
How It Works:
Fetches incident data from the database using fetch_incidents().
Calls the corresponding visualization function based on viz_type.
Output: Returns an HTML representation of the requested visualization.
Expected Use: Displays visual insights into the incident data.

## Visualization Functions
## 10. `clustering_visualization(df)`
Purpose: Groups incident types using K-Means clustering.
Input:
df: A pandas DataFrame containing incident data.
How It Works:
Calculates the frequency of each incident type.
Scales the frequency data and applies K-Means clustering.
Uses PCA to reduce dimensions for plotting.
Creates an interactive scatter plot showing clusters.
Output: HTML representation of the scatter plot.
Expected Use: Highlights clusters of incident types based on frequency.

## 11. `bar_graph_visualization(df)`
Purpose: Creates a bar chart showing incident frequencies.
Input:
df: A pandas DataFrame containing incident data.
How It Works:
Counts the occurrences of each incident type.
Creates an interactive bar chart using Plotly.
Output: HTML representation of the bar chart.
Expected Use: Compares the frequency of different incident types.

## 12. `custom_visualization(df)`
Purpose: Produces a line chart for incident frequency trends.
Input:
df: A pandas DataFrame containing incident data.
How It Works:
Counts incident frequencies.
Creates a line chart with markers to show trends.
Output: HTML representation of the line chart.
Expected Use: Displays trends in incident data over categories or time.


`index.html`
The index.html file serves as the user interface for the Norman PD Incident Visualization application. It provides users with an intuitive and visually appealing platform to upload incident reports, process URLs, and access visualizations. The design prioritizes simplicity, ensuring that both technical and non-technical users can interact with the system effortlessly.

`Structure and Layout`
The webpage is divided into distinct sections, each catering to a specific functionality:

Header Section: Displays the application's title.
Feedback Section: Provides real-time feedback on user actions (e.g., success or error messages).
File Upload Section: Allows users to upload PDF files for processing.
URL Processing Section: Enables users to input URLs for remote PDF processing.
Visualization Navigation: Links to various data visualizations generated by the system.
Visualization Display Section: Placeholder for the visual outputs of the application.
Styling and Aesthetic Choices
`The design is modern and user-focused, utilizing:`

A gradient background that transitions from green to teal, creating a calming and professional visual tone.
The Roboto font, imported from Google Fonts, for clean and readable typography.
Vivid colors like gold and orange to highlight important elements such as headings, buttons, and links.
Subtle hover effects and shadows to make the interface interactive and engaging.
`Functionality of Each Section`
# 1. `Header Section`
The header prominently displays the application's title, "Norman PD Incident Visualization," in large gold text. This sets the context for the user immediately upon landing on the page. The styling ensures the title is eye-catching, with a text shadow adding depth.

# 2. `Feedback Section`
The feedback section dynamically displays messages to users based on their actions. For example:

If a user successfully uploads a file, a success message (e.g., "File uploaded successfully!") is shown in yellow.
If an error occurs, such as uploading an invalid file type, an error message (e.g., "Invalid file format!") is displayed in red. This feedback is generated using Flask's backend and ensures that users are always aware of the application's response to their actions.
# 3. `File Upload Section`
This section allows users to upload PDF files directly from their devices. It supports multiple file uploads at once, making it convenient for processing large datasets. Users simply select the files and click the "Upload PDFs" button. The uploaded files are sent to the server for processing, and feedback is provided after the operation.

# 4. `URL Processing Section`
For users who have incident reports stored online, this section enables them to input one or more URLs pointing to PDF files. The textarea provides clear instructions on how to format the input (e.g., comma-separated URLs). After submitting the form, the URLs are processed on the server, and the extracted data is handled similarly to uploaded files. This option provides flexibility for users working with remote datasets.

# 5. `Visualization Navigation`
This section acts as a gateway to the application's visualization features. It presents three distinct links:

Clustering Visualization: Groups incidents by similarity and displays patterns in the data.
Bar Graph Visualization: Shows a frequency distribution of different incident types.
Time Series Visualization: Highlights trends over time. These links guide users directly to the visualization pages, making it easy to explore the processed data in multiple formats.
# 6. `Visualization Display Section`
At the bottom of the page, a dedicated area serves as a placeholder for visual outputs. This section is visually distinct with a dark background and rounded edges, ensuring that it stands out from the rest of the page. Users can view the generated visualizations in this area, allowing for a seamless transition from interaction to analysis.

`User Interaction Workflow`
Step 1: Users arrive at the page and are greeted by the application title and background design, setting a professional tone.
Step 2: Users choose to either upload files or input URLs, depending on their data source.
File uploads are handled through a simple "drag-and-drop" style interface.
URL inputs are entered into a large, clear textarea field.
Step 3: After submitting their files or URLs, users receive immediate feedback, such as "3 files processed successfully" or "Error: Invalid URL."
Step 4: Users navigate to the visualization section by clicking the appropriate link. Each visualization is dynamically loaded based on the processed data.
Design Considerations
Clarity and Usability: The interface is designed with minimal distractions, focusing users on their tasks (uploading files, inputting URLs, and accessing visualizations).
Consistency: Similar styles are applied across forms, buttons, and links, ensuring a cohesive experience.
Responsiveness: The layout adapts to different screen sizes, making it functional on both desktop and mobile devices.
Engagement: Subtle animations, such as button hover effects and dynamic feedback messages, keep the interface engaging.


## Test Cases :
## 1. `client()`
Purpose: Sets up a test environment for the Flask application.
How It Works:
Recreates the database by calling createdb().
Configures Flask for testing with temporary upload and static directories (test_uploads and test_static).
Creates a Flask test client that simulates user requests without running the server.
Cleans up test files and directories after tests.
Input: None (runs automatically via the pytest fixture).
Output: Provides a Flask test client for use in tests.
## 2. `populate_test_data()`
Purpose: Inserts mock incident data into the database for testing visualizations.
How It Works:
Defines a list of mock incident records and a corresponding nature_list.
Uses the populatedb() function to populate the database with these records.
Input: None (runs automatically in tests needing pre-populated data).
Output: Prepares a database filled with sample incidents for visualization tests.
## 3. `generate_test_pdf(filepath)`
Purpose: Creates a sample PDF file for testing upload and processing functionality.
How It Works:
Uses the reportlab library to generate a PDF containing mock incident records.
Writes text simulating NormanPD-style incident data into the PDF.
Input:
filepath: The path where the test PDF will be saved.
Output: A sample PDF file containing mock incident data.
## 4. `test_home(client)`
Purpose: Tests if the homepage loads correctly.
How It Works:
Sends a GET request to the home route (/).
Verifies that the HTTP status code is 200 (OK).
Checks if the page content contains the title "Norman PD Incident Visualization."
Input: None (uses the client fixture).
Output: Confirms that the homepage is accessible and contains the correct content.
## 5. `test_upload_pdfs(client)`
Purpose: Tests the functionality of uploading PDF files.
How It Works:
Creates a test directory and generates a sample PDF using generate_test_pdf().
Simulates a POST request to the /upload route with the test PDF file.
Verifies the HTTP response is 200 and contains a success message ("file(s) uploaded and processed successfully!").
Cleans up the test directory after the test.
Input: A sample PDF file.
Output: Confirms that PDF uploads are handled correctly and processed successfully.
## 6. `test_process_urls(client)`
Purpose: Tests the functionality of processing PDFs from URLs.
How It Works:
Sends a POST request to the /process_url route with a test URL in JSON format.
Verifies the HTTP response status is 500 because the test URL does not point to a valid PDF.
Input: A mock URL (https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-01_daily_incident_summary.pdf).
Output: Confirms the system’s behavior when an invalid URL is provided.
## 7. `test_clustering_visualization(client, populate_test_data)`
Purpose: Tests the clustering visualization functionality.
How It Works:
Sends a GET request to the /visualize/clustering route.
Verifies the HTTP response status is 200.
Checks if the response contains the expected title, "Clustering of Incidents by Time."
Input: A pre-populated database with mock incident data.
Output: Confirms that the clustering visualization is generated successfully.
## 8. `test_bar_graph_visualization(client, populate_test_data)`
Purpose: Tests the bar graph visualization functionality.
How It Works:
Sends a GET request to the /visualize/bargraph route.
Verifies the HTTP response status is 200.
Checks if the response contains the title "Incident Nature Counts."
Input: A pre-populated database with mock incident data.
Output: Confirms that the bar graph visualization is generated successfully.
## 9. `test_custom_visualization(client, populate_test_data)`
Purpose: Tests the custom visualization functionality (e.g., time series trends).
How It Works:
Sends a GET request to the /visualize/custom route.
Verifies the HTTP response status is 200.
Checks if the response contains HTML elements like <table> and <img> that are typically part of the visualization.
Input: A pre-populated database with mock incident data.
Output: Confirms that the custom visualization is generated successfully.




## Visuilization 

## 1. `Clustering Visualization`
Purpose: Groups incidents by frequency and similarity using K-Means clustering and PCA for 2D visualization.
Insights: Shows patterns among incidents, such as frequent issues like "Noise Complaints" clustering together, while rare incidents like "Kidnapping" form separate groups.
Use: Helps identify groups of incidents that require similar resources or responses.

## 2. `Bar Graph Visualization`
Purpose: Compares the frequency of incident types with bars representing their occurrence.
Insights: Highlights the most common incidents (e.g., "Traffic Stops") and less frequent but critical ones (e.g., "Homicide").
Use: Useful for prioritizing resources based on incident frequency.

## 3. `Time Series (Custom) Visualization`
Purpose: Tracks trends in incident frequencies over time or across categories using a line graph.
Insights: Identifies patterns like spikes in "Public Intoxication" during weekends or seasonal changes in "Vandalism."
Use: Helps in planning resources by spotting trends and peak times.

# Bugs
1. PDF Parsing: Relies on consistent NormanPD-style structure; deviations can cause errors or incomplete data extraction.
2. Multi-line Handling: Edge cases in concatenated lines may result in incorrect parsing.
3. Insufficient Data: Sparse or minimal data can cause clustering or visualization to fail.
4. URL Issues: Invalid or inaccessible URLs may not be handled gracefully.

# Assumptions
1. Consistent PDFs: Assumes all PDFs follow NormanPD's structure.
2. Valid Inputs: Assumes users provide correctly formatted files and URLs.
3. Data Sufficiency: Assumes enough data is available for meaningful visualizations.
4. Database Integrity: Assumes the SQLite database remains intact during runtime.
5. Environment Setup: Assumes Python 3.9 and all dependencies are installed.
6. File Compatibility: Assumes PDFs are compatible with the pypdf library.


 
