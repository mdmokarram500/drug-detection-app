from flask import Flask, render_template, request
import csv
import os
import re

app = Flask(__name__)

def read_csv(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

def search_drug_in_chats(drug_name, chat_files):
    results = []
    for file in chat_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if drug_name.lower() in line.lower():
                        results.append({'chat_file': file, 'line': line.strip()})
        except FileNotFoundError:
            results.append({'chat_file': file, 'line': 'File not found'})
    return results

def highlight_drugs(text, drug_names):
    highlighted_text = text
    found_drugs = set()
    for drug in drug_names:
        if drug.lower() in text.lower():
            found_drugs.add(drug)
        highlighted_text = re.sub(f'({re.escape(drug)})', r'<mark>\1</mark>', highlighted_text, flags=re.IGNORECASE)
    return highlighted_text, list(found_drugs)

@app.route('/')
def home():
    # Load drug data from CSV
    drug_data = read_csv('datasets/drugsComTest_raw.csv')

    # Paginate data (10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = 15
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = drug_data[start:end]

    # Calculate total pages
    total_pages = (len(drug_data) + per_page - 1) // per_page

    # Filter drugs with rating 10
    drugs_with_high_rating = [drug for drug in drug_data if drug['rating'] == '10']
    
    # Paginate high rating drugs
    paginated_high_rating_data = drugs_with_high_rating[start:end]

    return render_template('index.html', drugs=paginated_high_rating_data, page=page, total_pages=total_pages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/drugdetection')
def drugdetection():
    return render_template('drugdetection.html')

@app.route('/search', methods=['POST'])
def search():
    drug_name = request.form.get('drugName')
    if drug_name:
        # Load drug data from CSV
        drug_data = read_csv('datasets/drugsComTest_raw.csv')
        
        # Extract drug names from the data
        drug_names = [drug['drugName'] for drug in drug_data]

        # Check if drug name exists in drug data
        drug_found = any(drug_name.lower() == drug.lower() for drug in drug_names)
        
        if drug_found:
            chat_files = [
                'data/whatsapp_chat.txt',
                'data/instagram_chat.txt',
                'data/telegram_chat.txt'
            ]
            results = search_drug_in_chats(drug_name, chat_files)
            # Highlight drugs in search results
            highlighted_results = [{'chat_file': item['chat_file'], 'line': highlight_drugs(item['line'], drug_names)[0]} for item in results]
            if highlighted_results:
                return render_template('drugdetection.html', result=highlighted_results)
            else:
                return render_template('drugdetection.html', error="No matching drug found in chats.")
        else:
            return render_template('drugdetection.html', error="Drug not found in drug data.")
    return render_template('drugdetection.html', error="No drug name provided.")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        chat_text = request.form['chatText']
        # Load drug data from CSV
        drug_data = read_csv('datasets/drugsComTest_raw.csv')
        drug_names = [drug['drugName'] for drug in drug_data]
        highlighted_text, found_drugs = highlight_drugs(chat_text, drug_names)
        return render_template('chat.html', highlighted_text=highlighted_text, drug_names_found=found_drugs)
    return render_template('chat.html', highlighted_text=None, drug_names_found=None)

if __name__ == '__main__':
    app.run(debug=True)
