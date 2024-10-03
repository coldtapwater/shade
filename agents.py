import random
import re
import os
from tools import generate_response
from memory import ConversationManager

conversation = ConversationManager(max_tokens=128000)

class PlanningAgent:
    def plan(self, user_input, context):
        # Generate a plan using the [THINKING] tag
        plan_prompt = f"""Given the following context, create a detailed plan to achieve the following task: {context}


You are a planning assistant. Break down the user's request into detailed steps and decide how to approach it.

User's request: "{user_input}"

Do not to ask questions unless absolutely necessary. Instead, use the [THINKING] tag to outline your plan step by step. The CheckingAgent will clear up any concerns you may have. To ensure proper planning use the following format:

'''
[THINKING] Step 1:
+ Step 1 description and what to do/what the output may look like

[THINKING] Step 2:
+ Step 2 description and what to do/what the output may look like

...
'''

Overall ensure that you forcing the final output only be a plan with no comments, thoughts, or questions. If for whatever reason you need to ask a question, assume the user does not need to answer it. If you think the answer/question is essential to the task, assume the CheckingAgent will handle everything for you. YOU DO NOT NEED TO ASK QUESTIONS.


Use the [THINKING] tag to outline your plan step by step.

[THINKING]
"""
        print(context)
        plan_response = generate_response(plan_prompt)
        conversation.add_message("user", user_input)
        # Extract the [THINKING] section
        thinking_match = re.search(r'\[THINKING\](.*)', plan_response, re.DOTALL)
        if thinking_match:
            plan = thinking_match.group(1).strip()
            return f"[THINKING]\n{plan}"
            
        else:
            # If the model didn't include the tag, assume the whole response is the plan
            return f"[THINKING]\n{plan_response.strip()}"

class CheckingAgent:
    def check_plan(self, plan, user_input, context):
        # Refine the plan using the [SHADING] tag
        check_prompt = f"""
You are a reviewing assistant. Review and refine the plan below to better align with the user's intent. Do not include the plan in your response; instead, provide any necessary adjustments or comments. Answer any questions the plan may have asked.

User's request: "{user_input}"

Known context:
{context}

Plan to review:
{plan}

By reviewing the plan, here is what that means:
+ thinking critically about the request by the user; "{user_input}"
    * Does the plan adequately align with the user's intent?
        - If the plan does not address a way to respond to this issue then refine or recreate the plan to fix this issue.
        - If the plan DOES adequately align with the user's intent then there would be no need to refine that specific part of the plan.
    * Does the plan meet the user's needs?
        - What if the plan does not meet the user's needs?
            + If the plan does not address a way to respond to this issue then refine or recreate the plan to fix this issue.
        - If the plan DOES meet the user's needs then there would be no need to refine that specific part of the plan.
    * Does the plan meet the user's expectations?
        - What if the plan does not meet the user's expectations?
            + If the plan does not address a way to respond to this issue then refine or recreate the plan to fix this issue.
        - If the plan DOES meet the user's expectation then there would be no need to refine that specific part of the plan.
+ Adjust the plan if needed and iterate over each step provided by the plan.
+ If the plan contains questions, assume the user does not need to answer them or answer the question for the user. 
+ Only include the shaded (refined) plan in your response to streamline the final response. 
+ do not include your input unless it is to answer a question.
+ Ensure to include all necessary details and address the user's request fully.
+ Ensure to include the [SHADING] tag in your response.

If the plan included questions assume the role of the user to answer those questions to the best of your ability.
Use the [SHADING] tag to provide your refined plan and comments.

[SHADING]
"""
        print(context)
        check_response = generate_response(check_prompt)
        # Extract the [SHADING] section
        shading_match = re.search(r'\[SHADING\](.*)', check_response, re.DOTALL)
        if shading_match:
            refined_plan = shading_match.group(1).strip()
            return f"[SHADING]\n{refined_plan}"
        else:
            # If the model didn't include the tag, assume the whole response is the refined plan
            return f"[SHADING]\n{check_response.strip()}"

class CraftingAgent:
    def craft_response(self, shaded_plan, user_input, context):
        # Generate the final response without including the plan
        craft_prompt = f"""Known context: {context}


Based on the refined plan (do not include the plan in your response), generate a comprehensive response to the user's request.

User's request: 
{user_input}

Refined plan (do not include the plan in your response):
{shaded_plan}

Ensure to include all necessary details and address the user's request fully.

Use the "[OUTPUT]" tag to provide the final response. Again do not include the plan in your response. Simply include the final response.

For more complex outputs or prompts just include your final output as if you were responding to the user directly. Simply use the shaded plan as context.

[OUTPUT]
"""
        # Debugging: Print the prompt
        # print(f"\nDebug: Crafting Agent Prompt:\n{craft_prompt}")
        print(context)
        response = generate_response(craft_prompt)

        # Debugging: Print the raw response
        # print(f"\nDebug: Crafting Agent Raw Response:\n{response}")

        if response:
            # Extract the [OUTPUT] section
            output_match = re.search(r'\[OUTPUT\](.*)', response, re.DOTALL)
            if output_match:
                final_response = output_match.group(1).strip()
                conversation.add_message("assistant", response)
                return f"[OUTPUT]\n{final_response}"
            else:
                # If the model didn't include the tag, assume the whole response is the final output
                conversation.add_message("assistant", response)
                return f"[OUTPUT]\n{response}"
                
        else:
            response_content = f"[OUTPUT] I'm sorry, I couldn't generate a response."
            return response_content

class ConfidenceAgent:
    def evaluate_response(self, response, user_input):
        # Evaluate the response (you can implement a real evaluation here)
        confidence = random.uniform(0.95, 1.0)
        print(f"\n{confidence:.2f} confidence in the response.")
        return confidence

class SystemAgent:
    def decide_action(self, user_input, response):
        # Decide if any system-level action is needed
        if "write a story" in user_input.lower() or "write" in user_input.lower():
            text_editors = ["TextEdit", "Pages", "Microsoft Word", "Notes"]
            installed_editors = [app for app in text_editors if os.path.exists(f"/Applications/{app}.app")]
            if installed_editors:
                return {'action': 'open_app', 'target': installed_editors[0]}
            else:
                return None
        elif "create a file" in user_input.lower():
            file_match = re.search(r'create a file named (\S+)', user_input, re.IGNORECASE)
            if file_match:
                file_name = file_match.group(1)
                return {'action': 'create_file', 'target': file_name}
            else:
                return {'action': 'create_file', 'target': 'output.txt'}
        else:
            return None