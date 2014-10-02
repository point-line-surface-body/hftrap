import sys

def place_coefficients_in_model(ilist_file, reg_out_file, model_file):
    ilist = open(ilist_file, 'r')
    reg_out = open(ilist_file, 'r')
    model = open(ilist_file, 'w')
    ilist_lines = ilist.readlines()
    reg_out_lines = reg_out.readlines()
    ilist.close()
    reg_out.close()
    model.write(ilist_lines[0])
    model.write(ilist_lines[1])
    model.write('INDICATORSTART')
    indicators = {}
    indicator_idx = 1
    for i in range(3, len(ilist_lines)-1):
        if (not ilist_lines.startswith('#')):
            indicators[indicator_idx] = ilist_lines[i]
            indicator_idx += 1
    
    for i in range(0, len(reg_out_lines)):
        tokens1 = reg_out_lines[i].split()
        indicator_idx = int(tokens[0])
        tokens2 = indicators[indicator_idx].split()
        model.write(tokens2[0]+' ')
        model.write(float(tokens1[1]))
        for j in range(2, len(token2)):
            model.write(' '+str(tokens2[j]))
        model.write('\n')
    model.write('INDICATOREND\n')
    model.close()

def __main__():
    USAGE = 'USAGE: EXEC ILIST_FILE REG_OUT_FILE MODEL_FILE'    
    if (len(sys.argv) < 4):
        print USAGE
        exit()
    place_coefficients_in_model(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    __main__()