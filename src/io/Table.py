from typing import List, Any

class Table:    
    def __init__(self): # constructor
        self.headers: List[str] = []
        self.rows: List[List[Any]] = []
    
    def setHeaders(self, headers: List[str]) -> None: # bikin header
        self.headers = headers
    
    def addRow(self, rowData: List[Any]) -> None: #tambah baris
        self.rows.append(rowData)
    
    def display(self) -> None: # dari fungsi render dibawah diprintkan
        print(self.render())
    
    def render(self) -> str: # ini crit sectionnya, fungsi bikin tabelnya 
        if not self.headers:
            return ""
        
        # Hitung lebar kolom dengan padding
        colWidths = []
        for i, header in enumerate(self.headers):
            maxWidth = len(str(header))
            for row in self.rows:
                if i < len(row):
                    maxWidth = max(maxWidth, len(str(row[i])))
            colWidths.append(min(maxWidth + 2, 20))  # Max 20 chars per column with padding
        
        result = ""
        
        # Top border menggunakan ASCII
        result += "+" + "+".join("-" * width for width in colWidths) + "+\n"
        
        # Headers
        headerRow = "|"
        for i, header in enumerate(self.headers):
            headerRow += str(header)[:colWidths[i]-2].center(colWidths[i]) + "|"
        result += headerRow + "\n"
        
        # Header separator
        result += "+" + "+".join("=" * width for width in colWidths) + "+\n"
        
        # Data rows
        for row in self.rows:
            dataRow = "|"
            for i in range(len(self.headers)):
                cellData = str(row[i]) if i < len(row) else ""
                # Tambahkan padding space di kiri dan kanan
                paddedData = " " + cellData[:colWidths[i]-2].ljust(colWidths[i]-2) + " "
                dataRow += paddedData + "|"
            result += dataRow + "\n"
        
        # Bottom border
        result += "+" + "+".join("-" * width for width in colWidths) + "+\n"
        
        return result