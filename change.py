import csv
import re

# 原 CSV 文件名和输出文件名
input_file = 'neo4j_query_table_data.csv'
output_file = 'neo4j_query_table_data_fixed.csv'

# 利用正则，对像 "name: 金鲳鱼"、"label: 养殖方式" 这类没有引号的地方，加上单引号
# 示例中我们简单处理 "name:" 和 "label:" 两种情况；如果你还有别的键，也可以加。
def fix_fragment(fragment: str) -> str:
    if not fragment:
        return fragment
    
    # 给  name: XXX  的 XXX 加上引号
    fragment = re.sub(r"name:\s*([^,'}]+)", r"name: '\1'", fragment)
    # 给  label: XXX  的 XXX 加上引号
    fragment = re.sub(r"label:\s*([^,'}]+)", r"label: '\1'", fragment)

    return fragment

with open(input_file, 'r', encoding='utf-8') as fin, \
     open(output_file, 'w', encoding='utf-8', newline='') as fout:
    
    reader = csv.DictReader(fin)      # 假设第一行是表头 n,r,m
    fieldnames = reader.fieldnames    # ['n', 'r', 'm']
    
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()              # 写出表头
    
    for row in reader:
        row['n'] = fix_fragment(row['n'])
        row['r'] = fix_fragment(row['r'])
        row['m'] = fix_fragment(row['m'])
        writer.writerow(row)
