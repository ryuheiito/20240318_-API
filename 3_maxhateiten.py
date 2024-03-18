import requests
import csv
import json

def get_coordinates_from_csv(file_path):
    coordinates = []
    with open(file_path, mode='r', encoding='shift-jis') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            coordinates.append((row[0], row[2], row[1]))  # 建物名、経度、緯度の順でタプルとして保存
    return coordinates

def get_break_point_max_depth(lon, lat):
    url = f'https://suiboumap.gsi.go.jp/shinsuimap/Api/Public/GetBreakPointMaxDepth?lon={lon}&lat={lat}'
    response = requests.get(url)
    return response.json()

def main():
    input_csv_path = 'input/address.csv'
    output_csv_path = 'output/maxpoint_data.csv'

    coordinates = get_coordinates_from_csv(input_csv_path)
    
    with open(output_csv_path, mode='w', newline='', encoding='shift-jis') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["BuildingName", "ID", "BPName", "BPLocation", "BPLat", "BPLon", "WSID", "EntryRiverName", "RiverCode", "SubRiverCode", "OfficeCode", "CSVScale", "BPTime"])
        writer.writeheader()
        
        for building_name, lon, lat in coordinates:
            data = get_break_point_max_depth(lon, lat)
            if data:  # データがある場合
                data['BuildingName'] = building_name
                writer.writerow(data)
            else:  # データがない場合でも空行を出力する
                empty_row = {"BuildingName": building_name}
                writer.writerow(empty_row)
                print(f"No data found for coordinates: ({lon}, {lat})")

if __name__ == "__main__":
    main()
