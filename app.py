from flask import Flask, render_template_string, request
from main import multiturn_generate_content  # Import from main.py
from format import format_newsletter  # Import the format_newsletter function

app = Flask(__name__)

# Flask route to display the generated newsletter
@app.route('/', methods=['GET', 'POST'])
def generate_newsletter():
    if request.method == 'POST':
        topic = request.form['topic']  # Get the topic from the form
        newsletter = multiturn_generate_content(topic)  # Generate the newsletter
        formatted_newsletter = format_newsletter(newsletter)  # Format the newsletter
        return render_template_string(''' 
        <h1>Generated Newsletter</h1>
        <div>{{ newsletter | safe }}</div>  <!-- Use safe to render HTML -->
        <a href="/">Go Back</a>
        ''', newsletter=formatted_newsletter)
    
    # Return a form for the user to input a topic
    return '''
    <form method="POST">
        <label for="topic">Enter a topic for the newsletter:</label><br>
        <input type="text" id="topic" name="topic"><br><br>
        <input type="submit" value="Generate Newsletter">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
