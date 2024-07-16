from .tikz import generate_latex_table, generate_ferrers_tikz, generate_hasse_tikz
def generate_content_pages(label, subsections, data, partition, gap_poset, void_poset):
    latex_code = f"\\subsection{{Label: {label}}}\n"
    
    for subsection in subsections:
        latex_code += f"\\subsubsection*{{{subsection['title']}}}\n"
        if subsection['title'] == 'Invariants':
            latex_code += generate_latex_table(data)
        elif subsection['title'] == 'Partition':
            latex_code += generate_ferrers_tikz(partition)
        elif subsection['title'] == 'Gap Poset':
            elements, relations = gap_poset
            latex_code += generate_hasse_tikz(elements, relations)
        elif subsection['title'] == 'Void Poset':
            elements, relations = void_poset
            latex_code += generate_hasse_tikz(elements, relations)
    
    return latex_code

def wrap_with_section(content:str, section_title:str):
    latex_code = "\\section{section_title}\n"
    latex_code += content
    return latex_code

def wrap_with_headers_footers(content):
    latex_code = "\\documentclass{article}\n"
    latex_code += "\\usepackage{geometry}\n"
    latex_code += "\\usepackage{booktabs}\n"
    latex_code += "\\usepackage{tikz}\n"
    latex_code += "\\usepackage{hyperref}\n"
    latex_code += "\\usepackage{fancyhdr}\n"
    latex_code += "\\geometry{margin=1in}\n"
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