from typing import Dict, Any, List

class Info:    
    def __init__(self):
        self.infos: Dict[str, Any] = {}
        self.sections: List[tuple] = []
    
    def addInfo(self, key: str, value: Any) -> None:
        self.infos[key] = value # tambah info , pake dict
         # contoh : self.infos["Akurasi"] = 95.5
    
    def addSection(self, title: str, content: str) -> None:
        self.sections.append((title, content)) # tambah section, pake list of tuple
        # contoh : self.sections.append(("Analisis Jadwal", "Total Mata Kuliah: 50\nTotal Ruangan: 10"))
    
    def display(self) -> None:
        print(self.render())
    
    def render(self) -> str:
        if not self.infos and not self.sections:
            return ""
        
        result = ""
        
        # Render info key-value jika ada
        if self.infos:
            # Hitung lebar kotak berdasarkan content
            maxKeyLength = max(len(str(key)) for key in self.infos.keys()) if self.infos else 0
            maxValueLength = max(len(str(value)) for value in self.infos.values()) if self.infos else 0
            totalWidth = maxKeyLength + maxValueLength + 7  # " : " + padding
            totalWidth = min(max(totalWidth, 40), 80)  # Min 40, max 80 chars
            
            # Header box dengan karakter ASCII
            result += "+" + "=" * totalWidth + "+\n"
            result += "|" + " INFORMASI OPTIMASI ".center(totalWidth) + "|\n"
            result += "+" + "=" * totalWidth + "+\n\n"
            
            # Content box dengan karakter ASCII
            result += "+" + "-" * totalWidth + "+\n"
            result += "|" + " PARAMETER & HASIL ".center(totalWidth) + "|\n"
            result += "+" + "-" * totalWidth + "+\n"
            
            for key, value in self.infos.items():
                keyStr = str(key)[:maxKeyLength].ljust(maxKeyLength)
                valueStr = str(value)[:maxValueLength].rjust(maxValueLength)
                result += f"|  {keyStr} : {valueStr}  |\n"
            
            result += "+" + "-" * totalWidth + "+\n\n"
        
        # Render sections jika ada
        for title, content in self.sections:
            lines = content.split('\n')
            maxContentLength = max(len(line) for line in lines) if lines else 0
            boxWidth = max(40, len(title) + 4, maxContentLength + 4)
            boxWidth = min(boxWidth, 80)
            
            # Header dengan karakter ASCII
            result += "+" + "=" * boxWidth + "+\n"
            result += "|" + " DETAIL INFORMASI ".center(boxWidth) + "|\n"
            result += "+" + "=" * boxWidth + "+\n\n"
            
            # Content dengan karakter ASCII
            result += "+" + "-" * boxWidth + "+\n"
            result += "|" + f" {title} ".center(boxWidth) + "|\n"
            result += "+" + "-" * boxWidth + "+\n"
            
            for line in lines:
                paddedLine = f" {line} ".ljust(boxWidth)
                result += f"|{paddedLine}|\n"
            
            result += "+" + "-" * boxWidth + "+\n\n"
        
        return result