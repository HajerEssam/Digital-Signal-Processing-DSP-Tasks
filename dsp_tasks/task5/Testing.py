def ReadSignalFile(file_name):
    expected_indices = []
    expected_samples = []
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
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices, expected_samples
def Test(file_name,Your_indices, Your_samples):
    expectedIndices, expectedValues = ReadSignalFile(file_name)
    if( (len(Your_indices)!=len(expectedIndices)) or (len(Your_samples)!=len(expectedValues))):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expectedIndices[i]):
            print("Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(Your_samples)):
        if abs(Your_samples[i] - expectedValues[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one")
            return
    print("Test case passed successfully")