#!/usr/bin/env python3
"""
AI Image Generation Script with Multi-Provider Support

Supports multiple image generation providers with extensible architecture.
"""

import os
import sys
import argparse
import json
import time
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


class ImageProvider:
    """Base class for image generation providers"""

    def generate(self, prompt: str, **kwargs) -> bytes:
        """Generate image and return bytes"""
        raise NotImplementedError


class ModelScopeProvider(ImageProvider):
    """ModelScope image generation provider"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.modelscope.cn/"

    def generate(
        self, prompt: str, model: str = "Tongyi-MAI/Z-Image-Turbo", **kwargs
    ) -> bytes:
        """Generate image using ModelScope API"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "prompt": prompt,
        }

        if "width" in kwargs and "height" in kwargs:
            payload["size"] = f"{kwargs['width']}x{kwargs['height']}"

        if "loras" in kwargs:
            payload["loras"] = kwargs["loras"]

        # Submit generation request with async mode
        response = requests.post(
            f"{self.base_url}v1/images/generations",
            headers={**headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        )
        response.raise_for_status()
        result = response.json()

        # Get task_id from async response
        task_id = result.get("task_id")
        if not task_id:
            raise Exception(f"No task_id in response: {result}")

        # Poll for completion
        print(f"Task submitted: {task_id}")
        print("Waiting for image generation...")

        # Wait a bit before first poll
        time.sleep(3)

        while True:
            status_response = requests.get(
                f"{self.base_url}v1/tasks/{task_id}",
                headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            status_response.raise_for_status()
            result = status_response.json()

            task_status = result.get("task_status", "")

            if task_status == "SUCCEED":
                image_url = result["output_images"][0]
                print(f"Generation complete! Downloading image...")

                # Download the image
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                return img_response.content

            elif task_status == "FAILED":
                raise Exception(
                    f"Generation failed: {result.get('message', 'Unknown error')}"
                )

            time.sleep(5)  # Poll every 5 seconds


# Style templates for different artistic styles
STYLE_TEMPLATES = {
    "realistic": "{prompt}, photorealistic, highly detailed, 8k uhd, professional photography",
    "anime": "{prompt}, anime style, manga art, vibrant colors, detailed illustration",
    "cartoon": "{prompt}, cartoon style, colorful, playful, western animation",
    "oil-painting": "{prompt}, oil painting, classical art, brushstrokes, artistic",
    "watercolor": "{prompt}, watercolor painting, soft colors, artistic, flowing",
    "sketch": "{prompt}, pencil sketch, hand-drawn, artistic, detailed linework",
    "3d-render": "{prompt}, 3d render, octane render, highly detailed, professional",
    "cyberpunk": "{prompt}, cyberpunk style, neon lights, futuristic, sci-fi",
    "fantasy": "{prompt}, fantasy art, magical, ethereal, detailed illustration",
}


def load_env_config():
    """Load configuration from .env file"""
    # Get the skill directory (parent of scripts directory)
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"

    if not env_path.exists():
        print(f"Warning: .env file not found at {env_path}")
        print("Please copy .env.example to .env and add your API keys")
        sys.exit(1)

    load_dotenv(env_path)


def apply_style(prompt: str, style: str) -> str:
    """Apply style template to prompt"""
    if style and style in STYLE_TEMPLATES:
        return STYLE_TEMPLATES[style].format(prompt=prompt)
    return prompt


def get_provider(provider_name: str) -> ImageProvider:
    """Get provider instance based on name"""
    if provider_name == "modelscope":
        api_key = os.getenv("MODELSCOPE_TOKEN")
        if not api_key:
            raise ValueError("MODELSCOPE_TOKEN not found in .env file")
        return ModelScopeProvider(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI images with multiple providers"
    )
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument(
        "--style", help="Apply a style template", choices=list(STYLE_TEMPLATES.keys())
    )
    parser.add_argument(
        "--provider", default="modelscope", help="Image generation provider"
    )
    parser.add_argument(
        "--output", default="generated_image.png", help="Output file path"
    )
    parser.add_argument("--model", help="Specific model ID (provider-dependent)")
    parser.add_argument("--width", type=int, help="Image width")
    parser.add_argument("--height", type=int, help="Image height")

    args = parser.parse_args()

    # Load environment configuration
    load_env_config()

    # Apply style template if specified
    final_prompt = apply_style(args.prompt, args.style)
    print(f"Prompt: {final_prompt}")

    # Get provider and generate image
    provider = get_provider(args.provider)

    kwargs = {}
    if args.model:
        kwargs["model"] = args.model
    elif os.getenv("MODELSCOPE_MODEL"):
        kwargs["model"] = os.getenv("MODELSCOPE_MODEL")
    if args.width:
        kwargs["width"] = args.width
    if args.height:
        kwargs["height"] = args.height

    image_bytes = provider.generate(final_prompt, **kwargs)

    # Save the image
    image = Image.open(BytesIO(image_bytes))
    image.save(args.output)
    print(f"Image saved to: {args.output}")


if __name__ == "__main__":
    main()
