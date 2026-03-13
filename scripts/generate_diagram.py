import svgwrite

def create_architecture_diagram(filename):
    # Dimensions
    width = 1000
    height = 900
    dwg = svgwrite.Drawing(filename, profile='full', size=(f'{width}px', f'{height}px'))
    
    # --- Modern Design System ---
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        text { font-family: 'Inter', sans-serif; fill: #2d3436; }
        .layer-bg { rx: 15; ry: 15; stroke-width: 2; fill-opacity: 0.05; }
        .component-box { rx: 8; ry: 8; stroke-width: 1.5; fill: #ffffff; }
        
        .label-title { font-size: 20px; font-weight: 600; text-anchor: middle; fill: #2d3436; text-transform: uppercase; letter-spacing: 1px; }
        .label-header { font-size: 16px; font-weight: 600; text-anchor: middle; }
        .label-text { font-size: 13px; text-anchor: middle; }
        .label-italic { font-size: 12px; font-style: italic; opacity: 0.7; text-anchor: middle; }
        
        /* Professional Palette */
        .color-ds { fill: #0984e3; stroke: #0984e3; }      /* Blue - Physical World */
        .color-cred { fill: #6c5ce7; stroke: #6c5ce7; }    /* Purple - Compliance */
        .color-edaan { fill: #00b894; stroke: #00b894; }   /* Green - Core Logic */
        .color-idsa { fill: #d63031; stroke: #d63031; }    /* Red - Standard */
        .color-bigowl { fill: #e67e22; stroke: #d35400; }  /* Orange - Workflow */
        
        .arrow { stroke: #636e72; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
        .arrow-dashed { stroke-dasharray: 8,5; }
        .arrow-label { font-size: 11px; font-weight: 600; fill: #636e72; }
    """))
    
    # Arrowhead
    marker = dwg.marker(id='arrowhead', insert=(10,5), size=(4,4), orient='auto')
    marker.add(dwg.path(d='M0,0 L10,5 L0,10 Z', fill='#636e72'))
    dwg.defs.add(marker)

    # --- 1. PHYSICAL/DATA SPACE LAYER (TOP) ---
    dwg.add(dwg.rect(insert=(50, 40), size=(900, 120), class_='layer-bg color-ds'))
    dwg.add(dwg.text('Data Space (Physical Assets)', insert=(500, 70), class_='label-title'))
    
    # Physical Assets
    dwg.add(dwg.rect(insert=(120, 95), size=(250, 45), class_='component-box color-ds'))
    dwg.add(dwg.text('Data Assets & Files', insert=(245, 123), class_='label-header'))
    
    # Apps
    dwg.add(dwg.rect(insert=(630, 95), size=(250, 45), class_='component-box color-ds'))
    dwg.add(dwg.text('Algorithms & App Services', insert=(755, 123), class_='label-header'))

    # --- 2. SEMANTIC LAYER (CENTER) ---
    dwg.add(dwg.rect(insert=(50, 220), size=(900, 480), fill='#fdfdfd', stroke='#b2bec3', class_='layer-bg'))
    dwg.add(dwg.text('Semantic Interoperability (Ontology)', insert=(500, 245), class_='label-title'))

    # Left: CRED / Cataloging
    dwg.add(dwg.rect(insert=(70, 280), size=(220, 240), class_='layer-bg color-cred'))
    dwg.add(dwg.text('CRED Cataloging', insert=(180, 305), class_='label-header color-cred'))
    
    nodes_cred = [('dcat:Catalog', 325), ('dcat:Dataset', 365), ('dcat:DataService', 405), ('odrl:Offer / Policy', 445), ('foaf:Agent', 485)]
    for txt, y in nodes_cred:
        dwg.add(dwg.rect(insert=(90, y), size=(180, 32), class_='component-box color-cred'))
        dwg.add(dwg.text(txt, insert=(180, y+21), class_='label-text'))

    # Right: IDSA Standards
    dwg.add(dwg.rect(insert=(710, 280), size=(220, 120), class_='layer-bg color-idsa'))
    dwg.add(dwg.text('IDSA Standards', insert=(820, 305), class_='label-header color-idsa'))
    dwg.add(dwg.rect(insert=(730, 325), size=(180, 35), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataResource', insert=(820, 348), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 365), size=(180, 35), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataApp', insert=(820, 388), class_='label-text'))

    # Center: EDAAnOWL Core
    dwg.add(dwg.rect(insert=(310, 280), size=(380, 400), class_='layer-bg color-edaan'))
    dwg.add(dwg.text('EDAAnOWL v1.0.0 Core', insert=(500, 305), class_='label-header color-edaan'))

    # Top Part: DataAsset & DataApp
    dwg.add(dwg.rect(insert=(330, 325), size=(160, 50), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataAsset', insert=(410, 348), class_='label-header'))
    dwg.add(dwg.text('(Supply Side)', insert=(410, 365), class_='label-italic'))

    dwg.add(dwg.rect(insert=(510, 325), size=(160, 50), class_='component-box color-edaan'))
    dwg.add(dwg.text('SmartDataApp', insert=(590, 348), class_='label-header'))
    dwg.add(dwg.text('(Demand Side)', insert=(590, 365), class_='label-italic'))

    # Matchmaking Core (DECOUPLED)
    match_y = 400
    dwg.add(dwg.rect(insert=(330, match_y), size=(340, 160), class_='layer-bg color-edaan', style='fill-opacity: 0.1; stroke-dasharray: 4,4;'))
    dwg.add(dwg.text('v1.0.0 MATCHMAKING', insert=(500, match_y+20), class_='label-italic'))
    
    dwg.add(dwg.rect(insert=(350, match_y+30), size=(300, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataSpecification (Atomic Meaning)', insert=(500, match_y+53), class_='label-header'))

    # Supply Bridge
    dwg.add(dwg.rect(insert=(350, match_y+75), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('FieldMapping', insert=(420, match_y+98), class_='label-text'))
    dwg.add(dwg.rect(insert=(350, match_y+115), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('Metric / Unit', insert=(420, match_y+138), class_='label-text'))

    # Demand Bridge
    dwg.add(dwg.rect(insert=(510, match_y+75), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('InputProfile', insert=(580, match_y+98), class_='label-text'))
    dwg.add(dwg.rect(insert=(510, match_y+115), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataConstraint', insert=(580, match_y+138), class_='label-text'))

    # Base: Semantic Anchors
    dwg.add(dwg.rect(insert=(330, 580), size=(340, 80), class_='component-box color-edaan', style='fill:#f0fbf0; stroke-dasharray: 2,2;'))
    dwg.add(dwg.text('SOSA/QUDT Semantic Anchoring', insert=(500, 605), class_='label-header'))
    dwg.add(dwg.text('ObservableProperty / FeatureOfInterest / Unit', insert=(500, 630), class_='label-text'))
    dwg.add(dwg.text('(Domain Interoperability)', insert=(500, 650), class_='label-italic'))

    # --- 3. ANALYTICAL LAYER (BOTTOM) ---
    dwg.add(dwg.rect(insert=(710, 580), size=(220, 140), class_='layer-bg color-bigowl'))
    dwg.add(dwg.text('BIGOWL Workflows', insert=(820, 605), class_='label-header color-bigowl'))
    dwg.add(dwg.rect(insert=(730, 630), size=(180, 32), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Workflow', insert=(820, 651), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 670), size=(180, 32), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Component', insert=(820, 691), class_='label-text'))

    # --- CLEAN ARROWS/FLOWS ---
    # Straight down from Data Space to Semantic Layer
    dwg.add(dwg.line(start=(245, 140), end=(245, 280), class_='arrow'))
    dwg.add(dwg.text('Describe', insert=(215, 210), class_='arrow-label'))
    
    dwg.add(dwg.line(start=(755, 140), end=(755, 280), class_='arrow'))
    dwg.add(dwg.text('Describe', insert=(725, 210), class_='arrow-label'))

    # Supply Internal Flow (Clear vertical line)
    dwg.add(dwg.line(start=(410, 375), end=(410, 475), class_='arrow'))
    dwg.add(dwg.text('mapped via', insert=(365, 415), class_='arrow-label'))

    # Demand Internal Flow (Clear vertical line)
    dwg.add(dwg.line(start=(590, 375), end=(590, 475), class_='arrow'))
    dwg.add(dwg.text('requires', insert=(625, 415), class_='arrow-label'))

    # Converge to Specification (Diagonal but clear)
    dwg.add(dwg.line(start=(420, 475), end=(450, 435), class_='arrow'))
    dwg.add(dwg.line(start=(580, 475), end=(550, 435), class_='arrow'))

    # Down to Anchoring
    dwg.add(dwg.line(start=(500, 435), end=(500, 580), class_='arrow arrow-dashed'))

    # Horizontal Bridge: CRED/IDs -> Core
    dwg.add(dwg.line(start=(290, 348), end=(330, 348), class_='arrow arrow-dashed')) # CRED Metadata
    dwg.add(dwg.line(start=(710, 348), end=(490, 348), class_='arrow')) # IDSA specialization

    # App to Analytics
    dwg.add(dwg.line(start=(670, 388), end=(710, 388), class_='arrow')) # SmartApp -> ids:DataApp
    dwg.add(dwg.line(start=(820, 400), end=(820, 580), class_='arrow')) # ids:DataApp -> BIGOWL

    dwg.save()

if __name__ == '__main__':
    create_architecture_diagram('images/eda-an-architecture-en.svg')
