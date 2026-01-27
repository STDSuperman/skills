---
name: image-generator
description: AI image generation with support for multiple providers and artistic styles. Use when users request image generation, creation, or visualization tasks such as "generate an image of...", "create a picture showing...", "make an illustration of...", or when they specify artistic styles like anime, realistic, cartoon, oil painting, etc.
---

# Image Generator

Generate AI images using various providers and artistic styles.

## Quick Start

Generate an image with a simple prompt:

```bash
python scripts/generate_image.py "A golden cat sitting on a cloud"
```

Generate with a specific style:

```bash
python scripts/generate_image.py "A golden cat" --style anime
```

## Configuration

1. Copy `.env.example` to `.env` in the skill directory
2. Add your API keys:
   ```
   MODELSCOPE_TOKEN=your_token_here
   JIEKOU_API_KEY=your_jiekou_key_here
   JIEKOU_ENABLE=true
   ```

## Supported Providers

Currently supported:
- **ModelScope** (default): Tongyi-MAI/Z-Image-Turbo model
- **Jiekou.ai** (即梦 4.5): seedream-4.5 model

For adding new providers, see [references/providers.md](references/providers.md).

## Style Templates

The skill includes built-in style templates to enhance prompts. Available styles:

- `realistic` - Photorealistic images
- `anime` - Japanese animation style
- `cartoon` - Western cartoon style
- `oil-painting` - Classical oil painting
- `watercolor` - Watercolor painting
- `sketch` - Pencil sketch
- `3d-render` - 3D rendered style
- `cyberpunk` - Cyberpunk aesthetic
- `fantasy` - Fantasy art style

For complete style descriptions and customization, see [references/styles.md](references/styles.md).

## Script Usage

```bash
python scripts/generate_image.py <prompt> [options]

Options:
  --style STYLE         Apply a style template (see references/styles.md)
  --provider PROVIDER   Choose provider (default: modelscope)
  --output PATH         Output file path (default: generated_image.png)
  --model MODEL         Specific model ID (provider-dependent)
```

## Workflow

1. Load API credentials from `.env`
2. Apply style template if specified
3. Call the selected provider's API
4. Poll for completion (async providers)
5. Save the generated image

## Examples

Generate a realistic portrait:
```bash
python scripts/generate_image.py "A woman with blue eyes" --style realistic
```

Generate anime-style artwork:
```bash
python scripts/generate_image.py "A magical girl" --style anime --output magical_girl.png
```
