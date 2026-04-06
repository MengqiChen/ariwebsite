import os
import re

file_path = "arichen-portfolio-recreation/index.html"

with open(file_path, 'r') as f:
    content = f.read()

# 1. Update Work Section Overlay Alignment
# Current CSS:
# .project-overlay { ... padding: 2rem; color: white; }
# .project-overlay h3, .project-overlay p, .project-overlay .paragraph_small { color: white !important; }
# Needs explicit left alignment.

# I will update the CSS block.
# Look for `.project-overlay {`
if ".project-overlay {" in content:
    # Replace the block or add text-align
    # Let's replace the whole CSS style block to be safe and clean.
    
    old_css = """.project-overlay {
    position: relative;
    z-index: 1;
    background: rgba(0, 0, 0, 0.9);
    width: 100%;
    padding: 2rem;
    color: white;
  }"""
    
    new_css = """.project-overlay {
    position: relative;
    z-index: 1;
    background: rgba(0, 0, 0, 0.9);
    width: 100%;
    padding: 2rem;
    color: white;
    text-align: left; /* Explicit left alignment */
  }"""
    
    content = content.replace(old_css, new_css)

# 2. Update Timeline SVG
# Need arrows on the path.
# And specific segments: 1->2 (L->R), 2->3 (R->L), 3->4 (L->R).
# Grid:
# 1 (Salesforce) [Left]   2 (AAU) [Right]
# 3 (Rule 14) [Left]      4 (GT) [Right]
#
# Card centers approx:
# 1: 25, 25
# 2: 75, 25
# 3: 25, 75
# 4: 75, 75
#
# Path segments:
# 1->2: M 25 25 L 75 25
# 2->3: M 75 25 L 25 75 (Diagonal? Or Down then Left? "Snake" usually implies orthogonal or curvy)
# User sketch said "line between salesforce and AAU...". Snake usually means:
# [1] -> [2]
#         |
# [3] <- -'
# |
# '-> [4]
# But 3 is Bottom Left.
# So 2 (Top Right) to 3 (Bottom Left). That's a long diagonal across the screen.
# The user said "line between AAU and rULE14".
# Is Rule 14 on the left?
# Yes, card 3 is bottom left.
# So 2->3 is diagonal.
# And 3->4 is Left to Right (25,75 -> 75,75).
#
# Arrows pointing to later card:
# 1->2: Arrow at 2.
# 2->3: Arrow at 3.
# 3->4: Arrow at 4.
#
# I need markers.
# SVG defs for markers.
#
# Replace the whole <div class="timeline-svg-container"> block.

old_svg_block = """<div class="timeline-svg-container">
            <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
                <!-- Simple connecting path logic: Top Right -> Top Left -> Bottom Left -> Bottom Right -->
                <!-- Coordinates are approximate for visual line -->
                <path d="M 75 25 C 50 25 50 25 25 25 C 0 25 0 75 25 75 C 50 75 50 75 75 75" vector-effect="non-scaling-stroke" stroke="#007bff" stroke-width="2" fill="none" stroke-dasharray="5,5" />
            </svg>
        </div>"""

# Updated SVG with separate lines and markers
# Coordinates:
# 1 (SF): 25, 20 (Center of top row approx? Card height is implicit)
# Let's assume grid is 50% width each. Centers are 25% and 75%.
# Vertical centers: 25% and 75% of container.
#
# Line 1: (25, 25) -> (75, 25). Marker at end.
# Line 2: (75, 25) -> (25, 75). Marker at end.
# Line 3: (25, 75) -> (75, 75). Marker at end.
# 
# To avoid overlap with content, maybe curve it?
# Or just straight lines.
# Dashed blue lines.

new_svg_block = """<div class="timeline-svg-container">
            <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
                        markerWidth="6" markerHeight="6"
                        orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#007bff" />
                    </marker>
                </defs>
                
                <!-- Line 1: Salesforce (Top Left) -> AAU (Top Right) -->
                <path d="M 30 25 L 70 25" vector-effect="non-scaling-stroke" stroke="#007bff" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow)" />
                
                <!-- Line 2: AAU (Top Right) -> Rule 14 (Bottom Left) -->
                <!-- Diagonal -->
                <path d="M 70 30 L 30 70" vector-effect="non-scaling-stroke" stroke="#007bff" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow)" />
                
                <!-- Line 3: Rule 14 (Bottom Left) -> Georgia Tech (Bottom Right) -->
                <path d="M 30 75 L 70 75" vector-effect="non-scaling-stroke" stroke="#007bff" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow)" />
            </svg>
        </div>"""

content = content.replace(old_svg_block, new_svg_block)

# 3. Update Testimonial Layout
# "Testimonial shall be placed below the paragraph not next to it. make the quote text black"
# Current: grid_2-col.
# Need to change to grid_1-col for this container.
# And ensure quote text is black.

# Find the about container
about_container_start = content.find('<div class="about-intro-container w-layout-grid grid_2-col tablet-1-col gap-large">')
if about_container_start != -1:
    # Replace grid_2-col with grid_1-col
    content = content.replace(
        '<div class="about-intro-container w-layout-grid grid_2-col tablet-1-col gap-large">',
        '<div class="about-intro-container w-layout-grid grid_1-col gap-large">'
    )

# Update blockquote style for black text
if "blockquote {" in content:
    # Add color: black; to blockquote style
    # Or rely on inline/class?
    # I'll update the CSS block for blockquote
    
    old_quote_css = """blockquote {
      background: #f0f4f8;
      border-radius: 20px;
      border-bottom-left-radius: 4px;
      padding: 2rem;
      position: relative;
      margin-top: 2rem;
  }"""
    
    new_quote_css = """blockquote {
      background: #f0f4f8;
      border-radius: 20px;
      border-bottom-left-radius: 4px;
      padding: 2rem;
      position: relative;
      margin-top: 2rem;
      color: black; /* Explicit black text */
  }"""
    
    content = content.replace(old_quote_css, new_quote_css)

with open(file_path, 'w') as f:
    f.write(content)

print("Updated index.html")

