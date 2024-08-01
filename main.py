from flask import Flask, render_template, request, jsonify, url_for
import markdown
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form.get('title')
    description = request.form.get('description')
    installation = request.form.get('installation')
    usage = request.form.get('usage')
    contributing = request.form.get('contributing')
    license = request.form.get('license')
    additional_sections = request.form.getlist('additional_section')
    additional_contents = request.form.getlist('additional_content')

    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('uploaded_file', filename=filename)

    readme_content = f"""# {title}

## Description
{description}

"""
    if image_url:
        readme_content += f"![Image]({image_url})\n\n"

    readme_content += f"""## Installation
{installation}

## Usage
{usage}

## Contributing
{contributing}

## License
{license}
"""

    for section, content in zip(additional_sections, additional_contents):
        if section and content:
            readme_content += f"""## {section}
{content}

"""

    # Convert Markdown to HTML
    readme_html = markdown.markdown(readme_content)

    return render_template('result.html', readme_html=readme_html, readme_content=readme_content)

@app.route('/add-field', methods=['GET'])
def add_field():
    return render_template('field.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'../uploads/{filename}'))

if __name__ == '__main__':
    app.run(debug=True)
