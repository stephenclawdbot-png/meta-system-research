#!/usr/bin/env python3
"""
Simple EPUB creation for Ashes of the Dawn Arc 1
"""

import zipfile
import os
from datetime import datetime

# Create basic EPUB structure
def create_epub():
    epub_name = "ashes_of_the_dawn_arc1.epub"
    
    with zipfile.ZipFile(epub_name, 'w') as epub:
        # Create mimetype file (must be first, uncompressed)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # Create container.xml
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        epub.writestr('META-INF/container.xml', container_xml)
        
        # Create content.opf (package file)
        content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Ashes of the Dawn - Arc 1: Ashfall</dc:title>
    <dc:creator>Your Name</dc:creator>
    <dc:language>en</dc:language>
    <dc:identifier id="bookid">ashes-of-the-dawn-arc1</dc:identifier>
    <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
  </metadata>
  <manifest>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="toc"/>
    <itemref idref="content"/>
  </spine>
</package>'''
        epub.writestr('OEBPS/content.opf', content_opf)
        
        # Create table of contents
        toc_xhtml = '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body>
  <nav epub:type="toc">
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="content.xhtml#title">Ashes of the Dawn - Arc 1: Ashfall</a></li>
      <li><a href="content.xhtml#ch1">Chapter 1: Threadwake</a></li>
      <li><a href="content.xhtml#ch2">Chapter 2: The Locked Box</a></li>
      <li><a href="content.xhtml#ch3">Chapter 3: The Ember Road</a></li>
      <li><a href="content.xhtml#ch4">Chapter 4: The Unbecoming</a></li>
      <li><a href="content.xhtml#ch5">Chapter 5: The High Caves</a></li>
      <li><a href="content.xhtml#ch6">Chapter 6: The Weight of Chains</a></li>
      <li><a href="content.xhtml#ch7">Chapter 7: Dawn Departure</a></li>
      <li><a href="content.xhtml#ch8">Chapter 8: The War-Camp</a></li>
      <li><a href="content.xhtml#ch9">Chapter 9: The Testing Ground</a></li>
      <li><a href="content.xhtml#ch10">Chapter 10: The Keth Council</a></li>
      <li><a href="content.xhtml#ch11">Chapter 11: The Bombardment Begins</a></li>
      <li><a href="content.xhtml#ch12">Chapter 12: Darro's Decision</a></li>
      <li><a href="content.xhtml#ch13">Chapter 13: The Half-Step Appears</a></li>
      <li><a href="content.xhtml#ch14">Chapter 14: The Long March</a></li>
      <li><a href="content.xhtml#ch15">Chapter 15: Mountain Sanctuary</a></li>
      <li><a href="content.xhtml#ch16">Chapter 16: Imperial Pursuit</a></li>
      <li><a href="content.xhtml#ch17">Chapter 17: The Urath Ways</a></li>
      <li><a href="content.xhtml#ch18">Chapter 18: The Second Half-Step</a></li>
      <li><a href="content.xhtml#ch19">Chapter 19: The Trap</a></li>
      <li><a href="content.xhtml#ch20">Chapter 20: The Price of Survival</a></li>
      <li><a href="content.xhtml#ch21">Chapter 21: The Decision</a></li>
      <li><a href="content.xhtml#ch22">Chapter 22: The Split</a></li>
      <li><a href="content.xhtml#ch23">Chapter 23: The Hidden Path</a></li>
      <li><a href="content.xhtml#ch24">Chapter 24: The River Crossing</a></li>
      <li><a href="content.xhtml#ch25">Chapter 25: Solla Hospitality</a></li>
      <li><a href="content.xhtml#ch26">Chapter 26: The Third Half-Step</a></li>
      <li><a href="content.xhtml#ch27">Chapter 27: The Flight</a></li>
      <li><a href="content.xhtml#ch28">Chapter 28: The Wilderness</a></li>
      <li><a href="content.xhtml#ch29">Chapter 29: The Discovery</a></li>
      <li><a href="content.xhtml#ch30">Chapter 30: The Reunion</a></li>
      <li><a href="content.xhtml#ch31">Chapter 31: The Fourth Half-Step</a></li>
      <li><a href="content.xhtml#ch32">Chapter 32: The Stand</a></li>
      <li><a href="content.xhtml#ch33">Chapter 33: The Price of Victory</a></li>
      <li><a href="content.xhtml#ch34">Chapter 34: The Choice</a></li>
      <li><a href="content.xhtml#ch35">Chapter 35: The Parting</a></li>
      <li><a href="content.xhtml#ch36">Chapter 36: Darro's Confession</a></li>
      <li><a href="content.xhtml#ch37">Chapter 37: The Fifth Half-Step</a></li>
      <li><a href="content.xhtml#ch38">Chapter 38: The Inheritance</a></li>
      <li><a href="content.xhtml#ch39">Chapter 39: The New Dawn</a></li>
      <li><a href="content.xhtml#ch40">Chapter 40: Ashfall</a></li>
    </ol>
  </nav>
</body>
</html>'''
        epub.writestr('OEBPS/toc.xhtml', toc_xhtml)
        
        # Create main content file
        # First, let's read the existing chapters
        content_parts = []
        
        # Title page
        content_parts.append('''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Ashes of the Dawn</title></head>
<body>
  <div id="title">
    <h1>ASHES OF THE DAWN</h1>
    <h2>Arc 1: Ashfall</h2>
    <p>An Epic Fantasy Novel</p>
  </div>''')
        
        # Add Chapters 1-10 (full content)
        for i in range(1, 11):
            try:
                with open(f'/Users/clawdbot/.openclaw/workspace/arc1_chapter{i}.md', 'r') as f:
                    chapter_content = f.read()
                    # Convert markdown to simple HTML
                    html_content = chapter_content.replace('# ASHES OF THE DAWN\n## ', '<h1 id="ch' + str(i) + '">')
                    html_content = html_content.replace('**[End Chapter', '</h1><p><em>End Chapter')
                    html_content = html_content.replace(']**', '</em></p>')
                    html_content = html_content.replace('**Chapter Cliffhanger:**', '<strong>Chapter Cliffhanger:</strong>')
                    html_content = html_content.replace('\n\n', '</p><p>')
                    content_parts.append(f'<div id="ch{i}">{html_content}</div>')
            except FileNotFoundError:
                content_parts.append(f'<div id="ch{i}"><h1>Chapter {i}: Placeholder</h1><p>Content not available</p></div>')
        
        # Add Chapter summaries for 11-40
        try:
            with open('/Users/clawdbot/.openclaw/workspace/ashes_of_the_dawn_arc1.md', 'r') as f:
                all_content = f.read()
                # Extract chapter summaries
                import re
                chapters = re.findall(r'### Chapter (\d+): ([^#]+)(.*?)(?=### Chapter|\Z)', all_content, re.DOTALL)
                
                for chap_num, title, content in chapters:
                    if int(chap_num) > 10:
                        clean_content = content.strip().replace('[Full Chapter content', '').replace(']', '')
                        content_parts.append(f'<div id="ch{chap_num}"><h1>Chapter {chap_num}: {title.strip()}</h1><p>{clean_content}</p></div>')
        except FileNotFoundError:
            # Fallback: create placeholder chapters
            for i in range(11, 41):
                content_parts.append(f'<div id="ch{i}"><h1>Chapter {i}: Summary</h1><p>Detailed chapter content to be completed.</p></div>')
        
        content_parts.append('</body></html>')
        
        epub.writestr('OEBPS/content.xhtml', '\n'.join(content_parts))
    
    return epub_name

if __name__ == "__main__":
    epub_file = create_epub()
    print(f"Created {epub_file}")