#!/usr/bin/env python3

import os
import markdown
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Define the EPUB metadata
def create_epub():
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('ashes_of_the_dawn')
    book.set_title('Ashes of the Dawn - Complete World Bible')
    book.set_language('en')
    book.add_author('Fantasy Writing Project')
    
    # Read all markdown files
    chapters = []
    
    # Main world bible
    with open('drafts/ashes_world_bible_complete.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content)
    
    # Create chapter
    chapter1 = epub.EpubHtml(title='World Bible', file_name='world_bible.xhtml', lang='en')
    chapter1.content = f'<h1>Ashes of the Dawn - Complete World Bible</h1>{html_content}'
    
    book.add_item(chapter1)
    
    # Add late chapters
    with open('drafts/late-chapters.md', 'r', encoding='utf-8') as f:
        late_content = f.read()
    
    html_late = markdown.markdown(late_content)
    chapter2 = epub.EpubHtml(title='Late Chapters', file_name='late_chapters.xhtml', lang='en')
    chapter2.content = f'<h1>Late Chapters</h1>{html_late}'
    
    book.add_item(chapter2)
    
    # Add character bibles
    character_files = [
        'bibles/ashes_character_bible_v3.md',
        'bibles/ashes_complete_character_bible.md'
    ]
    
    for i, char_file in enumerate(character_files):
        if os.path.exists(char_file):
            with open(char_file, 'r', encoding='utf-8') as f:
                char_content = f.read()
            html_char = markdown.markdown(char_content)
            chapter_char = epub.EpubHtml(title=f'Character Bible {i+1}', file_name=f'character_{i+1}.xhtml', lang='en')
            chapter_char.content = f'<h1>Character Bible</h1>{html_char}'
            book.add_item(chapter_char)
    
    # Create table of contents
    book.toc = [
        epub.Link('world_bible.xhtml', 'World Bible', 'world_bible'),
        epub.Link('late_chapters.xhtml', 'Late Chapters', 'late_chapters'),
    ]
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav'] + [chapter1, chapter2]
    
    # Write the EPUB file
    epub.write_epub('ashes_of_the_dawn.epub', book, {})
    print("EPUB created successfully!")

if __name__ == "__main__":
    create_epub()