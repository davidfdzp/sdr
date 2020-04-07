# File: ascfun.py
# Functions for conversion between characters and bits
# from numpy import np
import numpy as np
def asc2bin(txt, bits=8):
    """
    Text message to serial binary conversion
    >>>>> dn = asc2bin(txt, bits) <<<<<
    where txt	Text message (text string)
    abs(bits)	bits per character, default: 8
    bits > 0	LSB first parallel to serial conv
    bits < 0	MSB first parallel to serial conv
    dn		binary output DT sequence
    """
    txtnum = np.array([ord(c) for c in txt], np.int16)
    if bits > 0:
    # powers of 2: 2**0, 2**-1, 2**-2, ..., 2**-(bits-1)
        p2 = np.array(np.power(2.0, -np.arange(bits)), np.float32)
    else:
    # powers of 2: 2**(bits+1), ..., 2**-2, 2**-1, 2**0
        p2 = np.array(np.power(2.0, np.arange(bits+1,1)), np.float32)
    # 2-dim array of bits, one row per character in txt
    B = np.array(np.mod(np.floor(np.outer(txtnum,p2)),2),np.int8)
    # parallel to serial conversion
    return np.reshape(B, -1)

def bin2asc(dn, bits=8, flg=1):
    """
    Serial binary to ASCII text conversion
    >>>>> txt = bin2asc(dn, bits, flg) <<<<<
    where dn
    binary input sequence
    abs(bits) bits per char, default=8
    bits > 0
    LSB first parallel to serial
    bits < 0
    MSB first parallel to serial
    flg != 0
    limit range to [0...127]
    txt
    output text string
    """
    B = np.reshape(dn, (len(dn)/abs(bits), abs(bits)))
    if bits > 0:
    # powers of 2: 2**0, 2**1, 2**2, ..., 2**(bits-1)
        p2 = np.array(np.power(2.0, np.arange(bits)), np.float32)
        if flg!=0 and bits > 7:        
            p2[7:] = 0
    else:
    # powers of 2: 2**(-bits-1), ..., 2**2, 2**1, 2**0
        p2 = np.array(np.power(2.0, -np.arange(bits+1,1)), np.float32)
        if flg!=0 and bits > 7:       
            p2[:bits-7] = 0
    txtnum = np.array(np.inner(B,p2), np.int8)
    return txtnum.tobytes()