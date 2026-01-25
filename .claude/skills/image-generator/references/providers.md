# Adding New Image Generation Providers

This guide explains how to add support for new image generation APIs.

## Architecture

The skill uses a provider pattern for extensibility:

1. Each provider implements the `ImageProvider` base class
2. Providers are registered in the `get_provider()` function
3. API keys are loaded from the `.env` file

## Adding a New Provider

### Step 1: Create Provider Class

Add a new class in `scripts/generate_image.py`:

```python
class YourProviderName(ImageProvider):
    """Your provider description"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://api.yourprovider.com/'

    def generate(self, prompt: str, **kwargs) -> bytes:
        """Generate image and return bytes"""
        # Implement your API call here
        # Return image as bytes
        pass
```

### Step 2: Register Provider

Add to the `get_provider()` function:

```python
def get_provider(provider_name: str) -> ImageProvider:
    if provider_name == "modelscope":
        # existing code
    elif provider_name == "yourprovider":
        api_key = os.getenv("YOUR_PROVIDER_API_KEY")
        if not api_key:
            raise ValueError("YOUR_PROVIDER_API_KEY not found in .env")
        return YourProviderName(api_key)
```

### Step 3: Update .env.example

Add the new API key to `.env.example`:

```
YOUR_PROVIDER_API_KEY=your_key_here
```

### Step 4: Update SKILL.md

Add the provider to the "Supported Providers" section.

## Provider Implementation Guidelines

### Return Format
Always return image bytes that can be opened with PIL:

```python
return image_bytes  # bytes object
```

### Error Handling
Raise descriptive exceptions:

```python
if response.status_code != 200:
    raise Exception(f"API error: {response.text}")
```

### Async APIs
For async APIs, implement polling:

```python
while True:
    status = check_status(task_id)
    if status == "complete":
        return download_image(task_id)
    elif status == "failed":
        raise Exception("Generation failed")
    time.sleep(2)
```

### Optional Parameters
Accept provider-specific parameters via `**kwargs`:

```python
def generate(self, prompt: str, **kwargs) -> bytes:
    model = kwargs.get('model', 'default-model')
    size = kwargs.get('size', '1024x1024')
```

## Example: Adding Stability AI

```python
class StabilityAIProvider(ImageProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://api.stability.ai/'

    def generate(self, prompt: str, **kwargs) -> bytes:
        response = requests.post(
            f"{self.base_url}v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            }
        )
        response.raise_for_status()

        # Extract image from response
        image_data = response.json()["artifacts"][0]["base64"]
        import base64
        return base64.b64decode(image_data)
```

## Testing New Providers

Test your provider implementation:

```bash
python scripts/generate_image.py "test prompt" --provider yourprovider
```
