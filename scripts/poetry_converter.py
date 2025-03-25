#!/usr/bin/env python3
import json
import yaml
import os
import random
import re
from pathlib import Path


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_content(text):
    """清理诗词内容"""
    # 移除注释
    text = re.sub(r'[（\(].*?[）\)]', '', text)
    # 移除空行和过短的行
    lines = [line.strip() for line in text.split(
        '\n') if line.strip() and len(line.strip()) > 1]
    return '\n'.join(lines)


def convert_poem(poem, dynasty):
    """将JSON格式的诗词转换为YAML格式"""
    content = ''

    # 处理宋词格式
    if 'rhythmic' in poem:
        content = clean_content('\n'.join(poem.get('paragraphs', [])))
        if not content:  # 如果内容为空，跳过
            return None
        return {
            'title': poem.get('rhythmic', '无题'),
            'author': poem.get('author', '佚名'),
            'dynasty': dynasty,
            'content': content
        }
    # 处理诗经和楚辞格式
    elif 'content' in poem and isinstance(poem['content'], list):
        content = clean_content('\n'.join(poem['content']))
        if not content:  # 如果内容为空，跳过
            return None
        return {
            'title': poem.get('title', '无题'),
            'author': poem.get('author', '佚名'),
            'dynasty': dynasty,
            'content': content
        }
    # 处理唐诗格式
    else:
        content = clean_content('\n'.join(poem.get('paragraphs', [])))
        if not content:  # 如果内容为空，跳过
            return None
        return {
            'title': poem.get('title', '无题'),
            'author': poem.get('author', '佚名'),
            'dynasty': dynasty,
            'content': content
        }


def process_poetry_files(base_dir, output_file, total_poems=10000):
    """处理诗词文件并生成YAML输出"""
    all_poems = []

    # 调整分配策略
    # 唐诗 50%, 宋词 40%, 元曲 8%, 诗经 1.5%, 楚辞 0.5%
    distribution = {
        '唐': int(total_poems * 0.50),
        '宋': int(total_poems * 0.40),
        '元': int(total_poems * 0.08),
        '先秦诗经': int(total_poems * 0.015),
        '先秦楚辞': int(total_poems * 0.005)
    }

    # 处理唐诗
    tang_dir = os.path.join(base_dir, '全唐诗')
    if os.path.exists(tang_dir):
        tang_files = [f for f in os.listdir(tang_dir) if f.startswith(
            'poet.tang.') and f.endswith('.json')]
        tang_poems = []

        print('正在处理唐诗...')
        for file in tang_files:
            try:
                poems = load_json_file(os.path.join(tang_dir, file))
                converted = [p for p in (convert_poem(poem, '唐')
                                         for poem in poems) if p is not None]
                tang_poems.extend(converted)
            except Exception as e:
                print(f'处理文件 {file} 时出错: {e}')

        print(f'共找到 {len(tang_poems)} 首唐诗')
        selected_tang = random.sample(
            tang_poems, min(distribution['唐'], len(tang_poems)))
        all_poems.extend(selected_tang)

    # 处理宋词
    ci_dir = os.path.join(base_dir, '宋词')
    if os.path.exists(ci_dir):
        ci_files = [f for f in os.listdir(ci_dir) if f.endswith('.json')]
        song_poems = []

        print('正在处理宋词...')
        for file in ci_files:
            try:
                poems = load_json_file(os.path.join(ci_dir, file))
                converted = [p for p in (convert_poem(poem, '宋')
                                         for poem in poems) if p is not None]
                song_poems.extend(converted)
            except Exception as e:
                print(f'处理文件 {file} 时出错: {e}')

        print(f'共找到 {len(song_poems)} 首宋词')
        selected_song = random.sample(
            song_poems, min(distribution['宋'], len(song_poems)))
        all_poems.extend(selected_song)

    # 处理诗经
    shijing_file = os.path.join(base_dir, '诗经/shijing.json')
    if os.path.exists(shijing_file):
        print('正在处理诗经...')
        try:
            poems = load_json_file(shijing_file)
            shijing_poems = []
            for p in poems:
                p['author'] = '佚名'  # 诗经作者多为佚名
                converted = convert_poem(p, '先秦')
                if converted:
                    shijing_poems.append(converted)

            print(f'共找到 {len(shijing_poems)} 首诗经')
            selected_shijing = random.sample(shijing_poems, min(
                distribution['先秦诗经'], len(shijing_poems)))
            all_poems.extend(selected_shijing)
        except Exception as e:
            print(f'处理诗经时出错: {e}')

    # 处理楚辞
    chuci_file = os.path.join(base_dir, '楚辞/chuci.json')
    if os.path.exists(chuci_file):
        print('正在处理楚辞...')
        try:
            poems = load_json_file(chuci_file)
            chuci_poems = []
            for p in poems:
                converted = convert_poem(p, '先秦')
                if converted:
                    chuci_poems.append(converted)

            print(f'共找到 {len(chuci_poems)} 首楚辞')
            selected_chuci = random.sample(chuci_poems, min(
                distribution['先秦楚辞'], len(chuci_poems)))
            all_poems.extend(selected_chuci)
        except Exception as e:
            print(f'处理楚辞时出错: {e}')

    # 处理元曲
    yuan_dir = os.path.join(base_dir, '元曲')
    if os.path.exists(yuan_dir):
        print('正在处理元曲...')
        yuan_poems = []
        for file in os.listdir(yuan_dir):
            if file.endswith('.json'):
                try:
                    poems = load_json_file(os.path.join(yuan_dir, file))
                    converted = [p for p in (convert_poem(
                        poem, '元') for poem in poems) if p is not None]
                    yuan_poems.extend(converted)
                except Exception as e:
                    print(f'处理文件 {file} 时出错: {e}')

        print(f'共找到 {len(yuan_poems)} 首元曲')
        selected_yuan = random.sample(
            yuan_poems, min(distribution['元'], len(yuan_poems)))
        all_poems.extend(selected_yuan)

    print(f'共选择 {len(all_poems)} 首诗词')

    # 随机打乱顺序
    random.shuffle(all_poems)

    # 写入YAML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(all_poems, f, allow_unicode=True, sort_keys=False)


def main():
    # 设置路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    base_dir = os.path.join(os.path.dirname(workspace_dir), 'chinese-poetry')
    output_dir = os.path.join(workspace_dir, '_data')

    print(f'数据库路径: {base_dir}')
    print(f'输出目录: {output_dir}')

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 生成诗词数据
    output_file = os.path.join(output_dir, 'poems.yml')
    process_poetry_files(base_dir, output_file, total_poems=10000)

    print(f'已生成诗词数据：{output_file}')


if __name__ == '__main__':
    main()
