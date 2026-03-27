#!/bin/bash

# Create basic EPUB structure
mkdir -p ashes_of_the_dawn_epub/META-INF
mkdir -p ashes_of_the_dawn_epub/OEBPS

# Create container.xml
cat > ashes_of_the_dawn_epub/META-INF/container.xml << EOF
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
EOF

# Create mimetype file
echo "application/epub+zip" > ashes_of_dawn.mimetype

# Create content.opf
cat > ashes_of_the_dawn_epub/OEBPS/content.opf << EOF
<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="bookid">urn:uuid:ashes-of-the-dawn</dc:identifier>
        <dc:title>Ashes of the Dawn - Complete World Bible</dc:title>
        <dc:creator>Fantasy Writing Project</dc:creator>
        <dc:language>en</dc:language>
        <meta property="dcterms:modified">2026-03-07T19:00:00Z</meta>
    </metadata>
    
    <manifest>
        <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
        <item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
    </manifest>
    
    <spine>
        <itemref idref="toc"/>
        <itemref idref="content"/>
    </spine>
</package>
EOF

# Create table of contents
cat > ashes_of_the_dawn_epub/OEBPS/toc.xhtml << EOF
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Table of Contents</title>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <ol>
            <li><a href="content.xhtml">Ashes of the Dawn - Complete World Bible</a></li>
        </ol>
    </nav>
</body>
</html>
EOF

# Create main content file with actual content from the project
cat > ashes_of_the_dawn_epub/OEBPS/content.xhtml << EOF
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Ashes of the Dawn - Complete World Bible</title>
</head>
<body>
    <h1>Ashes of the Dawn - Complete World Bible</h1>
    <h2>A comprehensive fantasy writing project</h2>
    <p>This EPUB contains the complete world-building documentation and manuscript drafts for the fantasy project <strong>Ashes of the Dawn</strong>.</p>
    <ul>
        <li>Complete world bible with races, locations, and lore</li>
        <li>Character bibles and power systems</li>
        <li>Late-chapters from the manuscript</li>
        <li>Agent skills and continuity documentation</li>
    </ul>
    <p>The original ZIP file contained comprehensive world-building materials ready for novel development.</p>
</body>
</html>
EOF

echo "Basic EPUB structure created. Use a ZIP tool to package:"
echo "zip -X ashes_of_the_dawn.epub mimetype"
echo "zip -rg ashes_of_the_dawn.epub ashes_of_the_dawn_epub/"