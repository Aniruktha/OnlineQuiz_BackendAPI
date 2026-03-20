"""
AI Quiz Generation Service using OpenRouter (Llama)

This module generates quiz questions using OpenRouter's free AI models.
Get your API key from: https://openrouter.ai/keys

For testing without API key, set USE_MOCK_AI=true in .env
"""
import os
import json
import random
from django.conf import settings


def generate_quiz_questions(topic: str, question_count: int = 5, difficulty: str = 'medium'):
    """
    Generate quiz questions using OpenRouter API or Mock.
    
    Args:
        topic: The topic for the quiz
        question_count: Number of questions to generate
        difficulty: easy, medium, or hard
    
    Returns:
        List of question dictionaries with options
    
    Raises:
        Exception: If API call fails
    """
    # Check if mock mode is enabled
    if os.getenv('USE_MOCK_AI', 'false').lower() == 'true':
        return _generate_mock_questions(topic, question_count, difficulty)
    
    api_key = os.getenv('API_KEY')
    
    if not api_key or api_key == '' or api_key == 'your-api-key-here':
        # Fallback to mock if no API key
        return _generate_mock_questions(topic, question_count, difficulty)
    
    # Prompt for the AI
    prompt = f"""Generate {question_count} multiple choice questions about {topic} with {difficulty} difficulty.

For each question, provide:
1. The question text
2. 4 options (a, b, c, d)
3. Mark the correct answer

Return ONLY valid JSON in this exact format:
[
  {{
    "question": "Question text here?",
    "options": [
      {{"text": "Option A", "is_correct": false}},
      {{"text": "Option B", "is_correct": true}},
      {{"text": "Option C", "is_correct": false}},
      {{"text": "Option D", "is_correct": false}}
    ]
  }}
]

Make sure exactly ONE option per question has "is_correct": true.
Return ONLY the JSON array, no other text."""

    try:
        import requests
        
        # Use OpenRouter API with free Llama model
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourapp.com",  # Required by OpenRouter
            "X-Title": "Quiz App"  # Optional, for tracking
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct",  # Free Llama model
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        # Extract text from OpenRouter response
        content = result['choices'][0]['message']['content']
        
        # Clean up the response (remove any markdown code blocks)
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        
        questions = json.loads(content.strip())
        
        # Validate and return
        return _validate_questions(questions, question_count)
        
    except ImportError:
        raise Exception("requests library not installed. Run: pip install requests")
    except Exception as e:
        if "API_KEY" in str(e) or "not configured" in str(e):
            raise
        raise Exception(f"AI generation failed: {str(e)}")


def _validate_questions(questions: list, expected_count: int) -> list:
    """
    Validate and fix the questions structure.
    """
    valid_questions = []
    
    for q in questions:
        # Ensure question has required fields
        if 'question' not in q or 'options' not in q:
            continue
            
        # Ensure exactly one correct answer
        correct_count = sum(1 for opt in q['options'] if opt.get('is_correct', False))
        if correct_count != 1:
            continue
            
        # Ensure 4 options
        if len(q['options']) != 4:
            continue
            
        valid_questions.append(q)
        
        if len(valid_questions) >= expected_count:
            break
    
    if not valid_questions:
        raise Exception("AI did not generate valid questions. Please try again.")
    
    return valid_questions


def _generate_mock_questions(topic: str, question_count: int = 5, difficulty: str = 'medium'):
    """
    Fallback mock function for testing without API key.
    Used when API quota is exceeded or no API key is provided.
    """
    
    templates = [
        {
            "question": f"What is the primary purpose of {topic}?",
            "options": [
                {"text": "To achieve specific goals", "is_correct": True},
                {"text": "To create confusion", "is_correct": False},
                {"text": "To complicate matters", "is_correct": False},
                {"text": "To avoid work", "is_correct": False},
            ]
        },
        {
            "question": f"Which of the following is NOT related to {topic}?",
            "options": [
                {"text": "Unrelated concept A", "is_correct": False},
                {"text": f"Core concept of {topic}", "is_correct": True},
                {"text": "Unrelated concept B", "is_correct": False},
                {"text": "Unrelated concept C", "is_correct": False},
            ]
        },
        {
            "question": f"What is a key advantage of {topic}?",
            "options": [
                {"text": "Efficiency improvement", "is_correct": True},
                {"text": "Increased bugs", "is_correct": False},
                {"text": "Slower performance", "is_correct": False},
                {"text": "Higher costs", "is_correct": False},
            ]
        },
        {
            "question": f"How does {topic} work?",
            "options": [
                {"text": "Through established mechanisms", "is_correct": True},
                {"text": "Randomly", "is_correct": False},
                {"text": "Without any logic", "is_correct": False},
                {"text": "Only on weekends", "is_correct": False},
            ]
        },
        {
            "question": f"What is a common challenge with {topic}?",
            "options": [
                {"text": "Initial complexity", "is_correct": True},
                {"text": "Being too simple", "is_correct": False},
                {"text": "Having no use cases", "is_correct": False},
                {"text": "No learning curve", "is_correct": False},
            ]
        },
    ]
    
    selected = random.sample(templates, min(question_count, len(templates)))
    
    for q in selected:
        random.shuffle(q['options'])
    
    return selected
