import requests
import csv
import json
import os

def get_coordinates_from_csv(file_path):
    coordinates = []
    with open(file_path, mode='r', encoding='shift-jis') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            coordinates.append((row[0], row[2], row[1]))  # 建物名、経度、緯度の順でタプルとして保存
    return coordinates

def get_break_points(lon, lat):
    url = f'https://suiboumap.gsi.go.jp/shinsuimap/Api/Public/GetBreakPoint?lon={lon}&lat={lat}'
    response = requests.get(url)
    return response.json()

def main():
    input_csv_path = 'input/address.csv'
    output_folder = 'output/破堤点一覧'

    # 出力フォルダが存在しない場合は作成する
    os.makedirs(output_folder, exist_ok=True)

    coordinates = get_coordinates_from_csv(input_csv_path)
    
    for building_name, lon, lat in coordinates:
        data = get_break_points(lon, lat)
        output_csv_path = os.path.join(output_folder, f'{building_name}.csv')
        
        with open(output_csv_path, mode='w', newline='', encoding='shift-jis') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["ID", "BPName", "BPLocation", "BPLat", "BPLon", "WSID", "CSVScale", "EntryRiverName", "RiverCode", "SubRiverCode", "OfficeCode", "BPTime", "isDepthMax", "isStartMax", "isDurationMax"])
            writer.writeheader()
            
            for bp_data in data:
                writer.writerow(bp_data)
                
if __name__ == "__main__":
    main()
