import sys

from JackTokenizer import JackTokenizer
from TokenToXML import generate_xml

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
        
        

if __name__ == "__main__":
    main()