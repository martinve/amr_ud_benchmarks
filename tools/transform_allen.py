import convert_tests as conv
import spacy

nlp = spacy.load("en_core_web_sm")


def main():
    s = conv.read_file("tests_allen.py")
    tests = eval(s)

    fp = open(conv.datadir + "/bench_allen_premise.txt", "w")
    fh = open(conv.datadir + "/bench_allen_hypothesis.txt", "w")
    fl = open(conv.datadir + "/bench_allen_label.txt", "w")

    total_sents = 0
    for it in tests:
        doc = nlp(it[0])
        sents = list(doc.sents)

        premise = " ".join([x.text.strip() for x in sents[:-1]])
        hypothesis = sents[-1].text
        label = it[1]
        total_sents += len(sents)

        print(premise, hypothesis, label)

        fp.write(f"{premise}\n")
        fh.write(f"{hypothesis}\n")
        fl.write(f"{label}\n")

    fp.close()
    fh.close()
    fl.close()

    print(f"Total sentences: {total_sents}")


if __name__ == "__main__":
    main()
