# Wing IDE Professional 6.x KeyGen
# made to run on Python3.x and Python2.7
from __future__ import print_function
try:
    from future import standard_library
except ImportError as e:
    try:
        m = "Probably something with module 'future' not found"
        m = e.message
    finally:
        input ('ImportError: ' + m + ' \nrun [c:\Python27\Scripts\]\n'
               '-> pip install future\n'
               'To install python 2/3 compatibility layer')
    exit()
standard_library.install_aliases()
from future.builtins import (input, str, range)
import string
import random
import hashlib
import sys

def randomstring(size = 20, chars = string.ascii_uppercase + string.digits):
    return ''.join(( random.choice( chars ) for _ in range(size) ) )

def BaseConvertHex( number, to_digits,
                    ignore_negative = True):
    # isNegative = number < 0
    # if isNegative and not ignore_negative:
    #     number = abs( number )
    # make an integer out of the number
    x = int( number, 16)

    # create the result in base 'len(to_digits)'
    res = ''
    toDigitsLen   = len( to_digits )
    while x > 0:  # divide of /seperate digit's from x until it's empty
        digit =   x % toDigitsLen
        res   =   to_digits[ digit ] + res
        x   //=   toDigitsLen
    #  if isNegative:
    #      res = - res
    return res
def AddHyphens( code ):
    """Insert hyphens into given license id or activation request to
    make it easier to read"""
    return code[   : 5 ] + '-' + \
           code[  5:10 ] + '-' + \
           code[ 10:15 ] + '-' + \
           code[ 15:   ]

def ToBase30( digest ):

    result = BaseConvertHex( digest .upper(),  BASE30)

    return result .rjust( KeyLen, '1' )

def mulHash16( inValue, lichash ):
    part = 0
    for c in lichash:
        part *= inValue
        part += ord( c )
        part &= 0xFFFFF
    return format( part, '05x' )
def GenRandomLicID( kPrefix_LicenseId ):
    LicenseId   = AddHyphens( kPrefix_LicenseId +
                              #BASE30[1] * (KeyLen + 1) )
                        randomstring( 18, BASE30))
    return LicenseId

def GetRequestCode(kRequestPrefix):
    RequestCode = input( \
        'Enter request code : ' ).upper()

    if RequestCode.startswith(kRequestPrefix) == False:
        print(
            (' '*19) + '  ' + kRequestPrefix.ljust(5,"x") + '-xxxxx'*3 + '\n' +
                (' '*14) + 'OOPS : Your request code should start with: ' + kRequestPrefix + '...\n' +
                (' '*14) + '       You probably made a mistake, \n' +
                (' '*14) + ' ...or didn\'t enter anything at all.\n' +
                (' '*14) + '       Like this the activation code WON\'T WORK !\n' +
                (' '*14) + '' +
                (' '*14) + '       or this keygen is not setup for the requested 2.OSVersion or 3.WingVersion, \n'
        )
    return RequestCode
 
def GenActivationCode( LicenseId, RequestCode):
    # 1. Gen SHA1 from 'activation code' and 'LicenseId'
    hasher                  = hashlib.sha1( (RequestCode + LicenseId) .encode() ) \
        .hexdigest()
    # 2. Take only every second diget; starting with the first
    Every2ndDigest = ''.join( [ c for i, c in enumerate( hasher ) if i % 2 == 0 ] )
    lichash = ToBase30( Every2ndDigest )
    return  lichash
def GenActivationCode2( lichash ):
    # 3. Apply mulhash
    part5    = [ mulHash16( key,  lichash)  \
                     for key in KeyLicVer     ]
    part5   = ''.join( part5 )

    part5   = Prefix_ActivationId + \
        ToBase30( part5 )
    return AddHyphens ( part5 )
 
#########################################################
##
##  M a i n
##
# Key vectors for Wing IDE Professional x
#<Wing IDE 6.0>\bin\ide-2.7\src\process\pycontrol.pyo
#<Wing IDE 6.0>\bin\ide-2.7\src\process\ctlutil.pyd
KeyLicVerX            = [   0,   0,   0,  0 ]
#    Other
KeyLicVer2            = [  48, 104, 234, 247 ]
KeyLicVer3            = [ 254,  52,  98, 235 ]
KeyLicVer4            = [ 207, 45,  198, 189 ]

#    "macosx"
KeyLicVer2            = [  41, 207, 104,  77 ]
KeyLicVer3            = [ 128, 178, 104,  95 ]
KeyLicVer4            = [  67, 167,  74,  13 ]
#    "linux"
KeyLicVer2            = [  142,  43, 201,  38 ]
KeyLicVer3            = [  123, 163,   2, 115 ]
KeyLicVer4            = [   17,  87, 120,  34 ]

#    "windows"
KeyLicVer2            = [ 123, 202,  97, 211 ]
KeyLicVer3            = [ 127,  45, 209, 198 ]
KeyLicVer4            = [ 240,   4,  47,  98 ]
KeyLicVer5            = [   7, 123,  23,  87 ]
KeyLicVer6            = [  23, 161,  47,   9 ]

WingVer               = 6
#key for Ver6
KeyLicVer             = KeyLicVer6
kVersionRequestCodes = {
    '2': 'X',
 '3': '3',
 '4': '4',
 '5': '5',
 '6': '6'
}
kRequestVersionCode = kVersionRequestCodes[ '6'  ]
kOSRequestCodes = {
    'win32': 'W',
 'linux': 'L',
 'darwi': 'M',
 'sunos': 'N',
 'freeb': 'F',
 'tru64': 'T',
 'netbs': 'E',
 'openb': 'B'
}

kRequestPrefix = 'R'
if  sys.platform.startswith('linux') and \
    os.uname()[4] in ('ppc', 'ppc64'):
    kVerPrefix  = 'P'
else:
    kVerPrefix  = kOSRequestCodes [ sys.platform[:5] ]

kVerPrefix += kRequestVersionCode
kLicenseUseCodes = \
[    'C'    , #'Perpetual License - Commercial Use'
         'E'    , #'Perpetual License - Non-Commercial Use'
        'N'    , #'Perpetual License - Educational Use'
        'T'    , #'Trial License - Evaluation Use Only'
        'Y'    , #'Annual License - Commercial Use')
        'H'    , #'Annual License - Non-Commercial Use'
        '6'    , #'Free Annual License - Educational Use'
        ]

Prefix_LicenseId      =  kLicenseUseCodes[0] + "N"   # "CN6"
Prefix_RequestId      =  kRequestPrefix      + kVerPrefix   # "RW6"
Prefix_ActivationId   = "AXX"  #  = kActivationPrefix       # "AXX"
KeyLen                = 17

BASE16 = '0123456789ABCDEF'
BASE30 = BASE16[1:] +'GH''JKLMNPQR''T''VWXY' # no I,S,U
 
print('Wing IDE Professional ' + str(WingVer) + '.x - Keygen v2\n' + \
      '=' * 37 + '\n')

#0. Module Testing:
def Testing():
    Test_LicenseId = "CN222-22222-22222-22222"
    Test_ReqCode   = "RW62G-VARNH-H8KEG-EH82G"
    Test_ActCode   = "AXX37-R7JNG-RNF1R-D1MWE"

    RemovePreFixAndHyphens = lambda x : x.replace('-','')[3:]  
    assert RemovePreFixAndHyphens ( Test_LicenseId ) == \
           ToBase30( "5E4C5A46401C8CC33DCB" ) , \
            "T0-1:  Testing ToBase30()"
 
    Test_ReqCode2 = "RW62W-9C7JP-RRLRK-VKRT7" # note: that's some intermediate code requestcode that is not shown
    assert  RemovePreFixAndHyphens (Test_ReqCode2 )  == \
            GenActivationCode(Test_LicenseId, Test_ReqCode) , \
             "T0-2: Testing GenActivationCode()"

    assert    Test_ActCode == \
              GenActivationCode2(Test_ReqCode2), \
             "T0-3: Testing GenActivationCode2()"

    #Oldversion
    assert "AXX" + "23-QB7YB-6RG4M-YFQ86"  == \
           GenActivationCode2(  \
               GenActivationCode( Test_LicenseId, "" ) ) , \
           "0-4: Test GenActivationCode() [OldStyle]"
Testing()

# 1. Gen random LicID
LicenseId      = GenRandomLicID( Prefix_LicenseId )
print('License id         : ' + LicenseId)
# 2. GetRequestCode
RequestCode    = GetRequestCode( Prefix_RequestId )
# 3. Gen activation code
ActivationCode = GenActivationCode( LicenseId, RequestCode )
# That's what somehow got updated in ver 6.00 to 6.09
ActivationCode = AddHyphens( RequestCode[:3] + ActivationCode )
ActivationCode = GenActivationCode2( ActivationCode )

print('Activation    code : ' +  ActivationCode )
input('\nGood luck !                             cw2k [at] gmx [dot] net')
 
