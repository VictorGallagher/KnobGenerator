
import FreeCAD as App
import FreeCADGui as Gui
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QRadioButton, QGroupBox, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QLabel, QPushButton
from FreeCAD import Base
import Part
import math



class KnobGenerator(QtWidgets.QWidget):
    def __init__(self):
        super(KnobGenerator, self).__init__()
        self.initUI()

    def initUI(self):
        # Create input widgets
        # Knob Shape
        knob_group = QGroupBox('Knob Head')
        shape_label = QLabel('Knob Shape:')
        self.shape_combo = QComboBox()
        self.shape_combo.addItem('Round')
        self.shape_combo.addItem('Square')
        self.shape_combo.addItem('Hex')
        self.shape_combo.addItem('Cross')
        self.shape_combo.addItem('Star')
        self.shape_combo.addItem('Tapered')
        # Knob Height
        height_label = QLabel('Height (mm):')
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(12)
        self.height_spin.setMaximum(100)
        # Knob Diameter
        knob_diameter_label = QLabel('Diameter (mm):')
        self.knob_diameter_spin = QSpinBox()
        self.knob_diameter_spin.setMinimum(36)
        self.knob_diameter_spin.setMaximum(100)

        # Knurls
        # Knurl size
        knurl_group = QGroupBox('Knurls')
        knurl_label = QLabel('Knurl Count:')
        self.knurl_count_spin = QSpinBox()
        self.knurl_count_spin.setMinimum(0)
        self.knurl_count_spin.setMaximum(100)
        # Knurl Shape
        knurl_shape_label = QLabel('Knurl Shape:')
        self.knurl_shape_combo = QComboBox()
        self.knurl_shape_combo.addItem('Round')
        self.knurl_shape_combo.addItem('Triangular')
        self.knurl_shape_combo.addItem('Hex')
        self.knurl_shape_combo.setEnabled(False)

        # Shank
        shank_flange_group = QGroupBox('Shank or Flange?')
        self.shank_radio = QRadioButton('Shank')
        self.flange_radio = QRadioButton('Flange')
        self.no_shank_flange_radio = QRadioButton('None')
        self.shank_radio.setChecked(True)
        # Shank diameter
        shank_diameter_label = QLabel('Shank Diameter (mm):')
        self.shank_diameter_spin = QSpinBox()
        self.shank_diameter_spin.setMinimum(18)
        self.shank_diameter_spin.setMaximum(100)
        self.shank_diameter_spin.setEnabled(True)
        # Shank Length
        self.shank_length_label = QLabel('Shank Length (mm):')
        self.shank_length_spin = QSpinBox()
        self.shank_length_spin.setMinimum(15)
        self.shank_length_spin.setMaximum(100)
        self.shank_length_spin.setEnabled(True) 

        # Hole Type
        hole_group = QGroupBox('Hole:')
        self.hole_radio = QRadioButton('Through Hole')
        self.half_hole_radio = QRadioButton('Half Hole')
        self.hole_radio.setChecked(True)
        # Hole Diameter
        hole_label = QLabel('Hole Diameter (mm):')
        self.hole_spin = QSpinBox()
        self.hole_spin.setMinimum(6)
        self.hole_spin.setMaximum(20)

        # Fasener Type
        # Nut or Bolt
        nut_bolt_group = QGroupBox('Nut or Bolt?')
        self.nut_radio = QRadioButton('Nut')
        self.bolt_radio = QRadioButton('Bolt')
        self.both_radio = QRadioButton('Both')
        self.both_radio.setChecked(True)
        self.nut_bolt_none_radio =  QRadioButton('None')
        # Bolt Type
        bolt_type_label = QLabel('Bolt Type:')
        self.bolt_type_combo = QComboBox()
        self.bolt_type_combo.addItem('Hex Head')
        self.bolt_type_combo.addItem('Carriage Bolt')
        self.bolt_type_combo.addItem('Screw')
        # Nut Type
        nut_type_label = QLabel('Nut Type:')
        self.nut_type_combo = QComboBox()
        self.nut_type_combo.addItem('Hex Nut')
        self.nut_type_combo.addItem('T Nut')
        #self.nut_type_combo.addItem('Insertion Nut')

        generate_button = QPushButton('Generate')
        generate_button.clicked.connect(self.generateKnob)

        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

 
        # Create layout
        layout = QVBoxLayout()

        layout.addWidget(knob_group)
        knob_layout = QHBoxLayout()
        knob_layout.addWidget(shape_label)
        knob_layout.addWidget(self.shape_combo)
        knob_layout.addWidget(height_label)
        knob_layout.addWidget(self.height_spin)
        knob_layout.addWidget(knob_diameter_label)
        knob_layout.addWidget(self.knob_diameter_spin)
        knob_group.setLayout(knob_layout)

        layout.addWidget(knurl_group)
        knurl_layout = QHBoxLayout()
        knurl_layout.addWidget(knurl_label)
        knurl_layout.addWidget(self.knurl_count_spin)
        knurl_layout.addWidget(knurl_shape_label)
        knurl_layout.addWidget(self.knurl_shape_combo)
        knurl_group.setLayout(knurl_layout)

        layout.addWidget(shank_flange_group)
        shank_flange_layout = QHBoxLayout()
        shank_flange_layout.addWidget(self.shank_radio)
        shank_flange_layout.addWidget(self.flange_radio)
        shank_flange_layout.addWidget(self.no_shank_flange_radio)

        shank_flange_layout.addWidget(shank_diameter_label)
        shank_flange_layout.addWidget(self.shank_diameter_spin)
        shank_flange_layout.addWidget(self.shank_length_label)
        shank_flange_layout.addWidget(self.shank_length_spin)
        shank_flange_group.setLayout(shank_flange_layout)
       
        layout.addWidget(hole_group)
        hole_layout = QHBoxLayout()
        hole_layout.addWidget(self.hole_radio)
        hole_layout.addWidget(self.half_hole_radio)
        hole_layout.addWidget(hole_label)
        hole_layout.addWidget(self.hole_spin)       
        hole_group.setLayout(hole_layout)
        hole_layout.addWidget(hole_label)
        hole_layout.addWidget(self.hole_spin)

        layout.addWidget(nut_bolt_group)
        nut_bolt_layout = QHBoxLayout()
        nut_bolt_layout.addWidget(self.nut_radio)
        nut_bolt_layout.addWidget(self.bolt_radio)
        nut_bolt_layout.addWidget(self.both_radio)
        nut_bolt_group.setLayout(nut_bolt_layout)
        nut_bolt_layout.addWidget( self.nut_bolt_none_radio)
        nut_bolt_layout.addWidget(bolt_type_label)
        nut_bolt_layout.addWidget(self.bolt_type_combo)
        nut_bolt_layout.addWidget(nut_type_label)
        nut_bolt_layout.addWidget(self.nut_type_combo)

        layout.addWidget(generate_button)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setWindowTitle('Knob Generator')


        #Gray out controls
        self.shank_radio.toggled.connect(self.onShankFlangeToggled)
        self.bolt_radio.toggled.connect(self.onNutBoltToggled)
        self.both_radio.toggled.connect(self.onNutBoltToggled)
        self.nut_radio.toggled.connect(self.onNutBoltToggled)
        self.knurl_count_spin.valueChanged.connect(self.OnValueChange_knurl_count)
#        self.no_hole_radio.toggled.connect(self.onHoleToggled)
#        self.hole_radio.toggled.connect(self.onHoleToggled)

    line_number = 5

    def onShankFlangeToggled(self):
        if self.shank_radio.isChecked():
            self.shank_diameter_spin.setEnabled(True)
            self.shank_length_spin.setEnabled(True)
        else:
            self.shank_diameter_spin.setEnabled(False)
            self.shank_length_spin.setEnabled(False)

    def onNutBoltToggled(self):
        if self.nut_radio.isChecked():
            self.nut_type_combo.setEnabled(True)
            self.bolt_type_combo.setEnabled(False)
        elif self.bolt_radio.isChecked():
            self.bolt_type_combo.setEnabled(True)
            self.nut_type_combo.setEnabled(False)
        elif self.both_radio.isChecked():
            self.bolt_type_combo.setEnabled(True)
            self.nut_type_combo.setEnabled(True)
        elif self.nut_bolt_none_radio.isChecked():
            self.bolt_type_combo.setEnabled(False)
            self.nut_type_combo.setEnabled(False)


    def OnValueChange_knurl_count(self, v):
        if v != 0 :
            self.knurl_shape_combo.setEnabled(True)
        else:
            self.knurl_shape_combo.setEnabled(False)

    def hypotenuse_length(self, a, b):
        c = math.sqrt(a**2 + b**2)
        return c

    def inverse_hypotenuse(self, h):
        a = h * math.sin(math.radians(45))
        return a

    def point_to_angle(x, y, radius):
        dx = x - radius
        dy = y - radius
        r = math.sqrt(dx**2 + dy**2)
        theta = math.atan2(dy, dx)
        return (r, theta)

    def calculate_rotation(self, knurl_number, hypotenuse_length, knurl_count):
        angle_between_knurls = 360 / knurl_count
        half_angle_between_knurls = angle_between_knurls / 2
        knurl_to_parameter_distance = (hypotenuse_length / 2) / math.sin(math.radians(half_angle_between_knurls))
        angle = math.radians(knurl_number * angle_between_knurls + half_angle_between_knurls)
        return angle

    def get_circumradius(self, part):
        if hasattr( part, 'Radius'):
            length = part.Radius
        elif hasattr( part, 'Circumradius'):
           length = part.Circumradius
        elif hasattr(part, 'Radius1'):
            length = part.Radius1
        elif hasattr(part, 'Length'):
            length = part.Length/2
        elif hasattr(part, 'Shape'):
            part = part.Shape
            if hasattr( part, 'Radius'):
                length = part.Radius
            elif hasattr( part, 'Circumradius'):
               length = part.Circumradius
            elif hasattr(part, 'Radius1'):
                length = part.Radius1
            elif hasattr(part, 'Length'):
                length = part.Length/2
            return length/25
        else:
            return None

        return length

    def cut_parts(self, part, cut_part, name):
        doc = App.activeDocument()
        knob_shape = doc.addObject("Part::Cut", name)
        knob_shape.Base = part
        knob_shape.Tool = cut_part
        return knob_shape
    
    def fuse_parts(self, part1, part2 ):
        """Fuse the knob top and shank/flange """
        if (part1 is not None) and (part2 is not None):
            fusion = App.activeDocument().addObject("Part::MultiFuse", "Knob")
            fusion.Shapes = [part1, part2]
            return fusion

    def make_hole(self, knob, diameter, knob_height, shank_length):
        docName = App.ActiveDocument.Name
        obj_name = 'Hole'
        total_height = knob_height + shank_length + 10
        hole_shape = App.ActiveDocument.addObject('Part::Cylinder', 'Hole')
        hole_shape.Radius = diameter/2
        hole_shape.Height = total_height
        hole_shape.Placement.Base = App.Vector(0, 0, -(total_height)/2)
        hole_shape = self.cut_parts(knob, hole_shape, 'Hole')
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Hole Radius', str(diameter/2))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius', u'Sheet.'+ alias)
        return hole_shape

    def make_half_hole(self, knob, diameter, knob_height, shank_length):
        docName = App.ActiveDocument.Name
        obj_name = 'Hole'
        if shank_length is not None:
            total_height = (shank_length+knob_height)/2 + 5
        else:
            total_height = (knob_height/2)+5
        hole_shape = App.ActiveDocument.addObject('Part::Cylinder', 'HalfHole')
        hole_shape.Radius = diameter/2
        hole_shape.Height = total_height
        hole_shape.Placement.Base = App.Vector(0, 0, (-total_height/2))
        hole_shape = self.cut_parts(knob, hole_shape, 'Knob')
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Hole Radius', str(diameter/2))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Hole Depth', str(total_height))
        getattr(App.getDocument(docName),obj_name).setExpression('Height', u'Sheet.'+ alias)

        return hole_shape


    def make_shank(self, diameter, length, head_height):
        docName = App.ActiveDocument.Name
        obj_name = 'Shank'
        shank_shape = App.ActiveDocument.addObject('Part::Cylinder', 'Shank')
        shank_shape.Radius = diameter/2
        shank_shape.Height = length
        shank_shape.Placement.Base = App.Vector(0, 0, -length)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Shank Radius', str(diameter/2))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Shank Length', str(length))
        getattr(App.getDocument(docName),obj_name).setExpression('Height', u'Sheet.'+ alias)
        return shank_shape

    def make_flange(self, diameter, height):
        docName = App.ActiveDocument.Name
        obj_name = 'Flange'
        flange_top_dia =diameter/2
        flange_bottom_dia = (flange_top_dia * 0.25) + (flange_top_dia)
        flange_height = height 
        flange_shape = App.ActiveDocument.addObject("Part::Cone","Flange")
        flange_shape.Radius1 = flange_bottom_dia
        flange_shape.Radius2 = flange_top_dia
        flange_shape.Height = height
        flange_shape.Placement.Base = App.Vector(0, 0, -flange_height)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Flange Top Radius', str(flange_top_dia))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius2', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Flange Bottom Radius', str(flange_bottom_dia))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius1', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Flange Thinkness', str(height))
        getattr(App.getDocument(docName),obj_name).setExpression('Height', u'Sheet.'+ alias)

        return flange_shape


    
    #Interior Faseners 

    def make_hexnut(self, shank_length, diameter):
        docName = App.ActiveDocument.Name
        obj_name = 'Nut'
        nut_shape = App.ActiveDocument.addObject('Part::Prism', 'Nut')
        nut_shape.Circumradius = diameter
        nut_shape.Height = shank_length / 2
        nut_shape.Placement.Base = App.Vector(0, 0, -(shank_length))
        self.line_number += 1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Nut Radius', str(diameter))
        nut_shape.setExpression('Circumradius', u'Sheet.' + alias)
        self.line_number += 1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Nut Length', str(shank_length / 2))
        nut_shape.setExpression('Height', u'Sheet.' + alias)
        self.line_number += 1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Nut Placement', str(-shank_length))
        nut_shape.setExpression('Placement.Base.z', u'Sheet.' + alias)

        return nut_shape


    def make_hex_bolt(self, knob_height, diameter):
        docName = App.ActiveDocument.Name
        obj_name = 'Bolt'
        bolt_head_length = knob_height
        nut_shape = App.ActiveDocument.addObject('Part::Prism', 'Bolt')
        nut_shape.Circumradius = diameter
        nut_shape.Height = knob_height
        nut_shape.Placement.Base = App.Vector(0, 0,  0)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Bolt Head Radius', str(diameter))
        getattr(App.getDocument(docName),obj_name).setExpression('Circumradius', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Bolt Head Length',str( bolt_head_length ))
        getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Bolt Head Placement', str(bolt_head_length/2))
        getattr(App.getDocument(docName), obj_name).setExpression('Placement.Base.z', u'Sheet.'+ alias)
        return nut_shape

    def make_carriage_bolt(self, knob_height, diameter):
        docName = App.ActiveDocument.Name
        obj_name = 'CariageBolt'
        bolt_height = knob_height/4
        nut_shape = App.ActiveDocument.addObject('Part::Cylinder', 'CarriageBolt')
        nut_shape.Radius = diameter/3
        nut_shape.Height = knob_height/4
        nut_shape.Placement.Base = App.Vector(0, 0,  0)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Cariage Head Radius', str(diameter))
        getattr(App.getDocument(docName),obj_name).setExpression('Circumradius', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Cariage Head Length',str( bolt_head_length ))
        getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Cariage Head Placement', str(bolt_head_length/2))
        getattr(App.getDocument(docName), obj_name).setExpression('Placement.Base.z', u'Sheet.'+ alias)
        return nut_shape



    def make_tnut(self, length, diameter):
        docName = App.ActiveDocument.Name
        obj_name = 'TNut'
        nut_shape = App.ActiveDocument.addObject('Part::Cylinder', 'TNut')
        nut_length =  length*0.1
        nut_radius = (diameter/2)-2.5
        nut_shape.Radius = nut_radius
        nut_shape.Height = nut_length
        nut_shape.Placement.Base = App.Vector(0, 0, -(length))
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'TNut Radius', str(nut_radius))
        getattr(App.getDocument(docName),obj_name).setExpression('Radius', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'TNut Length',str( nut_length))
        getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+ alias)
        self.line_number+=1
        alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'TNut Placement', str(-length))
        getattr(App.getDocument(docName), obj_name).setExpression('Placement.Base.z', u'Sheet.'+ alias)

        return nut_shape

    # Knurls 

    def make_triangle_knurls(self, knob, knurl_count, knurl_height):
            docName = App.ActiveDocument.Name
            obj_name = 'Knurl'
            knurl_pos = self.get_circumradius(knob)
            if knurl_pos is None:
                return knob     
            knob_circumference = 3.14 * (knurl_pos * 2)
            knurl_diameter = (knob_circumference/2)/knurl_count
            step = int(360/knurl_count)
            knurls = []  # List to store the Knurl objects
            offsets = [0,0,75,46,22,9,0,-6,-11,-15,-18,-21,-22, -24, -29, -29,-30, -32,-32,-33,-33, -34, -34, -35]
            offset = offsets[knurl_count]
            if knurl_count > 2:
                for deg, count in zip(range(-step, 360, step), range(0,knurl_count)):
                    knurl = App.ActiveDocument.addObject('Part::Box', 'Tri-Knurl')
                    knurl.Height = knurl_height+8
                    hypot = self.inverse_hypotenuse(knurl_diameter)
                    knurl.Length = hypot
                    knurl.Width = hypot
                    rad = math.radians(deg)
                    rotation =round( -((360/knurl_count) * count)) + offset
                    x = (knurl_pos) * math.sin(rad)
                    y = (knurl_pos) * math.cos(rad)
                    knurl.Placement.Base = FreeCAD.Vector(x, y,  0)
                    knurl.Placement.Rotation = App.Rotation(FreeCAD.Vector(0, 0, 1), rotation)
                    knurls.append(knurl) 
                    self.line_number += 1
                    alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Tri Knurl ' + str(count + 1) + ' Length', str(hypot))
                    knurl.setExpression('Length', u'Sheet.' + alias) 
                    self.line_number += 1
                    alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Tri Knurl ' + str(count + 1) + ' Width', str(hypot))
                    knurl.setExpression('Width', u'Sheet.' + alias) 
                    knob = self.cut_parts(knob, knurl, 'KnurlCut'+ str(deg))
            return knob


    '''Create an empty list called knurls before the loop starts. Inside the loop, 
    we append each Knurl object to the knurls list. Then, when setting the expression for the radius, 
    we can directly access the Knurl object using knurl.setExpression('Radius', u'Sheet.' + alias).
    By using the knurls list, you can access the Knurl objects without relying on 
    object names that include the count variable.'''
    
    def make_round_knurls(self, knob, knurl_count, knurl_height):
        docName = App.ActiveDocument.Name
        obj_name = 'Knurl'
        knurl_pos = self.get_circumradius(knob)
        if knurl_pos is None:
            return knob

        knob_circumference = 3.14 * (knurl_pos * 2)
        knurl_diameter = (knob_circumference / 2) / knurl_count
        step = int(360 / knurl_count)
        knurls = []  # List to store the Knurl objects

        for deg, count in zip(range(0, 360, step), range(0, knurl_count)):
            knurl = FreeCAD.ActiveDocument.addObject('Part::Cylinder', 'RoundKnurl')
            knurl.Height = knurl_height
            knurl.Radius = knurl_diameter / 2
            rad = math.radians(deg)
            knurl.Placement.Base = FreeCAD.Vector(knurl_pos * math.sin(rad), knurl_pos * math.cos(rad), 0)
            knurls.append(knurl)  
            self.line_number += 1
            alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Hex Knurl ' + str(count + 1) + ' Radius', str(knurl_diameter / 2))
            knurl.setExpression('Radius', u'Sheet.' + alias)  
            knob = self.cut_parts(knob, knurl, 'KnurlCut' + str(deg))

        return knob

    def make_hex_knurls(self, knob, knurl_count, knurl_height):
        knurl_pos = self.get_circumradius(knob)
        if knurl_pos is None:
            return knob     
        knob_circumference = 3.14 * (knurl_pos * 2)
        knurl_diameter = (knob_circumference/2)/knurl_count
        step = int(360/knurl_count)
        knurls = []  # List to store the Knurl objects
        for deg, count in zip(range(0,360, step), range(0,knurl_count)):
            knurl = App.ActiveDocument.addObject('Part::Prism', 'Hex-Knurl')
            knurl.Circumradius = knurl_diameter/2
            knurl.Height = knurl_height
            rad = math.radians(deg)
            rotation =round( -(360/knurl_count) * (count))
            x = (knurl_pos) * math.sin(rad)
            y = (knurl_pos) * math.cos(rad)
            knurl.Placement.rotate(App.Vector(0.00,0.00,0.00), App.Vector(0.00,0.00,0.00), rotation )
            knurl.Placement.Base = FreeCAD.Vector(x, y,  0)
            knurls.append(knurl)  # Add the Knurl object to the list
            self.line_number += 1
            alias = self.initialize_cell_link(self.spreadsheet, self.line_number, 'Knurl ' + str(count + 1) + ' Radius', str(knurl_diameter / 2))
            knurl.setExpression('Circumadius', u'Sheet.' + alias)  # Set the expression directly on the Knurl object
            knob = self.cut_parts(knob, knurl, 'KnurlCut'+ str(deg))
        return knob

    def get_alias_value(self, doc, alias):
            cell = doc.getCellFromAlias( alias)
            value = doc.getContents(cell)
            return value



    def initialize_cell_link(self, sheet, line_number, constraint_name, cell_formula):
        name_column = 'A'
        value_column = 'B'
        cell_A = name_column + str(line_number)
        cell_B = value_column + str(line_number)
        alias_name =  constraint_name.replace(" ", "")
        sheet.set(cell_A, constraint_name)
        sheet.setAlignment(cell_A,  'center', 'keep')
        sheet.setColumnWidth(cell_A, 200)
        sheet.setAlias(cell_B,  alias_name)
        sheet.setAlignment(cell_B,  'center', 'keep')
        sheet.setStyle(cell_B, 'bold', 'add')
        sheet.set(cell_B, cell_formula)
        sheet.setDisplayUnit(cell_B, 'mm')
        return alias_name



    def make_knob_head(self, knob_shape, radius, knob_height):
        line_number = self.line_number
        spreadsheet = self.spreadsheet

        if knob_shape == 'Round':
            obj_name = 'Round_Knob'
            docName = App.ActiveDocument.Name
            base_shape = App.ActiveDocument.addObject('Part::Cylinder', obj_name)
            base_shape.Radius = radius
            base_shape.Height = knob_height

            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Radius', str(radius))
            getattr(App.getDocument(docName),obj_name).setExpression('Radius', u'Sheet.'+alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Height', str(knob_height))
            getattr(App.getDocument(docName),obj_name).setExpression('Height', u'Sheet.'+alias)

        if knob_shape == 'Tapered':
            obj_name = 'Tapered_Knob'
            docName = App.ActiveDocument.Name
            base_shape = App.ActiveDocument.addObject("Part::Cone",obj_name)
            base_shape.Radius1 = radius
            base_shape.Radius2 = radius * 0.85
            base_shape.Height = knob_height

            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Bottom Radius', str(radius))
            getattr(App.getDocument(docName), obj_name).setExpression('Radius1', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Top Radius', str(radius * 0.85))
            getattr(App.getDocument(docName), obj_name).setExpression('Radius2', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, selfline_number, 'Knob Height', str(knob_height))
            getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+ alias)


        if knob_shape == 'Hex':
            obj_name = knob_shape + "_Knob"
            docName = App.ActiveDocument.Name
            base_shape = App.ActiveDocument.addObject('Part::Prism', obj_name)
            base_shape.Circumradius = radius
            base_shape.Height = knob_height

            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Circumradius Radius', str(radius))
            getattr(App.getDocument(docName),obj_name).setExpression('Circumradius', u'Sheet.'+alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Height', str(knob_height))
            getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+alias)


        if knob_shape == 'Square':
            obj_name = knob_shape + "_Knob"
            docName = App.ActiveDocument.Name
            base_shape = App.ActiveDocument.addObject('Part::Box', obj_name)
            base_shape.Height = knob_height
            base_shape.Length = radius * 2
            base_shape.Width= radius * 2
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Length', str(radius*2))
            getattr(App.getDocument(docName), obj_name).setExpression('Length', u'Sheet.'+alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Width', str(radius *2))
            getattr(App.getDocument(docName), obj_name).setExpression('Width', u'Sheet.'+alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Height', str(knob_height))
            getattr(App.getDocument(docName), obj_name).setExpression('Height', u'Sheet.'+alias)

            base_shape.Placement.Base = FreeCAD.Vector(-radius, -radius,  0)


        if knob_shape == 'Cross':
            obj_nameX = knob_shape + "_KnobY"
            docName = App.ActiveDocument.Name
            dx = (radius * 2)/3
            dy = (radius * 2)
            base_shape1 = App.ActiveDocument.addObject('Part::Box', obj_nameX)
            base_shape1.Height = knob_height
            base_shape1.Length = (radius * 2)/3
            base_shape1.Width = (radius * 2)
            base_shape1.Placement.Base = App.Vector(-dx/2, -dy/2, 0)

            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob Radius', str(radius ))
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'DX',  '=((KnobRadius*2)/3 )' )
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'DY', '=(KnobRadius*2 )')    
            self.line_number+=1
            #alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Knob LengthY', str((radius*2)/3))
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Vertical Length', '=(KnobRadius*2)/3'  )
            getattr(App.getDocument(docName), obj_nameX).setExpression('Length', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Vertical Width', str(radius *2))
            getattr(App.getDocument(docName), obj_nameX).setExpression('Width', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Vertical Height',str( knob_height))
            getattr(App.getDocument(docName), obj_nameX).setExpression('Height', u'Sheet.'+ alias)


            obj_nameY = knob_shape + "_KnobX"      
            base_shape2 = App.ActiveDocument.addObject('Part::Box', obj_nameY)
            base_shape2.Height = knob_height
            base_shape2.Length =(radius * 2)
            base_shape2.Width = (radius * 2)/3
            base_shape2.Placement.Base = App.Vector(-dy/2, -dx/2, 0)
            base_shape2.Placement.Base.x = -dy/2
            base_shape2.Placement.Base.y = -dx/2
            base_shape2.Placement.Base.z = 0

            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Horizontal Length', '=DY')
            getattr(App.getDocument(docName), obj_nameY).setExpression('Length', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Horizontal Width', '=DX')
            getattr(App.getDocument(docName), obj_nameY).setExpression('Width', u'Sheet.'+ alias)
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Horizontal Height',str( knob_height))
            getattr(App.getDocument(docName), obj_nameY).setExpression('Height', u'Sheet.'+ alias)
            #FreeCAD.Placement(FreeCAD.Vector(-18.0, -6.0, 0.0),FreeCAD.Rotation(0,0,0,1))
            self.line_number+=1
            alias = self.initialize_cell_link(spreadsheet, self.line_number, 'Horizontal Placement', str(base_shape2.Placement.Base.y))
            getattr(App.getDocument(docName), obj_nameY).setExpression('Placement.Base.y', u'Sheet.'+ alias)

            base_shape = self.fuse_parts(base_shape1, base_shape2)
            base_shape.Refine = True
    

        if knob_shape == 'Star':
            base_shape1 = App.ActiveDocument.addObject("Part::Wedge","Wedge")
            base_shape1.Xmin=-radius
            base_shape1.Ymin=0
            base_shape1.Zmin=0
            base_shape1.X2min=0
            base_shape1.Z2min=0
            base_shape1.Xmax=radius
            base_shape1.Ymax=math.sin(math.radians(60)) * (radius*2)
            base_shape1.Zmax=knob_height
            base_shape1.X2max=0
            base_shape1.Z2max=knob_height
            base_shape1.Placement.Base = App.Vector(0, -base_shape1.Ymax/6, 0)

            base_shape2 = App.ActiveDocument.addObject("Part::Wedge","Wedge")
            base_shape2.Xmin=-radius
            base_shape2.Ymin=0
            base_shape2.Zmin=0
            base_shape2.X2min=0
            base_shape2.Z2min=0
            base_shape2.Xmax=radius
            base_shape2.Ymax=math.sin(math.radians(60)) * (radius*2)
            base_shape2.Zmax=knob_height
            base_shape2.X2max=0
            base_shape2.Z2max=knob_height
            base_shape2.Placement.Base = App.Vector(radius/2, 0,0)
            base_shape2.Placement.rotate(App.Vector(0.00,0.00,0.00), App.Vector(0.00,0.00,0.00), 60.00) # Apply rotation
            base_shape = self.fuse_parts(base_shape1, base_shape2)
            #base_shape.refine = True
            base_shape.Placement.Base = App.Vector(0, -base_shape1.Ymax/6, 0)

        return base_shape


    def get_edges(self, shape):
        edges = [i for i in shape.Edges]
        print('Edge Count ', len(edges))
        return edges


    def select_edges(self, myshape, radius):
        edges = self.get_edges(myshape.Shape)
        if not edges:
            raise ValueError("No edges found in shape.")
        if len(edges) == 1:
            raise ValueError("Only one edge found in shape.")
        fillets = []
        label1 = myshape.Label
        label2 = myshape.Label2
        for n, edge in enumerate(edges):
            Gui.Selection.addSelection(label2, label1, f"Edge{n}")
            fillets.append((n+1, radius, radius))
        return fillets


    def fillet_edges(self, doc, part, radius):
        fillets = self.select_edges(part, radius)
        fillet_part = doc.addObject("Part::Fillet", "Fillet")
        fillet_part.Base = part
        fillet_part.Edges = fillets
        part.Visibility = False
        try:
            doc.recompute()
            if fillet_part.isValid():
                return fillet_part
        except Part.OCCError:
            print("Failed to create fillet.")
        return None


    def generateKnob(self):
        App.newDocument("Knob")
        doc = App.activeDocument()
        doc.addObject("Part::Feature", "Base")
        base = doc.Base

        bolt = self.bolt_radio.isChecked()
        bolt_type = self.bolt_type_combo.currentText()
        both = self.both_radio.isChecked()
        flange = self.flange_radio.isChecked()
        half_hole = self.half_hole_radio.isChecked()
        hole = self.hole_radio.isChecked()
        hole_diameter = self.hole_spin.value()
        knob_diameter = self.knob_diameter_spin.value()
        knob_shape = self.shape_combo.currentText()
        knob_head_height = self.height_spin.value()
        knurl_count = self.knurl_count_spin.value()
        knurl_shape = self.knurl_shape_combo.currentText()
        nut = self.nut_radio.isChecked()
        nut_type = self.nut_type_combo.currentText()
        shank = self.shank_radio.isChecked()
        shank_diameter = self.shank_diameter_spin.value()
        shank_length = self.shank_length_spin.value()
        flange_height = knob_head_height * 0.25

        self.spreadsheet = App.ActiveDocument.addObject('Spreadsheet::Sheet', 'Sheet')
        knob_head = self.make_knob_head(knob_shape, knob_diameter/2, knob_head_height)
        #fillets = self.fillet_edges(knob_head, 3)
        #knob_head = fillets

        if knurl_count > 0:
            if knurl_shape == 'Round':
                knob_head =  self.make_round_knurls(knob_head, knurl_count, knob_head_height)
            elif knurl_shape == 'Triangular':
                knob_head =  self.make_triangle_knurls(knob_head, knurl_count, knob_head_height)
            elif knurl_shape == 'Hex':
                knob_head = self.make_hex_knurls(knob_head, knurl_count, knob_head_height)

        FreeCAD.ActiveDocument.recompute()
    
        doc.recompute

        if shank:
            shank = self.make_shank(shank_diameter, shank_length, knob_head_height)
            knob_head = self.fuse_parts(knob_head, shank)

        if flange:
            flange = self.make_flange(knob_diameter, flange_height)
            knob_head = self.fuse_parts(knob_head, flange)
            shank_length = flange_height

        if hole:
            knob_head = self.make_hole(knob_head, hole_diameter, knob_head_height, shank_length)

        if not flange and not shank:
            shank_length = None

        if  half_hole:
            knob_head = self.make_half_hole(knob_head, hole_diameter, knob_head_height, shank_length)

        if nut or both:
            if nut_type == 'Hex Nut':
                hex_nut =  self.make_hexnut(shank_length, hole_diameter)
                knob_head = self.cut_parts(knob_head, hex_nut, 'Hex-Nut-Cut')
            elif nut_type == 'T Nut':
                t_nut = self.make_tnut(shank_length, shank_diameter)
                knob_head = self.cut_parts(knob_head, t_nut, 'T-Nut-Cut')

        if bolt or both:
            if bolt_type == 'Hex Head':
                hex_bolt = self.make_hex_bolt(knob_head_height, hole_diameter)
                knob_head = self.cut_parts(knob_head, hex_bolt, 'Hex-Head-Cut')
            elif bolt_type == 'Carriage Bolt':
                carriage_bolt = self.make_carriage_bolt(knob_head_height, knob_diameter)
                knob_head = self.cut_parts(knob_head, carriage_bolt, 'Carriage-Bolt-Cut')

        FreeCAD.ActiveDocument.recompute()
        self.hide()
    
    Gui.SendMsgToActiveView("ViewFit")

    #def closeEvent(self, event):
     #   App.closeDocument("Knob")   

    def closeEvent(self, event):
        event.accept()
        self.hide() 


knob_generator = KnobGenerator()
knob_generator.show()




