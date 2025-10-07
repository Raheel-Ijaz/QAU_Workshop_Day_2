import streamlit as st
import random
import re

def extract_key_phrases(text, max_phrases=10):
    """Extract key phrases from text based on sentence structure"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Extract noun phrases (simplified - words that might be important)
    words = text.lower().split()
    # Filter out common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                   'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                   'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                   'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    
    key_words = [w for w in words if len(w) > 4 and w not in common_words]
    
    return sentences, list(set(key_words))[:max_phrases]

def generate_assignments(text, sentences, key_words):
    """Generate 2 assignment questions based on the text"""
    assignments = []
    
    if len(sentences) >= 2:
        # Assignment 1: Analysis question
        topic = key_words[0] if key_words else "the main topic"
        assignments.append(
            f"Write an essay analyzing the key concepts related to {topic} "
            f"discussed in the text. Support your analysis with specific examples."
        )
        
        # Assignment 2: Application question
        if len(key_words) >= 2:
            assignments.append(
                f"Compare and contrast {key_words[0]} and {key_words[1]}. "
                f"How do these concepts relate to each other in the context provided?"
            )
        else:
            assignments.append(
                f"Discuss the implications and real-world applications of the concepts "
                f"presented in the text. Provide at least three examples."
            )
    else:
        assignments.append("Summarize the main ideas presented in the text and explain their significance.")
        assignments.append("Critically evaluate the information provided and discuss potential limitations or areas for further exploration.")
    
    return assignments

def generate_quiz_questions(text, sentences, key_words):
    """Generate 3 multiple-choice quiz questions"""
    quiz_questions = []
    
    if len(sentences) >= 3:
        # Question 1: Based on a specific sentence
        sentence = random.choice(sentences[:min(3, len(sentences))])
        words_in_sentence = sentence.split()
        
        if len(words_in_sentence) > 5:
            # Create a fill-in-the-blank style question
            important_word = random.choice([w for w in words_in_sentence if len(w) > 4][:3] if [w for w in words_in_sentence if len(w) > 4] else words_in_sentence)
            question_text = sentence.replace(important_word, "______", 1)
            
            # Generate wrong answers
            other_words = [w for w in key_words if w != important_word.lower()][:3]
            options = [important_word] + other_words
            random.shuffle(options)
            
            quiz_questions.append({
                'question': f"Complete the following statement: {question_text}",
                'options': options[:4],
                'answer': important_word
            })
        
        # Question 2: Main idea question
        if key_words:
            correct = key_words[0]
            wrong_options = ['irrelevant concept', 'unrelated topic', 'minor detail']
            options = [correct] + wrong_options
            random.shuffle(options)
            
            quiz_questions.append({
                'question': f"Which of the following is a key concept discussed in the text?",
                'options': options,
                'answer': correct
            })
        
        # Question 3: Comprehension question
        if len(sentences) >= 2:
            quiz_questions.append({
                'question': "Based on the text, which statement is most accurate?",
                'options': [
                    f"The text primarily discusses {key_words[0] if key_words else 'the topic'}",
                    "The text focuses on unrelated topics",
                    "The text provides no clear information",
                    "The text contradicts itself throughout"
                ],
                'answer': f"The text primarily discusses {key_words[0] if key_words else 'the topic'}"
            })
    
    # Ensure we have 3 questions (add generic ones if needed)
    while len(quiz_questions) < 3:
        quiz_questions.append({
            'question': f"What is the main subject matter of the provided text?",
            'options': [
                f"{key_words[0] if key_words else 'The specified topic'}",
                "Unrelated subjects",
                "No clear subject",
                "Multiple unconnected topics"
            ],
            'answer': f"{key_words[0] if key_words else 'The specified topic'}"
        })
    
    return quiz_questions[:3]

# Streamlit App
st.set_page_config(page_title="Assignment & Quiz Generator", page_icon="📝", layout="wide")

st.title("📝 Assignment & Quiz Generator")
st.markdown("Generate assignments and quiz questions from any text or topic!")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This tool analyzes your input text and generates:\n"
        "- 2 Assignment Questions\n"
        "- 3 Multiple Choice Quiz Questions"
    )
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Enter or paste your text/document")
    st.markdown("2. Click 'Generate'")
    st.markdown("3. Review your questions!")

# Main content
input_text = st.text_area(
    "Enter your document or topic text:",
    height=200,
    placeholder="Paste your text here... (e.g., a paragraph about photosynthesis, history, or any topic)"
)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    generate_btn = st.button("🚀 Generate Questions", type="primary")
with col2:
    if st.button("🗑️ Clear"):
        st.rerun()

if generate_btn:
    if input_text.strip():
        with st.spinner("Generating questions..."):
            # Extract information
            sentences, key_words = extract_key_phrases(input_text)
            
            if not sentences or not key_words:
                st.error("⚠️ Please provide more detailed text (at least a few sentences).")
            else:
                # Generate assignments
                assignments = generate_assignments(input_text, sentences, key_words)
                
                # Generate quiz questions
                quiz_questions = generate_quiz_questions(input_text, sentences, key_words)
                
                # Display results
                st.success("✅ Questions generated successfully!")
                
                st.markdown("---")
                
                # Assignments Section
                st.header("📋 Assignment Questions")
                for i, assignment in enumerate(assignments, 1):
                    st.subheader(f"Assignment {i}")
                    st.write(assignment)
                    st.markdown("")
                
                st.markdown("---")
                
                # Quiz Section
                st.header("❓ Quiz Questions")
                for i, q in enumerate(quiz_questions, 1):
                    st.subheader(f"Question {i}")
                    st.write(q['question'])
                    
                    # Display options
                    for j, option in enumerate(q['options'], 1):
                        st.write(f"{chr(64+j)}. {option}")
                    
                    # Show answer in expander
                    with st.expander("Show Answer"):
                        st.success(f"✓ Correct Answer: {q['answer']}")
                    
                    st.markdown("")
    else:
        st.warning("⚠️ Please enter some text to generate questions.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Made with ❤️ using Streamlit | Simple NLP-based Question Generation"
    "</div>",
    unsafe_allow_html=True
)