import sys

from JackTokenizer import JackTokenizer
from TokenToXML import generate_xml
from parser import Parser

def main():
    args = sys.argv

    if(args.__len__() < 2):
        print("Digite o nome do arquivo jack sem a extensão.")
        sys.exit(1)
    
    print("Realizando análise léxica do arquivo " + args[1] + ".jack")

    # Testando apenas tokens
    tokenizer = JackTokenizer(args[1])
    tokenizer.getTokens()

    # Testando token e xml
    generate_xml(args[1])

    parser = Parser(tokenizer.tokens)
    parser.parse_class()

    output_filename = f"{args[1]}.xml"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(parser.get_xml())

    print("Sucesso! Arquivo " + args[1] + ".xml gerado.")
        
        

if __name__ == "__main__":
    main()