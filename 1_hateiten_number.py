import csv
import os
from collections import Counter

def get_most_flooded_break_points(input_folder):
    all_break_points = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, mode='r', encoding='shift-jis') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    break_point_id = row[0]
                    csv_scale = int(row[6])
                    if csv_scale == 0:
                        try:
                            latitude = float(row[3])  # 緯度
                            longitude = float(row[4])  # 経度
                            all_break_points.append((break_point_id, latitude, longitude))
                        except ValueError:
                            print(f"Warning: Skipping invalid latitude/longitude in file {file_path}")
    top_10_break_points = Counter(all_break_points).most_common(10)
    return top_10_break_points

def output_filename_list(output_folder):
    filename_list = os.listdir(output_folder)
    with open(os.path.join(output_folder, 'output_file_list.txt'), 'w', encoding='utf-8') as f:
        for filename in filename_list:
            f.write(f"{filename}\n")

def main():
    input_folder = 'output/破堤点一覧'
    output_folder = 'output/最も浸水する箇所が多い破堤点'
    os.makedirs(output_folder, exist_ok=True)

    top_10_break_points = get_most_flooded_break_points(input_folder)

    for i, ((break_point_id, latitude, longitude), count) in enumerate(top_10_break_points, start=1):
        output_file_path = os.path.join(output_folder, f'top_{i}_break_points.csv')
        with open(output_file_path, mode='w', newline='', encoding='shift-jis') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['建物名', '破堤点ID', '出現回数', '緯度', '経度'])
            # フォルダ内のすべてのCSVファイルを処理して、該当する破堤点IDがあるか確認し、あれば建物名とともに書き込む
            for filename in os.listdir(input_folder):
                if filename.endswith('.csv'):
                    file_path = os.path.join(input_folder, filename)
                    with open(file_path, mode='r', encoding='shift-jis') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)  # Skip header
                        for row in reader:
                            if row[0] == break_point_id:
                                writer.writerow([filename[:-4], break_point_id, count, latitude, longitude])
                                break  # 同じ破堤点IDがあれば一度だけ出力する

    # 出力したファイル名のリストをテキストファイルとして出力
    output_filename_list(output_folder)

if __name__ == "__main__":
    main()
