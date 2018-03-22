

# takes a famDict and break down how often each module is assigned to each family
# output:
#   Dict:
#       Key: family number
#       Val: module numbers occurring in those family proteins
def analyzeFamDict(famDict):
    famInfoDict = {}
    moduleInFams = []
    for protName in famDict.keys():
        family = int(protName.split("_")[0][1:])

        borders = famDict[protName]

        for border in borders:
            m = int(border[0])
            moduleInFams.append(m)
            if family in famInfoDict.keys():
                famInfoDict[family].append(m)
            else:
                famInfoDict[family] = [m]
    # sort info

    for f in famInfoDict.keys():
        famInfoDict[f].sort()
    moduleInFams = list(set(moduleInFams))
    moduleInFams.sort()

    # how many module numbers occur on multiple families?
    moduleWithMultFams = []
    for m in moduleInFams:
        numFam = 0
        for f in famInfoDict.keys():
            if m in famInfoDict[f]:
                numFam += 1
        if numFam > 1:
            moduleWithMultFams.append(m)
    return famInfoDict, moduleInFams, moduleWithMultFams


def filterBorderDict(borderDict):
    famDict = {}
    fusedDict = {}

    for protName in borderDict.keys():
        # family proteins has shorter names in my simulator
        if len(protName) < 15:
            famDict[protName] = borderDict[protName]
        else:
            fusedDict[protName] = borderDict[protName]

    return famDict, fusedDict


# main function of this file
def analyizeBorder(borderDict, checkOnlyModuleInFams=False):
    famDict, fusedDict = filterBorderDict(borderDict)

    famInfoDict, moduleInFams, moduleWithMultFams = analyzeFamDict(famDict)

    totalBorders = 0
    success = 0
    for protName in fusedDict.keys():
        # Reference:
        # 0  1 2  3 4  5 6 7 8       9   10    11
        # ID_0_F1_0_F2_1_G_0_SplitPt_459_GenID_0
        splitInfo = protName.split("_")
        # id = splitInfo[1]
        f1 = int(splitInfo[3])
        f2 = int(splitInfo[5])
        # g = int(splitInfo[7])
        split = int(splitInfo[9])
        # genID = int(splitInfo[11])

        borders = fusedDict[protName]

        for border in borders:

            m = border[0]
            s = border[1]
            e = border[2]

            toggle = not checkOnlyModuleInFams
            if m in moduleInFams or toggle:
                totalBorders += 1
                # determine which side the interval is leaning
                if (split - s) + (split - e) > 0:
                    f = f1
                else:
                    f = f2
                if m in famInfoDict[f]:
                    success += 1

    successRatio = float(success)/totalBorders

    return successRatio, success, totalBorders

