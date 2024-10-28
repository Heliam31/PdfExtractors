"""
Parsing of the PDF File as an image using LLM
"""

from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
from PIL import Image
import requests

device = torch.device("cuda")
model = AutoModelForImageTextToText.from_pretrained(
    "HuggingFaceM4/idefics2-8b",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
).to(device)
processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics2-8b")

image = Image.open("page_0.png")

messages = {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Fetch the text and describe the images in this image"},
        ]
    }

prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[images[0], images[1]], return_tensors="pt").to(device)

with torch.no_grad():
    generated_ids = model.generate(**inputs, max_new_tokens=500)
generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)

print(generated_texts)