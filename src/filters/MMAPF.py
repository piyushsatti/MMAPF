import numpy as np

def get_noise_density(nImg:np.array):
    salt_count = np.count_nonzero(nImg == 255)
    pepper_count = np.count_nonzero(nImg == 0)
    return (salt_count + pepper_count)/nImg.size

def RnS(I1:np.array, I2:np.array, nImg:np.array):
    oImg = (I1+I2)/2
    for row in range(1, nImg.shape[0]):
        for col in range(1, nImg.shape[1]):
            if nImg[row, col] in [0,255]:
                W1_3x3 = I1[row-1:row+2, col-1:col+2]
                W1nf_3x3 = W1_3x3[np.logical_and(W1_3x3 != 0, W1_3x3 != 255)]
                if len(W1nf_3x3):
                    oImg[row, col] = np.mean(W1nf_3x3)
    
    return oImg

def CMMP(_I1_test:np.array, _I2_test:np.array, mode:str):
    # Init
    _O1_test = np.zeros(
        shape=_I1_test.shape
    )
    _O2_test = np.zeros(
        shape=_I2_test.shape
    )
    
    for row in range(1, _I1_test.shape[0]):
        for col in range(1, _I1_test.shape[1]):
            if _I1_test[row, col] not in [0,255]:
                _O1_test[row, col] = _I1_test[row, col]
                _O2_test[row, col] = _I1_test[row, col]
                continue
            # Noise Free Windows for both sub-images
            W1_3x3 = _I1_test[row-1:row+2, col-1:col+2]
            W1nf_3x3 = W1_3x3[np.logical_and(W1_3x3 != 0, W1_3x3 != 255)]
            W2_3x3 = _I1_test[row-1:row+2, col-1:col+2]
            W2nf_3x3 = W2_3x3[np.logical_and(W2_3x3 != 0, W2_3x3 != 255)]
            
            if len(W1nf_3x3)>0 and len(W2nf_3x3)>0:
                if mode == 'max':
                    _O1_test[row, col], _O2_test[row, col] = max(W1nf_3x3), min(W1nf_3x3)
                else:
                    _O1_test[row, col], _O2_test[row, col] = max(W1nf_3x3), min(W1nf_3x3)
            else:
                _O1_test[row, col], _O2_test[row, col] = _I1_test[row, col], _I1_test[row, col]

    return _O1_test, _O2_test

def IEHCLND(nImg:np.array, Nd:float):
    # Init
    oImg = np.zeros(
        shape=nImg.shape
    )
    alpha = np.floor(Nd/0.1)
    for row in range(1, nImg.shape[0]):
        for col in range(1, nImg.shape[1]):
            if nImg[row, col] not in [0,255]:
                oImg[row, col] = nImg[row, col]
                continue
            W_3x3 = nImg[row-1:row+2, col-1:col+2]
            Wnf_3x3 = W_3x3[np.logical_and(W_3x3 != 0, W_3x3 != 255)]
            if len(Wnf_3x3) > alpha:
                oImg[row, col] = np.median(Wnf_3x3)
            else:
                oImg[row, col] = nImg[row, col]
    return oImg

def MMAPF(nImg:np.array):
    # Init
    Nd = get_noise_density(nImg)
    # Padding
    nImg_padded = np.zeros(
        shape = (
            int(nImg.shape[0])+2, 
            int(nImg.shape[1])+2
        )
    )
    nImg_padded[
        1:int(nImg_padded.shape[0])-1, 
        1:int(nImg_padded.shape[1])-1
    ] = nImg

    if Nd<0.45:
        _I_IEHCLND_test = IEHCLND(nImg_padded, Nd)
    else:
        _I_IEHCLND_test = nImg_padded
    
    _I1_test = _I_IEHCLND_test.copy()
    _I2_test = _I_IEHCLND_test.copy()

    layers = ['max','min','max','min']
    for layer in layers:
        _I1_test, _I2_test = CMMP(_I1_test, _I2_test, layer)
    
    outImg = RnS(_I1_test, _I2_test, nImg)

    return outImg[1:-1,1:-1].astype(np.uint8, order='c')