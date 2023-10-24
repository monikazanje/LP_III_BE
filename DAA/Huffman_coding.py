class Nodes:
    def __init__(self, probability, symbol, left=None, right=None):
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''

def CalculateProbability(the_data):
    the_symbols = dict()
    for item in the_data:
        if the_symbols.get(item) is None:
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols  # Return the dictionary of symbol frequencies

def CalculateCodes(node, value=''):
    newValue = value + str(node.code)
    the_codes = {}  # Define the_codes dictionary
    if node.left:
        the_codes.update(CalculateCodes(node.left, newValue))
    if node.right:
        the_codes.update(CalculateCodes(node.right, newValue))
    if not node.left and not node.right:
        the_codes[node.symbol] = newValue
    return the_codes

def OutputEncoded(the_data, coding):
    encodingOutput = []
    for element in the_data:
        encodingOutput.append(coding[element])
    the_string = ''.join([str(item) for item in encodingOutput])
    return the_string

def TotalGain(the_data, coding):
    beforeCompression = len(the_data) * 8
    afterCompression = 0
    the_symbols = coding.keys()
    for symbol in the_symbols:
        the_count = the_data.count(symbol)
        afterCompression += the_count * len(coding[symbol])
    print("Space usage before compression (in bits):", beforeCompression)
    print("Space usage after compression (in bits):", afterCompression)
    return beforeCompression, afterCompression  # Return space usage values

def HuffmanEncoding(the_data):
    symbolWithProbs = CalculateProbability(the_data)
    the_symbols = list(symbolWithProbs.keys())  # Convert keys to a list
    the_nodes = [Nodes(symbolWithProbs[symbol], symbol) for symbol in the_symbols]

    while len(the_nodes) > 1:
        the_nodes = sorted(the_nodes, key=lambda x: x.probability)
        right = the_nodes[0]
        left = the_nodes[1]
        left.code = 0
        right.code = 1

        newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

        the_nodes.remove(left)
        the_nodes.remove(right)
        the_nodes.append(newNode)

    huffmanEncoding = CalculateCodes(the_nodes[0])
    print("symbols with codes", huffmanEncoding)
    beforeCompression, afterCompression = TotalGain(the_data, huffmanEncoding)
    encodedOutput = OutputEncoded(the_data, huffmanEncoding)
    return encodedOutput, the_nodes[0]

def HuffmanDecoding(encodedData, huffmanTree):
    treeHead = huffmanTree
    decodedOutput = []
    huffmanTree = treeHead  # Initialize huffmanTree

    for x in encodedData:
        if x == '1':
            huffmanTree = huffmanTree.right
        elif x == '0':
            huffmanTree = huffmanTree.left

        if not huffmanTree.left and not huffmanTree.right:  # Check if it's a leaf node
            decodedOutput.append(huffmanTree.symbol)
            huffmanTree = treeHead  # Reset huffmanTree

    the_string = ''.join([str(item) for item in decodedOutput])
    return the_string

the_data = input("Enter the String: ")
print(the_data)
encoding, the_tree = HuffmanEncoding(the_data)
print("Encoded output:", encoding)
decoded_output = HuffmanDecoding(encoding, the_tree)
print("Decoded Output:", decoded_output)
