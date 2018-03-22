import Configurations as conf
import os
from cPickle import load
from src import borderAnalysis, util


def main():
    filenames = os.listdir(conf.inputFolder)
    util.generateDirectories(conf.resultFolder)
    with open(os.path.join(conf.resultFolder, "Results.txt"), "w") as wf:
        wf.write("TEvo\tNFam\tNFusions\ts%\ts\tlen\ts%_f\ts_f\tlen_f\n")
        for filename in filenames:
            # reference:
            # 0 1    2    3    4    5 6        7 8    9   10   11 12
            # M_mjtt_SeqL_1000_NFam_2_NFusions_2_TEvo_1.5_NGen_5_ BorderInformation
            parsed = filename.split("_")
            # model = parsed[1]
            # seqLen = parsed[3]
            NFam = parsed[5]
            NFusions = parsed[7]
            TEvo = parsed[9]
            # NGen = parsed[11]

            borderDict = load(open(os.path.join(conf.inputFolder, filename), "rb"))
            successRatio, success, totalBorders = borderAnalysis.analyizeBorder(borderDict)
            successRatio2, success2, totalBorders2 = borderAnalysis.analyizeBorder(borderDict, False)

            wf.write(str(TEvo) + "\t" + str(NFam) + "\t" + str(NFusions) + "\t")
            wf.write(str(successRatio) + "\t" + str(successRatio) + "\t" + str(totalBorders) + "\t")
            wf.write(str(successRatio2) + "\t" + str(successRatio2) + "\t" + str(totalBorders2) + "\n")


if __name__ == '__main__':
    main()
