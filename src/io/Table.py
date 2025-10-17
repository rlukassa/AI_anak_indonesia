from typing import List, Any

class Table:    
	def __init__(self):
		"""Initialize table with empty headers and rows."""
		self.headers: List[str] = []
		self.rows: List[List[Any]] = []
	
	def setHeaders(self, headers: List[str]) -> None:
		"""Set table header columns."""
		self.headers = headers
	
	def addRow(self, rowData: List[Any]) -> None:
		"""Append a new row to the table."""
		self.rows.append(rowData)
	
	def display(self) -> None:
		"""Print the formatted table to console."""
		print(self.render())
	
	def render(self) -> str:
		"""Build and return a formatted ASCII table as string."""
		if not self.headers:
			return ""
		
		colWidths = []
		for i, header in enumerate(self.headers):
			maxWidth = len(str(header))
			for row in self.rows:
				if i < len(row):
					maxWidth = max(maxWidth, len(str(row[i])))
			colWidths.append(min(maxWidth + 2, 20))

		result = ""
		result += "+" + "+".join("-" * width for width in colWidths) + "+\n"
		
		headerRow = "|"
		for i, header in enumerate(self.headers):
			headerRow += str(header)[:colWidths[i]-2].center(colWidths[i]) + "|"
		result += headerRow + "\n"
		
		result += "+" + "+".join("=" * width for width in colWidths) + "+\n"
		
		for row in self.rows:
			dataRow = "|"
			for i in range(len(self.headers)):
				cellData = str(row[i]) if i < len(row) else ""
				paddedData = " " + cellData[:colWidths[i]-2].ljust(colWidths[i]-2) + " "
				dataRow += paddedData + "|"
			result += dataRow + "\n"
		
		result += "+" + "+".join("-" * width for width in colWidths) + "+\n"
		
		return result
