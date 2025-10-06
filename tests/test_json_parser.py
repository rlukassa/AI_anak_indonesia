from src.io.json_parser import JSONParser

def main():
    path = "data/sample_input.json"
    parser = JSONParser(path)
    
    print("Top-level keys in JSON:")
    print(list(parser.data.keys()))
    
    for section_key in ["kelas_mata_kuliah", "ruangan", "mahasiswa"]:
        try:
            section = parser.parse_section(section_key)
            print(f"\nSection '{section_key}':")
            for i, item in enumerate(section[:]):
                print(f"  {i+1}. {item}")
        except ValueError as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
