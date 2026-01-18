import csv
import os

# Ensure these paths are correct relative to where you run the script
CSV_FILES = [
    'Vision/empty_test.csv', 
    'Vision/occupied_test.csv'
]

def generate_js_config():
    js_output = "const SYSTEM_CONFIG = {\n"
    spot_count = 1
    
    # Base GPS (San Francisco generic location)
    base_lat = 37.7706
    base_lng = -122.4678
    
    for filename in CSV_FILES:
        if not os.path.exists(filename):
            print(f"⚠️ Warning: Could not find {filename}")
            continue
            
        print(f"Reading {filename}...")
        
        with open(filename, 'r') as f:
            reader = list(csv.reader(f))
            
            # Iterate in steps of 2 because your format uses 2 rows per spot
            for i in range(0, len(reader), 2):
                # Ensure we have a pair of rows
                if i + 1 >= len(reader):
                    break
                    
                row1 = reader[i]
                row2 = reader[i+1]
                
                # Basic validation
                if not row1 or not row2:
                    continue

                try:
                    # Parse coordinates
                    p1 = list(map(int, row1))
                    p2 = list(map(int, row2))
                    
                    x1, y1 = p1[0] * 2, p1[1] * 2
                    x2, y2 = p2[0] * 2, p2[1] * 2
                    
                    # Normalize box (x1 must be smaller than x2)
                    coords = [
                        min(x1, x2), 
                        min(y1, y2), 
                        max(x1, x2), 
                        max(y1, y2)
                    ]
                    
                    spot_id = f"spot_{spot_count}"
                    
                    # Generate Mock GPS logic
                    lat_offset = (spot_count * 0.00005) 
                    lng_offset = 0
                    if spot_count % 2 == 0:
                        lng_offset = (spot_count * 0.00005)

                    js_output += f"    {spot_id}: {{\n"
                    js_output += f"        coords: {coords},\n"
                    js_output += f"        lat: {base_lat + lat_offset:.6f}, lng: {base_lng + lng_offset:.6f},\n"
                    js_output += f"        name: 'Spot {spot_count}'\n"
                    js_output += "    },\n"
                    
                    spot_count += 1
                    
                except ValueError:
                    continue # Skip rows that aren't integers

    js_output += "};"
    
    print("\n✅ COPY THE CODE BELOW INTO frontend/src/CameraConsole.js:\n")
    print(js_output)

if __name__ == "__main__":
    generate_js_config()