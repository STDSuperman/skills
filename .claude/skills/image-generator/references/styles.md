# Style Templates Reference

This document describes the built-in style templates and how to customize them.

## Available Styles

### realistic
**Description**: Photorealistic images with high detail
**Template**: `{prompt}, photorealistic, highly detailed, 8k uhd, professional photography`
**Best for**: Portraits, landscapes, product photography

### anime
**Description**: Japanese animation style
**Template**: `{prompt}, anime style, manga art, vibrant colors, detailed illustration`
**Best for**: Characters, scenes, fantasy subjects

### cartoon
**Description**: Western cartoon style
**Template**: `{prompt}, cartoon style, colorful, playful, western animation`
**Best for**: Fun, playful subjects, children's content

### oil-painting
**Description**: Classical oil painting style
**Template**: `{prompt}, oil painting, classical art, brushstrokes, artistic`
**Best for**: Portraits, landscapes, classical subjects

### watercolor
**Description**: Soft watercolor painting
**Template**: `{prompt}, watercolor painting, soft colors, artistic, flowing`
**Best for**: Gentle subjects, nature, artistic interpretations

### sketch
**Description**: Pencil sketch style
**Template**: `{prompt}, pencil sketch, hand-drawn, artistic, detailed linework`
**Best for**: Concept art, studies, artistic renderings

### 3d-render
**Description**: 3D rendered style
**Template**: `{prompt}, 3d render, octane render, highly detailed, professional`
**Best for**: Product visualization, architectural renders

### cyberpunk
**Description**: Cyberpunk aesthetic
**Template**: `{prompt}, cyberpunk style, neon lights, futuristic, sci-fi`
**Best for**: Futuristic scenes, technology, urban environments

### fantasy
**Description**: Fantasy art style
**Template**: `{prompt}, fantasy art, magical, ethereal, detailed illustration`
**Best for**: Fantasy characters, magical scenes, mythical subjects

## Customizing Styles

To add or modify styles, edit the `STYLE_TEMPLATES` dictionary in `scripts/generate_image.py`:

```python
STYLE_TEMPLATES = {
    "your-style": "{prompt}, your custom style modifiers here",
}
```

## Tips for Better Results

1. **Be specific**: More detailed prompts produce better results
2. **Combine styles**: You can manually combine style elements in your prompt
3. **Iterate**: Try different styles to find what works best
4. **Quality keywords**: Add terms like "high quality", "detailed", "professional"
