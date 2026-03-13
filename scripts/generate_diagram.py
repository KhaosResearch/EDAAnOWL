import svgwrite

def create_architecture_diagram(filename):
    # Dimensions and Grid
    width = 1000
    height = 850
    dwg = svgwrite.Drawing(filename, profile='full', size=(f'{width}px', f'{height}px'))
    
    # --- Modern Design System ---
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        text { font-family: 'Inter', -apple-system, sans-serif; fill: #2d3436; }
        .layer-bg { rx: 12; ry: 12; stroke-width: 2; fill-opacity: 0.1; }
        .component-box { rx: 8; ry: 8; stroke-width: 1.5; fill: #ffffff; }
        
        .label-title { font-size: 18px; font-weight: 600; text-anchor: middle; fill: #2d3436; }
        .label-header { font-size: 15px; font-weight: 600; text-anchor: middle; }
        .label-text { font-size: 13px; text-anchor: middle; }
        .label-italic { font-size: 11px; font-style: italic; opacity: 0.8; text-anchor: middle; }
        
        /* Layer Colors */
        .color-ds { fill: #0984e3; stroke: #0984e3; }
        .color-cred { fill: #6c5ce7; stroke: #6c5ce7; }
        .color-edaan { fill: #00b894; stroke: #00b894; }
        .color-idsa { fill: #d63031; stroke: #d63031; }
        .color-bigowl { fill: #fdcb6e; stroke: #e17055; }
        
        .arrow { stroke: #636e72; stroke-width: 1.5; fill: none; marker-end: url(#arrowhead); }
        .arrow-dashed { stroke-dasharray: 6,4; }
    """))
    
    # Arrowhead
    marker = dwg.marker(id='arrowhead', insert=(10,5), size=(5,5), orient='auto')
    marker.add(dwg.path(d='M0,0 L10,5 L0,10 Z', fill='#636e72'))
    dwg.defs.add(marker)

    # --- 1. DATA SPACE LAYER ---
    dwg.add(dwg.rect(insert=(50, 40), size=(900, 100), class_='layer-bg color-ds'))
    dwg.add(dwg.text('DATA SPACE LAYER (Physical Domain)', insert=(500, 70), class_='label-title'))
    
    # Data Assets Box
    dwg.add(dwg.rect(insert=(120, 85), size=(220, 40), class_='component-box color-ds'))
    dwg.add(dwg.text('Data Assets & Distributions', insert=(230, 110), class_='label-header'))
    
    # Apps Box
    dwg.add(dwg.rect(insert=(660, 85), size=(220, 40), class_='component-box color-ds'))
    dwg.add(dwg.text('Data Apps & Services', insert=(770, 110), class_='label-header'))

    # --- 2. SEMANTIC LAYER CONTAINER ---
    dwg.add(dwg.rect(insert=(50, 170), size=(900, 520), fill='#fdfdfd', stroke='#b2bec3', class_='layer-bg'))
    dwg.add(dwg.text('SEMANTIC INTEROPERABILITY LAYER', insert=(500, 195), class_='label-title'))

    # CRED Section
    dwg.add(dwg.rect(insert=(70, 230), size=(220, 240), class_='layer-bg color-cred'))
    dwg.add(dwg.text('CRED / DCAT-AP 3.0', insert=(180, 255), class_='label-header'))
    
    cred_nodes = [('dcat:Catalog', 275), ('dcat:Dataset', 315), ('dcat:DataService', 355), ('odrl:Policy', 395), ('foaf:Agent', 435)]
    for text, y in cred_nodes:
        dwg.add(dwg.rect(insert=(90, y), size=(180, 30), class_='component-box color-cred'))
        dwg.add(dwg.text(text, insert=(180, y+20), class_='label-text'))

    # IDSA Section
    dwg.add(dwg.rect(insert=(710, 230), size=(220, 140), class_='layer-bg color-idsa'))
    dwg.add(dwg.text('IDSA ALIGNMENT', insert=(820, 255), class_='label-header'))
    
    dwg.add(dwg.rect(insert=(730, 275), size=(180, 30), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataResource', insert=(820, 295), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 315), size=(180, 30), class_='component-box color-idsa'))
    dwg.add(dwg.text('ids:DataApp', insert=(820, 335), class_='label-text'))

    # EDAAnOWL Core v1.0.0
    dwg.add(dwg.rect(insert=(310, 230), size=(380, 440), class_='layer-bg color-edaan'))
    dwg.add(dwg.text('EDAAnOWL CORE (v1.0.0)', insert=(500, 255), class_='label-header'))

    # Supply/Demand split
    dwg.add(dwg.rect(insert=(330, 275), size=(160, 60), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataAsset', insert=(410, 300), class_='label-header'))
    dwg.add(dwg.text('(Supply Side)', insert=(410, 320), class_='label-italic'))

    dwg.add(dwg.rect(insert=(510, 275), size=(160, 60), class_='component-box color-edaan'))
    dwg.add(dwg.text('Smart Data App', insert=(590, 300), class_='label-header'))
    dwg.add(dwg.text('(Demand Side)', insert=(590, 320), class_='label-italic'))

    # Matchmaking Sub-group
    dwg.add(dwg.rect(insert=(330, 350), size=(340, 180), class_='layer-bg color-edaan', style='fill-opacity: 0.05; stroke-dasharray: 4,4;'))
    dwg.add(dwg.text('V1.0.0 MATCHMAKING DECOUPLING', insert=(500, 370), class_='label-italic'))

    dwg.add(dwg.rect(insert=(350, 385), size=(300, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataSpecification (Atomic Meaning)', insert=(500, 408), class_='label-header'))

    dwg.add(dwg.rect(insert=(350, 435), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('FieldMapping', insert=(420, 458), class_='label-text'))

    dwg.add(dwg.rect(insert=(510, 435), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('InputProfile', insert=(580, 458), class_='label-text'))

    dwg.add(dwg.rect(insert=(350, 480), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('Metric / Unit', insert=(420, 503), class_='label-text'))

    dwg.add(dwg.rect(insert=(510, 480), size=(140, 35), class_='component-box color-edaan'))
    dwg.add(dwg.text('DataConstraint', insert=(580, 503), class_='label-text'))

    # Grounding (Bottom of Core)
    dwg.add(dwg.rect(insert=(350, 550), size=(300, 100), class_='component-box color-edaan', style='fill: #ffffff; stroke-dasharray: 2,2;'))
    dwg.add(dwg.text('Semantic Anchoring (SOSA)', insert=(500, 575), class_='label-header'))
    dwg.add(dwg.text('ObservableProperty & FeatureOfInterest', insert=(500, 605), class_='label-text'))
    dwg.add(dwg.text('(Cross-Domain Interoperability)', insert=(500, 630), class_='label-italic'))

    # --- 3. WORKFLOW LAYER (Bottom) ---
    dwg.add(dwg.rect(insert=(710, 550), size=(220, 140), class_='layer-bg color-bigowl'))
    dwg.add(dwg.text('BIGOWL ANALYTICS', insert=(820, 575), class_='label-header'))
    
    dwg.add(dwg.rect(insert=(730, 600), size=(180, 30), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Workflow', insert=(820, 620), class_='label-text'))
    dwg.add(dwg.rect(insert=(730, 640), size=(180, 30), class_='component-box color-bigowl'))
    dwg.add(dwg.text('bigwf:Component', insert=(820, 660), class_='label-text'))

    # --- ARROWS ---
    # Assets to Semantics
    dwg.add(dwg.line(start=(230, 125), end=(230, 275), class_='arrow'))
    dwg.add(dwg.line(start=(770, 125), end=(770, 275), class_='arrow'))

    # Cross-layer links
    dwg.add(dwg.line(start=(290, 260), end=(330, 275), class_='arrow arrow-dashed')) # CRED -> Assets
    dwg.add(dwg.line(start=(710, 260), end=(490, 275), class_='arrow')) # IDSA -> Assets

    # Supply Side
    dwg.add(dwg.line(start=(410, 335), end=(420, 435), class_='arrow'))
    dwg.add(dwg.line(start=(420, 470), end=(420, 480), class_='arrow'))
    
    # Demand Side
    dwg.add(dwg.line(start=(590, 335), end=(580, 435), class_='arrow'))

    # All converging to Spec
    dwg.add(dwg.line(start=(420, 435), end=(450, 420), class_='arrow'))
    dwg.add(dwg.line(start=(580, 435), end=(550, 420), class_='arrow'))

    # Spec to Grounding
    dwg.add(dwg.line(start=(500, 420), end=(500, 550), class_='arrow'))

    # BIGOWL connection
    dwg.add(dwg.line(start=(670, 320), end=(730, 330), class_='arrow')) # App -> IdsApp
    dwg.add(dwg.line(start=(820, 370), end=(820, 550), class_='arrow')) # IdsApp -> Workflow

    dwg.save()

if __name__ == '__main__':
    create_architecture_diagram('images/eda-an-architecture-en.svg')
