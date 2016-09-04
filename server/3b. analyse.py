from __future__ import print_function
with open('2. results.dat') as f:
  results = [l.strip() for l in f]
trickQuestions = [13,16,20,21]
with open('4. data.csv', 'w') as o:
  writer = []
  for each in results:
    each_arr = each.split(',')
    _isControl = True if each_arr[0] else False
    _start, _finish = each_arr[1:3]
    _questionResponses = each_arr[3:~0]
    _questionOrder = each_arr[~0].split('-')

    _questionsC = len(_questionResponses)
    _rquestions = range(_questionsC)
    _questionDict = dict(zip(_questionOrder, _questionResponses))
    _mistakes = [q for q in _rquestions if _questionDict[str(q+1)].split('-')[0] != _questionDict[str(q+1)].split('-')[1]]

    o_start = str(_start)
    o_finish = str(_finish)
    o_control = "Yes" if _isControl else "No"
    o_mistakesC = str(len(_mistakes))
    o_mistakes = "\n"+"\n".join(["(Q%s) %s -> %s%s" % (str(q+1), _questionDict[str(q+1)].split('-')[0], _questionDict[str(q+1)].split('-')[1]," (#trick)" if int(q) in trickQuestions else "") for q in _mistakes]) if _mistakes else ""
    o_accuracy = str(round((_questionsC-len(_mistakes))/float(len(_questionResponses))*100,2))+"%"
    print("=====================\n\nStart    : %s\nFinish   : %s\nControl  : %s\nMistakes : %s\nAccuracy : %s%s" % (o_start,o_finish,o_control,o_mistakesC,o_accuracy,o_mistakes),end="\n\n")
    writer.append(",".join(["y" if q+1 not in _mistakes else "n" for q in _rquestions]+["control" if _isControl else ""]))
  o.write(",".join([str(i+1) for i in _rquestions]+["control"])+"\n" + "\n".join(writer))
"""
try:
  raw_input()
except:
  input()
"""