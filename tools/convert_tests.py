import requests
import json
import config as cfg

"""
We have a fileset in datadir:
    bench_<benchmark>_premise.txt
    bench_<benchmark>_hypothesis.txt

We want to generate AMR parse trees named:
    bench_<benchmark>.txt.amrpremise
    bench_<benchmark>.txt.amrhypothesis
"""

datadir = cfg.datadir
resultdir = cfg.resultdir
server_url = cfg.server_url


def read_file(name):
    f = open(f"{datadir}/{name}")
    s = f.read()
    f.close
    return s

def read_prediction(name):
    f = open(f"{resultdir}/bench_{name}-simpleMetricP.txt")
    s = f.readlines()
    f.close
    s = [float(x) for x in s]
    return s


def get_amr_graph(sent):
    try:
        res = requests.post(server_url, {"text": sent})
        data = json.loads(res.text)
        return data["amr"]
    except requests.exceptions.HTTPError as err:
        print("Cannot connect to:", server_url)
        print(err.args[0])
        return


def extract_amr(benchmark,field):
    sents = read_file(f"bench_{benchmark}_{field}.txt")
    with open(f"{datadir}/bench_{benchmark}.txt.amr{field}", "w") as outfile:
        k = 0

        sents = sents.split("\n")
        print("")
        for sent in sents:
            if not sent:
                continue
            graph = get_amr_graph(sent)
            if graph:
                outfile.write(f"# ::id {k}\n")
                outfile.write(graph)
                outfile.write(2 * "\n")
            k += 1
            print(f"({benchmark}) {field[0].upper()}:  {k}/{len(sents)}")



def convert_benchmark(benchmark):
    extract_amr(benchmark, "premise")
    extract_amr(benchmark, "hypothesis")
    print("Done")


if __name__ == "__main__":
    convert_benchmark("allen")
    pass
