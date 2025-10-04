"""
Vercel Serverless Function for AI chat
"""
import os
import json
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

dashscope_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def handler(request):
    """Main handler for Vercel serverless function"""
    if request.method == "POST":
        try:
            # Parse request body
            body = request.get_json()
            if not body:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Invalid request body"})
                }
            
            message = body.get("message", "")
            conversation_history = body.get("conversation_history", [])
            
            # Generate AI response
            ai_response = generate_ai_response(message, conversation_history)
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({
                    "success": True,
                    "response": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
            }
            
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"AI对话时发生错误: {str(e)}"})
            }
    
    elif request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    else:
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"})
        }

def generate_ai_response(message: str, conversation_history: list) -> str:
    """Generate AI response using OpenAI API"""
    # Build conversation messages
    messages = [
        {"role": "system", "content": "你是一个专业的医疗AI助手，可以回答医疗相关问题，提供医学建议，但请注意提醒用户这些建议仅供参考，不能替代专业医生的诊断。"}
    ]
    
    # Add conversation history
    for msg in conversation_history:
        messages.append(msg)
    
    # Add current user message
    messages.append({"role": "user", "content": message})
    
    try:
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"AI对话失败：{str(e)}"

# Vercel entry point
def main(request):
    return handler(request)