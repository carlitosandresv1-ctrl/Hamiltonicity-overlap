import random, sys
sys.argv=[sys.argv[0], sys.argv[1]]
exec(open('test_gadget.py').read().split('rng = random.Random(1)')[0])
rng = random.Random(7); bad=0; tests=0
for trial in range(150):
    n = rng.choice([9,10,11,12,13])
    F0, H = random_F0(n, rng); G = F0 | H; x, y = 0, 1
    sub = sorted((G - {E(x,y)}) | {E(x,n), E(y,n)})
    through, ov_through = count(n+1, sub, sorted(F0))      # HCs of G through xy, best F0-overlap among them
    m = 4; W = {i: n+i for i in range(m)}
    FW = {E(W[0],W[2]), E(W[2],W[1]), E(W[1],W[3]), E(W[3],W[0])}
    P = {E(W[i],W[i+1]) for i in range(m-1)}
    Hn = (H - {E(x,y)}) | P | {E(x,W[0]), E(W[m-1],y)}; Fn = F0 | FW
    c, ov = count(n+m, sorted(Fn|Hn), sorted(Fn))
    s = len(Fn & Hn); tests += 1
    ok = (c == 2*through) and s == 1 and (through == 0 or ov == ov_through + 3)
    if not ok: bad += 1; print("MISMATCH", n, c, through, ov, ov_through, s)
print(tests, "tests, mismatches:", bad)
