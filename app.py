import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import random
import logging
import traceback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReadmeGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def generate_readme(self, project_title, sections):
        prompt = PromptTemplate(
            input_variables=["project_title", "sections"],
            template="""
            Create an exceptional, comprehensive, and human-like README.md file for a GitHub project with the following title:
            
            Project Title: {project_title}
            
            Include the following sections:
            {sections}
            
            Follow these guidelines to create an outstanding README:

            1. Start with an eye-catching project logo or banner (use a placeholder URL).
            2. Add badges for build status, version, license, etc., relevant to the project.
            3. Provide a concise but compelling project description that highlights its unique value proposition.
            4. For each section, provide detailed, accurate, and informative content tailored specifically to the project title.
            5. Use proper Markdown syntax, including headings, lists, code blocks, tables, and emphasis where appropriate.
            6. In the Features section, use emojis to make each feature stand out.
            7. For the Screenshots section, include placeholders for images with descriptive alt text.
            8. In the Installation section:
               - Carefully consider the frameworks and dependencies based on the project title.
               - Provide detailed, step-by-step instructions for different operating systems if relevant.
               - Include any necessary environment setup (e.g., virtual environments, database setup).
            9. For the Usage section, provide clear examples with code blocks and explanations.
            10. In the API Reference section (if applicable), use tables to display endpoints, methods, and parameters.
            11. For the Run Locally section:
                - Provide specific steps tailored to the project, not just general steps.
                - Include commands for cloning, installing dependencies, and running the project.
            12. In the Roadmap section, use a task list to show upcoming features or improvements.
            13. Add a 'Contributing' section with guidelines for potential contributors.
            14. Include a 'License' section with the appropriate license for the project.
            15. Add an 'Acknowledgements' section to credit libraries, tools, or contributors.
            16. Conclude with contact information or links to the project's community (e.g., Discord, Twitter).
            
            Ensure all content is creative yet professional, informative, and factually accurate, maintaining relevance to the project title. The README should be visually appealing, well-structured, and easy to navigate, resembling a high-quality, human-crafted document.
            """
        )

        # Combine sections into a single string with a newline separator
        sections_str = "\n".join(sections)
        
        # Generate the README content using the LLM chain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(project_title=project_title, sections=sections_str)
        
        return response


def set_page_config():
    st.set_page_config(page_title="AI README Generator By AiCraftAlchemy", page_icon="📝", layout="wide")
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .section-checkbox {
            font-size: 1.1em;
            margin-bottom: 0.5em;
        }
        .readme-preview {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 1em;
            background-color: #f9f9f9;
        }
        .footer {
            text-align: center;
            padding: 1rem;
            background-color: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border-top: 1px solid #3b82f6;
        }
        .footer a {
            color: #3b82f6;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .footer a:hover {
            color: #60a5fa;
        }
        .cool-title {
            font-size: 3em;
            color: #4a4a4a;
            text-align: center;
            margin-bottom: 1em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .feature-box {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .username-display {
            font-size: 1.2em;
            font-weight: bold;
            color: #4a4a4a;
            margin-bottom: 1em;
        }
        .username-input {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .error-message {
            background-color: #ffe6e6;
            color: #ff0000;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def generate_project_icon():
    icons = ["🚀", "💻", "🔧", "🎨", "📊", "🤖", "🌟", "🔬", "📱", "🎮"]
    return random.choice(icons)

def welcome_interface():
    st.markdown(f"<h1 class='cool-title'>{generate_project_icon()} AI README Generator By AiCraftAlchemy</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-box'>
    <h3>Welcome to the AI README Generator!</h3>
    <p>Our platform helps you create professional README files for your GitHub projects in minutes. Features include:</p>
    <ul>
        <li>AI-powered content generation</li>
        <li>Customizable sections</li>
        <li>Markdown formatting</li>
        <li>One-click download</li>
        <li>User-friendly interface</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        username = st.text_input("Enter your username to get started:", key="username_input")
    with col2:
        start_button = st.button("Get Started")
    
    if username and (start_button or st.session_state.get('enter_pressed', False)):
        logger.info(f"User logged in: {username}")
        st.session_state.username = username
        st.session_state.page = "generator"
        st.rerun()
    
    # Reset the enter_pressed state
    st.session_state.enter_pressed = False

def readme_generation_interface():
    # Create a clickable link for "AiCraftAlchemy"
    st.markdown(
        f"<h1 class='cool-title'>{generate_project_icon()} AI README Generator By <a href='https://www.linkedin.com/in/lokesh-e-60a583201' target='_blank'>AiCraftAlchemy</a></h1>",
        unsafe_allow_html=True
    )

    st.markdown(f"<p class='username-display'>Welcome, {st.session_state.username}!</p>", unsafe_allow_html=True)
    
    project_title = st.text_input("Enter your project title:", key="project_title")
    
    st.markdown("### Select README Sections")
    sections = [
        "Project Description", "Features", "Screenshots", "Installation", "Usage",
        "Run Locally", "Optimizations", "Deployment", "API Reference", "Contributing",
        "Authors", "Feedback", "Support", "License"
    ]
    
    selected_sections = []
    cols = st.columns(3)
    for i, section in enumerate(sections):
        with cols[i % 3]:
            if st.checkbox(section, key=f"section_{i}", value=True):
                selected_sections.append(section)
    
    if st.button("Generate README"):
        if project_title and selected_sections:
            try:
                with st.spinner("Generating your awesome README..."):
                    readme_content = st.session_state.readme_generator.generate_readme(project_title, selected_sections)
                
                st.success("README generated successfully!")
                
                st.markdown("## 📄 README Preview")
                st.markdown(readme_content, unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download README.md",
                    data=readme_content,
                    file_name="README.md",
                    mime="text/markdown",
                    key="download_button"
                )
                
                logger.info(f"README generated for project: {project_title} by user: {st.session_state.username}")
            except Exception as e:
                logger.error(f"Error generating README: {str(e)}")
                logger.error(traceback.format_exc())
                st.error("An error occurred. Please refresh the page and try again.")
        else:
            st.warning("Please enter a project title and select at least one section.")

def create_streamlit_app():
    try:
        set_page_config()
        
        if 'readme_generator' not in st.session_state:
            st.session_state.readme_generator = ReadmeGenerator()
        
        if 'page' not in st.session_state:
            st.session_state.page = "welcome"
        
        if st.session_state.page == "welcome":
            welcome_interface()
        elif st.session_state.page == "generator":
            readme_generation_interface()
        
        st.markdown("""
        <div class="footer">
            <p>Powered by <a href="https://www.linkedin.com/in/lokesh-e-60a583201" target="_blank">AI Craft Alchemy</a> | Contact: <a href="tel:+917661081043">+91 7661081043</a></p>
        </div>
        """, unsafe_allow_html=True)

        # Handle Enter key press
        if 'username_input' in st.session_state and st.session_state.username_input:
            st.session_state.enter_pressed = True

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    create_streamlit_app()
