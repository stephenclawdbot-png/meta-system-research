#!/usr/bin/env python3
"""
Simple EPUB generator for Ashes of the Dawn
"""
import os
import zipfile

def create_epub():
    # Create basic EPUB structure
    epub_content = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">ashes-of-the-dawn</dc:identifier>
    <dc:title>Ashes of the Dawn</dc:title>
    <dc:creator>Stephen</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="content"/>
  </spine>
</package>"""
    
    # Create simple HTML content
    with open('/Users/clawdbot/.openclaw/workspace/ashes_of_the_dawn_ebook.md', 'r') as f:
        content = f.read()
    
    # Convert markdown to simple HTML
    html_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Ashes of the Dawn</title>
    <style>
        body {{ font-family: serif; line-height: 1.6; margin: 2em; }}
        h1 {{ border-bottom: 1px solid #ccc; }}
        h2 {{ margin-top: 2em; }}
    </style>
</head>
<body>
{content}
</body>
</html>"""
    
    # Create EPUB structure
    with zipfile.ZipFile('/Users/clawdbot/.openclaw/workspace/ashes_of_the_dawn.epub', 'w') as epub:
        # MIME type
        epub.writestr('mimetype', 'application/epub+zip')
        
        # Container
        epub.writestr('META-INF/container.xml', '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''')
        
        # Content
        epub.writestr('content.opf', epub_content)
        epub.writestr('content.xhtml', html_content)
        epub.writestr('toc.xhtml', '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
  <nav>
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="content.xhtml">Ashes of the Dawn</a></li>
    </ol>
  </nav>
</body>
</html>''')

if __name__ == "__main__":
    create_epub()
    print("EPUB created successfully!")