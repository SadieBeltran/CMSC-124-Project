import re
from Variable import Variable

vars = []
class SyntaxAnalyzer:

    def program(self, tokens, lexeme, row):
        i = 0
        
        while(tokens[i] == 'COMMENT'):
            i += 1

        if tokens[i] == 'START':        #encountered start of program
            print("==== PROGRAM START! === \n")
            i += 1
            while tokens[i] != 'END' and i < len(tokens):
                if(tokens[i] == 'COMMENT'):
                    i+=1
                    continue

                if tokens[i] == 'WAZZUP':
                    i += 1
                    i = isVarDec(tokens, lexeme, row, i)
                

                i = statement(tokens, lexeme, row, i)
                
                if i >= len(tokens):
                    break
            if i == len(tokens):
                raise RuntimeError('End of program not found')
            # printVariables()
        else:
            raise RuntimeError('Start of program not found')
def isVarDec(tokens, lexeme, row, i):
    maxlen = len(tokens)
    while(tokens[i] != 'BUHBYE'):
        if tokens[i] == 'COMMENT': #aka BTW (single line comment)
            #comments are stored all in one, if it's a multiline is when we iterate thru so this is fine
            i += 1
            continue
        elif tokens[i] == 'VAR_DEC':
            #build line
            rowNum = row[i]
            line = []
            tline = []
            while rowNum == row[i]:
                line.append(lexeme[i])
                tline.append(tokens[i])
                i += 1
            storeVariable(tline, line, rowNum)
        else:
            raise RuntimeError('Unexpected %r on line %d, Only variable declarations are allowed in this section' % (lexeme[i], row[i]))

        if i >= maxlen:
            raise RuntimeError('Encountered end of file')
    return i

def storeVariable(tline, line, rowNum):
    global vars

    i = 1
    maxlength = len(tline)
    if tline[i] == 'VARIABLE':
        varName = line[i][:-1]
        i += 1
    else:
        raise RuntimeError('Expected VARIABLE NAME on line %d' % (rowNum))

    if i >= maxlength:
        vars.append(Variable(varName, 'NOOB', None))
        return

    if tline[i] == 'ITZ':
        i += 1
    else:
        raise RuntimeError('Expected \'ITZ\' on line %d' % (rowNum))
    
    if i >= maxlength:
        raise RuntimeError('Encountered end of file!')
    
    if tline[i] == 'NOOB' or tline[i] == 'YARN' or tline[i] == 'TROOF' or tline[i] == 'NUMBAR' or tline[i] == 'NUMBR' or tline[i] == 'VARIABLE':
        type = tline[i]
        value = line[i]
        vars.append(Variable(varName, type, value))
        return
    else:
        raise RuntimeError('Variable declaration can only be to a YARN, TROOF, NOOB etch')
    vars.append(Variable('IT', 'NOOB', ""))

def statement(tokens, lexeme, row, i):
    tline = []
    line = []
    rowNum = row[i]
    # print(rowNum)
    while rowNum == row[i]:
        tline.append(tokens[i])
        line.append(lexeme[i])
        i += 1
    
    if tline[0] == 'PRINT':
        printLine(line, tline)
    elif tline[0] == 'VAR_DEC':
        raise RuntimeError("Unexpected variable declaration at line %d" % (rowNum))
    elif tline[0] == 'BOOL_OPER':
        print(boolOpRegion(line, tline, 0, rowNum))
    elif tline[0] == 'COMPARISON':
        print(comparison(line, tline, 0, rowNum))
    return i

def comparison(line, tline, i, rowNum):
    compQ = []
    #print(line)
    if line[i] == 'BOTH SAEM': 
        i+=1
        if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
            compQ.append([tline[i],line[i]])
            i+=1
        elif tline[i] == 'VARIABLE':
            value, type = searchVarValue(line[i])
            compQ.append([type,value])
            i+=1
        else:
            raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
        if tline[i] != 'AN':
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i+=1
        if line[i] == 'BIGGR OF' or line[i] == 'SMALLR OF':
            compQ.append(line[i])
            i+=1
            if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                compQ.append([tline[i],line[i]])
                i+=1
            elif tline[i] == 'VARIABLE':
                value, type = searchVarValue(line[i])
                compQ.append([type,value])
                i+=1
            else:
                raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
            if compQ[0][1] != compQ[2][1]:
                raise RuntimeError("Value mismatch - operand 1 and 2 (%r and %r) must be same" % (compQ[0][1], compQ[2][1]))
            if tline[i] != 'AN':
                raise RuntimeError("Expected AN at line %d" % (rowNum))
            i+=1
            if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                compQ.append([tline[i],line[i]])
                i+=1
            elif tline[i] == 'VARIABLE':
                value, type = searchVarValue(line[i])
                compQ.append([type,value])
                i+=1
            else:
                raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
        elif tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
            compQ.append([tline[i],line[i]])
            i+=1
        elif tline[i] == 'VARIABLE':
            value, type = searchVarValue(line[i])
            compQ.append([type,value])
            i+=1
        else:
            raise RuntimeError("Expected NUMBR, NUMBAR, VARIABLE, BIGGR OF, or SMALLR OF at line %d" % (rowNum))
        
        #print(compQ)
        if compQ[1] == 'BIGGR OF':
            if compQ[2][0] != compQ[3][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[2][0] == 'NUMBR':
                if int(compQ[2][1]) >= int(compQ[3][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            elif compQ[2][0] == 'NUMBAR':
                if float(compQ[2][1]) >= float(compQ[3][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        elif compQ[1] == 'SMALLR OF':
            if compQ[2][0] != compQ[3][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[2][0] == 'NUMBR':
                if int(compQ[2][1]) <= int(compQ[3][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            elif compQ[2][0] == 'NUMBAR':
                if float(compQ[2][1]) <= float(compQ[3][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        else:
            if compQ[0][0] != compQ[1][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[0][1] == compQ[1][1]:
                return 'WIN'
            else:
                return 'FAIL'
    elif line[i] == 'DIFFRINT':
        i+=1
        if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
            compQ.append([tline[i],line[i]])
            i+=1
        elif tline[i] == 'VARIABLE':
            value, type = searchVarValue(line[i])
            compQ.append([type,value])
            i+=1
        else:
            raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
        if tline[i] != 'AN':
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i+=1
        if line[i] == 'BIGGR OF' or line[i] == 'SMALLR OF':
            compQ.append(line[i])
            i+=1
            if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                compQ.append([tline[i],line[i]])
                i+=1
            elif tline[i] == 'VARIABLE':
                value, type = searchVarValue(line[i])
                compQ.append([type,value])
                i+=1
            else:
                raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
            if compQ[0][1] != compQ[2][1]:
                raise RuntimeError("Value mismatch on line %d (%r and %r) must be same" % (rowNum, compQ[0][1], compQ[2][1]))
            if tline[i] != 'AN':
                raise RuntimeError("Expected AN at line %d" % (rowNum))
            i+=1
            if tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                compQ.append([tline[i],line[i]])
                i+=1
            elif tline[i] == 'VARIABLE':
                value, type = searchVarValue(line[i])
                compQ.append([type,value])
                i+=1
            else:
                raise RuntimeError("Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum))
        elif tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
            compQ.append([tline[i],line[i]])
            i+=1
        elif tline[i] == 'VARIABLE':
            value, type = searchVarValue(line[i])
            compQ.append([type,value])
            i+=1
        else:
            raise RuntimeError("Expected NUMBR, NUMBAR, VARIABLE, BIGGR OF, or SMALLR OF at line %d" % (rowNum))
        
        #print(compQ)
        if compQ[1] == 'BIGGR OF':
            if compQ[2][0] != compQ[3][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[2][0] == 'NUMBR':
                if int(compQ[3][1]) >= int(compQ[2][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            elif compQ[2][0] == 'NUMBAR':
                if float(compQ[3][1]) >= float(compQ[2][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        elif compQ[1] == 'SMALLR OF':
            if compQ[2][0] != compQ[3][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[2][0] == 'NUMBR':
                if int(compQ[3][1]) <= int(compQ[2][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            elif compQ[2][0] == 'NUMBAR':
                if float(compQ[3][1]) <= float(compQ[2][1]):
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        else:
            if compQ[0][0] != compQ[1][0]:
                raise RuntimeError("Type mismatch - cannot compare %r and %r" % (compQ[0][0], compQ[1][0]))
            if compQ[0][1] != compQ[1][1]:
                return 'WIN'
            else:
                return 'FAIL'    

def boolOp(line, tline, i, rowNum):
    if tline[i] == 'BOOL_OPER':
        opAddress = i
        boolQ = []
        i+=1
        i, boolQ0 = boolOp(line, tline, i, rowNum)
        boolQ.append(boolQ0)
        if line[opAddress] == 'NOT':
            if(boolQ[0] == 'WIN'):
                return i, 'FAIL'
            else:
                return i, 'WIN'
        i+=1
        if tline[i] != 'AN':
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i+=1
        i, boolQ1 = boolOp(line, tline, i, rowNum)
        boolQ.append(boolQ1)
        #print(boolQ)
        if line[opAddress] == 'BOTH OF':
            if(boolQ[0] == 'WIN' and boolQ[1] == 'WIN'):
                return i, 'WIN'
            else:
                return i, 'FAIL'
        elif line[opAddress] == 'EITHER OF':
            if(boolQ[0] == 'WIN' or boolQ[1] == 'WIN'):
                return i, 'WIN'
            else:
                return i, 'FAIL'
        elif line[opAddress] == 'WON OF':
            if(boolQ[0] != boolQ[1] and (boolQ[0] == 'WIN' or boolQ[1] == 'WIN')):
                return i, 'WIN'
            else:
                return i, 'FAIL'
    elif tline[i] == 'VARIABLE':
        if i < len(line)-1:
            line[i] = line[i][:-1]
        value, type = searchVarValue(line[i])
        if type != 'TROOF':
            value = typeCasting(value, type, 'TROOF', rowNum)
        return i, value
    elif tline[i] == 'TROOF':
        return i, line[i]
    else:
        raise RuntimeError("Unexpected %r at line %d" % (line[i], rowNum))

def boolOpRegion(line, tline, i, rowNum):
    #print(line)
    if line[i] == 'ALL OF' or line[i] == 'ANY OF':
        if line[i] == 'ALL OF':
            initCond = 'WIN'
            terminateCond = 'WIN'
        elif line[i] == 'ANY OF':
            terminateCond = 'FAIL'
            initCond = 'FAIL'
        i+=1
        while i < len(line) and initCond==terminateCond:
            initCond = boolOp(line, tline, i, rowNum)[1]
            #print(initCond, terminateCond)
            i+=1
            if line[i] == 'AN':
                i+=1
            else:
                raise RuntimeError("Expected AN at line %d" % (rowNum))
            if line[i] == 'MKAY':
                break
        return initCond
    else:
        return boolOp(line, tline, i, rowNum)[1]

def printLine(line, tline):
    #assume muna na YARN lang ung priniprint
    string = ""
    for i in range(0, len(line)):
        if tline[i] != 'PRINT' and tline[i] != 'COMMENT':
            if tline[i] == 'YARN':
                string = string + line[i][1:-1]
            elif tline[i] == 'VARIABLE':
                value, type = searchVarValue(line[i])
                if type != 'YARN':
                    value = typeCasting(value, type, 'YARN', i)
                else:
                    value = value[1:-1]
                string = string + value
            elif tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                value = typeCasting(line[i], tline[i], 'YARN', i)
                string = string + value
            elif tline[i] == 'TROOF':
                value = line[i]
                string = string + value
            else:
                raise RuntimeError("Type %r cannot be printed" % (tline[i]))
    print(string)

def searchVarValue(name):
    global vars
    for variable in vars:
        if variable.name == name:
            return variable.value, variable.dataType
    raise RuntimeError('Variable %r does not exist' % (name))

def typeCasting(value, type1, type2, rowNum):
    if type1 == 'NOOB':
        if type2 == 'TROOF':
            return False
        else:
            raise RuntimeError('Encountered error in line %d, cannot typecast NOOB to %r' % (rowNum, type2))
    elif type1 == 'NUMBR' or type1 == 'NUMBAR':
        match type2:
            case 'NUMBAR':
                return float(value)
            case 'NUMBR':
                return int(value)
            case 'YARN':
                return str(value)
            case 'TROOF':
                if value == 0:
                    return 'FAIL'
                else:
                    return 'WIN'
            case _:
                raise RuntimeError('Encountered error in line %d, cannot typecast NUMBR to %r' % (rowNum, type2))
    elif type1 == 'TROOF':
        match type2:
            case 'NUMBAR':
                if value == 'WIN':
                    return 1.0
                else:
                    return 0
            case 'NUMBR':
                if value == 'WIN':
                    return 1
                else:
                    return 0
            case 'YARN':
                return value
            case _:
                raise RuntimeError('Encoutnered error in line %d, cannot typecast TROOF to %r' % (rowNum, type2))
    elif type1 == 'YARN':
        value = value[1:-1]
        match type2:
            case 'NUMBR':
                if bool(re.search(r'-?\d(\d)*', value)):
                    return int(value)
                else:
                    raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))
            case 'NUMBAR':
                if bool(re.search(r'-?\d(\d)*\.\d(\d)*', value)):
                    return float(value)
                else:
                    raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))
            case 'TROOF':
                if value == "":
                    return 'FAIL'
                else:
                    return 'WIN'
            case _:
                 raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))

def printVariables():
    global vars
    for variable in vars:
        print(variable.name)
        print(variable.dataType)
        print(variable.value)
        print("")