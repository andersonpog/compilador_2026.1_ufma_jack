import sys
from JackTokenizer import JackTokenizer

def generate_xml(filename):
    # Inicializa o seu Tokenizer
    tokenizer = JackTokenizer(filename)
    
    # Mapeamento para as tags XML oficiais do curso
    TAG_MAP = {
        'KEYWORD': 'keyword',
        'SYMBOL': 'symbol',
        'INT_CONST': 'integerConstant',
        'STR_CONST': 'stringConstant',
        'IDENTIFIER': 'identifier'
    }

    # Caracteres que o XML não aceita diretamente
    XML_ESCAPE = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;'
    }

    output_filename = filename + "T.xml"
    
    with open(output_filename, 'w') as xml_file:
        xml_file.write("<tokens>\n")
        
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            
            kind = tokenizer.current_type
            value = tokenizer.current_value
            
            # Aplica o escape de XML se for um símbolo
            if kind == 'SYMBOL':
                value = XML_ESCAPE.get(value, value)
            
            tag = TAG_MAP[kind]
            xml_file.write(f"<{tag}> {value} </tag>\n")
            
        xml_file.write("</tokens>\n")
    
    print(f"Sucesso! Arquivo {output_filename} gerado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python jack_analyzer.py NomeDoArquivo (sem .jack)")
    else:
        generate_xml(sys.argv[1])