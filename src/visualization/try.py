from concurrent import futures
import read_pot as rp

pots = rp.read_pots()
ps = [v for k, v in pots.items()]

with futures.ProcessPoolExecutor() as pool:
    fs = [pool.submit(rp.cyclic_voltammetry, p) for p in ps]
    for f in futures.as_completed(fs):
        try:
            t, v, c = f.result()
        except ValueError:
            continue
        print('{} {} {}'.format(t, v, c))
