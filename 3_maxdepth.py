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

def get_break_point_id_from_csv(file_path):
    ids = []
    with open(file_path, mode='r', encoding='shift-jis') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            ids.append(row[1])  # 破堤点IDを保存
    return ids

def get_max_depth(lon, lat, bpid):
    url = f'https://suiboumap.gsi.go.jp/shinsuimap/Api/Public/GetMaxDepth?lon={lon}&lat={lat}&bpid={bpid}'
    response = requests.get(url)
    return response.json()

def main():
    input_csv_path = 'input/address.csv'
    bpid_csv_path = 'output/最大浸水深破堤点/maxpoint_data.csv'
    output_csv_path = 'output/最大包絡浸水深/max_depth_data.csv'

    coordinates = get_coordinates_from_csv(input_csv_path)
    bpid_list = get_break_point_id_from_csv(bpid_csv_path)
    
    with open(output_csv_path, mode='w', newline='', encoding='shift-jis') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["BuildingName", "Depth", "OfficeCode", "RiverCode", "SubRiverCode", "CSVScale", "GroupType"])
        writer.writeheader()
        
        for building_name, lon, lat in coordinates:
            found_data = False
            for bpid in bpid_list:
                data = get_max_depth(lon, lat, bpid)
                if data:  # データがある場合
                    data['BuildingName'] = building_name
                    writer.writerow(data)
                    found_data = True
                    break  # データがあったらループを抜ける
            if not found_data:  # データがなかった場合でも空の行を出力する
                empty_row = {"BuildingName": building_name, "Depth": "", "OfficeCode": "", "RiverCode": "", "SubRiverCode": "", "CSVScale": "", "GroupType": ""}
                writer.writerow(empty_row)
                print(f"No data found for coordinates: ({lon}, {lat})")

if __name__ == "__main__":
    main()
