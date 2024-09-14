import re

def format_newsletter(text):
    # Function to handle nested bold formatting
    def apply_bold_formatting(content):
        # Replace all instances of **text** with <strong>text</strong>
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)

    # Initialize formatted content
    formatted_content = ""

    # Split the input text into paragraphs or sections using newline indicators
    paragraphs = re.split(r'(\n|\n\n)', text)

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        # Handle title (## indicates title)
        if paragraph.startswith("##"):
            formatted_content += f"<h1>{paragraph[2:].strip()}</h1>\n"

        # Handle headers (**Header:** format)
        elif paragraph.startswith("**") and paragraph.endswith(":**"):
            formatted_content += f"<h3>{apply_bold_formatting(paragraph)}</h3>\n"

        # Handle bullet points that are bold but contain nested bold parts
        elif paragraph.startswith('* **"') and paragraph.endswith('"**'):
            # Remove the surrounding ** at the start and end of the sentence
            bullet_text = paragraph[4:-3]  # Remove * ** at the start and ** at the end
            # Apply bold formatting for nested bold parts
            formatted_content += f"<ul>\n<li>{apply_bold_formatting(bullet_text)}</li>\n</ul>\n"

        # Handle regular bullet points with bolded text inside
        elif paragraph.startswith("* **") and ":**" in paragraph:
            # Extract the bolded portion and the rest of the text after the colon
            bold_text, rest_of_text = paragraph.split(":**", 1)
            bold_text = bold_text.replace("* **", "").strip()
            rest_of_text = rest_of_text.strip()
            formatted_content += f"<ul>\n<li><strong>{bold_text}:</strong> {apply_bold_formatting(rest_of_text)}</li>\n</ul>\n"

        # Handle paragraphs with bolded words
        elif "**" in paragraph:
            formatted_content += f"<p>{apply_bold_formatting(paragraph)}</p>\n"

        # Treat everything else as a paragraph
        elif paragraph:
            formatted_content += f"<p>{paragraph}</p>\n"

    # Return the properly formatted content with HTML tags
    return formatted_content
