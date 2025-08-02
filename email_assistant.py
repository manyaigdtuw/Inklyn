from ai_engine import AIEngine

class EmailAssistant:
    def __init__(self):
        self.ai_engine = AIEngine()
    
    def write_email(self, context, requirements):
        """Help write an email with document context"""
        prompt = f"""
Please help me write a professional email based on the following:

Requirements: {requirements}

Document Context: {context}

Please provide:
1. Subject line
2. Professional email body
3. Appropriate greeting and closing

Make it clear, professional, and well-structured.
"""
        return self.ai_engine._call_openrouter_api([
            {"role": "system", "content": "You are a professional email writing assistant."},
            {"role": "user", "content": prompt}
        ])
    
    def reply_to_email(self, original_email, context, instructions=""):
        """Help reply to an email"""
        prompt = f"""
Please help me write a professional reply to this email:

Original Email:
{original_email}

Context from my documents: {context}

Additional instructions: {instructions}

Please write an appropriate professional reply.
"""
        return self.ai_engine._call_openrouter_api([
            {"role": "system", "content": "You are a professional email reply assistant."},
            {"role": "user", "content": prompt}
        ])
