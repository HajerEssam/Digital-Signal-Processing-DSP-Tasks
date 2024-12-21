import math


def ReadSignalFile(file_name):
    expected_amplitude = []
    expected_phase_shift = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = L[0].replace('f', '')
                V1 = float(V1)
                V2 = L[1].replace('f', '')
                V2 = float(V2)
                expected_amplitude.append(V1)
                expected_phase_shift.append(V2)
                line = f.readline()
            else:
                break
    return expected_amplitude, expected_phase_shift


# Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
                return False
            # elif SignalInput[i]!=SignalOutput[i]:
            #     return False
        return True


def RoundPhaseShift(P):
    while P < 0:
        P += 2 * math.pi
    return float(P % (2 * math.pi))


# Use to test the PhaseShift of DFT
def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            A = round(SignalInput[i])
            B = round(SignalOutput[i])
            if abs(A - B) > 0.0001:
                return False
            # elif A!=B:
            #     return False
        return True
