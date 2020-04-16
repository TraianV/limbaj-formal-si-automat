import copy
class automat:
     def __init__(self,n,m,v,q0,q,nod):
        self.n=n
        self.m=m
        self.v=v
        self.q0=q0
        self.q=q
        self.nod=nod
def citire(z):
    z.n = int(f.readline())
    z.m = int(f.readline())
    z.v = f.readline()
    z.v = z.v[:-1].split(" ")
    z.q0 = f.readline()
    z.q0 = z.q0[:-1]
    k = int(f.readline())
    b = f.readline()
    b = b[:-1].split(" ")
    z.q = []
    for i in range(len(b)):
        z.q.append(b[i])
    l = int(f.readline())
    a = []
    z.nod = {}
    for i in range(l):
        x = f.readline()
        if x[-1] == '\n':
            x = x[:-1].split(" ")
        else:
            x = x.split(" ")
        if x[0] not in z.nod:
            z.nod.update({x[0]: {x[1]: [x[2]]}})
        elif x[0] in z.nod and x[1] not in z.nod[x[0]]:
            z.nod[x[0]].update([(x[1], [x[2]])])
        elif x[0] in z.nod and x[1] in z.nod[x[0]] and x[2] not in z.nod[x[0]][x[1]]:
            z.nod[x[0]][x[1]].append(x[2])
def pas1(z):
    lin = [[i] for i in range(z.n)]
    for i in range(len(lin)):
        x=[]
        while x!=lin[i]:
            x=lin[i].copy()
            for j in x:
                if '$' in z.nod[str(j)].keys():
                    for k in z.nod[str(j)]['$']:
                        if k not in lin[i]:
                            lin[i].append(k)
    delta={i:{str(j):[] for j in range(len(lin))} for i in z.v}
    for i in z.v:
        for j in range(len(lin)):
            for k in lin[j]:
                if i in z.nod[str(k)].keys():
                    for l in z.nod[str(k)][i]:
                        if l not in delta[i][str(j)]:
                            delta[i][str(j)].append(l)
    for i in z.v:
        a = [[] for i in range(len(lin))]
        for j in range(len(lin)):
            for k in delta[i][str(j)]:
                for l in lin[int(k)]:
                    if str(l) not in a[j]:
                        a[j].append(str(l))
        for j in range(len(lin)):
            delta[i].update({str(j):a[j]})
    for i in range(len(lin)):
        for j in lin[i]:
            if str(i) not in z.q and j in z.q:
                z.q.append(str(i))
                break
    for i in z.nod:
        if '$' in z.nod[i]:
                z.nod[i].pop('$')
    for i in range(z.n):
        for j in range(i):
            if str(i) in delta[z.v[0]] and str(j) in delta[z.v[0]] and set(delta[z.v[0]][str(i)])==set(delta[z.v[0]][str(j)]):
                ok=1
                for k in range(len(z.v)):
                    if set(delta[z.v[k]][str(i)])!=set(delta[z.v[k]][str(j)]):
                        ok=0
                if ok==1:
                    for k in z.v:
                        if k in z.nod[str(i)]:
                            if k not in z.nod[str(j)]:
                                z.nod[str(j)].update({k:[]})
                            for l in z.nod[str(i)][k]:
                                if l not in z.nod[str(j)][k]:
                                    z.nod[str(j)][k].append(l)
                    for k in range(z.n):
                        for l in z.v:
                            if str(k) in z.nod and l in z.nod[str(k)] and str(i) in z.nod[str(k)][l]:
                                z.nod[str(k)].pop(l)
                                if l in z.nod[str(k)] and str(j)  not in z.nod[str(k)][l]:
                                    z.nod[str(k)][l].append(str(j))
                    z.nod.pop(str(i))
                    for k in z.v:
                        for l in delta[k]:
                            if str(i) in delta[k][l]:
                                delta[k][l].remove(str(i))
                                if str(j) not in delta[k][l]:
                                    delta[k][l].append(str(j))
                        if str(i) in delta[k]:
                            delta[k].pop(str(i))
                    if str(i) in z.q:
                        z.q.remove(str(i))
    d = {i: 0 for i in z.nod}
    j = 0
    for i in d:
        d.update({i: str(j)})
        j += 1
    dict = {i: {j: [] for j in z.nod[i]} for i in z.nod}
    for i in z.nod:
        for j in z.nod[i]:
            dict[i][j] = z.nod[i][j]
    z.nod={d[i]:{} for i in dict}
    for i in dict:
        for j in dict[i]:
            z.nod[d[i]].update({j:[]})
            for k in dict[i][j]:
                z.nod[d[i]][j].append(d[k])
    z.n=len(z.nod)
    return z
def pas2(z):
    b = [0 for i in range(z.n)]
    c = [z.q0]
    dict={tuple(z.q0):{j:[l for l in z.nod[z.q0][j]] for j in z.nod[z.q0]}}
    if z.q0 in z.nod:
        for i in z.v:
            if i in z.nod[z.q0]:
                c.append(z.nod[z.q0][i])
        c.pop(0)
    while (len(c) != 0):
        for j in c[0]:
            if j in z.nod and b[int(j)] == 0:
                for i in z.v:
                    if i in z.nod[j]:
                        c.append(list(set(z.nod[j][i])))
                        if tuple(c[0]) not in dict:
                            dict.update({tuple(c[0]): {l: [] for l in z.v}})
                            for l in tuple(c[0]):
                                for m in z.nod[l]:
                                    for n in z.nod[l][m]:
                                        if n not in dict[tuple(c[0])][m]:
                                            dict[tuple(c[0])][m].append(n)
                                    c.append(list(set(dict[tuple(c[0])][m])))
                                    if tuple(z.nod[l][m]) not in dict:
                                        dict.update({tuple(z.nod[l][m]):{}})
                                        for k in tuple(z.nod[l][m]):
                                            if tuple(k) in dict:
                                                for n in z.nod[k]:
                                                    if n not in dict[tuple(k)]:
                                                        dict[tuple(k)].update({n:[]})
                                                    dict[tuple(k)][n].extend(z.nod[k][n])
                        else:
                            for k in c[0]:
                                for l in z.nod[k]:
                                    if l not in dict[tuple(c[0])]:
                                        dict[tuple(c[0])].update({l:[]})
                                    for n in z.nod[k][l]:
                                        if n not in dict[tuple(c[0])][l]:
                                            dict[tuple(c[0])][l].append(n)
                b[int(j)]=1
        c.pop(0)
    for i in dict:
        for j in dict[i]:
            dict[i][j].sort()
    for i in dict:
        for j in dict[i]:
            dict[i][j]=list(set(dict[i][j]))
    for i in dict:
        for j in dict[i]:
            dict[i][j].sort()
            dict[i][j]=tuple(dict[i][j])
    for i in dict:
        for j in i:
            if j in z.q:
                z.q.append(i)
    for i in z.q:
        if tuple(i) not in dict:
            z.q.remove(i)
    z.nod={str(i):{}for i in range(len(dict))}
    d={i:0 for i in dict}
    j=0
    for i in d:
        d.update({i:str(j)})
        j+=1
    for i in dict:
        for j in dict[i]:
            for k in d:
                if set(dict[i][j]) == set(k):
                    z.nod[d[i]].update({j:d[k]})
    for i in range(len(z.q)):
        for j in d:
            if set(z.q[i])==set(j):
                z.q[i]=d[j]
    z.q=list(set(z.q))
    return z
def pas3(z):
    mat=[]
    for i in range(z.n):
        mat+=[[True]]
        for j in range(z.n-1):
            mat[i] += [True]
    for i in range(len(mat)):
        for j in range(i):
            if (str(i) in z.q and str(j) not in z.q) or (str(i) not in z.q and str(j) in z.q):
                mat[i][j]=False
                mat[j][i]=False
    for i in range(len(z.nod)):
        for j in range(i):
            for k in z.nod[str(i)]:
                if k in z.nod[str(i)] and k in z.nod[str(j)] and (mat[int(z.nod[str(i)][k])][int(z.nod[str(j)][k])]==False or mat[int(z.nod[str(j)][k])][int(z.nod[str(i)][k])]==False):
                    mat[i][j]=False
                    mat[j][i]=False
    dict={}
    g=[]
    for i in range(len(z.nod)):
        for j in range(len(mat[i][:i])):
            if mat[i][j]==True:
                if g==[]:
                    g.append([i,j])
                else:
                    ok=0
                    for k in range(len(g)):
                        if j in g[k]:
                            ok=1
                            break
                    if ok==1:
                        if i not in g[k]:
                            g[k].extend([i])
                    else:
                        g.append([i,j])
    for i in range(z.n):
        ok=0
        for j in range(len(g)):
            if i in g[j]:
                ok=1
        if ok==0:
            g.append([i])
    for i in g:
        dict.update({tuple(i):{}})
    for i in g:
        for j in i:
            if str(j) in z.nod:
                for k in z.nod[str(j)]:
                    if k not in dict[tuple(i)]:
                        dict[tuple(i)].update({k:[]})
                    for l in z.nod[str(j)][k]:
                        if l not in dict[tuple(i)][k]:
                            dict[tuple(i)][k].append(l)
    q=[]
    for i in g:
        for j in i:
            if str(j) in z.q:
                q.append(tuple(i))
                break
    z.q=q.copy()
    for i in g:
        for j in i:
            if z.q0==str(j):
                z.q0=tuple(i)
                break
    z.nod = {str(i): {} for i in range(len(dict))}
    d = {i: 0 for i in dict}
    j = 0
    for i in d:
        d.update({i: str(j)})
        j += 1
    for i in dict:
        for j in dict[i]:
            for k in g:
                for l in k:
                    if str(l) in dict[i][j]:
                        dict[i].update({j:tuple(k)})
                        break
    for i in dict:
        for j in dict[i]:
            z.nod[d[i]].update({j:d[dict[i][j]]})
    for i in range(len(z.q)):
        z.q[i]=d[tuple(z.q[i])]
    z.q0=d[tuple(z.q0)]
    dict={}
    while dict!=z.nod:
        dict={i:{j:[]for j in z.nod[i]}for i in z.nod}
        for i in z.nod:
            for j in z.nod[i]:
                dict[i][j]=z.nod[i][j]
        for i in dict:
            if len(i)==0:
                z.nod.pop(i)
                break
            ok=0
            for j in dict[i]:
                if i!=dict[i][j]:
                    ok=1
            if ok==0 and i!=z.q0 and i not in z.q:
                for k in dict:
                    for l in dict[k]:
                        if i==dict[k][l]:
                            z.nod[k].pop(l)
                z.nod.pop(i)
    z.n=len(z.nod)
    return z
def afis(z):
    print("Numarul de stari:",z.n)
    print("Numarul de literea ale afabetului:",z.m)
    print("Literele sunt:",z.v)
    print("Starea de inceput:",z.q0)
    print("Starea de final:",z.q)
    print("Numarul de tranzitii",len(z.nod))
    print("Tranzitiile sunt :")
    for i in z.nod:
        for j in z.nod[i]:
            print(i,'-',j,'-',z.nod[i][j])
f=open("date.in")
z=automat(0,0,[],'0',[],{})
citire(z)
z=pas1(z)
afis(z)
z=pas2(z)
afis(z)
z=pas3(z)
afis(z)
