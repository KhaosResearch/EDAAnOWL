import svgwrite

def create_architecture_diagram(filename):
    dwg = svgwrite.Drawing(filename, profile='full', size=('800px', '600px'))
    
    # Styles
    dwg.defs.add(dwg.style("""
        .box { stroke: black; stroke-width: 1; rx: 5; ry: 5; }
        .text { font-family: Arial; font-size: 12px; text-anchor: middle; }
        .label { font-family: Arial; font-size: 14px; font-weight: bold; text-anchor: middle; }
        .arrow { stroke: black; stroke-width: 1; marker-end: url(#arrowhead); }
        .dashed { stroke-dasharray: 5,5; }
    """))
    
    # Arrowhead marker
    marker = dwg.marker(id='arrowhead', insert=(10,5), size=(10,10), orient='auto')
    marker.add(dwg.path(d='M0,0 L10,5 L0,10', fill='black'))
    dwg.defs.add(marker)

    # Layers (Backgrounds)
    # Data Space
    dwg.add(dwg.rect(insert=(50, 50), size=(700, 100), fill='#e1f5fe', stroke='#01579b', class_='box'))
    dwg.add(dwg.text('Data Space Layer', insert=(400, 70), class_='label'))
    
    # Semantic Layer
    dwg.add(dwg.rect(insert=(50, 180), size=(700, 350), fill='#f5f5f5', stroke='#616161', class_='box'))
    dwg.add(dwg.text('Semantic Layer', insert=(400, 200), class_='label'))

    # IDSA
    dwg.add(dwg.rect(insert=(70, 220), size=(200, 120), fill='#f8bbd0', stroke='#880e4f', class_='box'))
    dwg.add(dwg.text('IDSA Model', insert=(170, 240), class_='label'))
    
    # EDAAnOWL
    dwg.add(dwg.rect(insert=(300, 220), size=(200, 250), fill='#c8e6c9', stroke='#1b5e20', class_='box'))
    dwg.add(dwg.text('EDAAnOWL', insert=(400, 240), class_='label'))
    
    # BIGOWL
    dwg.add(dwg.rect(insert=(530, 220), size=(200, 120), fill='#fff9c4', stroke='#f57f17', class_='box'))
    dwg.add(dwg.text('BIGOWL', insert=(630, 240), class_='label'))

    # External
    dwg.add(dwg.rect(insert=(300, 490), size=(200, 30), fill='#e0e0e0', stroke='#616161', class_='box dashed'))
    dwg.add(dwg.text('External (DQV, PROV)', insert=(400, 510), class_='text'))

    # Nodes
    # Data Space
    dwg.add(dwg.rect(insert=(100, 90), size=(120, 40), fill='white', class_='box'))
    dwg.add(dwg.text('Data Assets', insert=(160, 115), class_='text'))
    
    dwg.add(dwg.rect(insert=(550, 90), size=(120, 40), fill='white', class_='box'))
    dwg.add(dwg.text('Applications', insert=(610, 115), class_='text'))

    # IDSA Nodes
    dwg.add(dwg.rect(insert=(110, 260), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('ids:DataResource', insert=(170, 280), class_='text'))
    
    dwg.add(dwg.rect(insert=(110, 300), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('ids:DataApp', insert=(170, 320), class_='text'))

    # EDAAnOWL Nodes
    dwg.add(dwg.rect(insert=(340, 260), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('DataAsset', insert=(400, 280), class_='text'))
    
    dwg.add(dwg.rect(insert=(340, 300), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('SmartDataApp', insert=(400, 320), class_='text'))
    
    dwg.add(dwg.rect(insert=(340, 340), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('DataProfile', insert=(400, 360), class_='text'))
    
    dwg.add(dwg.rect(insert=(340, 380), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('Metric', insert=(400, 400), class_='text'))
    
    dwg.add(dwg.rect(insert=(340, 420), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('ObservableProp', insert=(400, 440), class_='text'))

    # BIGOWL Nodes
    dwg.add(dwg.rect(insert=(570, 260), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('Component', insert=(630, 280), class_='text'))
    
    dwg.add(dwg.rect(insert=(570, 300), size=(120, 30), fill='white', class_='box'))
    dwg.add(dwg.text('Workflow', insert=(630, 320), class_='text'))

    # Edges
    # DS -> IDSA
    dwg.add(dwg.line(start=(160, 130), end=(160, 260), class_='arrow'))
    dwg.add(dwg.line(start=(610, 130), end=(170, 300), class_='arrow')) # App -> DataApp (simplified path)

    # IDSA -> EDAAnOWL
    dwg.add(dwg.line(start=(230, 275), end=(340, 275), class_='arrow'))
    dwg.add(dwg.line(start=(230, 315), end=(340, 315), class_='arrow'))

    # EDAAnOWL Internal
    dwg.add(dwg.line(start=(400, 290), end=(400, 300), class_='arrow')) # Asset -> Profile (conceptual link)
    dwg.add(dwg.line(start=(400, 330), end=(400, 340), class_='arrow'))
    dwg.add(dwg.line(start=(400, 370), end=(400, 380), class_='arrow'))

    # EDAAnOWL -> BIGOWL
    dwg.add(dwg.line(start=(460, 315), end=(570, 275), class_='arrow')) # App -> Component

    # BIGOWL Internal
    dwg.add(dwg.line(start=(630, 290), end=(630, 300), class_='arrow'))

    # External Links
    dwg.add(dwg.line(start=(400, 410), end=(400, 490), class_='arrow dashed'))

    dwg.save()

if __name__ == '__main__':
    create_architecture_diagram('images/eda-an-architecture-en.svg')
