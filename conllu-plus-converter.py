from conllu import *

std_fields = ["ID", 
              "FORM", 
              "LEMMA", 
              "UPOS", 
              "XPOS", 
              "FEATS", 
              "HEAD", 
              "DEPREL", 
              "DEPS", 
              "MISC"]

def from_plus(path):
    """
    Given the path to a CoNLL-U Plus file, return the corresponding plain 
    CoNLL-U string.
    """
    with open(path) as f:
        plus_fields = [field.upper() for field in parse_conllu_plus_fields(f)]
        plus_content = f.read()
        plus_sentences = parse(plus_content, plus_fields)

    def from_plus_sentence(plus_sent):
        sent = TokenList()

        def from_plus_token(plus_tok):
            tok = {}
            for field in std_fields:
                if field in plus_fields:
                    tok[field] = plus_tok[field]
                else:
                    tok[field] = "_"
            for field in set(plus_fields) - set(std_fields):
                plus_key = field
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
    return "\n".join([sent.serialize() for sent in sentences])
        

def to_plus(path, plus_fields):
    with open(path) as f:
        sentences = parse(f.read())
        plus_fields = [field.upper() for field in plus_fields]

        def to_plus_sentence(sent):
            plus_sent = TokenList()

            def to_plus_token(tok):
                plus_tok = {}
                for field in plus_fields:
                    if field == "misc":
                        # dunno if this actually works, need to test
                        plus_tok[field] = dict(filter(lambda p: p[0] not in plus_fields, list(tok["misc"].items())))
                    elif field in std_fields:
                        # according to this damn library, field names are lowercase, but key names are uppercase
                        plus_tok[field] = tok[field.lower()]
                    else:
                        # because Key=val pairs are parsed as dictionaries
                        plus_tok[field] = tok["misc"][field]
                return plus_tok

            for tok in sent:
                plus_sent.append(to_plus_token(tok))
            return plus_sent

        plus_sentences = list(map(to_plus_sentence, sentences))
        cols = "# global.columns = " + " ".join([field.upper() for field in plus_fields])
        return "\n".join([cols] + [sent.serialize() for sent in plus_sentences])
    

if __name__ == "__main__":
    print(from_plus("test/test.conllup"))
    print(to_plus("test/test.conllu", ["ID", "FORM", "A", "D", "R", "TID"]))
