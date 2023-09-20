import convert_tests as conv

def main():
    s = conv.read_file("tests_hans.py")
    tests = eval(s)

    fp = open(conv.datadir + "/bench_hans_premise.txt", "w")
    fh = open(conv.datadir + "/bench_hans_hypothesis.txt", "w")
    fl = open(conv.datadir + "/bench_hans_label.txt", "w")

    for it in tests:
        pair = it[0].split(" . ")
        premise = pair[0] + " ."
        hypothesis = pair[1]
        label = it[1]

        fp.write(f"{premise}\n")
        fh.write(f"{hypothesis}\n")
        fl.write(f"{label}\n")

    fp.close()
    fh.close()
    fl.close()


if __name__ == "__main__":
    main()