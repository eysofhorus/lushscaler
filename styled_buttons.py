# styled_buttons.py

from dominate.tags import *


def generate_styled_button_html(button_text, button_id, color_code):
    doc = dominate.document(title='Styled Button')

    with doc.head:
        style("""
            .styled-button {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                color: white;
            }
            .styled-button:hover {
                opacity: 0.9;
            }
        """)

    with doc.body:
        button(button_text, _id=button_id, _class='styled-button', onclick=f'buttonClicked("{button_id}")', style=f"background-color: {color_code}")

        script("""
            function buttonClicked(buttonId) {
                console.log("Button clicked: " + buttonId);
                // Add your functionality here, e.g., fetching random weight via Streamlit
                Streamlit.setComponentValue("buttonClicked", buttonId);
            }
        """)

    # Generate the HTML content
    html_content = doc.render()

    return html_content
