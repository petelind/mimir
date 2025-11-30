"""
Markdown rendering utilities for activity guidance.

Provides safe Markdown-to-HTML conversion with support for:
- Rich formatting (headers, lists, tables, etc.)
- Code blocks with syntax highlighting
- Mermaid.js diagrams
- Images
- Sanitized HTML output
"""

import markdown
from markdown.extensions import fenced_code, tables, nl2br, sane_lists
import bleach


# Allowed HTML tags and attributes for safe rendering
ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'strong', 'em', 'u', 'del', 'code', 'pre',
    'ul', 'ol', 'li',
    'blockquote',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],  # For syntax highlighting classes
    'pre': ['class'],
    'div': ['class'],  # For mermaid diagrams
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'data']


def render_markdown(text):
    """
    Convert Markdown text to safe HTML.
    
    Supports:
    - Standard Markdown formatting
    - Fenced code blocks with syntax highlighting classes
    - Tables
    - Mermaid diagrams (```mermaid code blocks)
    - Images
    
    :param text: Markdown text string
    :return: Safe HTML string
    
    Example:
        >>> html = render_markdown("## Steps\n1. Review\n2. Implement")
        >>> # Returns: "<h2>Steps</h2><ol><li>Review</li><li>Implement</li></ol>"
    """
    if not text:
        return ''
    
    # Configure markdown processor
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        'nl2br',
        'sane_lists',
    ])
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Process mermaid code blocks (add special class for JS rendering)
    html = _process_mermaid_blocks(html)
    
    # Sanitize HTML (remove dangerous tags/attributes)
    safe_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    
    return safe_html


def _process_mermaid_blocks(html):
    """
    Transform <pre><code class="language-mermaid"> blocks into Mermaid-compatible divs.
    
    Converts:
        <pre><code class="language-mermaid">graph TD...</code></pre>
    To:
        <div class="mermaid">graph TD...</div>
    
    :param html: HTML string
    :return: Processed HTML string
    """
    # Simple replacement for mermaid code blocks
    html = html.replace(
        '<code class="language-mermaid">',
        '</code></pre><div class="mermaid">'
    )
    html = html.replace(
        '<pre><code class="language-mermaid">',
        '<div class="mermaid">'
    )
    
    # Close any open mermaid divs properly
    if '<div class="mermaid">' in html:
        html = html.replace('</code></pre>', '</div>', 1)
    
    return html


def get_mermaid_script():
    """
    Return the Mermaid.js initialization script for templates.
    
    :return: HTML script tag string
    """
    return '''
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        });
    </script>
    '''
