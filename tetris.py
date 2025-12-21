# tetris.py

# tetris.py

TETROMINOS = {
    'I': [['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  ']],
    'O': [['[]', '[]'],
          ['[]', '[]']],
    'T': [['  ', '[]', '  '],
          ['[]', '[]', '[]'],
          ['  ', '  ', '  ']],
    'J': [['  ', '[]', '  '],
          ['  ', '[]', '  '],
          ['[]', '[]', '  ']],
    'L': [['  ', '[]', '  '],
          ['  ', '[]', '  '],
          ['  ', '[]', '[]']],
    'S': [['  ', '[]', '[]'],
          ['[]', '[]', '  '],
          ['  ', '  ', '  ']],
    'Z': [['[]', '[]', '  '],
          ['  ', '[]', '[]'],
          ['  ', '  ', '  ']]
}

def rotate_clockwise(block):
    """
    주어진 블록을 시계 방향으로 90도 회전합니다.
    """
    return [list(row[::-1]) for row in zip(*block)]


def print_block(block):
    """
    주어진 블록 모양을 터미널에 출력합니다.
    """
    for row in block:
        print("".join(row))

if __name__ == "__main__":
    print("테트리스 블록 7종 및 회전 모습 출력:")
    for name, shape in TETROMINOS.items():
        print(f"\n--- {name} 블록 ---")
        
        rotations = [shape]
        current_shape = shape
        for _ in range(3):
            current_shape = rotate_clockwise(current_shape)
            rotations.append(current_shape)

        # 모든 회전 형태를 일관된 디스플레이를 위해 최대 높이를 결정합니다.
        max_height = max(len(r) for r in rotations if r)
        
        # 출력을 위해 모든 회전 형태를 단일 디스플레이 블록으로 결합합니다.
        display_grid = []
        for i in range(max_height):
            combined_row = []
            for j, rot_shape in enumerate(rotations):
                shape_height = len(rot_shape)
                shape_width = len(rot_shape[0]) if shape_height > 0 else 0

                if i < shape_height:
                    combined_row.extend(rot_shape[i])
                else:
                    # 짧은 모양은 빈 공간으로 채웁니다.
                    combined_row.extend(['  '] * shape_width)

                # 모양 사이에 구분자를 추가합니다.
                if j < len(rotations) - 1:
                    combined_row.extend([' | '])
            
            display_grid.append(combined_row)
        
        print_block(display_grid)
