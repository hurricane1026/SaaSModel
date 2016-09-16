#!/usr/bin/python

# mccr : monthly customer churn rate
# cac : month to recover CAC
# months : months ahead to show
# investment : investment for marketing and sales,
#    and the unit is MRR(Monthly Recurring Revenue)
def cashflow(investment = 1, mccr = 0.0, cac = 1.0, months = 120):
    # initial the first
    cashflows = []
    current_customers = investment * 1.0 / cac
    for m in range(months):
        cashflows.append(current_customers)
        new_customers = current_customers * 1.0 / cac
        loss_customers = current_customers * 1.0 * mccr
        current_customers = current_customers + new_customers - loss_customers
    return [int(n) for n in cashflows]

def paint(models, cashflows):
    import matplotlib.pyplot as plt
    colors = ['ro', 'bo', 'go', 'yo', 'ko', 'co', 'mo', 'r+', 'b+', 'g+', 'y+', 'k+', 'c+', 'm+', 'rx', 'bx', 'gx', 'yx', 'kx', 'cx', 'mx', 'rD', 'bD', 'gD', 'yD', 'kD', 'cD', 'mD']
    color_index = 0
    plt.figure(1)
    plt.title("CashFlow in different CAC Ratio")
    plt.xlabel('Months')
    plt.ylabel('Monthly CashFlow')
    for model, cf in zip(models, cashflows):
        print model
        model_str = "%3.3fm, %3.3fCAC Ratio, %1.2fCCR" % (model['cac'], model['ratio'], model['mccr'])
        plt.plot(0, 0, colors[color_index], label = '$%s$' % model_str)
        for month, cash in enumerate(cf):
            plt.plot(month+1, cash, colors[color_index])
        color_index = (color_index + 1) % len(colors)
    plt.legend()
    plt.show()

def calc_model(model):
    model_detail = 0
    if "cac" in model and model["cac"] is not None: model_detail += 1
    if "mccr" in model and model["mccr"] is not None: model_detail += 2
    if "ratio" in model and model["ratio"] is not None: model_detail += 4
    assert model_detail in (3, 5, 6)

    # calc all model's detail
    if model_detail == 3:
        model["ratio"] = 1.0 / model["mccr"] / model["cac"]
        pass
    elif model_detail == 5:
        model["mccr"] = 1.0 / (model["ratio"] * model["cac"])
    elif model_detail == 6:
        model["cac"] = 1.0 / model["mccr"] / model["ratio"]
    else:
        raise Exception("no mccr or ratio found in model")
    return model

def combine(ratioes, cacs, ccrs):
    print ratioes, cacs, ccrs
    models = []
    for x1 in ratioes:
        for x2 in cacs:
            for x3 in ccrs:
                models.append({"ratio": x1, "cac": x2, "mccr": x3})
    return models

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", "-m", type=int, default=120)

    parser.add_argument("--ratioes", "-rs")
    parser.add_argument("--cacs", "-cs")
    parser.add_argument("--ccrs")

    args = parser.parse_args()

    ratioes = [float(r) for r in args.ratioes.split(" ")] if args.ratioes else [None]
    cacs = [float(c) for c in args.cacs.split(" ")] if args.cacs else [None]
    ccrs = [float(cc) for cc in args.ccrs.split(" ")] if args.ccrs else [None]

    origin_models = combine(ratioes, cacs, ccrs)
    models = [calc_model(m) for m in origin_models]
    cashflows = [cashflow(mccr = m["mccr"], cac = m["cac"], months = args.month) for m in models]

    paint(models, cashflows)
    print "enjoy"

