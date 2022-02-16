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
        sent.metadata = plus_sent.metadata

        # workaround for globals being treated as sentence metadata by conllu
        plus_sent.metadata.pop("global.columns", None)

        def from_plus_token(plus_tok):
            tok = {}
            for field in std_fields:
                if field in plus_fields:
                    tok[field] = plus_tok[field]
                else:
                    tok[field] = "_"
            for field in set(plus_fields) - set(std_fields):
                plus_key = field
                plus_val = plus_tok[field] if field in plus_tok else "_"
                if "MISC" in tok:
                    tok["MISC"] += ("|{}={}".format(plus_key, plus_val))
                else:
                    tok["MISC"] = ("{}={}".format(plus_key, plus_val))
            return tok
        
        for plus_tok in plus_sent:
            sent.append(from_plus_token(plus_tok))
        return sent

    sentences = list(map(from_plus_sentence, plus_sentences))
    return "".join([sent.serialize() for sent in sentences])
        

def to_plus(path, fields):
    with open(path) as f:
        sentences = parse(f.read())
        fields = [field.upper() for field in fields] # fields of conllu+ file
        plus_fields = set(fields) - set(std_fields) # nonstandard fields

        def to_plus_sentence(sent):
            plus_sent = TokenList()
            plus_sent.metadata = sent.metadata

            def to_plus_token(tok):
                plus_tok = {}
                for field in fields:
                    if field == "MISC":
                        # dunno if this actually works, need to test
                        plus_tok[field] = dict(filter(
                            lambda p: p[0] not in plus_fields, 
                            tok["misc"].items()
                            ))
                    elif field in std_fields:
                        # using the conllu library, field names are lowercase
                        # but key names in Key=val pairs are uppercase (damn!)
                        plus_tok[field] = tok[field.lower()]
                    else:
                        # since Key=val pairs are parsed as dictionaries (!)
                        if field in tok["misc"]:
                            plus_tok[field] = tok["misc"][field]  
                        else:
                            plus_tok[field] = "_"
                return plus_tok

            for tok in sent:
                plus_sent.append(to_plus_token(tok))
            return plus_sent

        plus_sentences = list(map(to_plus_sentence, sentences))
        comment = "# global.columns = {}\n".format(
            " ".join([field.upper() for field in fields])
            )
        return "\n".join(
            [comment] + [sent.serialize() for sent in plus_sentences]
            )
    

if __name__ == "__main__":
    #print(from_plus("test/best.conllup"))
    print(to_plus("test/best.conllu", ["ID", "FORM", "LEMMA", "UPOS", "HEAD", "DEPREL", "DEPS", "MISC", "CORRECTION", "REPL"]))
