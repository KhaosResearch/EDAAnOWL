import svgwrite

def create_architecture_diagram(filename):
    # Dimensions
    width = 1000
    height = 900
    dwg = svgwrite.Drawing(filename, profile='full', size=(f'{width}px', f'{height}px'))
    
    # --- Modern Design System & Better Contrast ---
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        text { font-family: 'Inter', sans-serif; fill: #2d3436; }
        .layer-bg { rx: 15; ry: 15; stroke-width: 2; }
        .component-box { rx: 6; ry: 6; stroke-width: 1.5; fill: #ffffff; }
        
        .label-title { font-size: 20px; font-weight: 600; text-anchor: middle; fill: #2d3436; text-transform: uppercase; letter-spacing: 1.5px; }
        .label-header { font-size: 15px; font-weight: 600; text-anchor: middle; }
        .label-text { font-size: 13px; text-anchor: middle; fill: #2d3436; }
        .label-italic { font-size: 11px; font-style: italic; text-anchor: middle; fill: #636e72; }
        
        /* High Contrast Palette (Light Bases) */
        .color-ds { fill: #e3f2fd; stroke: #1565c0; }      /* Blue */
        .color-cred { fill: #f3e5f5; stroke: #7b1fa2; }    /* Purple */
        .color-edaan { fill: #e8f5e9; stroke: #2e7d32; }   /* Green */
        .color-idsa { fill: #fce4ec; stroke: #c2185b; }    /* Red */
        .color-bigowl { fill: #fffde7; stroke: #fbc02d; }  /* Yellow/Orange */
        
        /* Clear Solid Arrow Lines */
        .arrow-line { stroke: #535c68; stroke-width: 2.5; fill: none; marker-end: url(#arrowhead); }
        .arrow-dashed { stroke-dasharray: 8,6; }
        .arrow-text { font-size: 12px; font-weight: 600; fill: #535c68; text-anchor: middle; }
        
        .bg-canvas { fill: #ffffff; }
    """))
    
    # 0. Solid Background (prevents transparency issues)
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), class_='bg-canvas'))

    # Arrowhead definition (using better size/alignment)
    marker = dwg.marker(id='arrowhead', insert=(9,5), size=(10,10), orient='auto', markerUnits='strokeWidth')
    marker.add(dwg.path(d='M0,0 L10,5 L0,10 Z', fill='#535c68'))
    dwg.defs.add(marker)

    # --- 1. DATA SPACE LAYER (TOP) ---
    dwg.add(dwg.rect(insert=(50, 40), size=(900, 120), class_='layer-bg color-ds'))
    dwg.add(dwg.text('Data Space (Physical Assets)', insert=(500, 70), class_='label-title'))
    
    # Boxes
    dwg.add(dwg.rect(insert=(120, 95), size=(250, 45), class_='component-box color-ds'))
    dwg.add(dwg.text('Data Assets & Files', insert=(245, 122), class_='label-header'))
    
    dwg.add(dwg.rect(insert=(630, 95), size=(250, 45), class_='component-box color-ds'))
    dwg.add(dwg.text('Algorithms & Apps', insert=(755, 122), class_='label-header'))

    # --- 2. SEMANTIC LAYER (CENTER) ---
    dwg.add(dwg.rect(insert=(50, 220), size=(900, 500), stroke='#b2bec3', fill='#fcfcfc', class_='layer-bg'))
    dwg.add(dwg.text('Semantic Interoperability (Ontology)', insert=(500, 245), class_='label-title'))

    # CRED Section
    dwg.add(dwg.rect(insert=(70, 280), size=(220, 260), class_='layer-bg color-cred'))
    dwg.add(dwg.text('CRED / DCAT-AP', insert=(180, 305), class_='label-header'))
    
    cred_nodes = [('dcat:Catalog', 330), ('dcat:Dataset', 370), ('dcat:DataService', 410), ('odrl:Offer / Policy', 450), ('foaf:Agent', 490)]
    for txt, y in cred_nodes:
        dwg.add(dwg.rect(insert=(90, y), size=(180, 32), class_='component-box color-cred'))
        dwg.add(dwg.text(txt, insert=(180, y+21), class_='label-text'))

    # IDSA Section
    dwg.add(dwg.rect(insert=(710, 280), size=(220, 130), class_='layer-bg color-idsa'))
    dwg.add(dwg.text('IDSA Standards', insert=(820, 305), class_='label-header'))
    dwg.add(dwg.rect(insert=(730, 325), size=(180, 35), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataResource', insert=(820, 348), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 370), size=(180, 35), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataApp', insert=(820, 393), class_='label-text'))

    # EDAAnOWL Core
    dwg.add(dwg.rect(insert=(320, 280), size=(360, 420), class_='layer-bg color-edaan'))
    dwg.add(dwg.text('EDAAnOWL v1.0.0 Core', insert=(500, 305), class_='label-header'))

    # Boxes (DataAsset, DataApp)
    dwg.add(dwg.rect(insert=(340, 325), size=(150, 50), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataAsset', insert=(415, 348), class_='label-header'))
    dwg.add(dwg.text('(Supply)', insert=(415, 365), class_='label-italic'))

    dwg.add(dwg.rect(insert=(510, 325), size=(150, 50), class_='component-box color-edaan'))
    dwg.add(dwg.text('SmartDataApp', insert=(585, 348), class_='label-header'))
    dwg.add(dwg.text('(Demand)', insert=(585, 365), class_='label-italic'))

    # Matchmaking Sub-group
    match_y = 405
    dwg.add(dwg.rect(insert=(340, match_y), size=(320, 170), stroke='#2e7d32', fill='#f1f8f1', class_='layer-bg', style='stroke-dasharray: 4,4;'))
    dwg.add(dwg.text('MATCHMAKING BRIDGE', insert=(500, match_y+20), class_='label-italic'))
    
    dwg.add(dwg.rect(insert=(360, match_y+35), size=(280, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataSpecification (Meaning)', insert=(500, match_y+58), class_='label-header'))

    # Supply Bridge
    dwg.add(dwg.rect(insert=(360, match_y+85), size=(130, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('FieldMapping', insert=(425, match_y+108), class_='label-text'))
    dwg.add(dwg.rect(insert=(360, match_y+125), size=(130, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('Metric / Unit', insert=(425, match_y+148), class_='label-text'))

    # Demand Bridge
    dwg.add(dwg.rect(insert=(510, match_y+85), size=(130, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('InputProfile', insert=(575, match_y+108), class_='label-text'))
    dwg.add(dwg.rect(insert=(510, match_y+125), size=(130, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataConstraint', insert=(575, match_y+148), class_='label-text'))

    # SOSA Anchor
    dwg.add(dwg.rect(insert=(340, 600), size=(320, 80), class_='component-box color-edaan', style='stroke-dasharray: 2,2;'))
    dwg.add(dwg.text('SOSA Semantic Anchor', insert=(500, 625), class_='label-header'))
    dwg.add(dwg.text('Property / FOI / Unit URI', insert=(500, 650), class_='label-text'))

    # BIGOWL
    dwg.add(dwg.rect(insert=(710, 600), size=(220, 140), class_='layer-bg color-bigowl'))
    dwg.add(dwg.text('BIGOWL Workflows', insert=(820, 625), class_='label-header'))
    dwg.add(dwg.rect(insert=(730, 650), size=(180, 32), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Workflow', insert=(820, 671), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 690), size=(180, 32), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Component', insert=(820, 711), class_='label-text'))

    # --- 3. CLEAN UP ARROWS/LINES (Solid and Well-Targeted) ---
    # Assets to Semantics (Down)
    dwg.add(dwg.line(start=(245, 140), end=(245, 280), class_='arrow-line'))
    dwg.add(dwg.text('Describe', insert=(245, 200), class_='arrow-text'))
    
    dwg.add(dwg.line(start=(755, 140), end=(755, 280), class_='arrow-line'))
    dwg.add(dwg.text('Describe', insert=(755, 200), class_='arrow-text'))

    # Supply Vertical Flow
    dwg.add(dwg.line(start=(415, 375), end=(415, 485), class_='arrow-line'))
    dwg.add(dwg.text('mapped', insert=(375, 435), class_='arrow-text'))
    
    # Demand Vertical Flow
    dwg.add(dwg.line(start=(585, 375), end=(585, 485), class_='arrow-line'))
    dwg.add(dwg.text('requires', insert=(625, 435), class_='arrow-text'))

    # Conversions to Specification
    dwg.add(dwg.line(start=(425, 485), end=(485, 440), class_='arrow-line'))
    dwg.add(dwg.line(start=(575, 485), end=(515, 440), class_='arrow-line'))

    # Spec to Anchor
    dwg.add(dwg.line(start=(500, 440), end=(500, 600), class_='arrow-line arrow-dashed'))

    # Lateral Connections
    dwg.add(dwg.line(start=(290, 350), end=(340, 350), class_='arrow-line arrow-dashed')) # CRED Metadata
    dwg.add(dwg.line(start=(710, 350), end=(490, 350), class_='arrow-line')) # IDSA Link

    # Analytics Flow
    dwg.add(dwg.line(start=(660, 390), end=(730, 390), class_='arrow-line')) # App to ids:App
    dwg.add(dwg.line(start=(820, 410), end=(820, 600), class_='arrow-line')) # ids:App to Workflow

    dwg.save()

if __name__ == '__main__':
    create_architecture_diagram('images/eda-an-architecture-en.svg')
