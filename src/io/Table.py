from typing import List, Any

class Table:
    """Simple Table class untuk menampilkan tabel jadwal"""
    
    def __init__(self):
        self.headers: List[str] = []
        self.rows: List[List[Any]] = []
    
    def setHeaders(self, headers: List[str]) -> None:
        """Set header kolom tabel"""
        self.headers = headers
    
    def addRow(self, rowData: List[Any]) -> None:
        """Tambah baris ke tabel"""
        self.rows.append(rowData)
    
    def display(self) -> None:
        """Display tabel ke console"""
        print(self.render())
    
    def render(self) -> str:
        """Render tabel dengan format box drawing"""
        if not self.headers:
            return ""
        
        # Hitung lebar kolom
        colWidths = []
        for i, header in enumerate(self.headers):
            maxWidth = len(str(header))
            for row in self.rows:
                if i < len(row):
                    maxWidth = max(maxWidth, len(str(row[i])))
            colWidths.append(min(maxWidth, 15))  # Max 15 chars per column
        
        result = ""
        
        # Top border
        result += "┌" + "┬".join("─" * width for width in colWidths) + "┐\n"
        
        # Headers
        headerRow = "│"
        for i, header in enumerate(self.headers):
            headerRow += str(header)[:colWidths[i]].center(colWidths[i]) + "│"
        result += headerRow + "\n"
        
        # Header separator
        result += "├" + "┼".join("─" * width for width in colWidths) + "┤\n"
        
        # Data rows
        for row in self.rows:
            dataRow = "│"
            for i in range(len(self.headers)):
                cellData = str(row[i]) if i < len(row) else ""
                dataRow += cellData[:colWidths[i]].ljust(colWidths[i]) + "│"
            result += dataRow + "\n"
        
        # Bottom border
        result += "└" + "┴".join("─" * width for width in colWidths) + "┘\n"
        
        return result