import os
import sys
import math
import json

OutFile = "rulelist.txt"
Count = 0

def apply_rule(rule, num):
    bin_str = "{0:08b}".format(rule)[::-1]
    #print(bin_str)
    return bin_str[num]

def apply_rules(rule, num, count):
    binstr_in = ("{0:0%db}" % (3*count)).format(num)
    #print(binstr_in)
    binstr_out = ''
    for i in range(count):
        for j in range(3*count - (i+1)*2):
            #print(binstr_in[j:j+3])
            binstr_out += apply_rule(rule, int(binstr_in[j:j+3],2))
            #print("out", binstr_out)
        binstr_in = binstr_out
        binstr_out = ''
    return binstr_in

def apply_P_binstr(P_binstr, num):
    return P_binstr[num]

def apply_PPP_binstr(P_binstr, num):
    if not math.log(len(P_binstr),2).is_integer(): return ''
    N = int(math.log(len(P_binstr),2))
    num_binstr = ("{0:0%db}" % (N*3)).format(num)
    #print(num_binstr)
    binstr_out = ''
    for i in range(3):
        binstr_out += apply_P_binstr(P_binstr, int(num_binstr[i*N:(i+1)*N],2))
    #print(binstr_out)
    return binstr_out

def get_Ps(rule1, rule2, pidstr, i, order, next_candidate, findall = False):
    global Count
    if not math.log(len(pidstr),2).is_integer(): return None
    #print(order)
    #print(pidstr,i)
    maxlevel = len(pidstr)
    N = int(math.log(maxlevel,2))
    if i > maxlevel: return None
    if i == maxlevel:
        pid = int(pidstr[::-1],2)
        if pid == 0 or pid == pow(2,maxlevel) - 1: return []
    for (x,y,z) in [(x, y, z) for x in order[:i] for y in order[:i] for z in order[:i] if order[i-1] in (x,y,z)]:
        num = x*pow(2,2*N) + y*pow(2,N) + z
        #print(x,y,z)
        res2 = apply_rule(rule2, int(apply_PPP_binstr(pidstr, num),2))
        temp = int(apply_rules(rule1, num, N),2)
        if temp not in order[:i] and pidstr[temp] == '-':
            #print('aaa', num, temp, i, pidstr)
            pidstr = pidstr[:temp] + res2 + pidstr[temp+1:]
            #print('bbb', num, temp, i, pidstr)
            if temp not in order: order.append(temp)
        res1 = apply_P_binstr(pidstr, temp)
        Count += 1
        #print("res ", num, res1, res2, pidstr, i, temp)
        if res1 != res2:
            print("Cut ", num, res1, res2, pidstr, i, temp, order)
            return []
    else:
        if i == maxlevel:
            #print(order, next_candidate)
            pid = int(pidstr[::-1],2)
            #if pid == 0 or pid == pow(2,maxlevel) - 1: return []
            print("Found P", pid, pidstr, order)
            return [pid]
        else:
            if len(order) <= i: # nothing is added dynamically, so next_candidate is not in order yet
                order.append(next_candidate)
            if next_candidate in order:
                for j in range(maxlevel):
                    t = (order[0]-j) % maxlevel #order[-1]
                    if t not in order:
                        next_candidate = t #order.append(t)
                        break
                else:
                    next_candidate = None
                
            if pidstr[order[i]] == '0':
                #print("call_4")
                return get_Ps(rule1, rule2, pidstr, i+1, order, next_candidate, findall)
            elif pidstr[order[i]] == '1':
                #print("call_5")
                return get_Ps(rule1, rule2, pidstr, i+1, order, next_candidate, findall)
            else: # pidstr[i] == '-'
                pidstr_i_0 = pidstr[:order[i]] + '0' + pidstr[order[i]+1:]
                pidstr_i_1 = pidstr[:order[i]] + '1' + pidstr[order[i]+1:]
                #print("i,orderi", i, order[i], pidstr_i_0, pidstr_i_1)
                if findall:
                    #print("call_3")
                    return get_Ps(rule1, rule2, pidstr_i_0, i+1, order, next_candidate, findall) + get_Ps(rule1, rule2, pidstr_i_1, i+1, order, next_candidate, findall)
                else:
                    #print("call_1")
                    temp = get_Ps(rule1, rule2, pidstr_i_0, i+1, order, next_candidate, findall)
                    if temp == []:
                        #print("call_2")
                        return get_Ps(rule1, rule2, pidstr_i_1, i+1, order, next_candidate, findall)
                    else:
                        return temp

def check_rule_trans2(rule1, rule2, N, findall = False):
    global Count
    Count = 0
    #N = 2
    '''
    projs = []
    for i in range(pow(2,N)):
        projs.append([])
    for i in range(pow(2, 3*N)):
        p = int(apply_rules(rule1, i, N),2)
        projs[p].append(i)
    print(projs)
    '''
    if rule2 == 0:
        binstr = '1'*pow(2,N)
        for i in range(pow(2, 3*N)):
            p = int(apply_rules(rule1, i, N),2)
            binstr = binstr[:p] + '0' + binstr[p+1:]
        # TODO : need to support findall option
        return ([int(binstr,2)] if '1' in binstr else [])
    elif rule2 == 255:
        binstr = '0'*pow(2,N)
        for i in range(pow(2, 3*N)):
            p = int(apply_rules(rule1, i, N),2)
            binstr = binstr[:p] + '1' + binstr[p+1:]
        # TODO : need to support findall option
        return ([int(binstr,2)] if '0' in binstr else [])
    else:
        maxlevel = pow(2,N)
        pidstr = '-'*pow(2,N)
        #print("call_0")
        #order0 = list(range(maxlevel))
        #order1 = list(range(maxlevel))[::-1]
        #order2 = [ i^(i>>1) for i in range(maxlevel) ]
        #order3 = [ i^(i>>1) for i in range(maxlevel)[::-1] ]
        #order4 = order1[order1.index(0):] + order1[:order1.index(0)]
        #order5 = order0[order0.index(15):] + order0[:order0.index(15)]
        order = []
        #order.append(maxlevel-1)
        pidlist = get_Ps(rule1, rule2, pidstr, 0, order, maxlevel-1, findall)
        #print(pidlist)
        print("Count : ",Count)
        return pidlist

def sym_01(num):
    res = ''
    for x in "{0:08b}".format(num)[::-1]:
        res += '1' if x == '0' else '0'
    return int(res,2)

def sym_lr(num):
    res = "{0:08b}".format(num)
    res = res[0] + res[4] + res[2] + res[6] + res[1] + res[5] + res[3] + res[7]
    return int(res,2)

if __name__ == "__main__":
    total_count = 0
    if len(sys.argv) == 4:
        #(N,r1,r2) = (7, 162, 170)
        #(N,r1,r2) = (7, 29, 51)
        (N,r1,r2) = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        print(N,"processing",r1,"->",r2)
        res = check_rule_trans2(r1, r2, N, True)
        print(res)
    elif len(sys.argv) == 2:
        rulelist = {}
        if os.path.exists(OutFile):
            with open(OutFile, 'r') as filehandle:
                rulelist = json.load(filehandle)
        else:
            for i in range(256):
                rulelist[str(i)] = [None, None, None, None, None, None] # N = 2,3,4,5,6,7
        
        if sys.argv[1] == '-P':
            for i in range(256):
                print(i, [val for sublist in rulelist[str(i)] if sublist for val in sublist])
        elif sys.argv[1][:2] == '-N':
            N = int(sys.argv[1][2:])
            print("N :",N)
            if N < 2:
                print("N should be >= 2")
                exit()
            symlist = []
            for i in range(256):
                symlist.append((i, sym_01(i), sym_lr(i), sym_lr(sym_01(i))))

            for r1 in range(256):
                if rulelist[str(r1)][N-2] != None:
                    print("skip",r1)
                    continue
                print("processing",r1)
                if r1 == 0 or r1 == 255:
                    rulelist[str(r1)][N-2] = [0,255] if N == 2 else []
                else:
                    for i in range(4):
                        rulelist[str(symlist[r1][i])][N-2] = []
                    for r2 in range(256):
                        for j in range(2,N):
                            if r2 in rulelist[str(r1)][j-2]:
                                print("skip",r1,"->",r2)
                                break
                        else:
                            print("processing",r1,"->",r2)
                            res = check_rule_trans2(r1, r2, N)
                            total_count += Count
                            print("total_count : ", total_count)
                            if res != []:
                                #print(res)
                                for i in range(4):
                                    if symlist[r2][i] not in rulelist[str(symlist[r1][i])][N-2]:
                                        rulelist[str(symlist[r1][i])][N-2].append(symlist[r2][i])
                with open(OutFile, 'w') as filehandle:
                    json.dump(rulelist, filehandle)
            print("total_count : ", total_count)
    else:
        print("Argument is required: -P, -N2, -N3,...")
