# tetris.py

def create_block():
    """
    하나의 블록을 나타내는 간단한 구조를 반환합니다.
    여기서는 '[]' 문자를 사용하여 블록의 한 조각을 나타냅니다.
    """
    block_shape = [
        ["[]", "[]"],
        ["[]", "[]"]
    ]
    return block_shape

def print_block(block):
    """
    주어진 블록 모양을 터미널에 출력합니다.
    """
    for row in block:
        print("".join(row))

if __name__ == "__main__":
    print("블록 생성 및 출력:")
    my_block = create_block()
    print_block(my_block)
