import csv
import requests

# input/address.csvを読み込む
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='shift-jis') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# output_file_list.txtからファイル名を読み取り、ファイルをループしてデータを取得
def read_top_break_points():
    file_list = []
    with open('output/最も浸水する箇所が多い破堤点/output_file_list.txt', 'r') as file:
        for line in file:
            file_list.append(line.strip())
    
    all_data = {}
    for filename in file_list:
        data = {}
        with open(f'output/最も浸水する箇所が多い破堤点/{filename}', 'r', encoding='shift-jis') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row['建物名']] = row['破堤点ID']
        all_data[filename] = data
    return all_data

# URLからjsonを取得する
def get_max_depth(lon, lat, bpid):
    url = f'https://suiboumap.gsi.go.jp/shinsuimap/Api/Public/GetMaxDepth?lon={lon}&lat={lat}&bpid={bpid}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    # input/address.csvを読み込む
    address_data = read_csv('input/address.csv')

    # output_file_list.txtからファイル名を読み取り、ファイルをループしてデータを取得
    top_break_points = read_top_break_points()

    # 各建物の緯度経度と破堤点IDを使用してAPIから情報を取得する
    for filename, break_points in top_break_points.items():
        results = []
        for building in address_data:
            building_name = building['建物名']
            lon = building['経度']
            lat = building['緯度']

            if building_name in break_points:
                bpid = break_points[building_name]
                response = get_max_depth(lon, lat, bpid)
                if response:
                    result = {
                        "建物名": building_name,
                        "破堤点ID": bpid,
                        "深さ": response['Depth']
                    }
                    results.append(result)
                else:
                    print(f"建物名: {building_name}, 破堤点ID: {bpid}, 情報が取得できませんでした")

        # 結果をファイルに保存する
        output_filename = f'output/最も浸水する箇所が多い破堤点(浸水深)_{filename}'
        with open(output_filename, 'w', newline='', encoding='shift-jis') as file:
            writer = csv.DictWriter(file, fieldnames=["建物名", "破堤点ID", "深さ"])
            writer.writeheader()
            writer.writerows(results)

if __name__ == "__main__":
    main()
