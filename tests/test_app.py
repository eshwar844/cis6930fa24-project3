import pytest
import main
from main import app, createdb, populatedb
import os
from reportlab.pdfgen import canvas


@pytest.fixture
def client():
    # Set up the test client and database
    createdb()  # Recreate the database before tests
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.config['STATIC_FOLDER'] = 'test_static'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

    with app.test_client() as client:
        yield client

    # Clean up after tests
    for folder in [app.config['UPLOAD_FOLDER'], app.config['STATIC_FOLDER']]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        os.rmdir(folder)


@pytest.fixture
def populate_test_data():
    # Add mock data to the database
    nature_list = ['Welfare Check', 'Traffic Stop', 'Suspicious']
    mock_incidents = [
        "01/01/2024 12:00 1234567 Some Location Welfare Check ORI123",
        "01/02/2024 13:00 1234568 Another Location Traffic Stop ORI124",
        "01/03/2024 14:00 1234569 Some Other Location Suspicious ORI125",
    ]
    populatedb('normanpd.db', mock_incidents, nature_list)


def generate_test_pdf(filepath):
    c = canvas.Canvas(filepath)
    c.drawString(100, 750, "Norman Daily Incident Summary")
    c.drawString(100, 730, "01/01/2024 123456 Example Location Example Nature NORM123")
    c.drawString(100, 710, "01/02/2024 654321 Another Location Another Nature NORM654")
    c.save()

# Example Usage
test_dir = "test_files"
os.makedirs(test_dir, exist_ok=True)
test_pdf_path = os.path.join(test_dir, "test_incident.pdf")
generate_test_pdf(test_pdf_path)


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Norman PD Incident Visualization' in response.data


def test_upload_pdfs(client):
    # Create the test_files directory and a valid PDF file
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    test_pdf_path = os.path.join(test_dir, "test_incident.pdf")
    generate_test_pdf(test_pdf_path)

    # Upload the PDF
    data = {'files': (open(test_pdf_path, 'rb'), 'test_incident.pdf')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b"file(s) uploaded and processed successfully!" in response.data

    # Clean up
    os.remove(test_pdf_path)
    os.rmdir(test_dir)


def test_process_urls(client):
    test_url = "http://example.com/test_incident.pdf"
    response = client.post('/process_url', json={"urls": [test_url]})
    assert response.status_code == 500  # This will fail because the URL doesn't point to a valid PDF


def test_bar_graph_visualization(client, populate_test_data):
    response = client.get('/visualize/bargraph')
    assert response.status_code == 200
    assert b"Incident Nature Counts" in response.data


def test_custom_visualization(client, populate_test_data):
    response = client.get('/visualize/custom')
    assert response.status_code == 200

    # Update the check to match Plotly content instead of <table>
    assert b"PlotlyConfig" in response.data
    assert b"plotly.js" in response.data

