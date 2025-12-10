import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.pdfmetrics import stringWidth
import textwrap
from reportlab.lib import colors
useThisColor = colors.black #HexColor(0xFF00FF)

# Createa a labels page, matching Avery 5160, 8160, 6240, etc.

PADDING = 1
specs = labels.Specification(
    # og: 215.9, 279.4, 3, 10, 64, 25.4, corner_radius=2,
    # left_margin=5, right_margin=5, top_margin=13,
    # left_padding=PADDING, right_padding=PADDING, top_padding=PADDING,
    # bottom_padding=PADDING,
    # row_gap=0)
    215.9, 279.4, 3, 10, 66, 25.4, corner_radius=2,
    left_margin=5, right_margin=5, top_margin=13,
    left_padding=PADDING, right_padding=PADDING, top_padding=PADDING,
    bottom_padding=PADDING,
    row_gap=0)



def draw_address(label, width, height, address):

    # how many chars to fit one line 1 before wrapping
    FIRSTLINE_CHARS = 35

    # The order is flipped, because we're painting from bottom to top.
    lines = [
        address['line3'], #Line 3
        address['line2'], #Line 2
        address['line1'] #Line 1
    ]

    group = shapes.Group()
    x, y = 0, 15   #ORIGINAL: 0, 0
    if len(lines[2]) > FIRSTLINE_CHARS:
        newlines = textwrap.fill(lines[2], width = 30)
        newlines = newlines.split('\n')
        print(newlines)
        lines[2] = newlines[1]
        lines.append(newlines[0])
        y = 5
    for line in lines:
        if not line:
            continue
        font_size = 12
        text_width = width - 10
        line_width = stringWidth(line, "Helvetica", font_size)
        while line_width > text_width:
            font_size -= 0.5
            line_width = stringWidth(line, "Helvetica", font_size)
        shape = shapes.String(width/2.0, y, line, fontName="Helvetica", fontSize=font_size, textAnchor="middle", fillColor=useThisColor) #ORIGINAL: x, y
        _, _, _, y = shape.getBounds()
        # Some extra spacing between the lines, to make it easier to read
        y += 3
        label.add(shape) #ORIGINAL: group.shape
    #ORIGINAL: uncomment everything below    
    # _, _, lx, ly = label.getBounds()
    # _, _, gx, gy = group.getBounds()

    # # Make sure the label fits in a sticker
    # assert gx <= lx, (address, gx, lx)
    # assert gy <= ly, (address, gy, ly)

    # # Move the content to the center of the sticker
    # dx = (lx - gx) / 2
    # dy = (ly - gy) / 2
    # group.translate(dx, dy)

    # label.add(group)

def generatePDF(address):
    sheet = labels.Sheet(specs, draw_address, border=False)

    # put sticker in correct spot by setting the former stickers as "used"
    if address['stickerpos'] > 1:
        blanks = []
        for i in range(0, address['stickerpos']-1):
            x = i%3+1
            y = i//3+1
            #print(f"i = {i}, x = {x}, y = {y}")
            blanks.append((y, x))
        tuple(blanks)
        sheet.partial_page(1, blanks)

    sheet.add_label(address)

    sheet.save('toBePrinted/label.pdf')
    print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))

def generatePDFdemo(address):
    sheet = labels.Sheet(specs, draw_address, border=False)

    # put sticker in correct spot by setting the former stickers as "used"
    if address['stickerpos'] > 1:
        blanks = []
        for i in range(0, address['stickerpos']-1):
            x = i%3+1
            y = i//3+1
            #print(f"i = {i}, x = {x}, y = {y}")
            if (y, x) not in [(1, 1), (1, 3), (10, 1)]:
                blanks.append((y, x))
        tuple(blanks)
        sheet.partial_page(1, blanks)

    sheet.add_label(address)
    sheet.add_label(address)
    sheet.add_label(address)
    sheet.add_label(address)

    sheet.save('toBePrinted/label.pdf')
    print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))

#demo
if __name__ == "__main__":
    addressSample = {
        'line1':'Lincoln Kuehne',
        'line2':'11797 Spruce Run Dr.,  Unit A',
        'line3':'San Diego, CA 92131',
        'stickerpos':30
    }
    generatePDFdemo(addressSample)
