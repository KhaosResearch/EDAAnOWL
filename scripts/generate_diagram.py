import svgwrite

def create_architecture_diagram(filename):
    width = 1150
    height = 920
    dwg = svgwrite.Drawing(filename, profile='full', size=(f'{width}px', f'{height}px'))
    
    # Styles definition
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        text { font-family: 'Inter', sans-serif; fill: #2d3436; }
        .bg-canvas { fill: #ffffff; }
        
        /* Layer/Box Styles */
        .layer-box { rx: 12; ry: 12; stroke-width: 2; fill-opacity: 0.1; }
        .node-box { rx: 6; ry: 6; stroke-width: 1.5; fill: #ffffff; }
        
        /* Text Styles */
        .title { font-size: 20px; font-weight: 600; text-anchor: middle; letter-spacing: 1.5px; fill: #2c3e50; }
        .header { font-size: 15px; font-weight: 600; text-anchor: middle; }
        .text { font-size: 13px; text-anchor: middle; fill: #2d3436; }
        .italic { font-size: 12px; font-style: italic; text-anchor: middle; fill: #636e72; }
        .label { font-size: 11px; font-weight: 600; fill: #636e72; text-anchor: middle; }
        
        /* Thematic Colors */
        .theme-ds { fill: #3498db; stroke: #2980b9; }      /* Blue DataSpace */
        .theme-cred { fill: #9b59b6; stroke: #8e44ad; }    /* Purple CRED */
        .theme-edaan { fill: #2ecc71; stroke: #27ae60; }   /* Green EDAAnOWL */
        .theme-idsa { fill: #e74c3c; stroke: #c0392b; }    /* Red IDSA */
        .theme-bigowl { fill: #f1c40f; stroke: #f39c12; }  /* Yellow BIGOWL */
        
        /* Edges */
        .edge { stroke: #535c68; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
        .edge-dashed { stroke-dasharray: 6,5; }
        .edge-label-bg { fill: #ffffff; }
    """))

    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), class_='bg-canvas'))

    # Arrowhead
    marker = dwg.marker(id='arrowhead', insert=(8, 4), size=(8, 8), orient='auto', markerUnits='strokeWidth')
    marker.add(dwg.path(d='M 0 0 L 8 4 L 0 8 Z', fill='#535c68'))
    dwg.defs.add(marker)

    # Helper function to easily draw boxes
    def draw_box(x, y, w, h, theme_class, title=None, subtitle=None, is_layer=False):
        dwg.add(dwg.rect(insert=(x, y), size=(w, h), class_=f'layer-box {theme_class}' if is_layer else f'node-box {theme_class}'))
        if title:
            y_offset = y + 25 if is_layer else y + h/2 + 5
            if subtitle:
                y_offset -= 8
                dwg.add(dwg.text(subtitle, insert=(x + w/2, y_offset + 20), class_='italic'))
            dwg.add(dwg.text(title, insert=(x + w/2, y_offset), class_='title' if is_layer else 'header'))

    def draw_node(x, y, w, h, theme, text):
        dwg.add(dwg.rect(insert=(x, y), size=(w, h), class_=f'node-box {theme}'))
        dwg.add(dwg.text(text, insert=(x + w/2, y + h/2 + 4), class_='text'))

    def draw_path(points, dashed=False, label=None):
        classes = 'edge edge-dashed' if dashed else 'edge'
        d = f"M {points[0][0]},{points[0][1]} "
        for p in points[1:]:
            d += f"L {p[0]},{p[1]} "
        dwg.add(dwg.path(d=d.strip(), class_=classes))
        
        if label:
            if len(points) == 4:
                lx, ly = points[1][0], points[1][1]
                ly -= 10
                dwg.add(dwg.text(label, insert=(lx, ly), class_='label'))
            elif len(points) == 2:
                lx = (points[0][0] + points[1][0]) / 2 + 5
                ly = (points[0][1] + points[1][1]) / 2
                dwg.add(dwg.text(label, insert=(lx, ly), class_='label'))

    # ================= LAYOUT ================= #

    # 1. PHYSICAL LAYER
    draw_box(50, 40, 1050, 120, 'theme-ds', 'DATA SPACE (Physical Assets)', is_layer=True)
    draw_node(180, 90, 200, 45, 'theme-ds', 'Data Assets & Files')
    draw_node(770, 90, 200, 45, 'theme-ds', 'Algorithms & Apps')

    # 2. SEMANTIC LAYER
    draw_box(50, 200, 1050, 680, 'theme-edaan', 'SEMANTIC INTEROPERABILITY (Ontology)', is_layer=True)

    # CRED (Left)
    draw_box(70, 260, 220, 280, 'theme-cred', 'CRED / DCAT-AP', is_layer=True)
    for i, t in enumerate(['dcat:Catalog', 'dcat:Dataset', 'dcat:DataService', 'odrl:Policy', 'foaf:Agent']):
        draw_node(90, 310 + i * 40, 180, 32, 'theme-cred', t)

    # IDSA (Right)
    draw_box(860, 260, 220, 150, 'theme-idsa', 'IDSA STANDARDS', is_layer=True)
    draw_node(880, 310, 180, 35, 'theme-idsa', 'ids:DataResource')
    draw_node(880, 360, 180, 35, 'theme-idsa', 'ids:DataApp')

    # BIGOWL (Right Bottom)
    draw_box(860, 680, 220, 140, 'theme-bigowl', 'BIGOWL ANALYTICS', is_layer=True)
    draw_node(880, 730, 180, 35, 'theme-bigowl', 'bigwf:Workflow')
    draw_node(880, 780, 180, 35, 'theme-bigowl', 'bigwf:Component')

    # EDAAnOWL Core (Middle)
    draw_box(320, 260, 510, 560, 'theme-edaan', 'EDAAnOWL CORE v1.0.0', is_layer=True)

    # Supply/Demand
    draw_box(350, 310, 180, 50, 'theme-edaan', 'DataAsset', '(Supply Side)')
    draw_box(620, 310, 180, 50, 'theme-edaan', 'SmartDataApp', '(Demand Side)')

    # Decoupling Matchmaking Bridge
    dwg.add(dwg.rect(insert=(340, 400), size=(470, 220), class_='layer-box theme-edaan', fill='#f1f8f1', stroke_dasharray="4,4"))
    dwg.add(dwg.text('MATCHMAKING DECOUPLING', insert=(575, 420), class_='italic'))

    draw_node(365, 440, 150, 40, 'theme-edaan', 'FieldMapping')
    draw_node(365, 495, 150, 40, 'theme-edaan', 'Metric / Unit')

    draw_node(635, 440, 150, 40, 'theme-edaan', 'InputProfile')
    draw_node(635, 495, 150, 40, 'theme-edaan', 'DataConstraint')

    draw_box(410, 560, 330, 45, 'theme-edaan', 'DataSpecification (Meaning)', '') # 410, 560 is bottom of center layer

    # Anchoring
    draw_box(340, 720, 470, 75, 'theme-edaan', 'Semantic Anchoring (SOSA/QUDT)', '(ObservableProperty / FeatureOfInterest / Unit URI)')


    # ================= ORTHOGONAL ROUTING ================= #
    
    # 1. Top Down Descriptions
    # Top box centers: Left 280, Right 870
    draw_path([(280, 135), (280, 170), (440, 170), (440, 310)], label="Describe")
    draw_path([(870, 135), (870, 170), (710, 170), (710, 310)], label="Describe")

    # 2. Internal Core 
    draw_path([(440, 360), (440, 440)])
    draw_path([(440, 480), (440, 560)])
    
    draw_path([(710, 360), (710, 440)])
    draw_path([(710, 480), (710, 560)])

    # Anchoring line
    draw_path([(575, 605), (575, 720)], dashed=True)

    # 3. Horizontal connections
    draw_path([(270, 326), (350, 326)], dashed=True) # CRED Dataset -> DataAsset
    draw_path([(880, 327), (835, 327), (835, 290), (510, 290), (510, 310)]) # IDSA Resource -> DataAsset
    draw_path([(800, 345), (860, 345), (860, 377), (880, 377)]) # SmartDataApp -> ids:DataApp
    draw_path([(970, 395), (970, 680)]) # ids:DataApp -> BIGOWL

    dwg.save()

if __name__ == '__main__':
    create_architecture_diagram('images/eda-an-architecture-en.svg')
