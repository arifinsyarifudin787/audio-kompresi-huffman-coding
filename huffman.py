import heapq
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, left=None, right=None, char=None, freq=0):
        self.left = left
        self.right = right
        self.char = char
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(left=node1, right=node2, freq=node1.freq + node2.freq)
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix='', codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_encode(data):
    freq_map = Counter(data)
    huffman_tree = build_huffman_tree(freq_map)
    huffman_codes = build_codes(huffman_tree)

    encoded_data = ''.join(huffman_codes[char] for char in data)
    return encoded_data, huffman_codes

def huffman_decode(encoded_data, huffman_codes):
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    decoded_data = []
    code = ''
    for bit in encoded_data:
        code += bit
        if code in reverse_codes:
            decoded_data.append(reverse_codes[code])
            code = ''
    return ''.join(decoded_data)
