from flask import Flask, request, render_template, jsonify
import os
import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px
from werkzeug.utils import secure_filename
from datetime import datetime
import urllib.request
from pypdf import PdfReader
import matplotlib

matplotlib.use('Agg')

# Flask Configuration
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATABASE = 'normanpd.db'
STATIC_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


# Utility Functions (unchanged from original)
def validate_date(date_string, date_format="%m/%d/%Y"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def fetchincidents(url):
    headers = {'User-Agent': "Mozilla/5.0"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)

    # Validate the content type
    content_type = response.headers.get('Content-Type')
    if not content_type or 'pdf' not in content_type:
        raise ValueError(f"URL does not point to a valid PDF file. Content-Type: {content_type}")

    file_data = response.read()

    temp_pdf = os.path.join(UPLOAD_FOLDER, "incident_report.pdf")
    with open(temp_pdf, "wb") as pdf_file:
        pdf_file.write(file_data)
    return temp_pdf


def extractincidents(pdf_file):
    reader = PdfReader(pdf_file)
    incidents = []
    for page in reader.pages:
        text = page.extract_text()

        previous = ""
        for line in text.splitlines():
            l = line.split(" ")
            if l[0] not in ["", "Norman", "Daily", "Date"]:
                if not validate_date(l[0]):
                    line = previous + line
                    incidents.pop()
                incidents.append(line)
                previous = line
    return incidents


def createdb():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    conn.commit()
    conn.close()


def populatedb(db, incidents, nature_list):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    incident_tuples = []
    for incident in incidents:
        try:
            inc = incident.split(" ")
            date = inc[0] + " " + inc[1]
            incident_number = inc[2]
            incident_ori = inc[-1]
            location = ""
            nature = ""

            incident = incident.replace(date, "").replace(incident_number, "").replace(incident_ori, "")

            for nat in nature_list:
                if nat in incident:
                    nature = nat
                    location = incident.replace(nat, "")
                    break

            incident_tuples.append((date, incident_number, location, nature, incident_ori))
        except Exception:
            pass

    cursor.executemany('''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
        VALUES (?, ?, ?, ?, ?)
    ''', incident_tuples)
    conn.commit()
    conn.close()


def fetch_incidents():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()
    return df


# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdfs():
    files = request.files.getlist('files')  # Get all uploaded files
    if not files:
        return jsonify({"error": "No files provided"}), 400

    nature_list =['911 Call Nature Unknown', 'Welfare Check', 'Warrant Service', 'Vandalism'
              , 'VPO Violation', 'Unknown Problem/Man Down', 'Unconscious/Fainting', 'Trespassing'
              , 'Traumatic Injury', 'Transfer/Interfacility', 'Traffic Stop', 'Tobacco Violation'
              , 'Test Call', 'Suspicious', 'Supplement Report', 'Stroke', 'Stolen Vehicle', 'Stand By EMS'
              , 'Stake Out', 'Special Assignment', 'Sick Person', 'Shots Heard', 'Shooting Stabbing Penetrating'
              , 'Shooting', 'Runaway or Lost Child', 'Robbery', 'Road Rage', 'Reckless Driving', 'Public Intoxication'
              , 'Public Assist', 'Prowler', 'Preg/Child Birth/Miscarriage', 'Pick Up Partner', 'Pick Up Items'
              , 'Parking Problem', 'Overdose/Poisoning', 'Open Door/Premises Check', 'Officer in Danger', 'Officer Needed Nature Unk'
              , 'Noise Complaint', 'Nature','Fire Mutual Aid','EMS Mutual Aid', 'Mutual Aid', 'Motorist Assist', 'Molesting', 'Missing Person'
              , 'Medical Call Pd Requested', 'MVA With Injuries', 'MVA Non Injury', 'Loud Party', 'Larceny', 'Kidnapping'
              , 'Item Assignment', 'Indecent Exposure', 'Homicide', 'Hit and Run', 'Hemorrhage/Lacerations', 'Heat/Cold Exposure'
              , 'Heart Problems/AICD', 'Headache', 'Harassment / Threats Report', 'Fraud', 'Found Item', 'Forgery', 'Foot Patrol'
              , 'Follow Up', 'Fireworks', 'Fire Water Rescue', 'Fire Vehicle', 'Fire Transformer Blown', 'Fire Smoke Investigation'
              , 'Fire Residential', 'Fire Odor Investigation', 'Fire Grass', 'Fire Gas Leak', 'Fire Fuel Spill'
              , 'Fire Electrical Check', 'Fire Dumpster', 'Fire Down Power Line', 'Fire Controlled Burn', 'Fire Commercial'
              , 'Fire Carbon Monoxide Alarm', 'Fire Alarm', 'Fight', 'Falls', 'Eye Problems/Injuries', 'Extra Patrol', 'Escort/Transport'
              , 'Drunk Driver', 'Drug Violation', 'Drowning/Diving/Scuba Accident', 'Disturbance/Domestic', 'Diabetic Problems'
              , 'Debris in Roadway', 'Convulsion/Seizure', 'Contact a Subject', 'Civil Standby', 'Choking', 'Chest Pain', 'Check Area'
              , 'Cardiac Respritory Arrest', 'Carbon Mon/Inhalation/HazMat','HazMat','COP Relationships', 'COP Problem Solving', 'COP DDACTS'
              , 'Burns/Explosions', 'Burglary', 'Breathing Problems', 'Bomb/Threats/Package', 'Body Reported', 'Bike Patrol'
              , 'Barking Dog', 'Bar Check', 'Back Pain', 'Assist Police', 'Assist Fire', 'Assist EMS', 'Assault EMS Needed', 'Assault'
              , 'Animal at Large', 'Animal Vicious', 'Animal Trapped', 'Animal Livestock', 'Animal Injured', 'Animal Dead'
              , 'Animal Complaint', 'Animal Bites/Attacks', 'Animal Bite', 'Allergies/Envenomations', 'Alcohol Violation'
              , 'Alarm Holdup/Panic', 'Alarm', 'Abdominal Pains/Problems']

    incidents = []
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        incidents.extend(extractincidents(filepath))  # Combine incidents from all files

    createdb()
    populatedb(DATABASE, incidents, nature_list)

    return jsonify({"message": f"{len(files)} file(s) uploaded and processed successfully!"})

@app.route('/process_url', methods=['POST'])
def process_urls():
    urls = []

    # Check if JSON input is provided
    if request.is_json:
        urls = request.json.get('urls', [])
    elif request.form.get('urls'):  # Fallback to form data
        # Split URLs by comma or newline
        urls = [url.strip() for url in request.form.get('urls').split(',') if url.strip()]

    # If no URLs provided, return an error
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    nature_list =['911 Call Nature Unknown', 'Welfare Check', 'Warrant Service', 'Vandalism'
              , 'VPO Violation', 'Unknown Problem/Man Down', 'Unconscious/Fainting', 'Trespassing'
              , 'Traumatic Injury', 'Transfer/Interfacility', 'Traffic Stop', 'Tobacco Violation'
              , 'Test Call', 'Suspicious', 'Supplement Report', 'Stroke', 'Stolen Vehicle', 'Stand By EMS'
              , 'Stake Out', 'Special Assignment', 'Sick Person', 'Shots Heard', 'Shooting Stabbing Penetrating'
              , 'Shooting', 'Runaway or Lost Child', 'Robbery', 'Road Rage', 'Reckless Driving', 'Public Intoxication'
              , 'Public Assist', 'Prowler', 'Preg/Child Birth/Miscarriage', 'Pick Up Partner', 'Pick Up Items'
              , 'Parking Problem', 'Overdose/Poisoning', 'Open Door/Premises Check', 'Officer in Danger', 'Officer Needed Nature Unk'
              , 'Noise Complaint', 'Nature','Fire Mutual Aid','EMS Mutual Aid', 'Mutual Aid', 'Motorist Assist', 'Molesting', 'Missing Person'
              , 'Medical Call Pd Requested', 'MVA With Injuries', 'MVA Non Injury', 'Loud Party', 'Larceny', 'Kidnapping'
              , 'Item Assignment', 'Indecent Exposure', 'Homicide', 'Hit and Run', 'Hemorrhage/Lacerations', 'Heat/Cold Exposure'
              , 'Heart Problems/AICD', 'Headache', 'Harassment / Threats Report', 'Fraud', 'Found Item', 'Forgery', 'Foot Patrol'
              , 'Follow Up', 'Fireworks', 'Fire Water Rescue', 'Fire Vehicle', 'Fire Transformer Blown', 'Fire Smoke Investigation'
              , 'Fire Residential', 'Fire Odor Investigation', 'Fire Grass', 'Fire Gas Leak', 'Fire Fuel Spill'
              , 'Fire Electrical Check', 'Fire Dumpster', 'Fire Down Power Line', 'Fire Controlled Burn', 'Fire Commercial'
              , 'Fire Carbon Monoxide Alarm', 'Fire Alarm', 'Fight', 'Falls', 'Eye Problems/Injuries', 'Extra Patrol', 'Escort/Transport'
              , 'Drunk Driver', 'Drug Violation', 'Drowning/Diving/Scuba Accident', 'Disturbance/Domestic', 'Diabetic Problems'
              , 'Debris in Roadway', 'Convulsion/Seizure', 'Contact a Subject', 'Civil Standby', 'Choking', 'Chest Pain', 'Check Area'
              , 'Cardiac Respritory Arrest', 'Carbon Mon/Inhalation/HazMat','HazMat','COP Relationships', 'COP Problem Solving', 'COP DDACTS'
              , 'Burns/Explosions', 'Burglary', 'Breathing Problems', 'Bomb/Threats/Package', 'Body Reported', 'Bike Patrol'
              , 'Barking Dog', 'Bar Check', 'Back Pain', 'Assist Police', 'Assist Fire', 'Assist EMS', 'Assault EMS Needed', 'Assault'
              , 'Animal at Large', 'Animal Vicious', 'Animal Trapped', 'Animal Livestock', 'Animal Injured', 'Animal Dead'
              , 'Animal Complaint', 'Animal Bites/Attacks', 'Animal Bite', 'Allergies/Envenomations', 'Alcohol Violation'
              , 'Alarm Holdup/Panic', 'Alarm', 'Abdominal Pains/Problems']


    incidents = []
    for url in urls:
        try:
            pdf_file = fetchincidents(url)
            incidents.extend(extractincidents(pdf_file))  # Combine incidents from all URLs
        except Exception as e:
            return jsonify({"error": f"Failed to process URL {url}: {str(e)}"}), 500

    createdb()
    populatedb(DATABASE, incidents, nature_list)

    return jsonify({"message": f"{len(urls)} URL(s) processed successfully!"})

@app.route('/visualize/<viz_type>')
def visualize(viz_type):
    df = fetch_incidents()

    if viz_type == 'clustering':
        return clustering_visualization(df)
    elif viz_type == 'bargraph':
        return bar_graph_visualization(df)
    elif viz_type == 'custom':
        return custom_visualization(df)
    else:
        return jsonify({"error": "Invalid visualization type"}), 400
    

def clustering_visualization(df):
    # Ensure 'nature' column exists and is not empty
    if df.empty or 'nature' not in df.columns:
        return "<p>No valid data available for clustering.</p>"

    # Handle missing or invalid nature data
    df = df.dropna(subset=['nature'])
    if df.empty:
        return "<p>No valid data available for clustering.</p>"

    # Compute frequency of each nature
    nature_counts = df['nature'].value_counts().reset_index()
    nature_counts.columns = ['nature', 'frequency']

    # K-Means Clustering
    scaler = StandardScaler()
    nature_counts_scaled = scaler.fit_transform(nature_counts[['frequency']])
    
    # Check if there are enough samples for clustering
    if len(nature_counts_scaled) < 2:  # Need at least 2 samples for meaningful clustering
        return "<p>Not enough data points for clustering visualization.</p>"

    kmeans = KMeans(n_clusters=4, random_state=42)
    nature_counts['cluster'] = kmeans.fit_predict(nature_counts_scaled)

    # PCA for Visualization
    n_components = min(2, len(nature_counts_scaled), nature_counts_scaled.shape[1])
    try:
        pca = PCA(n_components=n_components, random_state=42)
        reduced_data = pca.fit_transform(nature_counts_scaled)
        nature_counts['pca_x'] = reduced_data[:, 0]
        nature_counts['pca_y'] = reduced_data[:, 1] if n_components == 2 else 0  # Handle 1D case
    except ValueError as e:
        return f"<p>Error during PCA: {str(e)}</p>"

    # Plot
    fig = px.scatter(
        nature_counts,
        x='pca_x',
        y='pca_y' if n_components == 2 else None,
        color='cluster',
        size='frequency',
        text='nature',
        title='Clustering of Incident Natures by Frequency',
        labels={'pca_x': 'PCA Component 1', 'pca_y': 'PCA Component 2', 'cluster': 'Cluster'}
    )
    fig.update_traces(marker=dict(size=10), hovertemplate="Nature: %{text}<br>Cluster: %{marker.color}<br>Frequency: %{marker.size}")

    return fig.to_html(full_html=False)



def bar_graph_visualization(df):
    counts = df['nature'].value_counts().reset_index()
    counts.columns = ['nature', 'count']

    fig = px.bar(counts, x='nature', y='count', title='Incident Nature Counts')
    return fig.to_html(full_html=False)

def custom_visualization(df):
    # Ensure 'nature' column exists and is not empty
    if df.empty or 'nature' not in df.columns:
        return "<p>No data available for line graph visualization.</p>"

    # Count the occurrences of each nature
    counts = df['nature'].value_counts().reset_index()
    counts.columns = ['nature', 'count']

    # Create a line graph
    fig = px.line(
        counts,
        x='nature',
        y='count',
        title='Incident Nature Counts',
        markers=True,  # Adds markers to each point on the line
        labels={'nature': 'Nature of Incident', 'count': 'Count'}
    )
    fig.update_layout(
        plot_bgcolor="#f9f9f9",
        xaxis_title="Nature",
        yaxis_title="Frequency"
    )
    fig.update_xaxes(tickangle=45)  # Rotate x-axis labels for readability

    return fig.to_html(full_html=False)




if __name__ == '__main__':
    createdb()
    app.run(debug=True)

