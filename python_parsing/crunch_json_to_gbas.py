# Crunches the JSON representation of the C. Elegans
# connectome into a binary ROM to be used and read by
# an Arduino program

import json



f = open('connectome.json', 'r')

connectomeDict = json.loads(f.read())

linkedNeurons = []
unlinkedNeurons = []
for neuron, conn in connectomeDict.items():
  if len(list(conn.keys())) == 0:
    unlinkedNeurons.append(neuron)
  else:
    linkedNeurons.append(neuron)

linkedNeurons = sorted(linkedNeurons)
unlinkedNeurons = sorted(unlinkedNeurons)

connectomeList = linkedNeurons + unlinkedNeurons

indexDict = {}
i = 0
for neuron in connectomeList:
  indexDict[neuron] = i
  i += 1

romIndexList = []
romConnList = []

rawRomIndexList = []

rawIndexList = []
rawWeightList = []
rawNameList = []
rawUberNameList = []

with open('source/alltheneurons.gbas', 'w') as f:
    for neuron in linkedNeurons:
      conn = connectomeDict[neuron]
      f.write('dim ')
      if len(conn) > 1:
        f.write(neuron + '(' + str(len(conn)-1) + ') =')
      else:
        f.write(neuron  + '(1) =')
      #romIndexList.append(binascii.hexlify(struct.pack('>H', i)))
      rawRomIndexList.append(i)

      for connNeuron, weight in conn.items():
        connIndex = indexDict[connNeuron]

        rawIndexList.append(connIndex)
        rawNameList.append(connNeuron)
        rawWeightList.append(weight)
        rawUberNameList.append(neuron)
        
        indexWeight = weight * 512 + connIndex
      #  print(weight)
      #  print(connIndex)
        f.write(hex(abs(indexWeight))+ ',') #this is WRONG because sign is necessary
      f.write("\n")
      
    f.write('dim neurons(' + str(len(linkedNeurons)-1) + ') = ')
    for neuron in linkedNeurons:
      f.write('#' + neuron + ',')
    print("unlinked neurons:")
    print(unlinkedNeurons)
