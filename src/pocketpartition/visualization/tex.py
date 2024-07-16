from .tikz import generate_latex_table, generate_ferrers_tikz, generate_hasse_tikz
def generate_content_pages(label, subsections, data, partition, gap_poset, void_poset, max_width=10, max_height=10):
    latex_code = f"\\subsection{{MinGens: {label}}}\n"
    
    for subsection in subsections:
        latex_code += f"\\subsubsection*{{{subsection['title']}}}\n"
        if subsection['title'] == 'Invariants':
            latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
            latex_code += generate_latex_table(data)
            latex_code += "\\end{minipage}\n"
        elif subsection['title'] == 'Partition':
            latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
            latex_code += generate_ferrers_tikz(partition)
            latex_code += "\\end{minipage}\n"
        elif subsection['title'] == 'Gap Poset':
            elements, relations = gap_poset
            latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
            latex_code += generate_hasse_tikz(elements, relations)
            latex_code += "\\end{minipage}\n"
        elif subsection['title'] == 'Void Poset':
            elements, relations = void_poset
            latex_code += "\\begin{minipage}{0.48\\textwidth}\n"
            latex_code += generate_hasse_tikz(elements, relations)
            latex_code += "\\end{minipage}\n"
    
    return latex_code

def wrap_with_section(content:str, section_title:str):
    latex_code = f"\\section{section_title}\n"
    latex_code += content
    return latex_code

def wrap_with_headers_footers(content):
    latex_code = "\\documentclass[a4paper]{article}\n"
    latex_code += "\\usepackage{geometry}\n"
    latex_code += "\\usepackage{booktabs}\n"
    latex_code += "\\usepackage{tikz}\n"
    latex_code += "\\usepackage{ytableau}\n"  # Added ytableau package
    latex_code += "\\usepackage{hyperref}\n"
    latex_code += "\\usepackage{fancyhdr}\n"
    latex_code += "\\usepackage{multicol}\n"
    latex_code += "\\geometry{margin=0.5in}\n"
    latex_code += "\\pagestyle{fancy}\n"
    latex_code += "\\fancyhf{}\n"
    latex_code += "\\fancyhead[L]{Header}\n"
    latex_code += "\\fancyfoot[C]{\\thepage}\n"
    latex_code += "\\begin{document}\n"
    latex_code += "\\tableofcontents\n"
    latex_code += "\\newpage\n"

    latex_code += content
    latex_code += "\\end{document}\n"

    return latex_code

