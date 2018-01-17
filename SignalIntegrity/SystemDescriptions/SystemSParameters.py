'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from SignalIntegrity.SystemDescriptions import SystemDescription

class SystemSParameters(SystemDescription):
    def __init__(self,sd=None):
        SystemDescription.__init__(self,sd)
    def PortANames(self):
        return [x[1] for x in sorted
                ([(self[d].Name.strip('P'),self[d][0].A)
                  for d in range(len(self)) if self[d].Name[0]=='P'])]
    def PortBNames(self):
        return [x[1] for x in sorted
                ([(self[d].Name.strip('P'),self[d][0].B)
                  for d in range(len(self)) if self[d].Name[0]=='P'])]
    def OtherNames(self,K):
        return list(set(self.NodeVector())-set(K))
    def NodeVector(self):
        return [self[d][p].B for d in range(len(self)) for p in range(len(self[d]))]
    def StimulusVector(self):
        return [self[d][p].M for d in range(len(self)) for p in range(len(self[d]))]
    def WeightsMatrix(self,ToN=None,FromN=None):
        if not isinstance(ToN,list):
            nv = self.NodeVector()
            ToN = nv
        if not isinstance(FromN,list):
            FromN=ToN
        PWM = [[0]*len(FromN) for r in range(len(ToN))]
        for d in range(len(self)):
            for p in range(len(self[d])):
                if self[d][p].B in ToN:
                    r=ToN.index(self[d][p].B)
                    for c in range(len(self[d])):
                        if self[d][c].A in FromN:
                            ci=FromN.index(self[d][c].A)
                            PWM[r][ci]=self[d].SParameters[p][c]
        return PWM