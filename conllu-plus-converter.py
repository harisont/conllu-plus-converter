from conllu import *

std_fields = ["id", 
              "form", 
              "lemma", 
              "upos", 
              "xpos", 
              "feats", 
              "head", 
              "deprel", 
              "deps", 
              "misc"]

def from_plus_file(path):
    """
    Given the path to a CoNLL-U Plus file, return the corresponding plain 
    CoNLL-U string.
    """
    with open(path) as f:
        plus_fields = parse_conllu_plus_fields(f)
        plus_content = f.read()
        plus_sentences = parse(plus_content, plus_fields)

    def from_plus_sentence(plus_sent):
        sent = TokenList()

        def from_plus_token(plus_tok):
            tok = {}
            for field in std_fields:
                if field in plus_fields:
                    tok[field] = plus_tok[field]
            for field in set(plus_fields) - set(std_fields):
                plus_key = field.upper()
                plus_val = plus_tok[field]
                if "misc" in tok:
                    tok["misc"] += ("|{}={}".format(plus_key, plus_val))
                else:
                    tok["misc"] = ("{}={}".format(plus_key, plus_val))
            return tok
        
        for plus_tok in plus_sent:
            sent.append(from_plus_token(plus_tok))
        return sent

    sentences = list(map(from_plus_sentence, plus_sentences))
    return "\n".join([sentence.serialize() for sentence in sentences])

        
        

def to_plus_file(conllu_file):
    pass

if __name__ == "__main__":
    print(from_plus_file("test/test.conllup"))
