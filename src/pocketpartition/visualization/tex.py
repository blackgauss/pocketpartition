from .tikz import generate_latex_table, generate_ferrers_tikz, generate_hasse_tikz
def generate_content_pages(label, subsections, data, partition, gap_poset, void_poset):
    latex_code = f"\\section{{MinGens: {label}}}\n"

    # Top row: Invariants table and Partition diagram
    latex_code += "\\noindent\\begin{minipage}{0.6\\textwidth}\n"
    latex_code += "\\subsection*{Invariants}\n"
    latex_code += "\\centering\n"
    latex_code += generate_latex_table(data)
    latex_code += "\\end{minipage}%\n"
    latex_code += "\\begin{minipage}{0.4\\textwidth}\n"
    latex_code += "\\subsection*{Partition}\n"
    latex_code += "\\centering\n"
    latex_code += generate_ferrers_tikz(partition, display_hooks=False, box_size=0.4)
    latex_code += "\\end{minipage}\n"

    latex_code += "\\vspace{1cm}\n"  # Add some vertical space
    latex_code += "\\noindent \\newline"  # Ensure the next line starts at the left margin

    # Bottom row: Gap Poset and Void Poset in two columns
    latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
    latex_code += "\\subsection*{Gap Poset}\n"
    latex_code += "\\centering\n"
    elements, relations = gap_poset
    latex_code += generate_hasse_tikz(elements, relations, node_size=0.3, vertical_spacing=0.8, horizontal_spacing=0.8)
    latex_code += "\\end{minipage}%\n"
    latex_code += "\\hfill"  # Add horizontal space between posets
    latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
    latex_code += "\\subsection*{Void Poset}\n"
    latex_code += "\\centering\n"
    elements, relations = void_poset
    latex_code += generate_hasse_tikz(elements, relations, node_size=0.3, vertical_spacing=0.8, horizontal_spacing=0.8)
    latex_code += "\\end{minipage}\n"

    return latex_code

def wrap_with_section(content:str, section_title:str):
    latex_code = f"\\section{section_title}\n"
    latex_code += content
    return latex_code

def wrap_with_headers_footers(content):
    latex_code = "\\documentclass[a4paper]{article}\n"
    latex_code += "\\usepackage[margin=0.5in]{geometry}\n"
    latex_code += "\\usepackage{booktabs}\n"
    latex_code += "\\usepackage{tikz}\n"
    latex_code += "\\usepackage{ytableau}\n"
    latex_code += "\\usepackage{hyperref}\n"
    latex_code += "\\usepackage{fancyhdr}\n"
    latex_code += "\\usepackage{multicol}\n"
    latex_code += "\\usepackage{titlesec}\n"
    
    # Set up fancy headers and footers
    latex_code += "\\pagestyle{fancy}\n"
    latex_code += "\\fancyhf{}\n"
    latex_code += "\\fancyhead[L]{NumericalSemigroup Catalog}\n"
    latex_code += "\\fancyfoot[C]{\\thepage}\n"
    
    # Adjust section formatting
    latex_code += "\\titleformat{\\section}{\\normalfont\\Large\\bfseries}{}{0em}{}\n"
    latex_code += "\\titleformat{\\subsection}{\\normalfont\\large\\bfseries}{}{0em}{}\n"
    
    # Adjust spacing
    latex_code += "\\titlespacing*{\\section}{0pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}\n"
    latex_code += "\\titlespacing*{\\subsection}{0pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}\n"
    
    # Start the document
    latex_code += "\\begin{document}\n"
    latex_code += "\\tableofcontents\n"
    latex_code += "\\newpage\n"

    # Add the main content
    latex_code += content

    # End the document
    latex_code += "\\end{document}\n"

    return latex_code

