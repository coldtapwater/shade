import re

class ConversationManager:
    def __init__(self, max_tokens=128000):
        self.max_tokens = max_tokens  # Set the max context window size
        self.conversation_history = []  # Stores the conversation history as a list of messages
        self.current_tokens = 0  # Tracks the current number of tokens used

    def count_tokens(self, text):
        """Approximate token count based on word count for simplicity (each token is roughly 4 characters on average)."""
        return len(text.split())

    def add_message(self, role, message):
        """Adds a message to the conversation history and manages token usage."""
        tokens = self.count_tokens(message)
        if self.current_tokens + tokens > self.max_tokens:
            self.summarize_history()
        self.conversation_history.append({'role': role, 'message': message})
        self.current_tokens += tokens

    def summarize_history(self):
        """Summarizes older conversation to reduce token usage when exceeding the limit."""
        print(f"Summarizing conversation as it exceeded {self.max_tokens} tokens.")
        # Simple summarization technique: Remove older messages or replace with summary
        if len(self.conversation_history) > 2:
            summary = self.summarize_conversation(self.conversation_history[:-2])
            self.conversation_history = [{'role': 'system', 'message': summary}] + self.conversation_history[-2:]
            self.current_tokens = self.count_tokens(summary) + sum(self.count_tokens(m['message']) for m in self.conversation_history[-2:])
    
    def summarize_conversation(self, messages):
        """Generates a simple summary for older conversation."""
        conversation_text = ' '.join([m['message'] for m in messages])
        summary = f"Conversation Summary: {self.generate_summary(conversation_text)}"
        return summary

    def generate_summary(self, text):
        """Generates a basic summary for text. In practice, you'd use an AI model for this."""
        # This is a placeholder for AI summarization. You can integrate this with an actual summarization model if needed.
        summary = text[:1000]  # Simply truncate for now (placeholder)
        return summary

    def get_context(self):
        """Returns the current conversation context (for use by the AI agents)."""
        return '\n'.join([f"{m['role']}: {m['message']}" for m in self.conversation_history])


    def clear(self):
        """Clears the conversation history."""
        self.conversation_history = []
        self.current_tokens = 0