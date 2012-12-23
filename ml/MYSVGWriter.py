'''
Created on Sep 21, 2012

@author: masumadmin
'''
#define MARGIN_SIZE 50

class MYSVGWriter(object):
    MARGIN_SIZE = 50
    g_hex = "0123456789abcdef"
    m_ss = ""
    
    def __init__(self, width, height, xmin, ymin, xmax, ymax):
        self.m_unit = 1.0* (ymax - ymin) / height
#        self.m_unit = 1
        self.m_ss += "<?xml version=\"1.0\"?><svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\""
        self.m_ss += str(width + self.MARGIN_SIZE) + "\" height=\"" + str(height + self.MARGIN_SIZE) + "\">\n"
        self.m_ss += "<g transform=\"translate(" + str(self.MARGIN_SIZE) + " " + str(height) + ") scale("
        self.m_ss += str(width*1.0 / (xmax - xmin)) + " " + str(-height*1.0 / (ymax - ymin)) + ") translate(" + str(-xmin) + " " + str(-ymin) + ") \">\n"
        self.grid(20, xmin, ymin, xmax, ymax)
    
#
#
    def color(self, c):
    
        self.m_ss += '#' + self.g_hex[(c >> 20) & 0xf] + self.g_hex[(c >> 16) & 0xf]
        self.m_ss += self.g_hex[(c >> 12) & 0xf] + self.g_hex[(c >> 8) & 0xf]
        self.m_ss += self.g_hex[(c >> 4) & 0xf] + self.g_hex[c & 0xf]
#
#
    def grid(self, lines, xmin, ymin, xmax, ymax):    
        for i in range(lines):
            x = (xmax - xmin) * i / lines + xmin
            y = (ymax - ymin) * i / lines + ymin
            self.line(xmin, y, xmax, y, self.m_unit, 0xa0a0a0)
            self.text(xmin, y, str(y), self.m_unit, 0x000000)
            self.line(x, ymin, x, ymax, self.m_unit, 0xa0a0a0)
            self.text(x, ymin, str(x), self.m_unit, 0x000000, 90)
        
    
#
    def dot(self, x, y, r, col):    
        self.m_ss += "<circle cx=\"" + str(x) + "\" cy=\"" + str(y) + "\" r=\"" + str(r) + "\" fill=\""
        self.color(col)
        self.m_ss += "\" />\n"
    
#
    def line(self,  x1,  y1,  x2,  y2,  thickness, col):    
        self.m_ss += "<line x1=\"" + str(x1) + "\" y1=\"" + str(y1) + "\" x2=\"" + str(x2) + "\" y2=\"" + str(y2) + "\" style=\"stroke:"
        self.color(col)
        self.m_ss += ";stroke-width:" + str(thickness) + "\"/>\n"
    
#
    def rect(self,  x,  y,  w,  h,  col):    
        self.m_ss += "<rect x=\"" + str(x) + "\" y=\"" + str(y) + "\" width=\"" + str(w) + "\" height=\"" + str(h) + "\" style=\"fill:"
        self.color(col)
        self.m_ss += "\"/>\n"
    
#
    def text(self,  x,  y, szText,  size,  col= 0x000000,  angle= 0.0):    
        self.m_ss += "<text x=\"" + str(x) + "\" y=\"" + str(-y) + "\" style=\"font-size:" + str(size * 10) + "px;fill:"
        self.color(col)
        self.m_ss += ";font-family:Sans\" transform=\""
        if(angle != 0.0):
            self.m_ss += "rotate(" + str(angle) + " " + str(x) + " " + str(y) + ") "
        self.m_ss += "scale(1 -1)\" text-anchor=\"end\""
        self.m_ss += ">" + szText + "</text>\n"
    
#
    def unit(self):
        return self.m_unit
    
    def svgprint(self, path):
        self.m_ss += "</g></svg>\n"
        with open(path, 'w+') as f:
            f.write(self.m_ss)
        
#
#pw =  MYSVGWriter(500, 500, 0, 0, 100, 100)
##pw.line(20, 40, 50, 50, 1, 0x008000)
##pw.dot(20, 40, 1, 0x000080)
##pw.text(20, 40, "begin", pw.unit(), 0x000000)
##pw.dot(50, 50, 1, 0x000080)
##pw.text(50, 50, "end", pw.unit(), 0x000000)
#pw.rect(6, 0, 3, 27, 0x008080)
#pw.svgprint("myplot.svg");
#print 'done!'