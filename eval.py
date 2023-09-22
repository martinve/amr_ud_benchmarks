import tools.convert_tests as conv
import evaluatetasks as ev

if __name__ == "__main__":
    metric = "hans"

    gold = conv.read_gold_labels(metric)
    pred = conv.read_prediction(metric)

    print(pred)
    print(ev.convert_labels(pred))